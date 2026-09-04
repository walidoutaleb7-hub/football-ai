import os
import json
import time
import random
import requests

API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    raise SystemExit("❌ API_KEY غير موجود")

HEADERS = {
    "x-apisports-key": API_KEY
}

LEAGUES = [
    39,   # Premier League
    140,  # La Liga
    135,  # Serie A
    78,   # Bundesliga
    61,   # Ligue 1
    94,   # Primeira Liga
    88,   # Eredivisie
    203   # Süper Lig
]

SEASON = 2024
MAX_PLAYERS = 3000

players = {}

session = requests.Session()
session.headers.update(HEADERS)


def get_page(league, page):

    url = "https://v3.football.api-sports.io/players"

    for attempt in range(3):

        try:
            response = session.get(
                url,
                params={
                    "league": league,
                    "season": SEASON,
                    "page": page
                },
                timeout=30
            )

        except requests.RequestException as error:

            print(f"⚠️ خطأ في الاتصال: {error}")

            time.sleep(5)

            continue

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:

            print("⚠️ تجاوز حد API — ننتظر 15 ثانية...")

            time.sleep(15)

            continue

        print(f"⚠️ HTTP {response.status_code}")

        return None

    print("⏭️ فشل تحميل الصفحة، سيتم تخطيها.")

    return None


def calculate_difficulty(player):

    name = (player.get("name") or "").lower()

    # نجوم معروفين جدًا
    legendary_players = [
        "lionel messi",
        "cristiano ronaldo",
        "kylian mbappe",
        "erling haaland",
        "neymar",
        "mohamed salah",
        "kevin de bruyne",
        "vinicius junior",
        "robert lewandowski",
        "karim benzema",
        "luka modric",
        "toni kroos",
        "sergio ramos",
        "manuel neuer",
        "thibaut courtois"
    ]

    for legendary in legendary_players:
        if legendary in name:
            return "easy"

    # اللاعبين المعروفين
    famous_players = [
        "bruno fernandes",
        "bernardo silva",
        "rodri",
        "bukayo saka",
        "phil foden",
        "jude bellingham",
        "pedri",
        "gavi",
        "lamine yamal",
        "antoine griezmann",
        "lautaro martinez",
        "rafael leao",
        "son heung-min",
        "virgil van dijk",
        "alisson"
    ]

    for famous in famous_players:
        if famous in name:
            return "medium"

    # البقية أصعب
    return "hard"


# ==========================================
# جلب اللاعبين
# ==========================================

for league in LEAGUES:

    print()
    print("================================")
    print(f"🏆 الدوري رقم: {league}")
    print("================================")

    first_page = get_page(league, 1)

    if not first_page:

        print("⏭️ تخطي الدوري")

        continue

    paging = first_page.get("paging", {})

    total_pages = paging.get("total", 1)

    print(f"📄 إجمالي الصفحات: {total_pages}")

    pages_to_get = min(total_pages, 10)

    for page in range(1, pages_to_get + 1):

        if page == 1:
            data = first_page

        else:
            data = get_page(
                league,
                page
            )

        if not data:
            break

        response_players = data.get(
            "response",
            []
        )

        for item in response_players:

            player = item.get(
                "player",
                {}
            )

            name = player.get("name")

            image = player.get("photo")

            if not name or not image:
                continue

            birth = player.get(
                "birth",
                {}
            )

            players[name] = {

                "id": player.get("id"),

                "name": name,

                "image": image,

                "nationality": player.get(
                    "nationality",
                    "Unknown"
                ),

                "position": (
                    item.get("statistics", [{}])[0]
                    .get("games", {})
                    .get("position", "Unknown")
                ),

                "birth": birth.get(
                    "date",
                    "Unknown"
                ),

                "age": birth.get(
                    "age",
                    None
                ),

                "difficulty": calculate_difficulty(
                    player
                )
            }

            statistics = item.get(
                "statistics",
                []
            )

            if statistics:

                first_stats = statistics[0]

                team = first_stats.get(
                    "team",
                    {}
                )

                players[name]["club"] = team.get(
                    "name",
                    "Unknown"
                )

        print(
            f"📄 صفحة {page}/{pages_to_get}"
            f" | 👤 اللاعبين: {len(players)}"
        )

        if len(players) >= MAX_PLAYERS:
            break

        time.sleep(2)

    if len(players) >= MAX_PLAYERS:
        break


# ==========================================
# تحويل إلى قائمة
# ==========================================

players = list(
    players.values()
)

random.shuffle(
    players
)

players = players[
    :MAX_PLAYERS
]


# ==========================================
# حفظ JSON
# ==========================================

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


# ==========================================
# النتيجة
# ==========================================

print()
print("====================================")
print("🎉 انتهى إنشاء قاعدة اللاعبين")
print(f"👤 عدد اللاعبين: {len(players)}")
print("📁 الملف: popular_players.json")
print("====================================")

if len(players) < MAX_PLAYERS:

    print(
        f"⚠️ تم الحصول على {len(players)} فقط."
    )

else:

    print(
        "🔥 تم الوصول إلى 3000 لاعب!"
    )