import json
import os
import time
import requests

API_KEY = os.environ.get("API_KEY", "").strip()
SEASON = int(os.environ.get("SEASON", "2026"))
TARGET_PLAYERS = 1000

BASE_URL = "https://v3.football.api-sports.io/players"

if not API_KEY:
    raise RuntimeError("❌ API_KEY غير موجود في GitHub Secrets")

HEADERS = {
    "x-apisports-key": API_KEY
}

# الدوريات
LEAGUES = [
    {"id": 39, "name": "الدوري الإنجليزي"},
    {"id": 140, "name": "الدوري الإسباني"},
    {"id": 135, "name": "الدوري الإيطالي"},
    {"id": 78, "name": "الدوري الألماني"},
    {"id": 61, "name": "الدوري الفرنسي"},
    {"id": 307, "name": "الدوري السعودي"},
    {"id": 253, "name": "الدوري الأمريكي"},
]

# تصنيف اللاعبين المعروفين
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
    "Thibaut Courtois",
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
    "Florian Wirtz",
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
    "Eduardo Camavinga",
}


def get_level(name):
    if name in EASY_PLAYERS:
        return "easy"

    if name in MEDIUM_PLAYERS:
        return "medium"

    if name in HARD_PLAYERS:
        return "hard"

    return "hard"


def request_players(league_id, season, page):
    """
    إرسال طلب واحد إلى API-Football.
    """

    params = {
        "league": league_id,
        "season": season,
        "page": page,
    }

    try:
        response = requests.get(
            BASE_URL,
            headers=HEADERS,
            params=params,
            timeout=30,
        )

    except requests.RequestException as error:
        print(f"   ❌ خطأ في الاتصال: {error}")
        return None

    print(
        f"   📄 الموسم {season} | الصفحة {page} "
        f"| HTTP {response.status_code}"
    )

    # أخطاء HTTP
    if response.status_code != 200:

        if response.status_code == 401:
            print("   🔑 API Key غير صحيحة أو غير صالحة")

        elif response.status_code == 403:
            print("   🚫 الطلب مرفوض: تحقق من صلاحيات API أو الخطة")

        elif response.status_code == 429:
            print("   ⛔ تم تجاوز حد الطلبات API")

        else:
            print(
                f"   ❌ HTTP Error: {response.status_code}"
            )

        # نحاول طباعة رسالة API بدون كشف المفتاح
        try:
            error_data = response.json()

            if error_data.get("errors"):
                print(
                    f"   API Error: {error_data['errors']}"
                )

        except Exception:
            pass

        return None

    try:
        data = response.json()

    except ValueError:
        print("   ❌ API رجعت بيانات غير صالحة")
        return None

    # أخطاء API الداخلية
    if data.get("errors"):

        print(
            f"   ❌ API Error: {data['errors']}"
        )

        return None

    return data


def load_league(league_id, league_name, season, all_players, seen_ids):
    """
    تحميل لاعبين من دوري واحد.
    """

    print()
    print("=" * 55)
    print(f"📥 تحميل {league_name}")
    print(f"📅 الموسم: {season}")
    print("=" * 55)

    page = 1
    total_added = 0

    while len(all_players) < TARGET_PLAYERS:

        data = request_players(
            league_id,
            season,
            page,
        )

        if data is None:
            break

        results = data.get("response", [])

        if not results:

            if page == 1:
                print(
                    "   ⚠️ API لم ترجع أي لاعب لهذا الدوري/الموسم"
                )
            else:
                print("   🏁 لا توجد نتائج إضافية")

            break

        added = 0

        for item in results:

            player = item.get("player", {})

            player_id = player.get("id")
            name = player.get("name")
            nationality = player.get(
                "nationality",
                "غير معروف",
            )
            photo = player.get("photo")

            if not player_id:
                continue

            if not name:
                continue

            if not photo:
                continue

            if player_id in seen_ids:
                continue

            seen_ids.add(player_id)

            all_players.append({
                "id": player_id,
                "name": name,
                "nationality": nationality,
                "level": get_level(name),
                "image": photo,
            })

            added += 1
            total_added += 1

            if len(all_players) >= TARGET_PLAYERS:
                break

        print(
            f"   ✅ أضيف في الصفحة: {added} "
            f"| المجموع: {len(all_players)}"
        )

        paging = data.get("paging", {})

        current_page = paging.get(
            "current",
            page,
        )

        total_pages = paging.get(
            "total",
            page,
        )

        if current_page >= total_pages:
            print("   🏁 انتهت صفحات هذا الدوري")
            break

        page += 1

        # تخفيف الضغط على API
        time.sleep(0.2)

    return total_added


print()
print("🚀 بدء تحميل اللاعبين...")
print(f"📅 الموسم الأساسي: {SEASON}")
print(f"🎯 الهدف: {TARGET_PLAYERS} لاعب")
print()

all_players = []
seen_ids = set()

# الموسم الأساسي
for league in LEAGUES:

    if len(all_players) >= TARGET_PLAYERS:
        break

    load_league(
        league["id"],
        league["name"],
        SEASON,
        all_players,
        seen_ids,
    )


# إذا لم نجد لاعبين في الموسم الأساسي،
# نجرب الموسم السابق.
if len(all_players) == 0:

    FALLBACK_SEASON = SEASON - 1

    print()
    print("=" * 55)
    print(
        f"⚠️ لم نجد أي لاعب في الموسم {SEASON}"
    )
    print(
        f"🔄 تجربة الموسم الاحتياطي {FALLBACK_SEASON}"
    )
    print("=" * 55)

    for league in LEAGUES:

        if len(all_players) >= TARGET_PLAYERS:
            break

        load_league(
            league["id"],
            league["name"],
            FALLBACK_SEASON,
            all_players,
            seen_ids,
        )


# الحد الأقصى
all_players = all_players[:TARGET_PLAYERS]


print()
print("=" * 55)
print("📊 النتيجة النهائية")
print("=" * 55)
print(
    f"👥 عدد اللاعبين: {len(all_players)}"
)


# إذا بقي الملف فارغًا، نوقف الـWorkflow
# بدل إنشاء APK بقاعدة بيانات فارغة.
if len(all_players) == 0:

    raise RuntimeError(
        "❌ لم يتم الحصول على أي لاعب من API-Football. "
        "تحقق من API_KEY أو الموسم أو صلاحية API."
    )


# الإحصائيات
levels = {
    "easy": 0,
    "medium": 0,
    "hard": 0,
}

for player in all_players:

    level = player.get("level")

    if level in levels:
        levels[level] += 1


print()
print("📈 مستويات اللاعبين:")
print(f"🟢 سهل: {levels['easy']}")
print(f"🔵 متوسط: {levels['medium']}")
print(f"🟠 صعب: {levels['hard']}")


# حفظ JSON
output_path = "popular_players.json"

with open(
    output_path,
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        all_players,
        file,
        ensure_ascii=False,
        indent=2,
    )


print()
print("=" * 55)
print("🎉 تم إنشاء قاعدة اللاعبين بنجاح!")
print(f"📁 الملف: {output_path}")
print(f"👥 اللاعبين: {len(all_players)}")
print("=" * 55)