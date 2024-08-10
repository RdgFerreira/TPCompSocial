import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)

url = "https://knowyourmeme.com/memes/50914"
# 50915

# while True:

driver.get(url)
elements = driver.find_elements(By.TAG_NAME, "dl")
for element in elements:
    print(element.text)
    print("\n")

driver.quit()
