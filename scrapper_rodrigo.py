import os
import sys
import json
import signal
from alive_progress import alive_bar
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from seleniumwire import webdriver as sweb

# import random

# # # the list of proxy to rotate on 
# PROXIES = [
#     "http://20.235.159.154:80",
#     "http://149.169.197.151:80",
#     "http://138.197.102.119:80",
#     "http://212.76.118.242:97",
#     "http://198.49.68.80:80"
# ]

# # randomly select a proxy
# proxy = random.choice(PROXIES)

# # set selenium-wire options to use the proxy
# seleniumwire_options = {
#     "proxy": {
#         "http": proxy,
#         "https": proxy
#     },
# }

# Define Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.page_load_strategy = 'eager'

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

                # # dump the whole html to a txt file
                # with open(f"outputs/meme{id}.txt", "w") as file:
                #     file.write(browser.page_source)

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
