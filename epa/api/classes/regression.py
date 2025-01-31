from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np
import pickle
import warnings
import shutil
import os

warnings.filterwarnings('ignore')

matplotlib.use("agg")

KERAS_MODELS = ['dnn', 'lstm', 'mlp']
DATA_FILE_NAME = "/data.csv"
SERIALIZED_MODELS_FOLDER = "./models"
REGRESSION_FOLDER = "/regression/"
STATIC_FOLDER = "static/active_sessions/"
REGRESSION_REPORT_FILE_NAME = "regressionReport.csv"
IMG_EXTENSION = ".png"
AQI_BY_LOCATION_FILE_NAME = "aqiByLocation" + IMG_EXTENSION
AQI_BY_DATE_FILE_NAME = "aqiByDate" + IMG_EXTENSION
AQI_PIE_FILE_NAME = "aqiPie" + IMG_EXTENSION
CORR_MATRIX_FILE_NAME = "corrMatrix" + IMG_EXTENSION


SERIALIZED_MODELS = {
    "decisiontree": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/decisionTreeModel.pkl",
    "randomforest": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/randomForestModel.pkl",
    "xgboost": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/XGBoostModel.pkl",
    "dnn": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/dnnModel.keras",
    "lstm": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/lstmModel.keras",
    "mlp": SERIALIZED_MODELS_FOLDER + REGRESSION_FOLDER + "/mlpModel.keras"
}


class Regression:
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

    def isKerasModel(self, modelID):
        if modelID in KERAS_MODELS:
            return True;
        else:
            return False;

    @staticmethod
    def generateImgFullPath(user_id, img_folder, img_name, modelID):
        img_path = STATIC_FOLDER + user_id + img_folder + modelID
        full_path = img_path + "/" + img_name
        return full_path
    
    @staticmethod
    def saveImageToStaticFolder(user_id, root_folder, img_folder, img_name, modelID):
        img_path = STATIC_FOLDER + user_id + img_folder + modelID
        os.makedirs(os.path.join(root_folder, img_path), exist_ok=True)
        filename = secure_filename(img_name)
        plt.savefig(os.path.join(img_path, filename))
        return img_path + "/" + filename

    @staticmethod
    def checkIfImgExists(root_folder, img_path):
        imgExists = False
        if (os.path.isfile(os.path.join(root_folder, img_path))):
            imgExists = True
        return imgExists

    def callModel(self, root_folder, modelID):
        try:
            model_path = os.path.join(root_folder, SERIALIZED_MODELS[modelID])
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
            if (modelID == 'lstm'):
                X_new_scaled = np.expand_dims(X_new_scaled, axis=1)
            elif (self.isKerasModel(modelID)): 
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

    @staticmethod
    def extendDataframe(root_folder, prediction, dataframe, user_id, modelID):
        try:
            extendedDF = dataframe.copy()
            extendedDF['AQI'] = prediction
            file_path = STATIC_FOLDER + user_id + REGRESSION_FOLDER + modelID
            os.makedirs(os.path.join(root_folder, file_path), exist_ok=True)
            full_path = os.path.join(file_path, secure_filename(REGRESSION_REPORT_FILE_NAME))
            extendedDF.to_csv(full_path)
            return {
                "extendedDF": extendedDF,
                "fullPath": full_path
            }
        except Exception as error:
                print("- extendDataframe error:")
                print(f"- {type(error).__name__}: {error}")

    @staticmethod
    def generateAQIByLocationPlot(self, extendedDf, user_id, root_folder, modelID, strLocation):
        try:
            img_path = self.generateImgFullPath(user_id, REGRESSION_FOLDER, AQI_BY_LOCATION_FILE_NAME, modelID)
            if (self.checkIfImgExists(root_folder, img_path) == False):
                dfWithLocation = extendedDf.copy()
                dfWithLocation['strLocation'] = strLocation
                figWidth = 10
                if (strLocation.size > 5):
                    figWidth = 20
                elif (strLocation.size > 10):
                    figWidth = 35
                plt.figure(figsize=(figWidth, 6))
                location_aqi = dfWithLocation.groupby('strLocation')['AQI'].mean().reset_index()
                sns.barplot(data=location_aqi, x='strLocation', y='AQI', palette='rocket')
                plt.title('Average AQI for each location')
                plt.xlabel('strLocation')
                plt.ylabel('Average AQI')
                # save result
                img_path = self.saveImageToStaticFolder(user_id, root_folder, REGRESSION_FOLDER, AQI_BY_LOCATION_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateAQIByLocationPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def percantageAQIDistributionPlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = self.generateImgFullPath(user_id, REGRESSION_FOLDER, AQI_PIE_FILE_NAME, modelID)
            if (self.checkIfImgExists(root_folder, img_path) == False):
                aqi_distribution = extendedDf['AQI'].value_counts(bins=5)
                # Побудова кругової діаграми
                plt.figure(figsize=(8, 8))
                aqi_distribution.plot.pie(
                    autopct='%1.1f%%', 
                    startangle=140, 
                    colors=sns.color_palette('coolwarm'),
                    wedgeprops={'edgecolor': 'black'}
                )
                plt.title('Percentage distribution of AQI')
                plt.ylabel('')  # Remove the Y axis label
                # save result
                img_path = self.saveImageToStaticFolder(user_id, root_folder, REGRESSION_FOLDER, AQI_PIE_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- percantageAQIDistributionPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateCorrelationMatrixPlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = self.generateImgFullPath(user_id, REGRESSION_FOLDER, CORR_MATRIX_FILE_NAME, modelID)
            if (self.checkIfImgExists(root_folder, img_path) == False):
                corr_matrix = extendedDf[['AQI', 'PM2.5', 'PM10', 'O3', 'CO', 'SO2', 'NO2']].corr()
                plt.plot(legend=False)
                sns.heatmap(corr_matrix, annot=True, cmap='RdBu', fmt=".2f")
                plt.title('Correlation matrix')
                # save result
                img_path = self.saveImageToStaticFolder(user_id, root_folder, REGRESSION_FOLDER, CORR_MATRIX_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateCorrelationMatrixPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateAQIByTimePlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = self.generateImgFullPath(user_id, REGRESSION_FOLDER, AQI_BY_DATE_FILE_NAME, modelID)
            if (self.checkIfImgExists(root_folder, img_path) == False):
                extendedDf['Date'] = pd.to_datetime(extendedDf[['Year', 'Month', 'Day']])
                time_aqi = extendedDf.groupby('Date')['AQI'].mean().reset_index()
                plt.plot(time_aqi['Date'], time_aqi['AQI'], marker='.', linestyle='-', color='purple')
                plt.title('AQI dynamics over time')
                plt.xlabel('Date')
                plt.ylabel('Average AQI')
                plt.xticks(rotation=45)
                # save result
                img_path = self.saveImageToStaticFolder(user_id, root_folder, REGRESSION_FOLDER, AQI_BY_DATE_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateAQIByTimePlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))

    def __init__(self, user_id, customer_folder, root_folder, modelID):
        try:
            # Get customer data
            dataframe = self.getCustomerData(customer_folder)
            strLocation = dataframe['Location'].copy()
            processedDf = self.prepareData(dataframe)
            # Data scaling
            scaledData = self.scaleData(processedDf, modelID)
            # Call serialized model
            model = self.callModel(root_folder, modelID)
            # Predict results
            prediction = self.predict(model, scaledData)
            extendedDfObj = self.extendDataframe(root_folder, prediction, processedDf, user_id, modelID)
            extendedDf = extendedDfObj["extendedDF"]
            self.extendedDfPath = extendedDfObj["fullPath"]
            self.extendedDfFull = extendedDf.to_csv()
            self.aqiByTime = self.generateAQIByTimePlot(self, extendedDf, user_id, root_folder, modelID)
            self.correlationMatrix = self.generateCorrelationMatrixPlot(self, extendedDf, user_id, root_folder, modelID)
            self.aqiByLocation = self.generateAQIByLocationPlot(self, extendedDf, user_id, root_folder, modelID, strLocation)
            self.aqiPercantage = self.percantageAQIDistributionPlot(self, extendedDf, user_id, root_folder, modelID)
            archive_folder = STATIC_FOLDER + user_id + REGRESSION_FOLDER + modelID
            archive_file_path = archive_folder + '.zip'
            shutil.make_archive(archive_folder, 'zip', archive_file_path)
            self.archiveFilePath = archive_file_path
            plt.close("all")
        except Exception as error:
            print("- regression init error")
            print(f"-{type(error).__name__}: {error}")



        


