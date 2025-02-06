import React, { useState } from "react";
import '../styles/eda.css';


const serverURL = "http://127.0.0.1:5000/"
export function EDA() {
    function imageComponent(filename) {
        const imageUrl = serverURL + filename;
        return <img src={imageUrl} alt="filename" />;
    };

    const [resultEDA, setResultEDA] = useState("");
    // when the Button component is clicked
    const handleClick = async (event) => {
        let data = []
        let response = await fetch('/start-eda',
            {
                method: 'post',
                body: data,
            }
        );
        let res = await response.json();
        if (!res.success){
            alert('Error EDA processing');
        } else {
            let edaData = res.data
            let edaResult = {
                "correlationMatrixPlot": imageComponent(edaData.correlationMatrixPlot),
                "zScorePlot": imageComponent(edaData.zScorePlot),
                "pairplotPlot": imageComponent(edaData.pairplotPlot)
                //"classDistribution": imageComponent(edaData.classDistribution)
            }
            let dataDistributionPlots = {}
            for (const ddPlot in edaData.dataDistributionPlots) {
                dataDistributionPlots[ddPlot] = imageComponent(edaData.dataDistributionPlots[ddPlot])
            }
            edaResult.dataDistributionPlots = dataDistributionPlots;
            let emissionIndexPlots = {}
            for (const eiPlot in edaData.emissionIndexPlots) {
                emissionIndexPlots[eiPlot] = imageComponent(edaData.emissionIndexPlots[eiPlot])
            }
            edaResult.emissionIndexPlots = emissionIndexPlots;
            setResultEDA(edaResult);

            document.querySelector(".start-eda-button").value = 'Restart EDA';
            document.getElementById("predict").classList.remove("hidden");
        }
    }; 

    return (
        <div>
            <p>Exploratory Data Analysis, simply referred to as EDA, is the step where you understand the data in detail.</p>
            {!resultEDA ? 
                <button className="standard-upload start-eda-button" onClick={handleClick}>
                    Start EDA
                </button>
            : ''}
            {resultEDA ?
                <div class="eda">
                    {resultEDA.dataDistributionPlots ?
                        <>
                        <div class="row pt-4">
                            <p>Data Distribution</p>
                            <div class="col">
                                {resultEDA.dataDistributionPlots["PM2.5"]}
                            </div>
                            <div class="col">
                                {resultEDA.dataDistributionPlots["PM10"]}
                            </div>
                            <div class="col">
                                {resultEDA.dataDistributionPlots["O3"]}
                            </div>
                        </div>
                        <div class="row pt-4">
                            <div class="col">
                                {resultEDA.dataDistributionPlots["CO"]}
                            </div>
                            <div class="col">
                                {resultEDA.dataDistributionPlots["SO2"]}
                            </div>
                            <div class="col">
                                {resultEDA.dataDistributionPlots["NO2"]}
                            </div>
                        </div>
                        </>
                    : ''}
                    {resultEDA.emissionIndexPlots ?
                        <div class="row pt-4">
                            <p>Emission Index</p>
                            <div class="col">
                                {resultEDA.emissionIndexPlots["PM2.5"]}
                                {resultEDA.emissionIndexPlots["PM10"]}
                                {resultEDA.emissionIndexPlots["O3"]}
                            </div>
                            <div class="col">
                                {resultEDA.emissionIndexPlots["CO"]}
                                {resultEDA.emissionIndexPlots["SO2"]}
                                {resultEDA.emissionIndexPlots["NO2"]}
                            </div>
                        </div>
                    : ''}
                    <div class="row pt-4">
                        {resultEDA.correlationMatrixPlot ?
                            <div class="col correlation-matrix-plot">
                                <p>Correlation Matrix</p>
                                {resultEDA.correlationMatrixPlot}
                            </div>
                        : ''}
                        {resultEDA.zScorePlot ?
                            <div class="col z-score-plot">
                                <p>Z-Score</p>
                                {resultEDA.zScorePlot}
                            </div>
                        : ''}
                    </div>
                    {resultEDA.pairplotPlot ?
                        <div class="pairplot pt-4">
                            <p>Pairplot</p>
                            {resultEDA.pairplotPlot}
                        </div>
                    : ''}
                </div>
            : ''}
        </div>
    );
};