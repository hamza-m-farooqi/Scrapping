from DataBase.database_actions import Database_Actions
from DataBase.database_models import (
    AI_Generated_Images_Platforms_Info,
    AI_Generated_Images_Scrapping_Info,
)
import requests
import json
from datetime import datetime
import re


def fetch_api_results(next_id):
    print("===========================================")
    print(f"Going to fetch result for page {next_id}")
    print("===========================================")
    if next_id is not None:
        url = f"https://www.fotor.com/api/aigc/community/works/new?size=10&nextId={next_id}"
    else:
        url = f"https://www.fotor.com/api/aigc/community/works/new?size=10"
    payload = {}
    headers = {"Authority": "www.fotor.com", "X-App-Id": "app-fotor-web"}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def extract_formatted_image_url(raw_url):
    return str(raw_url).split("@")[0]


def extract_formatted_image_name(url):
    pattern = r"/([^/]+)$"
    match = re.search(pattern, url)
    if match:
        image_name = match.group(1)
        return image_name
    else:
        return None


def extract_formatted_image_id(image_name):
    return str(image_name).split(".")[0]


database_actions = Database_Actions("sqlite:///DataBase/database.db")
platform_id = database_actions.get(
    AI_Generated_Images_Platforms_Info, name="Fotor Hot Creations"
)[0].id
print(platform_id)

image_number = 0
latest_entry = database_actions.get_latest(
    AI_Generated_Images_Scrapping_Info,
    "image_number",
    platform_id=platform_id,
)
if latest_entry is not None:
    image_number = latest_entry.image_number

api_execution_flag = True
api_next_page_value = None
total_pages = 0
while api_execution_flag == True:
    search_result = fetch_api_results(api_next_page_value)
    if search_result["data"]["next_id"] == "" or search_result["data"]["next_id"] == "":
        api_execution_flag = False
        continue
    total_pages += 1
    api_next_page_value = search_result["data"]["next_id"]
    if search_result is not None:
        images_list = search_result["data"]["works"]
        for images_info in images_list:
            image_number += 1
            if len(images_info["images"]):
                image_src = extract_formatted_image_url(
                    images_info["images"][0]["preview_url"]
                )
                image_name = extract_formatted_image_name(image_src)
                image_id = extract_formatted_image_id(image_name)
                image_promt = ""
                if images_info["creative_type"] != "textToImage":
                    continue
                image_promt = images_info["source_option_params"]["aigc_prompt"]
                database_entity = AI_Generated_Images_Scrapping_Info(
                    date=datetime.now(),
                    platform_id=platform_id,
                    page_number=1,
                    image_number=image_number,
                    image_id=image_id,
                    image_name=image_name,
                    image_src=image_src,
                    image_promt=image_promt,
                    image_download_status=False,
                )
                entry_flag = database_actions.check_if_value_exists(
                    AI_Generated_Images_Scrapping_Info,
                    image_id=image_id,
                    platform_id=platform_id,
                )
            if entry_flag:
                print("========= Image Already Exists ==============")
                continue
            database_actions.add(database_entity)
            print(
                f"Image with Id {image_id} successfully added to database from Page {total_pages}."
            )
