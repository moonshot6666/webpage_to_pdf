
import time
import base64
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from src.utils import remove_existing_pdfs  # Absolute import from src

# Function to wait for all images to load and scroll to trigger lazy-loaded content
def wait_for_full_page_load(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(0.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    image_load_script = '''
    return Array.from(document.images).every(function(img) {
        return img.complete && (typeof img.naturalWidth == 'undefined' || img.naturalWidth > 0);
    });
    '''
    try:
        WebDriverWait(driver, 15).until(lambda d: d.execute_script(image_load_script))
    except TimeoutException:
        print("Some images may not have loaded, but proceeding...")

# Function to save webpage as PDF
def save_webpage_as_pdf(url, output_pdf_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--kiosk-printing')

    driver_path = "/usr/local/bin/chromedriver"  # Update this to the path of your ChromeDriver
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        wait_for_full_page_load(driver)
        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {})
        pdf_base64 = pdf_data['data']
        pdf_bytes = base64.b64decode(pdf_base64)
        with open(output_pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf_bytes)
        print(f"PDF saved successfully at {output_pdf_path}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
    finally:
        driver.quit()

# Function to process URLs from a txt file
def process_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    for idx, url in enumerate(urls):
        url = url.strip()
        if url:
            output_pdf_path = f'./output_{idx + 1}.pdf'
            print(f"Processing URL: {url}")
            save_webpage_as_pdf(url, output_pdf_path)

# Main execution
if __name__ == "__main__":
    remove_existing_pdfs('./data')  # Now removing PDFs in the data folder
    process_urls_from_file('./data/urls.txt')  # Update path as needed
