# LogsMate

A powerful log analysis tool that leverages LLMs and RAG to extract insights from log files.

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

1. Place your log file in the `data/logs` directory
2. Run the analyzer:

```bash
python -m src.main
```

### FastAPI Interface

1. Start the API server:

```bash
python run_api.py
```

2. The API will be available at: http://localhost:8000
3. Documentation is available at: http://localhost:8000/docs

### API Endpoints

- `POST /upload/`: Upload a log file (.log or .txt)
- `GET /logs/`: List all available log files
- `POST /analyze/{filename}`: Run analysis on a specific log file and return the complete analysis results
- `GET /status/{filename}`: Check the status of an analysis job

## Example API Usage

### Upload a Log File

```bash
curl -X POST "http://localhost:8000/upload/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/logfile.txt"
```

### List Available Log Files

```bash
curl -X GET "http://localhost:8000/logs/" -H "accept: application/json"
```

### Run Analysis and Get Results

```bash
curl -X POST "http://localhost:8000/analyze/logfile.txt" -H "accept: application/json"
```

This API waits for the complete analysis to finish and returns:
- The filename
- Success message
- Final summary report

## Testing with Postman

1. **Set up Postman requests**:

   **Upload Log File**
   - Method: POST
   - URL: http://localhost:8000/upload/
   - In "Body" tab:
     - Select "form-data"
     - Add a key called "file" and change type to "File"
     - Click "Select Files" and choose your .log or .txt file

   **Run Analysis**
   - Method: POST
   - URL: http://localhost:8000/analyze/{filename}
   - Replace {filename} with your actual filename (e.g., "Complete_Android_log (1).txt")
   - No body parameters required
   - Note: This request may take a while to complete as it performs the full analysis

2. **Testing workflow**:
   - First upload your file using the upload endpoint
   - Run the analysis using the analyze endpoint
   - The analyze endpoint will wait until the entire analysis is complete and return all results

## Output

The analysis produces:
- A PDF report (final_report.pdf)
- Detailed analysis of each log chunk
- Summary of findings and recommendations 