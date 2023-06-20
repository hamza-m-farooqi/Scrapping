import re
import os
import json
from datetime import datetime

def get_image_id_from_string(image_link):
    pattern=r"\d+$"
    image_id=""
    match=re.search(pattern=pattern,string=image_link)
    if match:
        image_id=match.group()
        print(image_id)
    return image_id

def update_scrapped_data_in_json_file(data,file_name):
    with open(file_name,'w') as f:
        json.dump(data,f,indent=4)