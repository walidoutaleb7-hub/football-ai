import json
import os
import time
import requests

# ============================================================
# الإعدادات
# ============================================================

API_KEY = os.environ.get("API_KEY", "")
SEASON = int(os.environ.get("SEASON", "2026"))
TARGET_PLAYERS = 1000

BASE_URL = "https://v3.football.api-sports.io/players"

if not API_KEY:
    raise RuntimeError("❌ API_KEY غير موجود في GitHub Secrets")

HEADERS = {
    "x-apisports-key": API_KEY
}

# ============================================================
# مستويات اللاعبين المشهورين
# ============================================================

EASY_PLAYERS = {
    "Cristiano Ronaldo",
    "Lionel Messi",
    "Kylian Mbappé",
    "Erling Haaland",
    "Neymar",
    "Mohamed Salah",
    "Vinicius Junior",
    "Jude Bellingham",
    "Lamine Yamal",
    "Robert Lewandowski",
    "Kevin De Bruyne",
    "Luka Modric",
    "Thibaut Courtois"
}

MEDIUM_PLAYERS = {
    "Bernardo Silva",
    "Rafael Leão",
    "Martin Ødegaard",
    "Declan Rice",
    "Bukayo Saka",
    "Phil Foden",
    "Lautaro Martinez",
    "Rodri",
    "Alexis Mac Allister",
    "Mateo Kovacic",
    "Dominik Szoboszlai",
    "William Saliba",
    "Ronald Araujo",
    "Jeremie Frimpong",
    "André Onana",
    "Nicolò Barella",
    "Federico Valverde",
    "Jamal Musiala",
    "Florian Wirtz"
}

HARD_PLAYERS = {
    "Ibrahima Konaté",
    "Federico Dimarco",
    "Marcus Thuram",
    "Micky van de Ven",
    "Denis Zakaria",
    "Rasmus Højlund",
    "Idrissa Gueye",
    "Jonathan David",
    "Loïs Openda",
    "Jérémy Doku",
    "Donyell Malen",
    "Nuno Tavares",
    "Renan Lodi",
    "Eduardo Camavinga"
}

# ============================================================
# الدوريات
# ============================================================

LEAGUES = [
    {"id": 39, "name": "الدوري الإنجليزي"},
    {"id": 140, "name": "الدوري الإسباني"},
    {"id": 135, "name": "الدوري الإيطالي"},
    {"id": 78, "name": "الدوري الألماني"},
    {"id": 61, "name": "الدوري الفرنسي"},
    {"id": 307, "name": "الدوري السعودي"},
    {"id": 253, "name": "الدوري الأمريكي"}
]

# ============================================================
# تحديد مستوى اللاعب
# ============================================================

def get_level(name):

    if name in EASY_PLAYERS:
        return "easy"

    if name in MEDIUM_PLAYERS:
        return "medium"

    if name in HARD_PLAYERS:
        return "hard"

    # اللاعب غير الموجود في القوائم
    # يعتبر صعب حتى لا تصبح اللعبة سهلة
    return "hard"


# ============================================================
# تحميل اللاعبين
# ============================================================

all_players = []
seen_ids = set()

print("🚀 بدء تحميل اللاعبين...")
print(f"📅 الموسم: {SEASON}")
print(f"🎯 الهدف: {TARGET_PLAYERS} لاعب")

for league in LEAGUES:

    if len(all_players) >= TARGET_PLAYERS:
        break

    league_id = league["id"]
    league_name = league["name"]

    print()
    print(f"📥 تحميل {league_name}")

    page = 1

    while len(all_players) < TARGET_PLAYERS:

        try:

            params = {
                "league": league_id,
                "season": SEASON,
                "page": page
            }

            response = requests.get(
                BASE_URL,
                headers=HEADERS,
                params=params,
                timeout=30
            )

            print(
                f"   📄 صفحة {page} | HTTP {response.status_code}"
            )

            if response.status_code != 200:
                print("   ❌ فشل الطلب")
                break

            data = response.json()

            if data.get("errors"):
                print(f"   ❌ API Error: {data['errors']}")
                break

            results = data.get("response", [])

            if not results:
                print("   🏁 لا توجد نتائج إضافية")
                break

            added = 0

            for item in results:

                player = item.get("player", {})

                player_id = player.get("id")
                name = player.get("name")
                nationality = player.get(
                    "nationality",
                    "غير معروف"
                )
                photo = player.get("photo")

                if not player_id or not name or not photo:
                    continue

                if player_id in seen_ids:
                    continue

                seen_ids.add(player_id)

                all_players.append({
                    "id": player_id,
                    "name": name,
                    "nationality": nationality,
                    "level": get_level(name),
                    "image": photo
                })

                added += 1

                if len(all_players) >= TARGET_PLAYERS:
                    break

            print(
                f"   ✅ أضيف {added} | المجموع {len(all_players)}"
            )

            # آخر صفحة
            paging = data.get("paging", {})

            current = paging.get("current", page)
            total = paging.get("total", page)

            if current >= total:
                print("   🏁 انتهى الدوري")
                break

            page += 1

            # توقف بسيط بين الطلبات
            time.sleep(0.15)

        except requests.RequestException as error:

            print(f"   ❌ خطأ اتصال: {error}")
            break

        except Exception as error:

            print(f"   ❌ خطأ: {error}")
            break


# ============================================================
# النتيجة
# ============================================================

all_players = all_players[:TARGET_PLAYERS]

print()
print("=" * 50)
print(f"👥 عدد اللاعبين: {len(all_players)}")
print("=" * 50)

if len(all_players) < TARGET_PLAYERS:
    print(
        f"⚠️ لم يتم الوصول إلى {TARGET_PLAYERS} لاعب"
    )

# ============================================================
# الإحصائيات
# ============================================================

levels = {
    "easy": 0,
    "medium": 0,
    "hard": 0
}

for player in all_players:

    level = player["level"]

    if level in levels:
        levels[level] += 1

print(f"🟢 سهل: {levels['easy']}")
print(f"🔵 متوسط: {levels['medium']}")
print(f"🟠 صعب: {levels['hard']}")

# ============================================================
# حفظ قاعدة البيانات
# ============================================================

with open(
    "popular_players.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        all_players,
        file,
        ensure_ascii=False,
        indent=2
    )

print()
print("🎉 تم إنشاء popular_players.json بنجاح!")