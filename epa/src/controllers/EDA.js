import React, { useState } from "react";
import '../styles/eda.css';
import { DownloadButton } from "./DownloadButton";


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
            edaResult.archiveFilePath = serverURL + edaData.archiveFilePath;
            setResultEDA(edaResult);

            document.querySelector(".start-eda-button").value = 'Restart EDA';
            document.getElementById("predict").classList.remove("hidden");
        }
    }; 

    return (
        <div>
            <div class="info-wrapper pt-4">
                <p>The EDA section provides you with an in-depth overview of the dataset you just uploaded. Through various visualizations and statistical summaries, you can examine data distributions, identify patterns, detect outliers, and explore correlations between variables.</p>
                <p>This step helps in understanding the structure and quality of the data, which is crucial for making informed decisions before proceeding with modeling and predictions.</p>
            </div>
            {!resultEDA ?
            <button className="standard-upload start-eda-button" onClick={handleClick}>
                Start EDA
            </button>
            : ''}
            {resultEDA ?
                <>
                <div class="eda">
                    {resultEDA.dataDistributionPlots ?
                        <>
                        <div class="row pt-4">
                            <div class="info-wrapper">
                                <p><mark>Data Distribution</mark></p>
                                <p>A Data Distribution plot is a graphical representation that shows how data points are spread across different values, helping to visualize patterns, trends, and the overall shape of the dataset.</p>
                            </div>
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
                            <div class="info-wrapper">
                                <p><mark>Emission Index</mark></p>
                                <p>An Emission Index plot visualizes the relationship between emission levels of pollutants (e.g., CO₂, NOx) and relevant variables like fuel consumption or engine performance, helping to analyze environmental impact.</p>
                            </div>
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
                                <div class="info-wrapper">
                                    <p><mark>Correlation Matrix</mark></p>
                                    <p>A Correlation Matrix is a table that displays correlation coefficients between multiple variables, showing the strength and direction of their relationships to identify patterns and dependencies in a dataset.</p>
                                </div>
                                {resultEDA.correlationMatrixPlot}
                            </div>
                        : ''}
                        {resultEDA.zScorePlot ?
                            <div class="col z-score-plot">
                                <div class="info-wrapper">
                                    <p><mark>Z-Score</mark></p>
                                    <p>A Z-Score plot visualizes how many standard deviations each data point is from the mean, helping to detect outliers and assess the distribution of a dataset relative to a normal distribution.</p>
                                </div>
                                {resultEDA.zScorePlot}
                            </div>
                        : ''}
                    </div>
                    {resultEDA.pairplotPlot ?
                        <div class="pairplot pt-4">
                            <div class="info-wrapper">
                                <p><mark>Pairplot</mark></p>
                                <p>A Pairplot is a grid of scatter plots that visualizes pairwise relationships between multiple numerical variables in a dataset, helping to identify correlations, trends, and distributions.</p>
                            </div>
                            {resultEDA.pairplotPlot}
                        </div>
                    : ''}
                    <DownloadButton filePath = {resultEDA.archiveFilePath} buttonText = {"Download ZIP report"}/>
                </div>
                </> 
            : ''}
        </div>
    );
};