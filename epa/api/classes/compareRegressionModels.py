import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import warnings
import sys
sys.path.append('../')

from helpers.predictHelper import *
from helpers.imgHelper import *
from helpers.dbHelper import *

warnings.filterwarnings('ignore')
matplotlib.use("agg")

BOXPLOT_FILE_NAME = "boxplot" + IMG_EXTENSION
MODEL_PRED_VAL_FILE_NAME = "modelPredValuesPlot" + IMG_EXTENSION
CORR_MATRIX_FILE_NAME = "corrMatrix" + IMG_EXTENSION
AQI_FORECAST = "aqiForecast" + IMG_EXTENSION

COMPARE_DATA_FILE_NAME
class compareRegression:
    @staticmethod
    def generateBoxPlot(dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, COMPARE_REGRESSION_FOLDER, BOXPLOT_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                plt.figure(figsize=(10, 6))
                sns.boxplot(data=dataframe)
                plt.title("Distribution of forecasts from different models")
                plt.ylabel("Predicted AQI value")
                plt.xlabel("Model")
                plt.xticks(rotation=45)
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, COMPARE_REGRESSION_FOLDER, BOXPLOT_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generateBoxPlot error")
            print(f" - {type(error).__name__}: {error}")

    @staticmethod
    def generateModelPredValuesPlot(dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, COMPARE_REGRESSION_FOLDER, MODEL_PRED_VAL_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                plt.figure(figsize=(12, 6))
                for model in MODEL_COLUMNS:
                    sns.kdeplot(dataframe[model], label=model, fill=True)
                plt.title("Distribution of model prediction values")
                plt.xlabel("Predicted AQI value")
                plt.ylabel("Density")
                plt.legend()
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, COMPARE_REGRESSION_FOLDER, MODEL_PRED_VAL_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generateModelPredValuesPlot error")
            print(f" - {type(error).__name__}: {error}")

    @staticmethod
    def generateCorrelationMatrixPlot(dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, COMPARE_REGRESSION_FOLDER, CORR_MATRIX_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                df_models = dataframe[MODEL_COLUMNS]
                plt.figure(figsize=(8, 6))
                sns.heatmap(df_models.corr(), annot=True, cmap="coolwarm", fmt=".2f")
                plt.title("Correlation matrix of model predictions")
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, COMPARE_REGRESSION_FOLDER, CORR_MATRIX_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generateCorrelationMatrixPlot error")
            print(f" - {type(error).__name__}: {error}")

    @staticmethod
    def generateAQIForecastPlot(dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, COMPARE_REGRESSION_FOLDER, AQI_FORECAST, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                plt.figure(figsize=(10, 6))
                for model in MODEL_COLUMNS:
                    plt.plot(dataframe['Day'], dataframe[model], marker='o', label=model)
                plt.title("AQI forecast by models depending on date")
                plt.xlabel("Day")
                plt.ylabel("Prediction AQI")
                plt.legend()
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, COMPARE_REGRESSION_FOLDER, AQI_FORECAST, None)
            return img_path
        except Exception as error:
            print("- generateAQIForecastPlot error")
            print(f" - {type(error).__name__}: {error}")

    def __init__(self, user_id, root_folder):
        try:
            # Get customer data
            dataframe = getCompareDf(root_folder, COMPARE_REGRESSION_FOLDER, user_id)
            # Generate Boxplot
            self.boxplotPlot = self.generateBoxPlot(dataframe, user_id, root_folder)
            # Generate model prediction values plot
            self.modelPredValuesPlot = self.generateModelPredValuesPlot(dataframe, user_id, root_folder)
            # Generate correlation matrix
            self.corrMatrixPlot = self.generateCorrelationMatrixPlot(dataframe, user_id, root_folder)
            # Generate correlation matrix
            self.aqiForecastPlot = self.generateAQIForecastPlot(dataframe, user_id, root_folder)
            # Close all the plots
            plt.close("all")
        except Exception as error:
            print("- compare regression models init error")
            print(f" - {type(error).__name__}: {error}")




        


