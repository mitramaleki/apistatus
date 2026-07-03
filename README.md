# URL Status Checker

A simple web tool to check if URLs are active (returning any HTTP response) or non-active. Built to run on GitHub Pages.

## Live Demo

Visit: https://mitramaleki.github.io/apistatus/

## Features

- Enter multiple URLs (one per line)
- Checks each URL for activity (any HTTP response means active)
- Shows status and HTTP status code (or error message)
- Download results as CSV file (can be opened in Excel)
- Simple, clean interface
- Runs entirely in the browser (no backend required)

## How It Works

The tool uses a CORS proxy (https://api.allorigins.win/) to bypass browser cross-origin restrictions when checking URLs. This allows us to check URLs from different domains while still getting meaningful status information.

## Usage

1. Go to https://mitramaleki.github.io/apistatus/
2. Enter or paste URLs into the textarea (one URL per line)
3. Click "Check URLs" button
4. Wait for the check to complete (there's a small delay between requests to be polite)
5. View results in the table below
6. Click "Download Results as CSV" to save the results to your computer

## Notes

- Due to browser security restrictions, we use a CORS proxy to make cross-origin requests
- Some websites may block the proxy or have strict security policies that prevent successful checks
- The tool considers any HTTP response (including 4xx and 5xx) as "Active" because it means the server is responding
- Network errors, timeouts, or invalid URLs are marked as "Non-active"
- For best results, include the protocol (http:// or https://) but the tool will automatically add http:// if missing

## Development

To run locally:
1. Clone this repository
2. Open index.html in your browser
3. No build process or dependencies required

## Deployment to GitHub Pages

1. Push the contents of this repository to the `main` branch
2. Go to Repository Settings > Pages
3. Set source to `main` branch and `/(root)` folder
4. Click Save
5. Your site will be published at `https://<username>.github.io/<repository-name>/`

## Credits

- Uses [allorigins.win](https://allorigins.win/) as a CORS proxy
- Built with plain HTML, CSS, and vanilla JavaScript

## License

MIT License - feel free to use and modify as needed.