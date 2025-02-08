import { FileShow } from "./FileShow";
import React, { useState } from 'react';
import '../styles/predict.css';
import { DownloadButton } from "./DownloadButton";

const serverURL = "http://127.0.0.1:5000/"
export function Compare() {
    function imageComponent(filename) {
        const imageUrl = serverURL + filename;
        return <img src={imageUrl} alt="filename" />;
    };

    let [modelType, setModelType] = useState("");
    const [compareResult, setCompareResult] = useState("");

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
        setCompareResult('');
    }; 

    // when the Button component is clicked
    const handleClick = async (event) => {
        let data = {
            modelType: modelType
        };
        let response = await fetch('/compare',
            {
                method: 'post',
                body: JSON.stringify(data)
            }
        );
        let res = await response.json();
        if (!res.success){
            alert('Error Compare processing');
        } else {
            let compareData = res.data;
            let compareResult = {};
            compareResult.type = compareData.type;
            compareResult.compareDfPath = serverURL + compareData.compareDfPath
            compareResult.compareDfFull = compareData.compareDfFull
            compareResult.archiveFilePath = serverURL + compareData.archiveFilePath;
            if (compareData.type === "classification") {
                compareResult.forecastComparePlot = imageComponent(compareData.forecastComparePlot);
                compareResult.heatmapPlot = imageComponent(compareData.heatmapPlot);
                compareResult.aqiDistributionPlot = imageComponent(compareData.aqiDistributionPlot);
                compareResult.popularityPlot = imageComponent(compareData.popularityPlot);
            } else if (compareData.type === "regression") {
                compareResult.boxplotPlot = imageComponent(compareData.boxplotPlot);
                compareResult.modelPredValuesPlot = imageComponent(compareData.modelPredValuesPlot);
                compareResult.corrMatrixPlot = imageComponent(compareData.corrMatrixPlot);
                compareResult.aqiForecastPlot = imageComponent(compareData.aqiForecastPlot);
            }
            setCompareResult(compareResult);
        }
    }; 

    return (
        <div>
            <div class="info-wrapper pt-4">
                <p>Here you can select between classification or regression models to analyze and compare their performance. Once a model type is chosen, the system generates relevant graphs and visualizations, such as histograms, line graphs, and correlation matrices, to display and evaluate the predictions and their accuracy.</p>
                <p>This helps you to understand how different models behave with the dataset, highlighting key trends, errors, and relationships in the data to aid in model selection and refinement.</p>
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
                {!compareResult ?
                    <button class="start-prediction standard-upload" onClick={handleClick}>
                        Start Compare
                    </button>
                : ''}
                {compareResult ?
                    <>
                    {compareResult.compareDfFull ? 
                        <>
                        <FileShow file = {compareResult.compareDfFull} markLastCol = {false} dataframePath = {compareResult.compareDfPath}/>
                        </>
                    : ''}

                    {compareResult.type === "classification" ? 
                        <div class="classification-wrapper pt-5">
                            <div class="info-wrapper">
                                <div class="row">
                                    <div class="col"> 
                                        <div class=""> 
                                            <p><mark>Comparison of model predictions for each location</mark></p>
                                            <p>Comparison of model predictions for each location involves evaluating and visualizing the predicted values (e.g., AQI levels) from a model against actual data for different geographic areas, helping to assess model accuracy and performance.</p>
                                            {compareResult.forecastComparePlot ? compareResult.forecastComparePlot : ''}
                                        </div>
                                        <div class="pt-5"> 
                                            <p><mark>Frequency of AQI class predictions</mark></p>
                                            <p>Frequency of AQI class predictions shows how often each Air Quality Index (AQI) category (e.g., Good, Moderate, Unhealthy) is predicted by a model, helping to analyze the distribution of predicted air quality levels in a dataset.</p>
                                            {compareResult.heatmapPlot ? compareResult.heatmapPlot : ''}
                                        </div>
                                    </div>
                                    <div class="col"> 
                                        <div class=""> 
                                            <p><mark>Distribution of model predictions by location</mark></p>
                                            <p>The Distribution of model predictions by location visualizes how predicted air quality levels (e.g., AQI) vary across different geographic areas, helping to identify spatial patterns and trends in the model's output.</p>
                                            {compareResult.aqiDistributionPlot ? compareResult.aqiDistributionPlot : ''}
                                        </div>
                                        <div class="pt-5"> 
                                            <p><mark>Analysis of the popularity of model predictions</mark></p>
                                            <p>The Analysis of the popularity of model predictions plot visualizes how frequently certain predictions or outcomes (e.g., specific AQI categories) occur, helping to identify which model predictions are most common or dominant in a dataset.</p>
                                            {compareResult.popularityPlot ? compareResult.popularityPlot : ''}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    : ''}

                    {compareResult.type === "regression" ? 
                        <div class="regression-wrapper pt-5">
                            <div class="info-wrapper">
                                <div class="row">
                                    <div class="col"> 
                                        <div class=""> 
                                            <p><mark>Distribution of model predictions</mark></p>
                                            <p>The distribution of model predictions shows how predicted values (e.g., AQI levels) are spread across a range, helping to understand the frequency and patterns of different prediction outcomes from the model.</p>
                                            {compareResult.boxplotPlot ? compareResult.boxplotPlot : ''}
                                        </div>
                                        <div class="pt-5"> 
                                            <p><mark>Line graph of forecast changes over time</mark></p>
                                            <p>A Line graph of forecast changes over time plot visualizes the predicted variations in a specific variable (e.g., AQI) over a time period, helping to track future trends and fluctuations based on the model's forecasts.</p>
                                            {compareResult.aqiForecastPlot ? compareResult.aqiForecastPlot : ''}
                                        </div>
                                    </div>
                                    <div class="col"> 
                                        <div class=""> 
                                            <p><mark>Correlation matrix of models</mark></p>
                                            <p>A correlation matrix of models shows the relationships between the predictions of different models, indicating how similarly or differently they perform and how their outputs are correlated with each other.</p>
                                            {compareResult.corrMatrixPlot ? compareResult.corrMatrixPlot : ''}
                                        </div>
                                        <div class="pt-5"> 
                                            <p><mark>Histograms of the distribution of model predictions</mark></p>
                                            <p>Histograms of the distribution of model predictions display the frequency of different predicted values (e.g., AQI levels), helping to visualize how the model's predictions are distributed across a range of outcomes.</p>
                                            {compareResult.modelPredValuesPlot ? compareResult.modelPredValuesPlot : ''}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    : ''}

                    <DownloadButton filePath = {compareResult.archiveFilePath} buttonText = {"Download ZIP report"}/>
                    </>
                : ''}
                </>
            : ''}
        </div>
    );
}