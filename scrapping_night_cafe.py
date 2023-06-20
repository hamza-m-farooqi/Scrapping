from DataBase.database_actions import Database_Actions
from DataBase.database_models import (
    AI_Generated_Images_Platforms_Info,
    AI_Generated_Images_Scrapping_Info,
)
import requests
from datetime import datetime
import json


def fetch_api_results(next_id):
    try:
        print("===========================================")
        print(f"Going to fetch result for page {next_id}")
        print("===========================================")
        with open("Data/current_page_at_night_cafe_community.json", "w") as f:
            file_data = {"current_page": next_id}
            json.dump(file_data, f, indent=4)
        if next_id is not None:
            url = f"https://us-central1-nightcafe-creator.cloudfunctions.net/api/creations?query=mixed&filter=none&lastVisibleId={next_id}"
        else:
            url = f"https://us-central1-nightcafe-creator.cloudfunctions.net/api/creations?query=mixed&filter=none"
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()
    except Exception as ex:
        print("An Error Occured while fetching records : ", str(ex))
        return None


def extract_formatted_image_name(url):
    splitted_url = str(url).split("/")
    return splitted_url[len(splitted_url) - 1]


def extract_formatted_image_id(image_name):
    return str(image_name).split(".")[0]


database_actions = Database_Actions("sqlite:///DataBase/night_cafe_images.db")
platform_id = database_actions.get(
    AI_Generated_Images_Platforms_Info, name="Night Cafe Community"
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
try:
    with open("Data/current_page_at_night_cafe_community.json", "r") as f:
        file_data = json.load(f)
        print(file_data)
        api_next_page_value = file_data["current_page"]
except Exception as ex:
    print("An Error Occured while reading page id : ", str(ex))
    pass
total_pages = 0
while api_execution_flag == True:
    search_result = fetch_api_results(api_next_page_value)
    if search_result is None:
        api_execution_flag = False
        continue

    total_pages += 1
    api_next_page_value = search_result["lastVisibleId"]
    images_list = search_result["results"]
    for image_info in images_list:
        image_number += 1
        image_src = "https://images.nightcafe.studio" + image_info["output"]
        image_name = extract_formatted_image_name(image_src)
        image_id = extract_formatted_image_id(image_name)
        image_promt = image_info["title"]
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
