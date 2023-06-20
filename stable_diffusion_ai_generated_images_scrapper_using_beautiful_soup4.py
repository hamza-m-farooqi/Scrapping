import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
from utility_methods import update_scrapped_data_in_json_file
from config import (
    BASE_DIRECTORY_FOR_SCRAPPED_DATA,
    STABLE_DIFFUSION_AI_GENERATED_IMAGES_COMMUNITY_DISCUSSION_INFO_FILE_NAME,
)
from DataBase.database_actions import Database_Actions
from DataBase.database_models import (
    AI_Generated_Images_Platforms_Info,
    AI_Generated_Images_Scrapping_Info,
)

base_page_link = (
    "https://huggingface.co/spaces/stabilityai/stable-diffusion/discussions"
)

with open(
    STABLE_DIFFUSION_AI_GENERATED_IMAGES_COMMUNITY_DISCUSSION_INFO_FILE_NAME, "r"
) as f:
    info_of_discussions = json.load(f)
scrapped_data_file_name = (
    BASE_DIRECTORY_FOR_SCRAPPED_DATA
    + "stable_diffusion_ai_generated_images_scrapping_withbs4_info.json"
)

database_actions = Database_Actions("sqlite:///DataBase/database.db")

stable_diffusion_platform_id = database_actions.get(
    AI_Generated_Images_Platforms_Info, name="Stable Diffusion Community"
)[0].id

total_images = 0

latest_scrapped_entry = database_actions.get_latest(
    AI_Generated_Images_Scrapping_Info, "image_number",platform_id=2
)
    
if latest_scrapped_entry.platform_id != stable_diffusion_platform_id:
    latest_scrapped_entry = None
else:
    total_images = latest_scrapped_entry.image_number
continuity_flag = False
print(latest_scrapped_entry, total_images)
try:
    if latest_scrapped_entry is not None:
        info_of_discussions = [
            obj
            for obj in info_of_discussions
            if obj["discussion_page_num"] > latest_scrapped_entry.page_number
        ]
        continuity_flag = True
except:
    continuity_flag = False
if continuity_flag is False:
    print("======================================================")
    print("===============Starting from Scratch==================")
    print("======================================================")

session = requests.Session()

for info in info_of_discussions:
    try:
        discussion_url = base_page_link + f"/{info['discussion_num']}"
        response = session.get(discussion_url)
        soup = BeautifulSoup(response.content, "html.parser")

        parent_div_with_images = None
        div_is_with_img_tags = False
        div_si_with_a_tags = False

        # Find the parent div with images
        divs_prose = soup.find_all("div", class_="prose")
        divs_prose_discussion = soup.find_all("div", class_="prose-discussion")

        for div in divs_prose:
            if div.find("img"):
                parent_div_with_images = div
                div_is_with_img_tags = True
                break

        if not parent_div_with_images:
            for div in divs_prose_discussion:
                if div.find("p").find("a"):
                    parent_div_with_images = div
                    div_si_with_a_tags = True
                    break

        if not parent_div_with_images:
            print("======================================================")
            print("==========Cannot Find Div Holding Images==============")
            print("======================================================")
            continue

        images = []
        if div_is_with_img_tags:
            images = parent_div_with_images.find_all("img")
        elif div_si_with_a_tags:
            images = parent_div_with_images.find("p").find_all("a")

        for image in images:
            total_images += 1
            scrapped_data_object = {
                "page_number": info["discussion_page_num"],
                "image_number": total_images,
                "image_id": "",
                "image_detail_link": "",
                "image_name": "",
                "image_src": "",
            }
            if div_is_with_img_tags:
                scrapped_data_object["image_src"] = image["src"]
            elif div_si_with_a_tags:
                scrapped_data_object["image_src"] = image["href"]

            pattern = r"/noauth/([^/]+)$"
            match = re.search(pattern, scrapped_data_object["image_src"])
            if match:
                scrapped_data_object["image_name"] = match.group(1)
            else:
                pattern = r"/uploads/([^/]+)$"
                match = re.search(pattern, scrapped_data_object["image_src"])
                if match:
                    scrapped_data_object["image_name"] = match.group(1)
            scrapped_data_object["image_id"] = str(
                scrapped_data_object["image_name"]
            ).split(".")[0]
            database_entity = AI_Generated_Images_Scrapping_Info(
                date=datetime.now(),
                platform_id=stable_diffusion_platform_id,
                page_number=int(scrapped_data_object["page_number"]),
                image_number=int(scrapped_data_object["image_number"]),
                image_id=scrapped_data_object["image_id"],
                image_name=scrapped_data_object["image_name"],
                image_src=scrapped_data_object["image_src"],
                image_promt=info["discussion_title"],
                image_download_status=False,
            )
            print(total_images,scrapped_data_object)
            database_actions.add(database_entity)
            # scrapping_info["Data"].append(scrapped_data_object)
        # Update scrapped data in JSON file
        # update_scrapped_data_in_json_file(scrapping_info, scrapped_data_file_name)
    except:
        continue
