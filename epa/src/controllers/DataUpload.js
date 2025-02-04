import React  from 'react';
import { FileUploader } from "./FileUploader";
import "../styles/base.css";

export default function DataUpload() {
    return (
        <div class="pt-4">
            <p>Upload your CSV file with environmental data.</p>
            <FileUploader />
        </div>
    );
}