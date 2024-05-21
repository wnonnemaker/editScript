from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import os

# Set up Selenium WebDriver (ensure chromedriver is in your PATH)
driver = webdriver.Chrome()

#chromedriver location: C:\Users\will\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\site-packages\chromedriver_binary

# Open Google Images
driver.get("https://www.britannica.com/art/Modernism-art/images-videos")

# Search for images
search_box = driver.find_element(By.NAME, "q")
search_query = "puppies"
search_box.send_keys(search_query + Keys.RETURN)

# Scroll to load more images
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Parse the page source and extract image URLs
soup = BeautifulSoup(driver.page_source, 'html.parser')
image_elements = soup.find_all('img')

image_urls = []
for img in image_elements:
    url = img.get('src')
    if url and 'http' in url:
        image_urls.append(url)

# Create a directory to save images
if not os.path.exists('images'):
    os.makedirs('images')

# Download images
for i, url in enumerate(image_urls):
    response = requests.get(url)
    with open(f'images/image_{i}.jpg', 'wb') as file:
        file.write(response.content)

# Close the WebDriver
driver.quit()
