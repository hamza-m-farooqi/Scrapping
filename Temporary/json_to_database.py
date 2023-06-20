import json
import sys
from datetime import datetime

sys.path.append("/home/itsmenotyou/Documents/VisualStudioCode/Python/Scrapping")
from DataBase.database_actions import Database_Actions
from DataBase.database_models import (
    AI_Generated_Images_Platforms_Info,
    AI_Generated_Images_Scrapping_Info,
)
from config import (
    BASE_DIRECTORY_FOR_SCRAPPED_DATA,
)

records = []
try:
    with open(
        BASE_DIRECTORY_FOR_SCRAPPED_DATA
        + "stable_diffusion_ai_generated_images_scrapping_withbs4_info.json",
        "r",
    ) as f:
        file_data = json.load(f)
        records = file_data["Data"]
except Exception as ex:
    print(f"An Error Occured while Reading File : {str(ex)}")

database_repository = Database_Actions("sqlite:///DataBase/database.db")
stable_diffusion_platform_id = database_repository.get(
    AI_Generated_Images_Platforms_Info, name="Stable Diffusion Community"
)[0].id
print(stable_diffusion_platform_id)
ai_generated_images_scrapping_info_from_stable_diffusion_community = []
latest_entry = database_repository.get_latest(
    AI_Generated_Images_Scrapping_Info, "image_number"
)
print(latest_entry)
# if records:
#     for record in records:
#         image_number += 1
#         ai_generated_images_scrapping_info_from_stable_diffusion_community.append(
#             AI_Generated_Images_Scrapping_Info(
#                 date=datetime.now(),
#                 platform_id=stable_diffusion_platform_id,
#                 page_number=int(record["page_number"]),
#                 image_number=int(record["image_number"]),
#                 image_id=record["image_id"],
#                 image_name=record["image_name"],
#                 image_src=record["image_src"],
#                 image_promt="",
#                 image_download_status=False,
#             )
#         )
#         print(image_number)

# database_repository.bulk_add(
#     ai_generated_images_scrapping_info_from_stable_diffusion_community
# )

# print("===========================================================")
# print("==========Entries Succussfully Added To Database===========")
# print("===========================================================")