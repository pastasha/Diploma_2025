from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np
import pickle
import os

matplotlib.use("agg")

KERAS_MODELS = ['dnn', 'lstm', 'mlp']
DATA_FILE_NAME = "/data.csv"
SERIALIZED_MODELS_FOLDER = "./models"
CLASSIFICATION_FOLDER = "/classification"
REGRESSION_FOLDER = "/regression"

SERIALIZED_MODELS = {
    "classification": {
        "decisiontree": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/decisionTreeModel.pkl",
        "randomforest": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/randomForestModel.pkl",
        "xgboost": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/XGBoostModel.pkl",
        "dnn": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/dnnModel.keras",
        "lstm": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/lstmModel.keras",
        "mlp": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/mlpModel.keras"
    },
    "regression": {
        "decisiontree": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/decisionTreeModel.pkl",
        "randomforest": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/randomForestModel.pkl",
        "xgboost": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/XGBoostModel.pkl",
        "dnn": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/dnnModel.keras",
        "lstm": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/lstmModel.keras",
        "mlp": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/mlpModel.keras"
    }
}


class Predict:
    @staticmethod
    def getCustomerData(customer_folder):
        try:
            data_path = customer_folder + DATA_FILE_NAME
            data = os.path.abspath(data_path)
            dataframe = pd.read_csv(data)
            return dataframe
        except Exception as error:
            print("- getCustomerData error:")
            print(f"- {type(error).__name__}: {error}")

    def prepareData(self, dataframe):
        try:
            requiredColumns = ["Location", "Day", "Hour", "PM2.5", "PM10", "O3", "CO", "SO2", "NO2"]
            processedDf = dataframe.loc[:, dataframe.columns.intersection(requiredColumns)]
            # Label encoding
            le = LabelEncoder()
            processedDf['Location'] = le.fit_transform(processedDf['Location'])
            processedDf['Hour'] = le.fit_transform(processedDf['Hour'])
            return processedDf
        except Exception as error:
                print("- prepareData error:")
                print(f"- {type(error).__name__}: {error}")

    def isKerasModel(self, modelID):
        if modelID in KERAS_MODELS:
            return True;
        else:
            return False;

    def callModel(self, root_folder, modelType, modelID):
        try:
            model_path = os.path.join(root_folder, SERIALIZED_MODELS[modelType][modelID])
            model = ''
            if self.isKerasModel(modelID):
                model = load_model(model_path)
            else:
                model = pickle.load(open(model_path, 'rb'))
            return model
        except Exception as error:
                print("- callModel error:")
                print(f"- {type(error).__name__}: {error}")

    def scaleData(self, dataframe, modelID):
        try:
            # Data scaling (use the same scaler as during training)
            scaler = MinMaxScaler()
            X_new_scaled = scaler.fit_transform(dataframe)
            if (self.isKerasModel(modelID)):
                X_new_scaled = np.expand_dims(X_new_scaled, axis=2)
            return X_new_scaled
        except Exception as error:
                print("- scaleData error:")
                print(f"- {type(error).__name__}: {error}")

    def predict(self, model, data):
        try:
            prediction = model.predict(data)
            return prediction
        except Exception as error:
                print("- predict error:")
                print(f"- {type(error).__name__}: {error}")
    
    def predictProba(self, model, data):
        try:
            predict_proba = model.predict_proba(data)
            return predict_proba
        except Exception as error:
                print("- predictProba error:")
                print(f"- {type(error).__name__}: {error}")

    def classificationResult(self, prediction, modelType, modelID):
        try:
            if (self.isKerasModel(modelID)):
                prediction = np.argmax(prediction, axis=1)
            elif (modelID == 'decisiontree'):
                prediction = np.argmax(prediction, axis=1)
            # Displaying categories
            category_mapping = {
                '0': 'Good',
                '1': 'Moderate',
                '2': 'USG', 
                '3': 'Unhealthy',
                '4': 'Very Unhealthy',
                '5': 'Severe'
            }
            predicted_categories = [category_mapping[str(cls)] for cls in prediction]
            return predicted_categories;
        except Exception as error:
                print("- classificationResult error:")
                print(f"- {type(error).__name__}: {error}")

    def __init__(self, user_id, customer_folder, root_folder, modelType, modelID):
        # Get customer data
        dataframe = self.getCustomerData(customer_folder)
        # Process data
        processedDf = self.prepareData(dataframe)
        # Data scaling
        scaledData = self.scaleData(processedDf, modelID)
        # Call serialized model
        model = self.callModel(root_folder, modelType, modelID)
        # Predict results
        prediction = ''
        if (modelType == 'classification' and modelID == 'decisiontree'):
            prediction = self.predictProba(model, scaledData)
        else:
            prediction = self.predict(model, scaledData)
        self.predictionResult = prediction
        print(self.predictionResult)
        self.predictedCategories = self.classificationResult(prediction, modelType, modelID)
        print(self.predictedCategories)

        


