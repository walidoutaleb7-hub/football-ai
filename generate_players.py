import json
import random
import os
import requests

API_KEY = os.environ.get('API_KEY', '')

# قائمة الدوريات (إنجلترا، إسبانيا، إيطاليا، ألمانيا، فرنسا، السعودية، أمريكا)
LEAGUES = [
    {'id': 39, 'name': 'الدوري الإنجليزي'},
    {'id': 140, 'name': 'الدوري الإسباني'},
    {'id': 135, 'name': 'الدوري الإيطالي'},
    {'id': 78, 'name': 'الدوري الألماني'},
    {'id': 61, 'name': 'الدوري الفرنسي'},
    {'id': 307, 'name': 'الدوري السعودي'},
    {'id': 253, 'name': 'الدوري الأمريكي'},
]

SEASON = 2024

# قوائم التصنيف حسب الشهرة (وليس المهارة)
EASY = [
    "كريستيانو رونالدو", "ليونيل ميسي", "كيليان مبابي", "إيرلينغ هالاند",
    "نيمار", "محمد صلاح", "فينيسيوس جونيور", "جود بيلينغهام",
    "روبرت ليفاندوفسكي", "كيفن دي بروين", "لوكا مودريتش"
]

MEDIUM = [
    "بوكايو ساكا", "فيل فودين", "مارتن أوديغارد", "ديكلان رايس",
    "رودري", "لاوتارو مارتينيز", "نيكولو باريلا", "فيدي فالفيردي",
    "جمال موسيالا", "فلوريان فيرتز"
]

HARD = [
    "دومينيك سوبوسلاي", "ويليام ساليبا", "إبراهيما كوناتي",
    "رونالد أراوخو", "جيريمي فريمبونغ", "أندريه أونانا",
    "فيديريكو ديماركو", "ماتيو كوفاسيتش", "أليكسيس ماك أليستر"
]

LEGEND = [
    "زين الدين زيدان", "رونالدينيو", "رونالدو نازاريو", "ريفالدو",
    "كاكا", "أندريا بيرلو", "تشافي", "أندريس إنييستا",
    "فرانك لامبارد", "ستيفن جيرارد", "تييري هنري"
]

all_players = []
seen = set()

print('🔄 جاري تحميل اللاعبين من جميع الدوريات...')

for league in LEAGUES:
    try:
        url = f'https://v3.football.api-sports.io/players?league={league["id"]}&season={SEASON}'
        headers = {'x-apisports-key': API_KEY}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            print(f'⚠️ فشل تحميل {league["name"]}')
            continue
        data = r.json()
        for p in data.get('response', []):
            player = p.get('player', {})
            name = player.get('name')
            photo = player.get('photo')
            if not name or not photo or name in seen:
                continue
            seen.add(name)

            # تصنيف الصعوبة
            level = 'easy'
            if name in LEGEND: level = 'legend'
            elif name in HARD: level = 'hard'
            elif name in MEDIUM: level = 'medium'
            elif name in EASY: level = 'easy'

            all_players.append({
                'id': player.get('id'),
                'name': name,
                'nationality': player.get('nationality', 'غير معروف'),
                'level': level,
                'image': photo
            })
        print(f'✅ {league["name"]}: تم إضافة {len(all_players)} لاعب')
    except Exception as e:
        print(f'❌ خطأ في {league["name"]}: {e}')

# خلط اللاعبين
random.shuffle(all_players)

# حفظ الملف
with open('popular_players.json', 'w', encoding='utf-8') as f:
    json.dump(all_players, f, ensure_ascii=False, indent=2)

print(f'✅ تم حفظ {len(all_players)} لاعباً بنجاح!')