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

FORECAST_COMPARE_FILE_NAME = "forecastCompare" + IMG_EXTENSION
HEATMAP_FILE_NAME = "heatmap" + IMG_EXTENSION
AQI_DISTRIBUTION_FILE_NAME = "aqiDistribution" + IMG_EXTENSION
POPULARITY_FORECAST = "popularity" + IMG_EXTENSION

class compareClassification:
    @staticmethod
    def generateForecastComparePlot(dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, COMPARE_CLASSIFICATION_FOLDER, FORECAST_COMPARE_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                plt.figure(figsize=(12, 6))
                for model in MODEL_COLUMNS:
                    sns.countplot(y=dataframe[model], label=model, alpha=0.7)
                plt.title("Comparing forecasts from different models")
                plt.xlabel("Number of predictions")
                plt.ylabel("AQI Class")
                plt.legend()
                plt.show()
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, COMPARE_CLASSIFICATION_FOLDER, FORECAST_COMPARE_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generateForecastComparePlot error")
            print(f" - {type(error).__name__}: {error}")

    @staticmethod
    def generateHeatmapPlot(dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, COMPARE_CLASSIFICATION_FOLDER, HEATMAP_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                df_melted = dataframe.melt(id_vars=["Location"], value_vars=MODEL_COLUMNS, var_name="Model", value_name="AQI_Class")
                plt.figure(figsize=(10, 6))
                heatmap_data = df_melted.pivot_table(index="AQI_Class", columns="Model", aggfunc="size", fill_value=0)
                sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", fmt="d")
                plt.title("Frequency of model predictions")
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, COMPARE_CLASSIFICATION_FOLDER, HEATMAP_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generateHeatmapPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateAQIDistributionPlot(dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, COMPARE_CLASSIFICATION_FOLDER, AQI_DISTRIBUTION_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                plt.figure(figsize=(12, 6))
                df_melted = dataframe.melt(id_vars=["Location"], value_vars=MODEL_COLUMNS, var_name="Model", value_name="AQI_Class")
                sns.histplot(data=df_melted, x="Location", hue="AQI_Class", multiple="stack", shrink=0.8)
                plt.title("Distribution of AQI class predictions by location")
                plt.xlabel("Location")
                plt.ylabel("Number of predictions")
                plt.xticks(rotation=45)
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, COMPARE_CLASSIFICATION_FOLDER, AQI_DISTRIBUTION_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generateAQIDistributionPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generatePopularityPlot(dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, COMPARE_CLASSIFICATION_FOLDER, POPULARITY_FORECAST, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                df_melted = dataframe.melt(id_vars=["Location"], value_vars=MODEL_COLUMNS, var_name="Model", value_name="AQI_Class")
                plt.figure(figsize=(12, 6))
                sns.countplot(y=df_melted["AQI_Class"], hue=df_melted["Model"])
                plt.title("Popularity of model predictions")
                plt.xlabel("Number")
                plt.ylabel("AQI Class")
                plt.legend(title="Model")
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, COMPARE_CLASSIFICATION_FOLDER, POPULARITY_FORECAST, None)
            return img_path
        except Exception as error:
            print("- generatePopularityPlot error")
            print(f"-{type(error).__name__}: {error}")

    def __init__(self, user_id, root_folder):
        try:
            # Get customer data
            compareDfObj = getCompareDf(root_folder, COMPARE_CLASSIFICATION_FOLDER, user_id)
            dataframe = compareDfObj["dataframe"]
            # Generate Forecast compare plot
            self.forecastComparePlot = self.generateForecastComparePlot(dataframe, user_id, root_folder)
            # Generate Heatmap plot
            self.heatmapPlot = self.generateHeatmapPlot(dataframe, user_id, root_folder)
            # Generate AQI distribution plot
            self.aqiDistributionPlot = self.generateAQIDistributionPlot(dataframe, user_id, root_folder)
            # Generate popularity plot
            self.popularityPlot = self.generatePopularityPlot(dataframe, user_id, root_folder)
            # Download CSV report
            self.compareDfPath = compareDfObj["fullPath"]
            dataframe['Location'] = dataframe['Location'].str.replace(',', ';').replace('"', '')
            self.compareDfFull = dataframe.head(5).to_csv(index=False, encoding='utf-8')
            # Create Zip archive
            archive_folder = STATIC_FOLDER + user_id + COMPARE_CLASSIFICATION_FOLDER
            zipDirectory(os.path.join(root_folder, archive_folder))
            self.archiveFilePath = archive_folder + ZIP_EXTENSION
            # Close all the 
            plt.close("all")
        except Exception as error:
            print("- compare classification models init error")
            print(f"- {type(error).__name__}: {error}")




        


