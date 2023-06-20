from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import json
from datetime import datetime
import requests
import base64
import time
from config import (
    BASE_DIRECTORY_FOR_SCRAPPED_DATA,
    PICS_ART_AI_GENERATED_SCRAPPED_IMAGES_INFO_FILE_NAME,
)
from utility_methods import get_image_id_from_string, update_scrapped_data_in_json_file
import re

base_page_link = "https://picsart.com"
ai_generated_images_page_link = "https://picsart.com/images/ai-generated-image?page="
total_pages = 63
total_images = 0
scrapped_data_file_name = (
    BASE_DIRECTORY_FOR_SCRAPPED_DATA
    + PICS_ART_AI_GENERATED_SCRAPPED_IMAGES_INFO_FILE_NAME
)
scrapping_info = {
    "Date": str(datetime.now().date()),
    "Link": base_page_link,
    "Data": [],
}
driver = webdriver.Chrome()
driver.maximize_window()
# Request Page
for page_number in range(total_pages):
    page = page_number + 1
    driver.get(ai_generated_images_page_link + str(page))
    # driver.implicitly_wait(5)
    # image_cards_div="photo-card-categories-root-0-2-100"
    image_cards_div = "photo-card-categories-root-0-2-93"
    # Wait for Page to Render
    wait = WebDriverWait(driver, 5.0)
    # wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,image_cards_div)))
    wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    # Find divs
    image_cards_list = driver.find_elements(By.CLASS_NAME, image_cards_div)
    for image_card in image_cards_list:
        total_images += 1
        scrapped_data_object = {
            "page_number": page,
            "image_number": total_images,
            "image_id": "",
            "image_detail_link": "",
            "image_name": "",
            "image_src": "",
        }
        a_tag = image_card.find_element(By.TAG_NAME, "a")
        a_tag_href = a_tag.get_attribute("href")
        img_tag = image_card.find_element(By.TAG_NAME, "img")
        img_src = img_tag.get_attribute("src")
        if img_src and not img_src.startswith("http"):
            img_style_value = img_tag.get_attribute("style")
            if img_style_value:
                url_match = re.search(r"url\(['\"]?([^'\"]+)['\"]?\)", img_style_value)
                if url_match:
                    img_src = url_match.group(1)

        scrapped_data_object["image_id"] = get_image_id_from_string(a_tag_href)
        scrapped_data_object["image_detail_link"] = a_tag_href
        scrapped_data_object["image_name"] = (
            "pics_art_ai_generated_image_" + scrapped_data_object["image_id"]
        )
        scrapped_data_object["image_src"] = img_src
        # Add in Main Data Object
        scrapping_info["Data"].append(scrapped_data_object)
        update_scrapped_data_in_json_file(scrapping_info, scrapped_data_file_name)
driver.quit()


def extract_image_format(base64_string):
    prefix = "data:image/"
    suffix = ";base64"

    start_index = base64_string.find(prefix)
    end_index = base64_string.find(suffix)

    if start_index != -1 and end_index != -1:
        format_start_index = start_index + len(prefix)
        format_end_index = end_index

        image_format = base64_string[format_start_index:format_end_index]
        return image_format

    return None


def scroll_browser_page():
    page_height = driver.execute_script("return document.documentElement.scrollHeight")
    while (
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight); return document.documentElement.scrollHeight;"
        )
        < page_height
    ):
        time.sleep(1)
        page_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )


def check_if_author_exists(author_name):
    for data in scrapped_data_object["Data"]:
        if data["AuthorName"] == author_name:
            return data["AuthorImage"]
    return None
