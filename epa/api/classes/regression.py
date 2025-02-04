from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
import os
import sys
sys.path.append('../')

from helpers.predictHelper import *
from helpers.imgHelper import *
from helpers.dbHelper import *

warnings.filterwarnings('ignore')
matplotlib.use("agg")


REGRESSION_FOLDER = "/regression/"
REGRESSION_REPORT_FILE_NAME = "regressionReport.csv"
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
    def scaleData(self, dataframe, modelID):
        try:
            # Data scaling (use the same scaler as during training)
            scaler = MinMaxScaler()
            X_new_scaled = scaler.fit_transform(dataframe)
            if (modelID == 'lstm'):
                X_new_scaled = np.expand_dims(X_new_scaled, axis=1)
            elif (isKerasModel(modelID)): 
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
            img_path = generateImgFullPath(user_id, REGRESSION_FOLDER, AQI_BY_LOCATION_FILE_NAME, modelID)
            if (checkIfImgExists(root_folder, img_path) == False):
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
                img_path = saveImageToStaticFolder(user_id, root_folder, REGRESSION_FOLDER, AQI_BY_LOCATION_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateAQIByLocationPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def percantageAQIDistributionPlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = generateImgFullPath(user_id, REGRESSION_FOLDER, AQI_PIE_FILE_NAME, modelID)
            if (checkIfImgExists(root_folder, img_path) == False):
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
                img_path = saveImageToStaticFolder(user_id, root_folder, REGRESSION_FOLDER, AQI_PIE_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- percantageAQIDistributionPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateCorrelationMatrixPlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = generateImgFullPath(user_id, REGRESSION_FOLDER, CORR_MATRIX_FILE_NAME, modelID)
            if (checkIfImgExists(root_folder, img_path) == False):
                corr_matrix = extendedDf[['AQI', 'PM2.5', 'PM10', 'O3', 'CO', 'SO2', 'NO2']].corr()
                plt.plot(legend=False)
                sns.heatmap(corr_matrix, annot=True, cmap='RdBu', fmt=".2f")
                plt.title('Correlation matrix')
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, REGRESSION_FOLDER, CORR_MATRIX_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateCorrelationMatrixPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateAQIByTimePlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = generateImgFullPath(user_id, REGRESSION_FOLDER, AQI_BY_DATE_FILE_NAME, modelID)
            if (checkIfImgExists(root_folder, img_path) == False):
                extendedDf['Date'] = pd.to_datetime(extendedDf[['Year', 'Month', 'Day']])
                time_aqi = extendedDf.groupby('Date')['AQI'].mean().reset_index()
                plt.plot(time_aqi['Date'], time_aqi['AQI'], marker='.', linestyle='-', color='purple')
                plt.title('AQI dynamics over time')
                plt.xlabel('Date')
                plt.ylabel('Average AQI')
                plt.xticks(rotation=45)
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, REGRESSION_FOLDER, AQI_BY_DATE_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateAQIByTimePlot error")
            print(f"-{type(error).__name__}: {error}")

    def __init__(self, user_id, customer_folder, root_folder, modelID):
        try:
            # Get customer data
            dataframe = getCustomerData(customer_folder)
            strLocation = dataframe['Location'].copy()
            processedDf = prepareData(dataframe)
            # Data scaling
            scaledData = self.scaleData(processedDf, modelID)
            # Call serialized model
            model = callModel(root_folder, modelID, SERIALIZED_MODELS)
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
            # Create Zip archive
            archive_folder = STATIC_FOLDER + user_id + REGRESSION_FOLDER + modelID
            zipDirectory(os.path.join(root_folder, archive_folder))
            self.archiveFilePath = archive_folder + ZIP_EXTENSION

            plt.close("all")
        except Exception as error:
            print("- regression init error")
            print(f"-{type(error).__name__}: {error}")



        


