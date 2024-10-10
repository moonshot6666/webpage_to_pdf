
# Webpage to PDF Project

## Description
This project is designed to scrape webpages from a list of URLs (provided in a txt file) and save each webpage as a PDF.

## Folder Structure
- **src/**: Contains the source code for the project.
- **data/**: Contains input files (such as `urls.txt`) and the output PDFs.
- **tests/**: Placeholder for tests.
- **scripts/**: Contains shell scripts to run the project.

## How to Use
1. Add URLs to the `data/urls.txt` file (one URL per line).
2. Run the script `webpage_to_pdf.py` from the project root to download the webpages as PDFs.
3. All existing PDFs in the output directory will be deleted before starting the process.

## Requirements
- Selenium
- ChromeDriver
