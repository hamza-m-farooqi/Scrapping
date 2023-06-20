from DataBase.database_actions import Database_Actions
from DataBase.database_models import (
    AI_Generated_Images_Search_Words,
    AI_Generated_Images_Search_Words_Track,
    AI_Generated_Images_Scrapping_Info,
    AI_Generated_Images_Platforms_Info,
)
import requests
from datetime import datetime


def fetch_search_results(search_word):
    print("===========================================")
    print(f"=== Going to search for {search_word} ====")
    print("===========================================")
    url = "https://api.craiyon.com/search"

    payload = {"text": search_word, "version": "hpv3obayw36clkqp"}
    files = []
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.json()


def extract_formatted_image_id(raw_id):
    return str(str(raw_id).split(".")[0]).replace("/", "_")


database_action = Database_Actions("sqlite:///DataBase/database.db")
search_action_flag = True
while search_action_flag == True:
    search_words_list = database_action.get_search_words_untracked_by_platform(
        "Craiyon AI"
    )
    print(search_words_list)
    if not search_words_list.__len__():
        search_action_flag = False
        continue
    print("Executing Search......")
    craiyon_platform_id = database_action.get(
        AI_Generated_Images_Platforms_Info, name="Craiyon AI"
    )[0].id
    print(craiyon_platform_id)
    image_number = 0
    latest_entry = database_action.get_latest(
        AI_Generated_Images_Scrapping_Info,
        "image_number",
        platform_id=craiyon_platform_id,
    )
    if latest_entry is not None:
        image_number = latest_entry.image_number

    for search_word in search_words_list:
        serarch_results = fetch_search_results(search_word.keyword)
        for search_result in serarch_results:
            image_number += 1
            image_id = extract_formatted_image_id(search_result["image_id"])
            image_name = image_id + ".jpg"
            database_entity = AI_Generated_Images_Scrapping_Info(
                date=datetime.now(),
                platform_id=craiyon_platform_id,
                page_number=1,
                image_number=image_number,
                image_id=image_id,
                image_name=image_name,
                image_src=f"https://pics.craiyon.com/{search_result['image_id']}",
                image_promt=search_result["prompt"],
                image_download_status=False,
            )
            entry_flag = database_action.check_if_value_exists(
                AI_Generated_Images_Scrapping_Info,
                image_id=image_id,
                platform_id=craiyon_platform_id,
            )
            if entry_flag:
                print("========= Image Already Exists ==============")
                continue
            database_action.add(database_entity)
            print(f"Image with Id {image_id} successfully added to database.")
        database_entry_for_tracking = AI_Generated_Images_Search_Words_Track(
            platform_id=craiyon_platform_id,
            search_word_id=search_word.id,
            search_status=True,
        )
        database_action.add(database_entry_for_tracking)
