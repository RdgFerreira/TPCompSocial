import csv
import time
import os
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Define Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

# Define paths
user_home_dir = os.path.expanduser("~")
chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
dir = os.path.dirname(__file__)
chromedriver_path = os.path.join(dir, "chromedriver")

# Set binary location and service
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

# url = "https://knowyourmeme.com/memes/50914"
# 50915

base_url = "https://knowyourmeme.com/memes/"

# Initialize Chrome WebDriver
with webdriver.Chrome(service=service, options=chrome_options) as browser:
    memes = []
    for id in range(1, 6):
        url = base_url + str(id)
        print(f"Browsing {url}")
        browser.get(url)

        meme_object = dict({})

        try:
            meme_title = browser.find_element(By.TAG_NAME, "h1").text
            print(f"Title: {meme_title}")
            meme_object["title"] = meme_title

            table_elements = browser.find_elements(By.TAG_NAME, "dl")
            [engagement_stats, general_info, tags_cnt] = table_elements

            views = engagement_stats.find_element(By.CLASS_NAME, "views").text
            print(f"Views: {views}")
            meme_object["views"] = int(views.replace(',', ''))

            videos = engagement_stats.find_element(By.CLASS_NAME, "videos").text
            print(f"Videos: {videos}")
            meme_object["videos"] = int(videos)

            photos = engagement_stats.find_element(By.CLASS_NAME, "photos").text
            print(f"photos: {photos}")
            meme_object["photos"] = int(photos)

            comments = engagement_stats.find_element(By.CLASS_NAME, "comments").text
            print(f"comments: {comments}")
            meme_object["comments"] = int(comments)

            category = general_info.find_element(By.CLASS_NAME, "entry-category-badge").text
            print(f"category: {category}")
            meme_object["category"] = category

            [statusElement, typeElement, yearElement, originElement] = general_info.find_elements(By.TAG_NAME, "dd")

            status = statusElement.text
            print(f"status: {status}")
            meme_object["status"] = status

            entry_type = typeElement.find_element(By.TAG_NAME, "a").text
            print(f"entry: {entry_type}")
            meme_object["type"] = entry_type

            year = yearElement.find_element(By.TAG_NAME, "a").text
            print(f"year {year}")
            meme_object["year"] = int(year)

            origin = originElement.find_element(By.TAG_NAME, "a").text
            print(f"origin: {origin}")
            meme_object["origin"] = origin

            tagsElement = tags_cnt.find_element(By.TAG_NAME, "dd")
            tagElements = tagsElement.find_elements(By.TAG_NAME, "a")
            tags = [tagElement.text for tagElement in tagElements]
            print(f"tags: {tags}")
            meme_object["tags"] = tags
        
            memes.append(meme_object)

        except:
            print(f"Element not found, Skipping meme {id}")

    with open("memes.json", "w") as outfile:
        json.dump(memes, outfile)

browser.quit()
