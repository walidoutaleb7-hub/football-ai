import json
import requests
import os

API_KEY = os.environ.get('API_KEY', '')

# ============================================================
#  تصنيف اللاعبين حسب "الشهرة" (صعوبة التخمين)
# ============================================================

# 🟢 سهل: نجوم خارقون يعرفهم الجميع
EASY_PLAYERS = [
    "كريستيانو رونالدو", "ليونيل ميسي", "كيليان مبابي", "إيرلينغ هالاند",
    "نيمار", "محمد صلاح", "كيليان مبابي", "فينيسيوس جونيور",
    "جود بيلينغهام", "لامين يامال", "روبرت ليفاندوفسكي",
    "كيفن دي بروين", "لوكا مودريتش", "تيبو كورتوا"
]

# 🔵 متوسط: نجوم معروفون لدى متابعي كرة القدم
MEDIUM_PLAYERS = [
    "برناردو سيلفا", "رافائيل لياو", "مارتن أوديغارد", "ديكلان رايس",
    "بوكايو ساكا", "فيل فودين", "لاوتارو مارتينيز", "رودري",
    "أليكسيس ماك أليستر", "ماتيو كوفاسيتش", "دومينيك سوبوسلاي",
    "ويليام ساليبا", "رونالد أراوخو", "جيريمي فريمبونغ",
    "أندريه أونانا", "نيكولو باريلا", "فيدي فالفيردي",
    "جمال موسيالا", "فلوريان فيرتز", "مسعود أوزيل"
]

# 🟠 صعب: لاعبون أقل شهرة (قد يعرفهم فقط متابعو دوري معين)
HARD_PLAYERS = [
    "إبراهيما كوناتي", "فيديريكو ديماركو", "ماركوس تورام",
    "ميكي فان دي فين", "ديني زكريا", "راسموس هويلوند",
    "إدريسا غي", "جوناثان ديفيد", "لويس أوبيندا",
    "جيريمي دوكو", "دونييل مالين", "نونو تافاريس",
    "رينان لودي", "إدواردو كامافينغا"  # (رغم شهرته، لكنه لا يزال غير معروف للجميع)
]

# 🔴 أسطوري: أساطير اعتزلوا
LEGEND_PLAYERS = [
    "زين الدين زيدان", "رونالدينيو", "رونالدو نازاريو", "ريفالدو",
    "كاكا", "أندريا بيرلو", "تشافي", "أندريس إنييستا",
    "فرانك لامبارد", "ستيفن جيرارد", "تييري هنري", "رونالد كومان",
    "باولو مالديني", "فرانكو باريزي", "لوتار ماتيوس"
]

# ============================================================
#  تحميل اللاعبين من جميع الدوريات
# ============================================================

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
all_players = []
seen_names = set()

print('🔄 جاري تحميل اللاعبين من جميع الدوريات...')

for league in LEAGUES:
    print(f'  📥 تحميل من {league["name"]}...')
    try:
        url = f'https://v3.football.api-sports.io/players?league={league["id"]}&season={SEASON}'
        headers = {'x-apisports-key': API_KEY}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f'    ⚠️ فشل تحميل {league["name"]} (كود {response.status_code})')
            continue
            
        data = response.json()
        if not data.get('response'):
            print(f'    ⚠️ لا يوجد لاعبين في {league["name"]}')
            continue

        count = 0
        for p in data['response']:
            player = p.get('player', {})
            name = player.get('name')
            photo = player.get('photo')
            
            if not name or not photo:
                continue
            if name in seen_names:
                continue
                
            seen_names.add(name)
            
            # ============================================
            #  تصنيف الصعوبة حسب الشهرة (من القوائم أعلاه)
            # ============================================
            if name in LEGEND_PLAYERS:
                level = 'legend'
            elif name in EASY_PLAYERS:
                level = 'easy'
            elif name in MEDIUM_PLAYERS:
                level = 'medium'
            elif name in HARD_PLAYERS:
                level = 'hard'
            else:
                level = 'easy'  # افتراضي: إذا لم يكن في أي قائمة، نعتبره سهل (لكن يمكنك تعديل هذا)
            
            all_players.append({
                'id': player.get('id'),
                'name': name,
                'nationality': player.get('nationality', 'غير معروف'),
                'level': level,
                'image': photo
            })
            count += 1
        print(f'    ✅ تم إضافة {count} لاعب من {league["name"]}')
        
    except Exception as e:
        print(f'    ❌ خطأ في {league["name"]}: {e}')

# في حال فشل API بالكامل
if len(all_players) == 0:
    print('⚠️ فشل تحميل جميع الدوريات، استخدام بيانات احتياطية.')
    all_players = [
        {"id": 1, "name": "كريستيانو رونالدو", "nationality": "البرتغال", "level": "easy", "image": "https://media.api-sports.io/football/players/257.png"},
        {"id": 2, "name": "ليونيل ميسي", "nationality": "الأرجنتين", "level": "easy", "image": "https://media.api-sports.io/football/players/457.png"},
        {"id": 3, "name": "كيليان مبابي", "nationality": "فرنسا", "level": "easy", "image": "https://media.api-sports.io/football/players/1495.png"},
        {"id": 4, "name": "زين الدين زيدان", "nationality": "فرنسا", "level": "legend", "image": "https://media.api-sports.io/football/players/1000.png"},
        {"id": 5, "name": "بوكايو ساكا", "nationality": "إنجلترا", "level": "medium", "image": "https://media.api-sports.io/football/players/14947.png"},
        {"id": 6, "name": "نيكولو باريلا", "nationality": "إيطاليا", "level": "hard", "image": "https://media.api-sports.io/football/players/10035.png"},
    ]

# حفظ الملف
with open('popular_players.json', 'w', encoding='utf-8') as f:
    json.dump(all_players, f, ensure_ascii=False, indent=2)

print(f'✅ تم حفظ {len(all_players)} لاعباً بنجاح!')
print('🎉 التصنيف الآن حسب الشهرة: سهل (نجوم خارقون) ← متوسط (معروفون) ← صعب (أقل شهرة) ← أسطوري (معتزلون)!')