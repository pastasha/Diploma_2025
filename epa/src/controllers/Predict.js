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
            <p>Select the model</p>

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
            <div class="model-description">
            </div>

            {modelID ? 
                <>
                <div class="container one-row-select-wrapper">
                    <p>Model type</p>

                    <button className="row-sm model-select model-select-type" data-model-type="classification" onClick={handleModelTypeSelect}>
                        Classification
                    </button>

                    <button className="row-sm model-select model-select-type" data-model-type="regression" onClick={handleModelTypeSelect}>
                        Regression
                    </button>
                </div>
            
                {modelType ?
                <>
                    {!predictionResult ?
                        <button class="start-prediction standard-upload" onClick={handleClick}>
                            Start Prediction
                        </button>
                    : ''}

                    {predictionResult ? 
                    <>
                        <FileShow file = {predictionResult.extendedDfFull} markLastCol = {true} dataframePath = {predictionResult.extendedDfPath}/>

                        {predictionResult.type === "classification" ? 
                            <div class="classification-wrapper">
                                <div class="row">
                                    <div class="col"> 
                                        <div class="data-overview-plot"> 
                                            {predictionResult.dataOverview ? predictionResult.dataOverview : ''}
                                        </div>
                                        <div class="aqi-classes"> 
                                            {predictionResult.aqiClasses ? predictionResult.aqiClasses : ''}
                                        </div>
                                    </div>
                                    <div class="col"> 
                                        <div class="aqi-by-month"> 
                                            {predictionResult.aqiByMonth ? predictionResult.aqiByMonth : ''}
                                        </div>
                                        <div class="corr-matrix"> 
                                            {predictionResult.correlationMatrix ? predictionResult.correlationMatrix : ''}
                                        </div>
                                    </div>
                                    <div class="aqi-by-location"> 
                                        {predictionResult.aqiByLocation ? predictionResult.aqiByLocation : ''}
                                    </div>
                                </div>
                            </div>
                        : ''}

                        {predictionResult.type === "regression" ? 
                            <div class="regression-wrapper">
                                <div class="row">
                                    <div class="col"> 
                                        <div class="aqi-percentage"> 
                                            {predictionResult.aqiPercantage ? predictionResult.aqiPercantage : ''}
                                        </div>
                                    </div>
                                    <div class="col"> 
                                        <div class="corr-matrix"> 
                                            {predictionResult.correlationMatrix ? predictionResult.correlationMatrix : ''}
                                        </div>
                                    </div>
                                    <div class="aqi-by-location"> 
                                        {predictionResult.aqiByLocation ? predictionResult.aqiByLocation : ''}
                                    </div>
                                    <div class="aqi-by-time"> 
                                        {predictionResult.aqiByTime ? predictionResult.aqiByTime : ''}
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