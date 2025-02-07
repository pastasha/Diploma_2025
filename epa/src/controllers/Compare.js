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
                        <div class="classification-wrapper">
                            <div class="row">
                                <div class="col"> 
                                    <div class=""> 
                                        {compareResult.forecastComparePlot ? compareResult.forecastComparePlot : ''}
                                    </div>
                                    <div class=""> 
                                        {compareResult.heatmapPlot ? compareResult.heatmapPlot : ''}
                                    </div>
                                </div>
                                <div class="col"> 
                                    <div class=""> 
                                        {compareResult.aqiDistributionPlot ? compareResult.aqiDistributionPlot : ''}
                                    </div>
                                    <div class=""> 
                                        {compareResult.popularityPlot ? compareResult.popularityPlot : ''}
                                    </div>
                                </div>
                            </div>
                        </div>
                    : ''}

                    {compareResult.type === "regression" ? 
                        <div class="regression-wrapper">
                            <div class="row">
                                <div class="col"> 
                                    <div class=""> 
                                        {compareResult.boxplotPlot ? compareResult.boxplotPlot : ''}
                                    </div>
                                    <div class=""> 
                                        {compareResult.aqiForecastPlot ? compareResult.aqiForecastPlot : ''}
                                    </div>
                                </div>
                                <div class="col"> 
                                    <div class=""> 
                                        {compareResult.corrMatrixPlot ? compareResult.corrMatrixPlot : ''}
                                    </div>
                                    <div class=""> 
                                        {compareResult.modelPredValuesPlot ? compareResult.modelPredValuesPlot : ''}
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