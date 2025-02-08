import React from 'react';
import { ReactComponent as DownloadIcon} from '../icons/download.svg';  // eslint-disable-next-line

export function DownloadButton(args) {

    // when the Button component is clicked
    const download = (event) => {
        const url = args.filePath;
        const link = document.createElement("a");
        link.href = url;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }; 

    return (
        <div>
            <div class="one-row-select-wrapper">
                <button className="standard-upload" onClick={download}>
                    <DownloadIcon/>
                    {args.buttonText}
                </button>
            </div>
        </div>
    );
}