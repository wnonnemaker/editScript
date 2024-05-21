from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import os
import time
import argparse

#use for any webpage
#parser = argparse.ArgumentParser(description='Description of your script.')
#parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the webpage containing the images')
#args = parser.parse_args()
#webpage_url = args.url

# Path to your chromedriver
chromedriver_path = r'C:\Users\will\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\site-packages\chromedriver_binary\chromedriver.exe'  # Update this path

# Set up the Chrome WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome()

# URL of the webpage containing the images
webpage_url = 'https://www.britannica.com/art/English-literature/images-videos'  # Update this URL

# Open the webpage
driver.get(webpage_url)

# Wait for the page to load completely
time.sleep(5)

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all image tags
img_tags = soup.find_all('img')

# Extract the URLs of the images
image_urls = [img['src'] for img in img_tags if 'src' in img.attrs]

# Create a directory to save images
if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')

# Download images
for i, url in enumerate(image_urls):
    # Make sure the URL is complete
    if not url.startswith(('http://', 'https://')):
        url = f'{webpage_url}/{url}'
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(f'downloaded_images/image_{i}.jpg', 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f'Downloaded image {i+1}')
        else:
            print(f'Failed to download image {i+1} (HTTP {response.status_code})')
    except Exception as e:
        print(f'Failed to download image {i+1}: {e}')

# Close the WebDriver
driver.quit()
