from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
import pandas as pd
import zipfile
import pickle
import os



ZIP_EXTENSION = '.zip'
KERAS_MODELS = ['dnn', 'lstm', 'mlp']
SERIALIZED_MODELS_FOLDER = "./models"
STATIC_FOLDER = "static/active_sessions/"
COMPARE_DATA_FILE_NAME = "compareData.csv"
REGRESSION_FOLDER = "/regression/"
CLASSIFICATION_FOLDER = "/classification/"
COMPARE_REGRESSION_FOLDER = REGRESSION_FOLDER + "compare/"
COMPARE_CLASSIFICATION_FOLDER = CLASSIFICATION_FOLDER + "compare/"
MODEL_COLUMNS = ['decisiontree', 'randomforest', 'xgboost', 'dnn', 'lstm', 'mlp']

def isKerasModel(modelID):
        if modelID in KERAS_MODELS:
            return True;
        else:
            return False;

def zipDirectory(folder_path):
    """
    Creates a ZIP archive with all files in the specified directory.
    :param folder_path: Path to the directory whose files you want to archive
    :param zip_name: Name of the output ZIP file (with the extension .zip)
    """
    try:
        with zipfile.ZipFile(folder_path + ZIP_EXTENSION, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname)
        print(f"Archive {folder_path} is created.")
    except Exception as error:
                print("- zipDirectory error:")
                print(f" - {type(error).__name__}: {error}")

def prepareData(dataframe):
    try:
        processedDf = dataframe[["Location", "Year", "Month", "Day", "Hour", "PM2.5", "PM10", "O3", "CO", "SO2", "NO2"]].copy()
        # Label encoding
        le = LabelEncoder()
        processedDf["Location"] = le.fit_transform(processedDf["Location"])
        processedDf["Hour"] = le.fit_transform(processedDf["Hour"])
        processedDf.fillna(processedDf.mean(), inplace=True)
        return processedDf
    except Exception as error:
            print("- prepareData error:")
            print(f" - {type(error).__name__}: {error}")

def callModel(root_folder, modelID, SERIALIZED_MODELS):
    try:
        model_path = os.path.join(root_folder, SERIALIZED_MODELS[modelID])
        model = ''
        if isKerasModel(modelID):
            model = load_model(model_path)
        else:
            model = pickle.load(open(model_path, 'rb'))
        return model
    except Exception as error:
            print("- callModel error:")
            print(f" - {type(error).__name__}: {error}")

def getCompareDf(root_folder, modelByTypeFolder, user_id):
    try:
        file_path = os.path.join(STATIC_FOLDER + user_id + modelByTypeFolder, secure_filename(COMPARE_DATA_FILE_NAME))
        if (os.path.isfile(os.path.join(root_folder, file_path))):
            df = pd.read_csv(os.path.abspath(file_path))
            return df
        else:
            raise Exception("Can't find the compare dataframe: " + file_path)
    except Exception as error:
            print("- compareDataframe error:")
            print(f" - {type(error).__name__}: {error}")

def appendCompareDf(root_folder, modelByTypeFolder, dataframe, prediction, user_id, modelID):
    try:
        df = ''
        folder_path = os.path.join(STATIC_FOLDER + user_id + modelByTypeFolder)
        file_path = os.path.join(folder_path, secure_filename(COMPARE_DATA_FILE_NAME))
        os.makedirs(folder_path, exist_ok=True)
        if (os.path.isfile(os.path.join(root_folder, file_path))):
            df = pd.read_csv(os.path.abspath(file_path))
        else:
            df = dataframe[["Location", "Year", "Month", "Day", "Hour"]].copy()
        df[modelID] = prediction
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        print(file_path)
        df.to_csv(file_path, index=False, encoding='utf-8')
    except Exception as error:
            print("- appendCompareDf error:")
            print(f" - {type(error).__name__}: {error}")

def prepareDataToCompare(dataframe):
    try:
        df_models = dataframe[MODEL_COLUMNS]
        return df_models
    except Exception as error:
            print("- prepareDataToCompare error:")
            print(f" - {type(error).__name__}: {error}")