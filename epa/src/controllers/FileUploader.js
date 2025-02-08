import React, { useState, useRef } from "react";
import Papa from "papaparse";
import "../styles/fileUploader.css";
import "../styles/base.css";

export function FileUploader() {

    // Create a reference to the hidden file input element
    const hiddenFileInput = useRef(null);

    // Programatically click the hidden file input element
    // when the Button component is clicked
    const handleClick = (event) => {
        hiddenFileInput.current.click();
    };

    // when the Button component is clicked
    const handleClickAnalyse = (event) => {
        document.querySelector(".analysis-button").classList.add("hidden");
        document.getElementById("analyze").classList.remove("hidden");
    };

    const [fileName, setFileName] = useState("");

    // States to store parsed data, table Column name and the values
    const [tableRows, setTableRows] = useState([]);
    const [values, setValues] = useState([]);

    // Call a function (passed as a prop from the parent component)
    // to handle the user-selected file
    const handleChange = async (event) => {
        const fileUploaded = event.target.files[0];
        if (fileUploaded != null && fileUploaded.type === 'text/csv') {

            const data = new FormData();
            data.append('file_from_react', fileUploaded);
        
            let response = await fetch('/upload-data',
                {
                    method: 'post',
                    body: data,
                }
            );
            let res = await response.json();
            if (res.status !== 1){
                alert('Error uploading file');
            } else {
                setFileName(fileUploaded.name);
                Papa.parse(fileUploaded, {
                    header: true,
                    skipEmptyLines: true,
                    complete: function (results) {
                        const rowsArray = [];
                        const valuesArray = [];
                
                        // Iterating data to get column name and their values
                        results.data.map((d) => { // eslint-disable-line
                            rowsArray.push(Object.keys(d));
                            valuesArray.push(Object.values(d));
                        });
                        // Filtered Column Names
                        setTableRows(rowsArray[0]);
                        // Filtered Values
                        setValues(valuesArray);

                        var analysisButton = document.querySelector(".analysis-button");
                        analysisButton.classList.remove("hidden");
                    }
                });
            }
        } else {
            alert('Unexpected file type.');
        }
    };
    return (
        <div>
            {/* Upload button */}
            <button id="uploadDataButton" className="standard-upload" onClick={handleClick}>
                {fileName ? 'Upload another file'
                : 'Upload a file'}
            </button>
            <input
                type="file"
                onChange={handleChange}
                ref={hiddenFileInput}
                style={{ display: "none" }} // Make the file input element invisible
                accept=".csv"
            />

            <div class=" info-wrapper pt-3">
                {fileName ? <p>Check the data you uploaded. If you are ready to start Exploratory Data Analysis, press <mark>Confirm data</mark> button.</p> : null}

                {fileName ? <p class="pt-3">Uploaded file: {fileName}</p> : null}

                <div class="uploaded-file-wrapper">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                {tableRows.map((rows, index) => {
                                    return <th scope="col" key={index}>{rows}</th>;
                                })}
                            </tr>
                        </thead>
                        <tbody>
                            {values.map((value, index) => { // eslint-disable-line
                                if (index < 5) {
                                    return (
                                        <tr key={index}> 
                                            {value.map((val, i) => {
                                                return <td key={i}>{val}</td>;
                                            })}
                                        </tr>
                                    );
                                }
                            })}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Analyse button */}
            <div class="analysis-button hidden">
                <button className="standard-upload" onClick={handleClickAnalyse}>
                    Confirm data
                </button>
            </div>
        </div>
    );
};
