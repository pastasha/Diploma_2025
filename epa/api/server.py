# Import flask and datetime module for showing date and time
import os
import psycopg2
import pandas as pd
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, make_response
from utilities import *
from classes.eda import ExploratoryDataAnalysis
from classes.classification import Classification
from classes.regression import Regression

# Initializing flask app
app = Flask(__name__)


# Connect to the database
try:
    # host, database, user, password
    conn_info = load_connection_info("db.ini")
    # Connect to the "houses" database
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()
    print("✔ Database connected successfully")
except:
    print("- Database not connected successfully")



@app.route("/get-session", methods=["GET"])
def get_session():
    user_id = request.cookies.get("user_id")
    if not user_id:
        # Generate a new guest session
        user_id = generate_user_id()
        # Insert customer if it not exist in database
        upsert_customer_to_db(user_id, app.instance_path, connection, cursor)
        # Send serponse
        response = make_response(jsonify({"message": "New guest session started", "user_id": user_id}))
        response.set_cookie(
            "user_id",
            user_id,
            max_age=SESSION_MAX_AGE,
            httponly=True,
            secure=False
        )
        print ("✔ New guest session started: " + user_id)
        return response

    return jsonify({"message": "Existing session", "user_id": user_id})


@app.route('/upload-data', methods=['POST'])
def upload_file():
    #Handles the upload of a file
    d = {}
    try:
        file = request.files['file_from_react']
        if file.filename == '':
            print('No selected file')
            d['status'] = 0
        if file and allowed_file(file.filename):
            user_id = request.cookies.get('user_id')
            get_statement = "SELECT * from " + USER_TABLE + " WHERE user_id='" + user_id + "'"
            col_names = get_column_names(USER_TABLE, cursor)
            user_df = pd.DataFrame(columns=col_names)
            user_df = get_data_from_db(get_statement, connection, cursor, user_df, col_names)[0][0]
            file_path = user_df['files_path']
            filename = secure_filename("data.csv")
            os.makedirs(os.path.join(file_path), exist_ok=True)
            file.save(os.path.join(file_path, filename))
            # Remove current user static folder 
            remove_user_static_folder(user_id)
            print(f"✔ Uploading file {filename}")
            d['status'] = 1
    except Exception as e:
        print(f"Couldn't upload file {e}")
        d['status'] = 0

    return jsonify(d)

@app.route('/start-eda', methods=['POST'])
def start_eda():
    success = False
    edaResult = None
    try:
        user_id = request.cookies.get('user_id')
        get_statement = "SELECT * from " + USER_TABLE + " WHERE user_id='" + user_id + "'"
        col_names = get_column_names(USER_TABLE, cursor)
        user_df = pd.DataFrame(columns=col_names)
        user_df = get_data_from_db(get_statement, connection, cursor, user_df, col_names)[0][0]
        customer_folder = user_df['files_path']
        edaObject = ExploratoryDataAnalysis(user_id, customer_folder, app.root_path)
        edaResult = {
            "dataDistributionPlots": edaObject.dataDistributionPlots,
            "emissionIndexPlots": edaObject.emissionIndexPlots,
            "correlationMatrixPlot": edaObject.correlationMatrixPlot,
            "zScorePlot": edaObject.zScorePlot,
            "pairplotPlot": edaObject.pairplotPlot
        }
        success = True
    except Exception as e:
        print(f"Couldn't process EDA: {e}")
    
    return jsonify({
        "success": success,
        "data": edaResult
    })

@app.route('/predict', methods=['POST'])
def predict():
    success = False
    predictionResult = None
    try:
        req = request.get_json(force=True)
        user_id = request.cookies.get('user_id')
        get_statement = "SELECT * from " + USER_TABLE + " WHERE user_id='" + user_id + "'"
        col_names = get_column_names(USER_TABLE, cursor)
        user_df = pd.DataFrame(columns=col_names)
        user_df = get_data_from_db(get_statement, connection, cursor, user_df, col_names)[0][0]
        customer_folder = user_df['files_path']
        predictionResult = {}
        if (req["modelType"] == "classification"):
            predictionObject = Classification(user_id, customer_folder, app.root_path, req["modelID"])
            predictionResult["type"] = "classification"
            predictionResult["dataOverview"] = predictionObject.dataOverview
            predictionResult["aqiClasses"] = predictionObject.aqiClasses
            predictionResult["aqiByLocation"] = predictionObject.aqiByLocation
            predictionResult["aqiByMonth"] = predictionObject.aqiByMonth
            predictionResult["correlationMatrix"] = predictionObject.correlationMatrix
        elif (req["modelType"] == "regression"):
            predictionObject = Regression(user_id, customer_folder, app.root_path, req["modelID"])
            predictionResult["type"] = "regression"
            predictionResult["aqiByLocation"] = predictionObject.aqiByLocation
            predictionResult["aqiPercantage"] = predictionObject.aqiPercantage
            predictionResult["aqiByTime"] = predictionObject.aqiByTime
            predictionResult["correlationMatrix"] = predictionObject.correlationMatrix
        success = True
    except Exception as e:
        print(f"Couldn't process prediction: {e}")
    
    return jsonify({
        "success": success,
        "data": predictionResult
    })


# Running app
if __name__ == '__main__':
    app.run(debug=True)
