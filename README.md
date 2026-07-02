# URL Status Checker

A simple web application to check the status of URLs (active/non-active) and download results as Excel.

## Features

- Paste URLs (one per line) in a textarea
- Check each URL for active/non-active status
- Display results in a table with:
  - URL
  - Status (Active/Non-active)
  - Status Info (status code or error message)
  - Response Time (seconds)
  - Status Code
- Download results as an Excel file
- Simple and cute interface using Bootstrap

## Requirements

- Python 3.x
- Required Python packages:
  - Flask
  - requests
  - pandas
  - openpyxl

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mitramaleki/apistatus.git
   cd apistatus
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://localhost:5000`

3. Enter URLs (one per line) in the textarea and click "Check URLs"

4. View the results in the table and click "Download Excel" to save the results

## How It Works

The application uses the same URL checking logic as the original `check_urls_fixed.py` script:
- Sends a HEAD request first
- If HEAD returns 405 or 501, falls back to GET
- If any request exception occurs, falls back to GET
- Considers status codes 200-299 as "Active", everything else as "Non-active"
- Uses concurrent threading (20 workers) for faster checking

## Files

- `app.py`: Main Flask application
- `templates/index.html`: Input form
- `templates/results.html`: Results display and download
- `requirements.txt`: Python dependencies

## Notes

- The application uses a default User-Agent string to mimic a browser
- Timeout for each request is set to 10 seconds
- Results are stored in the user's session for download (temporary, for the session)
- For production use, change the secret key in `app.py` and consider using a proper session store

## License

MIT