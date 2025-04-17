from fastapi import FastAPI, Request, UploadFile, Form, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil, os, json
from pathlib import Path
import requests
import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
DATA_FILE = "collection.json"
WISHLIST_FILE = "wishlist.json"
ALL_CARDS_FILE = "all_cards.json"
META_DECKS_DIR = "meta"

Path(UPLOAD_DIR).mkdir(exist_ok=True)
Path(META_DECKS_DIR).mkdir(exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

def fetch_meta_decks():
    print("Fetching meta decks...")
    sample_decks = [
        {
            "name": "Sapphire/Steel Control",
            "source": "sample",
            "cards": [
                {"name": "Belle - Strange But Special", "count": 4},
                {"name": "Ariel - Spectacular Singer", "count": 3}
            ],
            "last_fetched": str(datetime.date.today())
        },
        {
            "name": "Ruby/Amethyst Aggro",
            "source": "sample",
            "cards": [
                {"name": "Mickey Mouse - Brave Little Tailor", "count": 4},
                {"name": "Dr. Facilier - Agent Provocateur", "count": 3}
            ],
            "last_fetched": str(datetime.date.today())
        }
    ]
    for deck in sample_decks:
        safe_name = deck["name"].replace(" ", "_").lower()
        with open(f"{META_DECKS_DIR}/{safe_name}.json", "w") as f:
            json.dump(deck, f, indent=2)
    print("Meta decks saved.")

@app.get("/meta", response_class=HTMLResponse)
def view_meta_decks(request: Request):
    meta_path = Path(META_DECKS_DIR)
    deck_files = list(meta_path.glob("*.json"))
    decks = []
    for fpath in deck_files:
        with open(fpath, "r") as f:
            data = json.load(f)
            data["filename"] = fpath.name
            decks.append(data)
    return templates.TemplateResponse("meta.html", {"request": request, "decks": decks})

@app.post("/meta/copy_to_workshop")
async def copy_meta_to_workshop(request: Request):
    form = await request.form()
    deck_file = form.get("deck_file")
    meta_path = Path(f"{META_DECKS_DIR}/{deck_file}")
    if not meta_path.exists():
        return HTMLResponse("Meta deck not found", status_code=404)

    with open(meta_path, "r") as f:
        deck = json.load(f)

    safe_name = deck["name"].replace(" ", "_").lower()
    output_path = Path(f"decks/{safe_name}.json")
    with open(output_path, "w") as f:
        json.dump(deck, f, indent=2)

    return RedirectResponse(url="/workshop", status_code=302)

@app.get("/meta/fetch", response_class=HTMLResponse)
def manual_meta_fetch(request: Request):
    fetch_meta_decks()
    return RedirectResponse(url="/meta", status_code=302)

def auto_fetch_if_due():
    last_fetch_file = Path(f"{META_DECKS_DIR}/last_fetch.txt")
    today = datetime.date.today()

    if last_fetch_file.exists():
        with open(last_fetch_file, "r") as f:
            last_date = datetime.datetime.strptime(f.read().strip(), "%Y-%m-%d").date()
            # Only auto-fetch if it hasn't run this month and today is the 15th
            if last_date.month == today.month and last_date.year == today.year:
                return

    if today.day == 15:
        print("Auto-fetching meta decks...")
        fetch_meta_decks()
        with open(last_fetch_file, "w") as f:
            f.write(str(today))
