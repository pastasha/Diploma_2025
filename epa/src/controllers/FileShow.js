import React from "react";
import { CsvToHtmlTable } from 'react-csv-to-table';
import "../styles/fileUploader.css";

export function FileShow({file}) {

    return (
        <div class="uploaded-file-wrapper">
            <CsvToHtmlTable
            data={file}
            csvDelimiter=","
            tableClassName="table table-striped table-hover"
            tableColumnClassName="col df-col"
            />
        </div>
    );
};
