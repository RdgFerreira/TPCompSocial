import csv
import time
import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Define Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

# Define paths
user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

# Set binary location and service
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

# url = "https://knowyourmeme.com/memes/50914"
# 50915

base_url = "https://knowyourmeme.com/memes/"

with open("memes.csv", "w", newline="", encoding="utf-8") as csvfile:
    details_csv_writer = csv.writer(csvfile)

    details_csv_writer.writerow(
        [
            "id",
            "meme_title",
            "views",
            "status",
            "type(s)",
            "badges",
            "year",
            "origin",
            "region",
            "tags",
        ]
    )

    # Initialize Chrome WebDriver
    with webdriver.Chrome(service=service, options=chrome_options) as browser:
        for id in range(1, 3):
            details_csv_writer.writerow(
                [
                    str(id),
                    "undefined",
                    "undefined",
                    "undefined",
                    "undefined",
                    "undefined",
                    "undefined",
                    "undefined",
                    "undefined",
                    "undefined",
                ]
            )
            url = base_url + str(id)
            print(f"Browsing {url}")
            browser.get(url)

            try:
                meme_title = browser.find_element(By.TAG_NAME, "h1").text
                print(f"Title: {meme_title}")
                time.sleep(2)

                table_elements = browser.find_elements(By.TAG_NAME, "dl")
                print(f"Table elements: {table_elements}")
                [engagement_stats, general_info, tags] = table_elements

                views = engagement_stats.find_element(By.CLASS_NAME, "views").text
                print(f"Views: {views}")

                status = general_info.text.split("\n")
                print(f"Status: {status}")

                # split tags on comma or newline
                tags = tags.find_element(By.TAG_NAME, "dd").text.split(",")
                tags_fixed = []
                for tag in tags:
                    if "\n" in tag:
                        tag_sublist = tag.split("\n")
                        for sub_tag in tag_sublist:
                            sub_tag = re.sub(r"\s+", "_", sub_tag)
                            if sub_tag[0] == "_":
                                sub_tag = sub_tag[1:]
                            tags_fixed.append(sub_tag)
                    else:
                        tag = re.sub(r"\s+", "_", tag)
                        if tag[0] == "_":
                            tag = tag[1:]
                        tags_fixed.append(tag)
                print(f"Tags: {tags_fixed}")

            except NoSuchElementException:
                print(f"Element not found, Skipping meme {id}")
                continue

        browser.quit()
