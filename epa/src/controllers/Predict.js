import { DownloadButton } from "./DownloadButton";
import { FileShow } from "./FileShow";
import React, { useState } from 'react';
import '../styles/predict.css';

const serverURL = "http://127.0.0.1:5000/"
export function Predict() {
    function imageComponent(filename) {
        const imageUrl = serverURL + filename;
        return <img src={imageUrl} alt="filename" />;
    };

    let [modelID, setModelID] = useState("");
    let [modelType, setModelType] = useState("");

    // when the Button component is clicked
    const handleModelSelect = (event) => {
        let modelID = event.currentTarget.dataset.modelId;
        let modelSelect = document.getElementsByClassName('model-select');
        for(let index = 0 ; index < modelSelect.length ; ++index) {
            modelSelect[index].style.background='white';
            modelSelect[index].style.borderColor='black';
        }
        event.currentTarget.style.background='#deffde';
        event.currentTarget.style.borderColor='green';
        setModelID(modelID);
        setModelType(null);
        setPredictionResult(null);
    }; 

    // when the Button component is clicked
    const handleModelTypeSelect = (event) => {
        let modelType = event.currentTarget.dataset.modelType;
        let modelSelect = document.getElementsByClassName('model-select-type');
        for(let index = 0 ; index < modelSelect.length ; ++index) {
            modelSelect[index].style.background='white';
            modelSelect[index].style.borderColor='black';
        }
        event.currentTarget.style.background='#deffde';
        event.currentTarget.style.borderColor='green';
        setModelType(modelType);
        setPredictionResult(null);
    };

    const [predictionResult, setPredictionResult] = useState("");

    // when the Button component is clicked
    const handleClick = async (event) => {
        let data = {
            modelType: modelType,
            modelID: modelID
        };
        let response = await fetch('/predict',
            {
                method: 'post',
                body: JSON.stringify(data)
            }
        );
        let res = await response.json();
        if (!res.success){
            alert('Error Prediction processing');
        } else {
            let predictData = res.data;
            let predictResult = {};
            predictResult.type = predictData.type;
            predictResult.extendedDfPath = serverURL + predictData.extendedDfPath;
            predictResult.extendedDfFull = predictData.extendedDfFull;
            predictResult.archiveFilePath = serverURL + predictData.archiveFilePath;
            if (predictResult.type === "classification") {
                predictResult.dataOverview = imageComponent(predictData.dataOverview);
                predictResult.aqiClasses = imageComponent(predictData.aqiClasses);
                predictResult.aqiByLocation = imageComponent(predictData.aqiByLocation);
                predictResult.aqiByMonth = imageComponent(predictData.aqiByMonth);
                predictResult.correlationMatrix = imageComponent(predictData.correlationMatrix);
            } else if (predictResult.type === "regression") {
                predictResult.aqiPercantage = imageComponent(predictData.aqiPercantage);
                predictResult.aqiByTime = imageComponent(predictData.aqiByTime);
                predictResult.aqiByLocation = imageComponent(predictData.aqiByLocation);
                predictResult.correlationMatrix = imageComponent(predictData.correlationMatrix);
            }
            setPredictionResult(predictResult);
            document.getElementById("compare").classList.remove("hidden");
        }
    }; 

    return (
        <div>
            <div class="info-wrapper pt-4">
                <p>This section allows you to choose a specific model and then select  between regression or classification type to make a prediction. Once a model is chosen, the system generates various graphs and visualizations to display the predicted results, such as AQI trends, class distributions, and error analysis.</p>
                <p>These visualizations help users interpret the model’s predictions, compare them with actual data, and gain insights into air quality patterns based on the selected approach.</p>
            </div>
            <div class="container one-row-select-wrapper">
                <div class="row one-row-select"> 
                    <p>Algoritms</p>

                    <button className="col model-select" data-model-id="decisiontree" onClick={handleModelSelect}>
                        Decision Tree
                    </button>

                    <button className="col model-select" data-model-id="randomforest" onClick={handleModelSelect}>
                        Random Forest
                    </button>

                    <button className="col model-select" data-model-id="xgboost" onClick={handleModelSelect}>
                        XG Boost
                    </button>
                </div>
                <div class="row one-row-select"> 
                    <p>Neural networks</p>

                    <button className="col model-select" data-model-id="mlp" onClick={handleModelSelect}>
                        Multilayer perceptron
                    </button>

                    <button className="col model-select" data-model-id="lstm" onClick={handleModelSelect}>
                        Long short-term memory
                    </button>

                    <button className="col model-select" data-model-id="dnn" onClick={handleModelSelect}>
                        Deep Neural Network
                    </button>
                </div>
            </div>

            {modelID ? 
                <>
                <div class="info-wrapper">
                    {modelID === 'decisiontree' ? <p>A Decision Tree is a machine learning model that makes predictions by recursively splitting data into subsets based on feature values, creating a tree-like structure of decisions to classify or predict outcomes.</p> : ''}
                    {modelID === 'randomforest' ? <p>A Random Forest is an ensemble machine learning model that combines multiple decision trees to improve accuracy and reduce overfitting by averaging predictions or using majority voting across the trees.</p> : ''}
                    {modelID === 'xgboost' ? <p>XGBoost (Extreme Gradient Boosting) is a powerful machine learning algorithm that uses gradient boosting techniques to build an ensemble of decision trees, optimizing performance and efficiency for both classification and regression tasks.</p> : ''}
                    {modelID === 'mlp' ? <p>A Multilayer Perceptron (MLP) is a type of artificial neural network consisting of multiple layers of neurons, where each layer applies weighted connections and activation functions to learn complex patterns for classification or regression tasks.</p> : ''}
                    {modelID === 'lstm' ? <p>Long Short-Term Memory (LSTM) is a type of recurrent neural network (RNN) designed to process and learn from sequential data by maintaining long-term dependencies through specialized memory cells and gating mechanisms.</p> : ''}
                    {modelID === 'dnn' ? <p>A Deep Neural Network (DNN) is an artificial neural network with multiple hidden layers that learn complex patterns and representations from data, making it effective for tasks like classification, regression, and feature extraction.</p> : ''}
                
                    <div class="container one-row-select-wrapper">
                        <p><center><mark>Model type</mark></center></p>

                        <button className="row-sm model-select model-select-type" data-model-type="classification" onClick={handleModelTypeSelect}>
                            Classification
                        </button>

                        <button className="row-sm model-select model-select-type" data-model-type="regression" onClick={handleModelTypeSelect}>
                            Regression
                        </button>
                    </div>
                </div>
            
                {modelType ?
                <>
                    <div class="info-wrapper">
                        {modelType === 'classification' ? 
                            <p>A classification models are used to predict categorical outcomes, where the goal is to assign input data to one of several predefined classes or labels. </p>
                        : <p>A regression models are used to predict continuous numerical values, aiming to estimate relationships between input variables and a continuous target variable.</p>}
                    </div>
                    {!predictionResult ?
                        <button class="start-prediction standard-upload" onClick={handleClick}>
                            Start Prediction
                        </button>
                    : ''}

                    {predictionResult ? 
                    <>
                        <FileShow file = {predictionResult.extendedDfFull} markLastCol = {true} dataframePath = {predictionResult.extendedDfPath}/>

                        {predictionResult.type === "classification" ? 
                            <div class="classification-wrapper pt-5">
                                <div class="info-wrapper">
                                    <div class="row">
                                        <div class="col"> 
                                            <div class="data-overview-plot"> 
                                                <p><mark>AQI Class Distribution</mark></p>
                                                <p>An AQI Class Distribution plot visualizes the frequency or proportion of different Air Quality Index (AQI) categories (e.g., Good, Moderate, Unhealthy) in a dataset, helping to understand air quality patterns.</p>
                                                {predictionResult.dataOverview ? predictionResult.dataOverview : ''}
                                            </div>
                                            <div class="aqi-classes pt-5"> 
                                                <p><mark>Grouping data by AQI class</mark></p>
                                                <p>Grouping data by AQI class means categorizing air quality data into predefined AQI ranges (e.g., Good, Moderate, Unhealthy) to analyze trends, compare distributions, and extract meaningful insights.</p>
                                                {predictionResult.aqiClasses ? predictionResult.aqiClasses : ''}
                                            </div>
                                        </div>
                                        <div class="col"> 
                                            <div class="aqi-by-month"> 
                                                <p><mark>Distribution of AQI classes by time</mark></p>
                                                <p>The Distribution of AQI Classes by Month plot shows how air quality index (AQI) categories (e.g., Good, Moderate, Unhealthy) vary across different months, helping to identify seasonal trends and pollution patterns.</p>
                                                {predictionResult.aqiByMonth ? predictionResult.aqiByMonth : ''}
                                            </div>
                                            <div class="corr-matrix pt-5"> 
                                                <p><mark>Correlation between variables</mark></p>
                                                <p>A Correlation Between Variables plot visually represents the strength and direction of relationships between multiple variables, often using a heatmap or scatter plots to identify patterns and dependencies in the data.</p>
                                                {predictionResult.correlationMatrix ? predictionResult.correlationMatrix : ''}
                                            </div>
                                        </div>
                                        <div class="aqi-by-location"> 
                                            <p><mark>Distribution of AQI classes by location</mark></p>
                                            <p>The Distribution of AQI Classes by Location plot visualizes how air quality index (AQI) categories (e.g., Good, Moderate, Unhealthy) are distributed across different geographic locations, helping to compare air quality variations spatially.</p>
                                            {predictionResult.aqiByLocation ? predictionResult.aqiByLocation : ''}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        : ''}

                        {predictionResult.type === "regression" ? 
                            <div class="regression-wrapper pt-5">
                                <div class="info-wrapper">
                                    <div class="row">
                                        <div class="col"> 
                                            <div class="aqi-percentage"> 
                                                <p><mark>Grouping data by AQI</mark></p>
                                                <p>Grouping data by AQI involves categorizing data points into specific AQI ranges (e.g., Good, Moderate, Unhealthy) to analyze air quality trends, patterns, and variations across different segments of the data.</p>
                                                {predictionResult.aqiPercantage ? predictionResult.aqiPercantage : ''}
                                            </div>
                                        </div>
                                        <div class="col"> 
                                            <div class="corr-matrix"> 
                                                <p><mark>Correlation between variables</mark></p>
                                                <p>Correlation between variables refers to the statistical relationship between two or more variables, indicating how changes in one variable are associated with changes in another, either positively, negatively, or with no correlation.</p>
                                                {predictionResult.correlationMatrix ? predictionResult.correlationMatrix : ''}
                                            </div>
                                        </div>
                                        <div class="aqi-by-location"> 
                                            <p><mark>Average AQI for each location</mark></p>
                                            <p>The Average AQI for each location plot displays the mean Air Quality Index (AQI) for different geographic areas, helping to assess overall air quality levels at specific locations over time.</p>
                                            {predictionResult.aqiByLocation ? predictionResult.aqiByLocation : ''}
                                        </div>
                                        <div class="aqi-by-time"> 
                                            <p><mark>Time Analysis</mark></p>
                                            <p>A Line graph of AQI changes over time visualizes the fluctuations in the Air Quality Index (AQI) across a specific time period, helping to track trends and identify periods of improved or worsened air quality.</p>
                                            {predictionResult.aqiByTime ? predictionResult.aqiByTime : ''}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        : ''}

                        <DownloadButton filePath = {predictionResult.archiveFilePath} buttonText = {"Download ZIP report"}/>
                    </>
                    : ''}
                </>
                : ''}
            </>
            : ''}
        </div>
    );
}