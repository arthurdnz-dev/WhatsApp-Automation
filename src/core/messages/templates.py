# src/core/messages/templates.py
import json
import os

PATH = "data/templates.json"

def load_templates():
    if not os.path.exists(PATH):
        return {}
    with open(PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_templates(templates):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(templates, f, indent=4, ensure_ascii=False)
