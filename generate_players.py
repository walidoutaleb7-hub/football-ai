import os
import json
import requests

API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    raise SystemExit("❌ API_KEY غير موجود")

HEADERS = {
    "x-apisports-key": API_KEY
}

# دوريات مشهورة
LEAGUES = [
    39,   # Premier League
    140,  # La Liga
    135,  # Serie A
    78,   # Bundesliga
    61,   # Ligue 1
    2,    # Champions League
    3,    # Europa League
    94,   # Primeira Liga
    88,   # Eredivisie
    203,  # Süper Lig
]

SEASON = 2024
players = {}

for league in LEAGUES:

    print(f"جلب الدوري: {league}")

    page = 1

    while True:

        response = requests.get(
            "https://v3.football.api-sports.io/players",
            headers=HEADERS,
            params={
                "league": league,
                "season": SEASON,
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
                players[name] = {
                    "name": name,
                    "image": image
                }

        paging = data.get("paging", {})

        current = paging.get("current", page)
        total = paging.get("total", page)

        print(f"  صفحة {current}/{total}")

        if page >= total:
            break

        page += 1


# تحويل إلى قائمة
players = list(players.values())

# خلط اللاعبين
import random
random.shuffle(players)

# نأخذ أول 3000 فقط
players = players[:3000]

with open(
    "popular_players.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        players,
        file,
        ensure_ascii=False,
        indent=2
    )

print()
print("================================")
print(f"✅ عدد اللاعبين: {len(players)}")
print("✅ تم إنشاء popular_players.json")
print("================================")