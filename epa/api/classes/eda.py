import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import sys
sys.path.append('../')

from helpers.predictHelper import *
from helpers.imgHelper import *
from helpers.dbHelper import *

matplotlib.use("agg")


PLOTS_FOLDER = "/eda"
DATA_DISTRIBUTION_FOLDER = PLOTS_FOLDER + "/data_distribution"
EMISSION_INDEX_FOLDER = PLOTS_FOLDER + "/emission_index"
CORRELATION_MATRIX_FILE_NAME = "correlation_matrix" + IMG_EXTENSION
Z_SCOPE_FILE_NAME = "z_score" + IMG_EXTENSION
PAIRPLOT_FILE_NAME = "pairplot" + IMG_EXTENSION
CLASS_DISTRIBUTION_FILE_NAME = "class_distribution" + IMG_EXTENSION


class ExploratoryDataAnalysis:
    @staticmethod
    def generateDataDistributionPlot(self, dataframe, value, user_id, root_folder):
        try:
            img_name = value + IMG_EXTENSION
            img_path = generateImgFullPath(user_id, DATA_DISTRIBUTION_FOLDER, img_name, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                sns.displot(dataframe[value])
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, DATA_DISTRIBUTION_FOLDER, img_name, None)
            return img_path
        except Exception as error:
            print("- generateDataDistributionPlot error for:" + value)
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateEmissionIndexPlot(self, dataframe, value, user_id, root_folder):
        try:
            img_name = value + IMG_EXTENSION
            img_path = generateImgFullPath(user_id, EMISSION_INDEX_FOLDER, img_name, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                plt.figure(figsize=(13, 4))
                sns.boxplot(data=dataframe, x="Location", y=value)
                plt.title(value + " Emissions")
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, EMISSION_INDEX_FOLDER, img_name, None)
            return img_path
        except Exception as error:
            print("- generateEmissionIndexPlot error for:" + value)
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateCorrelationMatrixPlot(self, dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, PLOTS_FOLDER, CORRELATION_MATRIX_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                sns.heatmap(dataframe.corr())
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, PLOTS_FOLDER, CORRELATION_MATRIX_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generateCorrelationMatrixPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateZScorePlot(self, dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, PLOTS_FOLDER, Z_SCOPE_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                dataframe['z_score'] = (dataframe['CO'] - dataframe['CO'].mean()) / dataframe['CO'].std()
                # Selection of new (by rule: Z-score > 3)
                outliers = dataframe[np.abs(dataframe['z_score']) > 3]
                # Visualization 
                plt.figure(figsize=(8, 4))
                sns.scatterplot(x=range(len(dataframe)), y=dataframe['CO'], color='blue', label="Data")
                sns.scatterplot(x=outliers.index, y=outliers['CO'], color='red', label="Outliers")
                plt.legend()
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, PLOTS_FOLDER, Z_SCOPE_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generateZScorePlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generatePairplotPlot(self, dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, PLOTS_FOLDER, PAIRPLOT_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                plot = sns.pairplot(dataframe, hue="Location")
                fig = plot.fig
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, PLOTS_FOLDER, PAIRPLOT_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generatePairplotPlot error")
            print(f"-{type(error).__name__}: {error}")

    @staticmethod
    def generateClassDistributionPlot(self, dataframe, user_id, root_folder):
        try:
            img_path = generateImgFullPath(user_id, PLOTS_FOLDER, CLASS_DISTRIBUTION_FILE_NAME, None)
            if (checkIfImgExists(root_folder, img_path) == False):
                # Define a mapping dictionary to map the old labels to the new labels
                category_mapping = {
                    'a_Good': 'Good',
                    'b_Moderate': 'Moderate',
                    'c_Unhealthy_for_Sensitive_Groups': 'USG', 
                    'd_Unhealthy' : 'Unhealthy',
                    'e_Very_Unhealthy' : 'Very Unhealthy',
                    'f_Severe' : 'Severe'
                }
                # Apply the mapping to create a new column with modified category labels
                dataframe['Modified_AQI_Class'] = dataframe['AQI_Class'].map(category_mapping)
                # Now, you can plot the count of modified categories
                plt.figure(figsize=(12,6))
                plt.title('Class Distribution of Processed Dataset')
                custom_order = ['Good', 'Moderate', 'USG', 'Unhealthy', 'Very Unhealthy', 'Severe']
                sns.countplot(data=dataframe,x='Modified_AQI_Class', order=custom_order, palette='Set2', hue='AQI_Class', legend=False)
                # save result
                img_path = saveImageToStaticFolder(user_id, root_folder, PLOTS_FOLDER, CLASS_DISTRIBUTION_FILE_NAME, None)
            return img_path
        except Exception as error:
            print("- generateClassDistributionPlot error")
            print(f"-{type(error).__name__}: {error}")

    def __init__(self, user_id, customer_folder, root_folder):
        rawDf = getCustomerData(customer_folder)
        dataframe = prepareData(rawDf)
        values = ["PM2.5", "PM10", "O3", "CO", "SO2", "NO2"]
        self.dataDistributionPlots = {}
        self.emissionIndexPlots = {}
        for value in values:
            # generate data distribution plot
            self.dataDistributionPlots[value] = self.generateDataDistributionPlot(self, dataframe, value, user_id, root_folder)
        # generate correlation matrix plot
        self.correlationMatrixPlot = self.generateCorrelationMatrixPlot(self, dataframe, user_id, root_folder)
        # generate z-scope plot
        self.zScorePlot = self.generateZScorePlot(self, dataframe, user_id, root_folder)
        for value in values:
            # generate emission index plot
            self.emissionIndexPlots[value] = self.generateEmissionIndexPlot(self, dataframe, value, user_id, root_folder)
        # generate pairplot plot
        self.pairplotPlot = self.generatePairplotPlot(self, dataframe, user_id, root_folder)
        # generate class distribution plot
        #self.classDistribution = self.generateClassDistributionPlot(self, dataframe, user_id, root_folder)
        plt.close("all")


