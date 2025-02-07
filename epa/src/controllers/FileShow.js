import React from "react";
import { CsvToHtmlTable } from 'react-csv-to-table';
import "../styles/fileUploader.css";
import { DownloadButton } from "./DownloadButton";

export function FileShow({file, markLastCol, dataframePath}) {
    return (
        <div>
            <div class="uploaded-file-wrapper pt-3">
                <CsvToHtmlTable
                data={file}
                csvDelimiter=","
                tableClassName="table table-striped table-hover"
                tableColumnClassName={markLastCol ? "col df-col" : "col"}
                />
            </div>
            <DownloadButton filePath = {dataframePath} buttonText = {"Download CSV report"}/>
    </div>
    );
};
