import csv
import time
import os
import pandas as pd
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

base_url = "https://knowyourmeme.com/memes/"

range_start, range_end = int(sys.argv[1]), int(sys.argv[2])

# Initialize Chrome WebDriver
with webdriver.Chrome(service=service, options=chrome_options) as browser:
    memes = []
    for id in range(range_start, range_end+1):
        url = base_url + str(id)
        print(f"Browsing {url}")
        browser.get(url)
        meme_object = dict({})

        try:
            meme_object["id"] = id

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

            info_names = general_info.find_elements(By.TAG_NAME, "dt")
            info_values = general_info.find_elements(By.TAG_NAME, "dd")

            for name, value in zip(info_names, info_values): meme_object[name.text.strip()] = value.text.strip()

            tagsElement = tags_cnt.find_element(By.TAG_NAME, "dd")
            tagElements = tagsElement.find_elements(By.TAG_NAME, "a")
            tags = [tagElement.text for tagElement in tagElements]
            print(f"tags: {tags}")
            meme_object["tags"] = tags
        
            memes.append(meme_object)

        except:
            print(f"Element not found, Skipping meme {id}")

    with open(f"memes{range_start}-{range_end}.json", "w") as outfile:
        json.dump(memes, outfile)

browser.quit()