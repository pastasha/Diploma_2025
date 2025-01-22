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
            <button className="standard-upload start-eda-button" onClick={handleClick}>
                Start EDA
            </button>

            {resultEDA &&  resultEDA.dataDistributionPlots ? <p>Data Distribution</p> : ''}
            <div class="one-row-plots data-distribution-plots">
                {resultEDA &&  resultEDA.dataDistributionPlots ? Object.keys(resultEDA.dataDistributionPlots).map((plotName, index) => {
                    return (
                        <div class="one-row-plot dd-plot" data-plot-name={plotName}> 
                            {resultEDA.dataDistributionPlots[plotName]}
                        </div>
                    );
                }) : ""}
            </div>

            {resultEDA &&  resultEDA.emissionIndexPlots ? <p>Emission Index</p> : ''}
            <div class="emission-index-plots">
                {resultEDA &&  resultEDA.emissionIndexPlots ? Object.keys(resultEDA.emissionIndexPlots).map((plotName, index) => {
                    return (
                        <div class='ei-plot' data-plot-name={plotName}> 
                            {resultEDA.emissionIndexPlots[plotName]}
                        </div>
                    );
                }) : ''}
            </div>

            <div class="one-row-plots">
                <div class="one-row-plot correlation-matrix-plot">
                    {resultEDA && resultEDA.correlationMatrixPlot ? <p>Correlation Matrix</p> : ''}
                    {resultEDA && resultEDA.correlationMatrixPlot ? resultEDA.correlationMatrixPlot : ''}
                </div>

                <div class="one-row-plot z-score-plot">
                    {resultEDA && resultEDA.zScorePlot ? <p>Z-Score</p> : ''}
                    {resultEDA && resultEDA.zScorePlot ? resultEDA.zScorePlot : ''}
                </div>
            </div>

            <div class="pairplot-plot">
                {resultEDA && resultEDA.pairplotPlot ? <p>Pairplot</p> : ''}
                {resultEDA && resultEDA.pairplotPlot ? resultEDA.pairplotPlot : ''}
            </div>
        </div>
    );
};