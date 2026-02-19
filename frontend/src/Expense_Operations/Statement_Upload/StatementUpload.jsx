import './StatementUpload.css'

export function StatementUpload() {
    return (
        <div>
            <div className="hero-text">Upload your bank statement for automated reading and document understanding: -</div>
            <label htmlFor='statement-file-upload' className='custom-file-upload'>
                <input type='file' id='statement-file-upload' />
            </label>
        </div>
    )
}