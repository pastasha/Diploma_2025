import React, { useState, useEffect } from 'react';
import '../styles/predict.css';

export function Predict() {

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
            let predictResult = {
                "predictionResult": predictData.predictionResult,
                "predictedCategories": predictData.predictedCategories
            }
            setPredictionResult(predictResult);
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

            {modelID ? 
                <div class="container one-row-select-wrapper">
                    <p>Model type</p>

                    <button className="row-sm model-select model-select-type" data-model-type="classification" onClick={handleModelTypeSelect}>
                        Classification
                    </button>

                    <button className="row-sm model-select model-select-type" data-model-type="regression" onClick={handleModelTypeSelect}>
                        Regression
                    </button>
                </div>
            : ''}

            {modelID && modelType ?
                <button class="standard-upload" onClick={handleClick}>
                    Start Prediction
                </button>
            : ''}

            <br/>
            {predictionResult && predictionResult.predictionResult ? predictionResult.predictionResult : ''}
            <br/>
            {predictionResult && predictionResult.predictedCategories ? predictionResult.predictedCategories : ''}
        </div>
    );
}