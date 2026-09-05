import json
import requests
import os
import time

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
# تصنيف اللاعبين
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
# أساطير - بيانات ثابتة
# لأنهم معتزلون ولن يظهروا في موسم 2026
# ============================================================

LEGENDS = [
    {
        "id": 900001,
        "name": "زين الدين زيدان",
        "nationality": "فرنسا",
        "level": "legend",
        "image": "https://media.api-sports.io/football/players/865.png"
    },
    {
        "id": 900002,
        "name": "رونالدينيو",
        "nationality": "البرازيل",
        "level": "legend",
        "image": "https://media.api-sports.io/football/players/276.png"
    },
    {
        "id": 900003,
        "name": "رونالدو نازاريو",
        "nationality": "البرازيل",
        "level": "legend",
        "image": "https://media.api-sports.io/football/players/308.png"
    },
    {
        "id": 900004,
        "name": "كاكا",
        "nationality": "البرازيل",
        "level": "legend",
        "image": "https://media.api-sports.io/football/players/220.png"
    },
    {
        "id": 900005,
        "name": "أندريا بيرلو",
        "nationality": "إيطاليا",
        "level": "legend",
        "image": "https://media.api-sports.io/football/players/290.png"
    },
    {
        "id": 900006,
        "name": "تشافي",
        "nationality": "إسبانيا",
        "level": "legend",
        "image": "https://media.api-sports.io/football/players/172.png"
    },
    {
        "id": 900007,
        "name": "أندريس إنييستا",
        "nationality": "إسبانيا",
        "level": "legend",
        "image": "https://media.api-sports.io/football/players/153.png"
    },
    {
        "id": 900008,
        "name": "فرانك لامبارد",
        "nationality": "إنجلترا",
        "level": "legend",
        "image": "https://media.api-sports.io/football/players/250.png"
    },
    {
        "id": 900009,
        "name": "ستيفن جيرارد",
        "nationality": "إنجلترا",
        "level": "legend",
        "image": "https://media.api-sports.io/football/players/338.png"
    }
]

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
    {"id": 253, "الدوري الأمريكي"},
]

# ============================================================
# دالة تحديد المستوى
# ============================================================

def get_level(name):
    if name in EASY_PLAYERS:
        return "easy"

    if name in MEDIUM_PLAYERS:
        return "medium"

    if name in HARD_PLAYERS:
        return "hard"

    return "hard"


# ============================================================
# تحميل اللاعبين
# ============================================================

all_players = []
seen_ids = set()

print("🚀 بدء تحميل اللاعبين...")
print(f"📅 الموسم: {SEASON}")
print(f"🎯 الهدف: {TARGET_PLAYERS} لاعب")

# إضافة الأساطير أولاً
for legend in LEGENDS:
    if legend["id"] not in seen_ids:
        all_players.append(legend)
        seen_ids.add(legend["id"])

print(f"🏆 تمت إضافة {len(LEGENDS)} أساطير")


# ============================================================
# جلب اللاعبين من API-Football
# ============================================================

for league in LEAGUES:

    if len(all_players) >= TARGET_PLAYERS:
        break

    league_id = league["id"]
    league_name = league["name"]

    print()
    print(f"📥 {league_name}")

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
                f"   صفحة {page} | HTTP {response.status_code}"
            )

            if response.status_code != 200:
                print(
                    f"   ⚠️ فشل الطلب في {league_name}"
                )
                break

            data = response.json()

            # ------------------------------------------------
            # التحقق من API
            # ------------------------------------------------

            if data.get("errors"):
                print(
                    f"   ❌ API Error: {data['errors']}"
                )
                break

            players = data.get("response", [])

            if not players:
                print("   ℹ️ لا توجد نتائج إضافية.")
                break

            added_this_page = 0

            # ------------------------------------------------
            # معالجة اللاعبين
            # ------------------------------------------------

            for item in players:

                player = item.get("player", {})

                player_id = player.get("id")
                name = player.get("name")
                nationality = player.get(
                    "nationality",
                    "غير معروف"
                )
                photo = player.get("photo")

                if not player_id:
                    continue

                if not name:
                    continue

                if not photo:
                    continue

                # منع التكرار
                if player_id in seen_ids:
                    continue

                seen_ids.add(player_id)

                level = get_level(name)

                all_players.append({
                    "id": player_id,
                    "name": name,
                    "nationality": nationality,
                    "level": level,
                    "image": photo
                })

                added_this_page += 1

                if len(all_players) >= TARGET_PLAYERS:
                    break

            print(
                f"   ✅ أضيف: {added_this_page} "
                f"| المجموع: {len(all_players)}"
            )

            # ------------------------------------------------
            # معرفة آخر صفحة
            # ------------------------------------------------

            paging = data.get("paging", {})

            current_page = paging.get("current", page)
            total_pages = paging.get("total", page)

            if current_page >= total_pages:
                print("   🏁 انتهت صفحات هذا الدوري.")
                break

            page += 1

            # انتظار صغير لتجنب الضغط على API
            time.sleep(0.2)

        except requests.RequestException as e:

            print(
                f"   ❌ خطأ في الاتصال: {e}"
            )
            break

        except Exception as e:

            print(
                f"   ❌ خطأ غير متوقع: {e}"
            )
            break


# ============================================================
# التأكد من العدد
# ============================================================

print()
print("=" * 55)
print(f"📊 عدد اللاعبين النهائي: {len(all_players)}")
print("=" * 55)

if len(all_players) < TARGET_PLAYERS:
    print(
        f"⚠️ تم الحصول على {len(all_players)} فقط "
        f"بدل {TARGET_PLAYERS}."
    )
else:
    all_players = all_players[:TARGET_PLAYERS]
    print(f"🎯 تم الوصول إلى {TARGET_PLAYERS} لاعب!")


# ============================================================
# إعادة ترتيب IDs
# ============================================================

for index, player in enumerate(all_players, 1):
    player["id"] = index


# ============================================================
# حفظ JSON
# ============================================================

with open(
    "popular_players.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_players,
        f,
        ensure_ascii=False,
        indent=2
    )


# ============================================================
# إحصائيات
# ============================================================

levels = {
    "easy": 0,
    "medium": 0,
    "hard": 0,
    "legend": 0
}

for player in all_players:
    level = player.get("level")

    if level in levels:
        levels[level] += 1


print()
print("🎉 تم إنشاء popular_players.json")
print(f"👥 اللاعبين: {len(all_players)}")
print(f"🟢 سهل: {levels['easy']}")
print(f"🔵 متوسط: {levels['medium']}")
print(f"🟠 صعب: {levels['hard']}")
print(f"🔴 أسطوري: {levels['legend']}")
print()
print("✅ انتهى التوليد بنجاح!")