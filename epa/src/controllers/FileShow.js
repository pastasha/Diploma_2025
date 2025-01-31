import React, { useState } from "react";
import { CsvToHtmlTable } from 'react-csv-to-table';

export function FileShow({file}) {

    return (
        <CsvToHtmlTable
        data={file}
        csvDelimiter=","
        tableClassName="table table-striped table-hover"
        />
    );
};
