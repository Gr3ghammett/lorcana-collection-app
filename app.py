from fastapi import FastAPI, Request, UploadFile, Form, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil, os, json
from pathlib import Path
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
DATA_FILE = "collection.json"
WISHLIST_FILE = "wishlist.json"
ALL_CARDS_FILE = "all_cards.json"

Path(UPLOAD_DIR).mkdir(exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

def load_collection():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_to_collection(collection):
    with open(DATA_FILE, "w") as f:
        json.dump(collection, f, indent=2)

def fetch_all_lorcana_cards():
    print("Fetching full Lorcana card catalog...")
    url = "https://api.lorcana-api.com/cards/all"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    try:
        data = response.json()
        print(f"Fetched {len(data)} cards.")
        with open(ALL_CARDS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Saved successfully.")
    except Exception as e:
        print(f"Failed to parse or save: {e}")

# Fetch on startup
fetch_all_lorcana_cards()
