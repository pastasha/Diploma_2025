from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
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


CLASSIFICATION_REPORT_FILE_NAME = "classificationReport.csv"
DATA_OVERVIEW_FILE_NAME = "dataOverview" + IMG_EXTENSION
AQI_CLASSES_FILE_NAME = "aqiClasses" + IMG_EXTENSION
AQI_BY_LOCATION_FILE_NAME = "aqiByLocation" + IMG_EXTENSION
AQI_BY_MONTH_FILE_NAME = "aqiByMonth" + IMG_EXTENSION
CORR_MATRIX_FILE_NAME = "corrMatrix" + IMG_EXTENSION


SERIALIZED_MODELS = {
    "decisiontree": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/decisionTreeModel.pkl",
    "randomforest": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/randomForestModel.pkl",
    "xgboost": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/XGBoostModel.pkl",
    "dnn": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/dnnModel.keras",
    "lstm": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/lstmModel.keras",
    "mlp": SERIALIZED_MODELS_FOLDER + CLASSIFICATION_FOLDER + "/mlpModel.keras"
}


class Classification:
    def scaleData(self, dataframe, modelID):
        try:
            # Data scaling (use the same scaler as during training)
            scaler = MinMaxScaler()
            X_new_scaled = scaler.fit_transform(dataframe)
            if (isKerasModel(modelID)):
                X_new_scaled = np.expand_dims(X_new_scaled, axis=2)
            return X_new_scaled
        except Exception as error:
                print("- scaleData error:")
                print(f" - {type(error).__name__}: {error}")

    def predict(self, model, data):
        try:
            prediction = model.predict(data)
            return prediction
        except Exception as error:
                print("- predict error:")
                print(f" - {type(error).__name__}: {error}")
    
    def predictProba(self, model, data):
        try:
            predict_proba = model.predict_proba(data)
            return predict_proba
        except Exception as error:
                print("- predictProba error:")
                print(f" - {type(error).__name__}: {error}")

    def classificationResult(self, prediction, modelID):
        try:
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
                print(f" - {type(error).__name__}: {error}")

    @staticmethod
    def extendDataframe(root_folder, prediction, predictedCategories, dataframe, user_id, modelID):
        try:
            extendedDF = dataframe.copy()
            extendedDF['AQI'] = prediction
            extendedDF['AQI_Ctegories'] = predictedCategories
            file_path = STATIC_FOLDER + user_id + CLASSIFICATION_FOLDER + modelID
            os.makedirs(os.path.join(root_folder, file_path), exist_ok=True)
            full_path = os.path.join(file_path, secure_filename(CLASSIFICATION_REPORT_FILE_NAME))
            extendedDF.to_csv(full_path, index=False, encoding='utf-8')
            return {
                "extendedDF": extendedDF,
                "fullPath": full_path
            }
        except Exception as error:
                print("- extendDataframe error:")
                print(f" - {type(error).__name__}: {error}")

    @staticmethod
    def generateDataOverviewPlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = generateImgFullPath(user_id, CLASSIFICATION_FOLDER, DATA_OVERVIEW_FILE_NAME, modelID)
            if (checkIfImgExists(root_folder, img_path) == False):
                plt.figure(figsize=(12,6))
                plt.title('Class Distribution of Processed Dataset')
                plt.ylabel('Average AQI')
                custom_order = ['Good', 'Moderate', 'USG', 'Unhealthy', 'Very Unhealthy', 'Severe']
                sns.countplot(data=extendedDf,x='AQI_Ctegories', order=custom_order, palette='vlag')
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, CLASSIFICATION_FOLDER, DATA_OVERVIEW_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateDataOverviewPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateAQIClassesPlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = generateImgFullPath(user_id, CLASSIFICATION_FOLDER, AQI_CLASSES_FILE_NAME, modelID)
            if (checkIfImgExists(root_folder, img_path) == False):
                aqi_class_distribution = extendedDf['AQI_Ctegories'].value_counts()
                plt.figure(figsize=(8, 8))
                aqi_class_distribution.plot.pie(
                    autopct='%1.1f%%', 
                    startangle=140, 
                    colors=sns.color_palette('coolwarm'),
                    wedgeprops={'edgecolor': 'black'}
                )
                plt.title('Percentage distribution of AQI classes')
                plt.ylabel('')
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, CLASSIFICATION_FOLDER, AQI_CLASSES_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateAQIClassesPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateAQIByLocationPlot(self, extendedDf, user_id, root_folder, modelID, strLocation):
        try:
            img_path = generateImgFullPath(user_id, CLASSIFICATION_FOLDER, AQI_BY_LOCATION_FILE_NAME, modelID)
            if (checkIfImgExists(root_folder, img_path) == False):
                dfWithLocation = extendedDf.copy()
                dfWithLocation['strLocation'] = strLocation
                figWidth = 10
                if (strLocation.size > 5):
                    figWidth = 20
                elif (strLocation.size > 10):
                    figWidth = 35
                plt.figure(figsize=(figWidth, 6))
                sns.countplot(data=dfWithLocation, x='strLocation', hue='AQI_Ctegories', palette='coolwarm')
                plt.title('Distribution of AQI classes by location')
                plt.xlabel('Location')
                plt.ylabel('Average AQI')
                plt.legend(title='Клас AQI', loc='upper right')
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, CLASSIFICATION_FOLDER, AQI_BY_LOCATION_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateAQIByLocationPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateAQIByMonthPlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = generateImgFullPath(user_id, CLASSIFICATION_FOLDER, AQI_BY_MONTH_FILE_NAME, modelID)
            if (checkIfImgExists(root_folder, img_path) == False):
                plt.figure(figsize=(10, 6))
                sns.countplot(data=extendedDf, x='Month', hue='AQI_Ctegories', palette='coolwarm')
                plt.title('Distribution of AQI classes by month')
                plt.xlabel('Month')
                plt.ylabel('Average AQI')
                plt.legend(title='AQI Class', loc='upper right')
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, CLASSIFICATION_FOLDER, AQI_BY_MONTH_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateAQIByMonthPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateCorrelationMatrixPlot(self, extendedDf, user_id, root_folder, modelID):
        try:
            img_path = generateImgFullPath(user_id, CLASSIFICATION_FOLDER, CORR_MATRIX_FILE_NAME, modelID)
            if (checkIfImgExists(root_folder, img_path) == False):
                corr_matrix = extendedDf[['AQI', 'PM2.5', 'PM10', 'O3', 'CO', 'SO2', 'NO2']].corr()
                plt.plot(legend=False)
                sns.heatmap(corr_matrix, annot=True, cmap='RdBu', fmt=".2f")
                plt.title('Correlation matrix')
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, CLASSIFICATION_FOLDER, CORR_MATRIX_FILE_NAME, modelID)
            return img_path
        except Exception as error:
            print("- generateCorrelationMatrixPlot error")
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
            prediction = ''
            if (modelID == 'decisiontree'):
                predict_proba = self.predictProba(model, scaledData)
                prediction = np.argmax(predict_proba, axis=1)
            elif (isKerasModel(modelID)):
                prediction = self.predict(model, scaledData)
                prediction = np.argmax(prediction, axis=1)
            else:
                prediction = self.predict(model, scaledData)
            predictedCategories = self.classificationResult(prediction, modelID)
            extendedDfObj = self.extendDataframe(root_folder, prediction, predictedCategories, processedDf, user_id, modelID)
            extendedDf = extendedDfObj["extendedDF"]
            self.extendedDfPath = extendedDfObj["fullPath"]
            self.extendedDfFull = extendedDf.head(5).to_csv(index=False, encoding='utf-8')
            self.correlationMatrix = self.generateCorrelationMatrixPlot(self, extendedDf, user_id, root_folder, modelID)
            self.dataOverview = self.generateDataOverviewPlot(self, extendedDf, user_id, root_folder, modelID)
            self.aqiClasses = self.generateAQIClassesPlot(self, extendedDf, user_id, root_folder, modelID)
            self.aqiByLocation = self.generateAQIByLocationPlot(self, extendedDf, user_id, root_folder, modelID, strLocation)
            self.aqiByMonth = self.generateAQIByMonthPlot(self, extendedDf, user_id, root_folder, modelID)
            # Create Zip archive
            archive_folder = STATIC_FOLDER + user_id + CLASSIFICATION_FOLDER + modelID
            zipDirectory(os.path.join(root_folder, archive_folder))
            self.archiveFilePath = archive_folder + ZIP_EXTENSION
            # Append the compare df
            appendCompareDf(root_folder, COMPARE_CLASSIFICATION_FOLDER, dataframe, extendedDf['AQI_Ctegories'], user_id, modelID)
            # Close all the plots
            plt.close("all")
        except Exception as error:
            print("- classification init error")
            print(f"-{type(error).__name__}: {error}")




        


