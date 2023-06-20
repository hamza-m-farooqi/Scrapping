from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import json
from datetime import datetime
import requests
import base64
import time
import re
from config import (
    BASE_DIRECTORY_FOR_SCRAPPED_DATA,
    STABLE_DIFFUSION_AI_GENERATED_SCRAPPED_IMAGES_INFO_FILE_NAME,
    STABLE_DIFFUSION_AI_GENERATED_IMAGES_COMMUNITY_DISCUSSION_INFO_FILE_NAME
)
from utility_methods import update_scrapped_data_in_json_file


base_page_link = (
    "https://huggingface.co/spaces/stabilityai/stable-diffusion/discussions"
)
api_url_for_discussions = (
    "https://huggingface.co/api/spaces/stabilityai/stable-diffusion/discussions"
)
total_pages = 318
total_images = 0
scrapped_data_file_name = (
    BASE_DIRECTORY_FOR_SCRAPPED_DATA
    + STABLE_DIFFUSION_AI_GENERATED_SCRAPPED_IMAGES_INFO_FILE_NAME
)

scrapping_info = {
    "Date": str(datetime.now().date()),
    "Link": base_page_link,
    "Data": [],
}


def get_page_data_from_community_page():
    fetched_info = []
    for i in range(total_pages):
        try:
            params = {"p": i + 1, "status": "open"} 
            response = requests.get(api_url_for_discussions, params=params)
            if response.status_code == 200:
                json_data = response.json()
                rows_in_data = json_data["discussions"]
                for row in rows_in_data:
                    row_data = {
                        "discussion_page_num": i + 1,
                        "discussion_num": row["num"],
                        "discussion_title": row["title"],
                    }
                    fetched_info.append(row_data)
                    print(row_data)
            else:
                print("Error:", response.status_code)
        except:
            continue
        with open(STABLE_DIFFUSION_AI_GENERATED_IMAGES_COMMUNITY_DISCUSSION_INFO_FILE_NAME,"w") as f:
            json.dump(fetched_info,f,indent=4)

info_of_discussions = get_page_data_from_community_page()




# driver = webdriver.Chrome()
# driver.maximize_window()
# for info in info_of_discussions:
#     driver.get(base_page_link + f"/{info['discussion_num']}")
#     div_is_with_img_tags = False
#     div_si_with_a_tags = False
#     try:
#         parent_div_with_imgages = driver.find_element(
#             By.XPATH,
#             "//div[contains(@class, 'prose') and contains(@class, 'prose-discussion') and div/img]",
#         )
#         div_is_with_img_tags = True
#     except:
#         try:
#             parent_div_with_imgages = driver.find_element(
#                 By.XPATH,
#                 "//div[contains(@class, 'prose') and contains(@class, 'prose-discussion') and p/a]",
#             )
#             div_si_with_a_tags = True
#         except:
#             parent_div_with_imgages = None
#     if parent_div_with_imgages is None:
#         print("======================================================")
#         print("==========Connot Find Div Holding Images==============")
#         print("======================================================")
#         continue
#     if div_is_with_img_tags:
#         images = parent_div_with_imgages.find_elements(By.TAG_NAME, "img")
#     elif div_si_with_a_tags:
#         images = parent_div_with_imgages.find_elements(By.TAG_NAME, "a")
#     for image in images:
#         total_images += 1
#         scrapped_data_object = {
#             "page_number": info["discussion_page_num"],
#             "image_number": total_images,
#             "image_id": "",
#             "image_detail_link": "",
#             "image_name": "",
#             "image_src": "",
#         }
#         if div_is_with_img_tags:
#             scrapped_data_object["image_src"] = image.get_attribute("src")
#         elif div_si_with_a_tags:
#             scrapped_data_object["image_src"] = image.get_attribute("href")
#         pattern = r"/noauth/([^/]+)$"
#         match = re.search(pattern, scrapped_data_object["image_src"])
#         if match:
#             scrapped_data_object["image_name"] = match.group(1)
#         scrapped_data_object["image_id"] = str(
#             scrapped_data_object["image_name"]
#         ).split(".")[0]
#         scrapping_info["Data"].append(scrapped_data_object)
#     update_scrapped_data_in_json_file(scrapping_info, scrapped_data_file_name)
# driver.quit()
