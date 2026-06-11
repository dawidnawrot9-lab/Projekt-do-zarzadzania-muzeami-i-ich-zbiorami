import json
import os

DATA_FILE = "data.json"

def init_data_file():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "muzea": [],
            "magazyny": [],
            "pracownicy": []
        }
        save_data(default_data)

def load_data() -> dict:
    init_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)