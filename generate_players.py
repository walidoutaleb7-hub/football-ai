import os
import json
import requests

API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    raise SystemExit("❌ API_KEY غير موجود")

url = "https://v3.football.api-sports.io/players"

headers = {
    "x-apisports-key": API_KEY
}

players = []

for page in range(1, 31):
    print(f"جلب الصفحة {page}/30...")

    response = requests.get(
        url,
        headers=headers,
        params={
            "league": 39,
            "season": 2024,
            "page": page
        },
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    for item in data.get("response", []):
        player = item.get("player", {})

        name = player.get("name")
        image = player.get("photo")

        if name and image:
            players.append({
                "name": name,
                "image": image
            })

    if not data.get("response"):
        break


# إزالة اللاعبين المكررين
unique = {}

for player in players:
    unique[player["name"]] = player

players = list(unique.values())[:3000]

with open("popular_players.json", "w", encoding="utf-8") as file:
    json.dump(players, file, ensure_ascii=False, indent=2)

print(f"\n✅ تم إنشاء {len(players)} لاعب")