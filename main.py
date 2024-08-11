import csv
import time
import os
import pandas as pd
import sys
import json
import signal
from alive_progress import alive_bar
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.page_load_strategy = 'eager'

base_url = "https://knowyourmeme.com/memes/"

range_start, range_end = int(sys.argv[1]), int(sys.argv[2])

# Initialize Chrome WebDriver
with alive_bar(range_end-range_start+1) as bar:
    memes = []
    for id in range(range_start, range_end+1):
        with webdriver.Chrome(service=service, options=chrome_options) as browser:
            url = base_url + str(id)
            meme_object = dict({})

            def handler(signum, frame):
                raise Exception("end of time")
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(10)
                
            try:
                browser.get(url)

            except:
                print(f"Page not found in 10 seconds, Skipping meme {id}")
                signal.alarm(0)
                browser.quit()
                bar()
                continue

            try:
                meme_object["id"] = id

                meme_title = browser.find_element(By.TAG_NAME, "h1").text
                meme_object["title"] = meme_title

                table_elements = browser.find_elements(By.TAG_NAME, "dl")
                [engagement_stats, general_info, tags_cnt] = table_elements

                views = engagement_stats.find_element(By.CLASS_NAME, "views").text
                meme_object["views"] = int(views.replace(',', ''))

                videos = engagement_stats.find_element(By.CLASS_NAME, "videos").text
                meme_object["videos"] = int(videos)

                photos = engagement_stats.find_element(By.CLASS_NAME, "photos").text
                meme_object["photos"] = int(photos)

                comments = engagement_stats.find_element(By.CLASS_NAME, "comments").text
                meme_object["comments"] = int(comments)

                category = general_info.find_element(By.CLASS_NAME, "entry-category-badge").text
                meme_object["category"] = category

                info_names = general_info.find_elements(By.TAG_NAME, "dt")
                info_values = general_info.find_elements(By.TAG_NAME, "dd")

                for name, value in zip(info_names, info_values): meme_object[name.text.strip()] = value.text.strip()

                tagsElement = tags_cnt.find_element(By.TAG_NAME, "dd")
                tagElements = tagsElement.find_elements(By.TAG_NAME, "a")
                tags = [tagElement.text for tagElement in tagElements]
                meme_object["tags"] = tags
            
                memes.append(meme_object)
                signal.alarm(0)
                browser.quit()
                bar()

            except:
                print(f"Element not found, Skipping meme {id}")
                signal.alarm(0)
                browser.quit()
                bar()
            

        with open(f"outputs/memes{range_start}-{range_end}.json", "w") as outfile:
            json.dump(memes, outfile)