from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
import zipfile
import pickle
import os



ZIP_EXTENSION = '.zip'
KERAS_MODELS = ['dnn', 'lstm', 'mlp']
SERIALIZED_MODELS_FOLDER = "./models"
STATIC_FOLDER = "static/active_sessions/"

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
                print(f"- {type(error).__name__}: {error}")

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
            print(f"- {type(error).__name__}: {error}")

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
            print(f"- {type(error).__name__}: {error}")