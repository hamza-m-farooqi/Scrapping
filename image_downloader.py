import requests
import json
import os
from config import (
    BASE_DIRECTORY_FOR_DOWNLOADED_IMAGES,
    BASE_DIRECTORY_FOR_SCRAPPED_DATA,
    PICS_ART_AI_GENERATED_SCRAPPED_IMAGES_INFO_FILE_NAME,
)


def download_image(image_source, image_name, images_directory):
    try:
        image_format = ""
        image_data = ""
        if not image_source.startswith("http"):
            return "Image Source has not http address"
        else:
            try:
                image_response = requests.get(image_source)
                if image_response.status_code != 200:
                    return "Couldn't Download Image"
                splitted_image_source = str(image_source).split(".")
                image_format = splitted_image_source[len(splitted_image_source) - 1]
                image_data = image_response.content
            except:
                return "Couldn't Download Image"

        image_name = image_name + "." + image_format
        image_path = os.path.join(images_directory + image_name)
        print(image_path)
        with open(image_path, "wb") as file:
            file.write(image_data)
        return image_name
    except:
        return "Couldn't Download Image"


def read_scrapped_data_info(file_path):
    images_directory = (
        BASE_DIRECTORY_FOR_DOWNLOADED_IMAGES + "pics_art_ai_generated_images/"
    )
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)
        print("Directory Created : ",images_directory)
    with open(file_path, "r") as f:
        file_data = json.load(f)
        for scrapped_data_object in file_data["Data"]:
            download_image(
                image_source=scrapped_data_object["image_src"],
                image_name=scrapped_data_object["image_name"],
                images_directory=images_directory,
            )


read_scrapped_data_info(
    BASE_DIRECTORY_FOR_SCRAPPED_DATA
    + PICS_ART_AI_GENERATED_SCRAPPED_IMAGES_INFO_FILE_NAME
)
