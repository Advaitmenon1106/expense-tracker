import { useEffect, useState } from "react";
import "./StatementUpload.css";

// Move static data outside to prevent re-creation on every render
const SVG_MAPPER = {
    '.csv': (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M230-360h120v-60H250v-120h100v-60H230q-17 0-28.5 11.5T190-560v160q0 17 11.5 28.5T230-360Zm156 0h120q17 0 28.5-11.5T546-400v-60q0-17-11.5-31.5T506-506h-60v-34h100v-60H426q-17 0-28.5 11.5T386-560v60q0 17 11.5 30.5T426-456h60v36H386v60Zm264 0h60l70-240h-60l-40 138-40-138h-60l70 240ZM160-160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h640q33 0 56.5 23.5T880-720v480q0 33-23.5 56.5T800-160H160Zm0-80h640v-480H160v480Zm0 0v-480 480Z" /></svg>),
    ".pdf": (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M320-440h320v-80H320v80Zm0 120h320v-80H320v80Zm0 120h200v-80H320v80ZM240-80q-33 0-56.5-23.5T160-160v-640q0-33 23.5-56.5T240-880h320l240 240v480q0 33-23.5 56.5T720-80H240Zm280-520v-200H240v640h480v-440H520ZM240-800v200-200 640-640Z" /></svg>),
    ".jpg": (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm40-80h480L570-480 450-320l-90-120-120 160Zm-40 80v-560 560Z" /></svg>),
    ".png": (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm40-80h480L570-480 450-320l-90-120-120 160Zm-40 80v-560 560Z" /></svg>),
    ".xlsx": (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm240-240H200v160h240v-160Zm80 0v160h240v-160H520Zm-80-80v-160H200v160h240Zm80 0h240v-160H520v160ZM200-680h560v-80H200v80Z" /></svg>)
};

const getExtension = (filename) => "." + filename.split(".").pop().toLowerCase();

export function StatementUpload() {
    const [uploadedFiles, setUploadedFiles] = useState([]);

    useEffect(() => {
        const preventDefaultDrop = (e) => e.preventDefault();
        window.addEventListener("dragover", preventDefaultDrop);
        window.addEventListener("drop", preventDefaultDrop);
        return () => {
            window.removeEventListener("dragover", preventDefaultDrop);
            window.removeEventListener("drop", preventDefaultDrop);
        };
    }, []);

    const handleFiles = (files) => {
        const allowedTypes = [
            "image/png",
            "image/jpeg",
            "application/pdf",
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ];

        const validFiles = Array.from(files).filter(file => allowedTypes.includes(file.type));

        if (validFiles.length !== files.length) {
            alert("Some files were skipped due to unsupported types.");
        }

        setUploadedFiles((prev) => [...prev, ...validFiles]);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        if (e.dataTransfer.files.length) {
            handleFiles(e.dataTransfer.files);
        }
    };

    const handleInputChange = (e) => {
        if (e.target.files.length) {
            handleFiles(e.target.files);
        }
    };

    const removeFile = (indexToRemove) => {
        setUploadedFiles((prev) => prev.filter((_, index) => index !== indexToRemove));
    };

    return (
        <div className="upload-wrapper">
            <div className="hero-text">
                Upload your bank statement for automated reading and document understanding:
            </div>

            <label
                htmlFor='statement-file-upload'
                id='custom-file-upload'
                onDrop={handleDrop}
                onDragOver={(e) => e.preventDefault()}
            >
                <svg id='doc-upload-svg' xmlns="http://www.w3.org/2000/svg" height="48px" viewBox="0 -960 960 960" width="48px" fill="#e3e3e3">
                    <path d="M440-200h80v-167l64 64 56-57-160-160-160 160 57 56 63-63v167ZM240-80q-33 0-56.5-23.5T160-160v-640q0-33 23.5-56.5T240-880h320l240 240v480q0 33-23.5 56.5T720-80H240Zm280-520v-200H240v640h480v-440H520ZM240-800v200-200 640-640Z" />
                </svg>
                <input type='file' id='statement-file-upload' onChange={handleInputChange} multiple style={{ display: 'none' }} />
                <span id="statement-upload-instructions">Click to upload bank statements (.PDF, .PNG, .JPG, .CSV, .XLSX)</span>
                <span id="statement-upload-instructions-2">Or drag and drop</span>
            </label>

            {/* NEATER LIST CONTAINER */}
            {uploadedFiles.length > 0 && (
                <div className="uploaded-files-container">
                    {uploadedFiles.map((f, index) => {
                        const ext = getExtension(f.name);
                        const icon = SVG_MAPPER[ext];

                        return (
                            <div className="file-row" key={`${f.name}-${index}`}>
                                <div className="file-info">
                                    {icon}
                                    <span className="file-name">{f.name}</span>
                                </div>
                                <button
                                    className="remove-file-btn"
                                    onClick={() => removeFile(index)}
                                    title="Remove file"
                                >
                                    &times;
                                </button>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}