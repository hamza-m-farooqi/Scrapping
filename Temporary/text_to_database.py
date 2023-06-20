import json
import sys
from datetime import datetime

sys.path.append("/home/itsmenotyou/Documents/VisualStudioCode/Python/Scrapping")
from DataBase.database_actions import Database_Actions
from DataBase.database_models import (
    AI_Generated_Images_Platforms_Info,
    AI_Generated_Images_Search_Words,
)
from config import (
    BASE_DIRECTORY_FOR_SCRAPPED_DATA,
)


def read_file_to_list(filename):
    string_list = []
    with open(filename, "r") as file:
        for line in file:
            string_list.append(line.strip())
    return string_list


# text_files_list = [
#     "aliens.txt",
#     "animals.txt",
#     "bikes.txt",
#     "cars.txt",
#     "cultures.txt",
#     "famous_artists.txt",
#     "famous_buildings.txt",
#     "famous_cities.txt",
#     "famous_events.txt",
#     "famous_female_actors.txt",
#     "famous_foods.txt",
#     "famous_male_actors.txt",
#     "famous_paintings.txt",
#     "human_form.txt",
#     "modern.txt",
#     "mythical_creatures.txt",
#     "nouns.txt",
#     "war_strength_brutality.txt",
#     "words_to_describe_female_beauty.txt",
#     "words_to_describe_male_handsomeness.txt",
#     "world_leaders.txt",
# ]

text_files_list = [
    "famous_cartoon_characters.txt",
    "famous_animes.txt",
    "famous_anime_characters.txt",
    "famous_scientists.txt",
    "famous_superheroes.txt",
]
for text_file in text_files_list:
    search_words_list = read_file_to_list(f"Resources/WordsData/{text_file}")
    database_actions = Database_Actions("sqlite:///DataBase/database.db")
    for search_word in search_words_list:
        existance_flag = database_actions.check_if_value_exists(
            AI_Generated_Images_Search_Words, keyword=search_word
        )
        if existance_flag:
            print("=======================================")
            print(f"==== {search_word} already exists ====")
            print("=======================================")
            continue
        database_actions.add(AI_Generated_Images_Search_Words(keyword=search_word))
        print(f"{search_word} successfully added to database.")
