import requests
import json

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
        with open("all_cards.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Saved successfully.")
    except Exception as e:
        print(f"Failed to parse or save: {e}")

fetch_all_lorcana_cards()
