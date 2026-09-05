import json
import requests
import os

API_KEY = os.environ.get('API_KEY', '')

# قائمة بأشهر الدوريات حول العالم (ID الخاص بكل دوري في API-Football)
LEAGUES = [
    {'id': 39, 'name': 'الدوري الإنجليزي'},    # Premier League
    {'id': 140, 'name': 'الدوري الإسباني'},   # La Liga
    {'id': 135, 'name': 'الدوري الإيطالي'},   # Serie A
    {'id': 78, 'name': 'الدوري الألماني'},    # Bundesliga
    {'id': 61, 'name': 'الدوري الفرنسي'},     # Ligue 1
    {'id': 307, 'name': 'الدوري السعودي'},    # Saudi Pro League (يضم رونالدو)
    {'id': 253, 'name': 'الدوري الأمريكي'},   # MLS (يضم ميسي)
]

SEASON = 2024
all_players = []
seen_names = set()  # لمنع التكرار

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
            
            # تجاهل اللاعبين بدون صور أو أسماء مكررة
            if not name or not photo:
                continue
            if name in seen_names:
                continue
                
            seen_names.add(name)
            all_players.append({
                'id': player.get('id'),
                'name': name,
                'nationality': player.get('nationality', 'غير معروف'),
                'level': 'easy',  # سنتركها سهلة حالياً، لكن يمكنك تخصيصها لاحقاً
                'image': photo
            })
            count += 1
        print(f'    ✅ تم إضافة {count} لاعب من {league["name"]}')
        
    except Exception as e:
        print(f'    ❌ خطأ في {league["name"]}: {e}')

# في حال فشل API بالكامل (مثلاً انتهاء المفتاح)، استخدم بيانات احتياطية تضم رونالدو وميسي
if len(all_players) == 0:
    print('⚠️ فشل تحميل جميع الدوريات، استخدام بيانات احتياطية.')
    all_players = [
        {"id": 1, "name": "كريستيانو رونالدو", "nationality": "البرتغال", "level": "legend", "image": "https://media.api-sports.io/football/players/257.png"},
        {"id": 2, "name": "ليونيل ميسي", "nationality": "الأرجنتين", "level": "legend", "image": "https://media.api-sports.io/football/players/457.png"},
        {"id": 3, "name": "كيليان مبابي", "nationality": "فرنسا", "level": "easy", "image": "https://media.api-sports.io/football/players/1495.png"},
        {"id": 4, "name": "إيرلينغ هالاند", "nationality": "النرويج", "level": "easy", "image": "https://media.api-sports.io/football/players/10035.png"},
    ]

# حفظ الملف
with open('popular_players.json', 'w', encoding='utf-8') as f:
    json.dump(all_players, f, ensure_ascii=False, indent=2)

print(f'✅ تم حفظ {len(all_players)} لاعباً بنجاح!')
print('🎉 الآن اللعبة تحتوي على نجوم من جميع أنحاء العالم، بما فيهم رونالدو وميسي!')