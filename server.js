const express = require("express");
const cors = require("cors");
const crypto = require("crypto");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

const players = require("./popular_players.json");
const games = new Map();

const positionArabic = {
  Forward: "مهاجم",
  Midfielder: "وسط",
  Defender: "مدافع",
  Goalkeeper: "حارس مرمى"
};

const subPositionArabic = {
  "Attacking Midfield": "وسط هجومي",
  "Central Midfield": "وسط مركزي",
  "Centre-Back": "قلب دفاع",
  "Centre-Forward": "مهاجم صريح",
  "Defensive Midfield": "وسط دفاعي",
  Goalkeeper: "حارس مرمى",
  "Left Midfield": "وسط أيسر",
  "Left Winger": "جناح أيسر",
  "Left-Back": "ظهير أيسر",
  "Right Midfield": "وسط أيمن",
  "Right Winger": "جناح أيمن",
  "Right-Back": "ظهير أيمن",
  "Second Striker": "مهاجم ثاني"
};

const questions = [];

function addQuestion(text, test, type) {
  questions.push({ text, test, type });
}

// المركز
Object.entries(positionArabic).forEach(([english, arabic]) => {
  addQuestion(
    `هل اللاعب ${arabic}؟`,
    player => player.position === english,
    "position"
  );
});

// المركز الفرعي
Object.entries(subPositionArabic).forEach(([english, arabic]) => {
  addQuestion(
    `هل اللاعب ${arabic}؟`,
    player => player.subPosition === english,
    "subPosition"
  );
});

// القارة
const continentArabic = {
  Europe: "أوروبا",
  Africa: "إفريقيا",
  Asia: "آسيا",
  "South America": "أمريكا الجنوبية",
  "North America": "أمريكا الشمالية",
  Oceania: "أوقيانوسيا"
};

const continents = [
  ...new Set(players.map(p => p.continent).filter(Boolean))
];

continents.forEach(continent => {
  addQuestion(
    `هل اللاعب من قارة ${continentArabic[continent] || continent}؟`,
    player => player.continent === continent,
    "continent"
  );
});

// الدوري
const leagues = [
  ...new Set(players.map(p => p.league).filter(Boolean))
];

leagues.forEach(league => {
  addQuestion(
    `هل اللاعب يلعب في ${league}؟`,
    player => player.league === league,
    "league"
  );
});

// الدولة
const countries = [
  ...new Set(players.map(p => p.country).filter(Boolean))
];

countries.forEach(country => {
  addQuestion(
    `هل اللاعب من ${country}؟`,
    player => player.country === country,
    "country"
  );
});

// النادي
const clubs = [
  ...new Set(players.map(p => p.club).filter(Boolean))
];

clubs.forEach(club => {
  addQuestion(
    `هل اللاعب يلعب في ${club}؟`,
    player => player.club === club,
    "club"
  );
});

// القيمة السوقية
const values = [
  5000000,
  10000000,
  20000000,
  50000000,
  100000000
];

values.forEach(value => {
  addQuestion(
    `هل قيمة اللاعب السوقية أكبر من ${value / 1000000} مليون يورو؟`,
    player => Number(player.marketValue || 0) >= value,
    "marketValue"
  );
});

function pickQuestion(candidates, asked, allowedTypes) {
  let bestIndex = -1;
  let bestScore = Infinity;

  for (let i = 0; i < questions.length; i++) {
    if (asked.includes(i)) continue;

    if (allowedTypes && !allowedTypes.includes(questions[i].type)) {
      continue;
    }

    const yes = candidates.filter(questions[i].test).length;
    const no = candidates.length - yes;

    if (yes === 0 || no === 0) continue;

    const score = Math.abs(yes - no);

    if (score < bestScore) {
      bestScore = score;
      bestIndex = i;
    }
  }

  return bestIndex;
}

// الصفحة الرئيسية
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

// لعبة جديدة
app.post("/new-game", (req, res) => {
  const gameId = crypto.randomUUID();

  const candidates = [...players];
  const asked = [];

  const current = pickQuestion(
    candidates,
    asked,
    ["position"]
  );

  if (current === -1) {
    return res.json({
      success: false,
      message: "لا توجد أسئلة كافية"
    });
  }

  games.set(gameId, {
    candidates,
    asked,
    stageIndex: 0,
    current
  });

  res.json({
    success: true,
    gameId,
    finished: false,
    question: questions[current].text
  });
});

// الإجابة
app.post("/question", (req, res) => {
  const { gameId, answer } = req.body;

  const game = games.get(gameId);

  if (!game) {
    return res.json({
      success: false,
      message: "اللعبة غير موجودة"
    });
  }

  const question = questions[game.current];

  game.candidates = game.candidates.filter(player =>
    answer === "yes"
      ? question.test(player)
      : !question.test(player)
  );

  game.asked.push(game.current);

  // لا يوجد لاعب
  if (game.candidates.length === 0) {
    games.delete(gameId);

    return res.json({
      success: true,
      finished: true,
      player: null,
      restart: true
    });
  }

  const stages = [
    "position",
    "subPosition",
    "continent",
    "league",
    "country",
    "club",
    "marketValue"
  ];

  let nextQuestion = -1;
  let nextStageIndex = game.stageIndex;

  for (let i = game.stageIndex; i < stages.length; i++) {
    const q = pickQuestion(
      game.candidates,
      game.asked,
      [stages[i]]
    );

    if (q !== -1) {
      nextQuestion = q;
      nextStageIndex = i;
      break;
    }
  }

  // تم العثور على اللاعب
  if (nextQuestion === -1 || game.candidates.length === 1) {
    const player = game.candidates[0];

    games.delete(gameId);

    return res.json({
      success: true,
      finished: true,
      restart: true,
      player: player?.name || null,
      imageUrl: player?.imageUrl || null
    });
  }

  game.stageIndex = nextStageIndex;
  game.current = nextQuestion;

  res.json({
    success: true,
    finished: false,
    question: questions[nextQuestion].text,
    remaining: game.candidates.length
  });
});

app.listen(PORT, "127.0.0.1", () => {
  console.log(
    `Server running on http://127.0.0.1:${PORT}`
  );
});