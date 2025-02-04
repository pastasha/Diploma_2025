import React  from 'react';
import { CsvToHtmlTable } from 'react-csv-to-table';
import "../styles/base.css";

export default function Home() {
    let file = 'Location,Year,Month,Day,Hour,PM2.5,PM10,O3,CO,SO2,NO2\nLondon UK,2023,2,7,8:30,43,78,26,258,10,17\nNew York US,2023,2,3,12:00,500,480,91,78,17,47\nOdesa Ukraine,2022,10,16,6:30,185,199,10,52,12,26';
    return (
        <div>
            <div class="info-wrapper">
                <p>This system is designed for analyzing environmental data and assessing air quality using machine learning models. You can upload a CSV file. The file must contain air pollution indicators 
                    (<mark>PM2.5, PM10, O3, CO, SO2, NO2</mark>), <mark>Location</mark> and <mark>Date</mark>.
                </p>
                <p>The system will process the data, perform an in-depth analysis, and generate predictions. The results include visualizations, statistical insights, and air quality classifications, helping you monitor pollution levels and forecast trends.</p>
                <p>Please see the example of data to upload:</p>
                <CsvToHtmlTable
                    data={file}
                    csvDelimiter=","
                    tableClassName="table table-striped table-hover"
                />
            </div>
        </div>
    );
}