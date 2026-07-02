from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
import requests
import concurrent.futures
import pandas as pd
import time
import os
import io
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production!

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def normalize_url(url):
    url = url.strip()
    if not url:
        return url
    parsed = urlparse(url)
    if not parsed.scheme:
        return 'https://' + url
    return url

def check_url(url):
    original_url = url
    url = normalize_url(url)
    start = time.time()
    try:
        try:
            resp = requests.head(url, timeout=10, allow_redirects=True, headers=HEADERS)
            if resp.status_code in (405, 501):
                resp = requests.get(url, timeout=10, allow_redirects=True, stream=True, headers=HEADERS)
                resp.close()
            else:
                resp.close()
        except requests.exceptions.RequestException:
            resp = requests.get(url, timeout=10, allow_redirects=True, stream=True, headers=HEADERS)
            resp.close()
        status = resp.status_code
        reason = resp.reason
        elapsed = time.time() - start
        active = "Active"
        reason_str = f"{status} {reason}"
    except requests.exceptions.RequestException as e:
        elapsed = time.time() - start
        active = "Non-Active"
        reason_str = str(e)
        status = None
    return {
        "URL": original_url,
        "Status": active,
        "Reason": reason_str,
        "Response Time (s)": round(elapsed, 2),
        "Status Code": status
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls_text = request.form.get('urls', '')
        if not urls_text.strip():
            flash('Please enter at least one URL', 'error')
            return redirect(url_for('index'))

        # Parse URLs (one per line)
        lines = [line.strip() for line in urls_text.split('\n') if line.strip()]

        # Remove header if present
        if lines and lines[0].lower().startswith('url'):
            lines = lines[1:]

        if not lines:
            flash('No valid URLs found after processing', 'error')
            return redirect(url_for('index'))

        # Check URLs
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {executor.submit(check_url, url): url for url in lines}
            for i, future in enumerate(concurrent.futures.as_completed(future_to_url), 1):
                result = future.result()
                results.append(result)
                # Flash progress every 10 URLs or at the end
                if i % 10 == 0 or i == len(lines):
                    flash(f'Processed {i}/{len(lines)} URLs', 'info')

        # Store results in session for download
        session['results'] = results
        flash(f'Completed checking {len(lines)} URLs', 'success')
        return render_template('results.html', results=results)

    return render_template('index.html')

@app.route('/download')
def download():
    if 'results' not in session or not session['results']:
        flash('No results to download', 'error')
        return redirect(url_for('index'))

    results = session['results']
    df = pd.DataFrame(results)
    # Reorder columns for display
    df = df[["URL", "Status", "Reason", "Response Time (s)", "Status Code"]]

    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='URL Status Results')
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='url_check_results.xlsx'
    )

if __name__ == '__main__':
    # Check if required packages are installed
    try:
        import requests
        import pandas
    except ImportError as e:
        print(f"Missing required package: {e.name}. Attempting to install...")
        import subprocess
        import sys
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "pandas", "openpyxl", "flask"])
            import requests
            import pandas
        except subprocess.CalledProcessError:
            print("Failed to install required packages. Please install manually:")
            print("pip install requests pandas openpyxl flask")
            sys.exit(1)

    app.run(debug=True, host='0.0.0.0', port=5000)