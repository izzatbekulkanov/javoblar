import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\Farangiz\metodica\bilets.json', 'r', encoding='utf-8') as f:
    bilets = json.load(f)

# Convert keys to int and sort
bilets_sorted = {int(k): v for k, v in bilets.items()}

# Build JS data
js_data = json.dumps(bilets_sorted, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Metodika - Imtihon Biletlari</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0f0f1a;
    --surface: #1a1a2e;
    --surface2: #16213e;
    --card: #1e2040;
    --accent: #7c3aed;
    --accent2: #4f46e5;
    --accent3: #06b6d4;
    --text: #e2e8f0;
    --text-muted: #94a3b8;
    --border: #2d2d50;
    --success: #10b981;
    --warning: #f59e0b;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Animated background */
  body::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 20% 20%, rgba(124,58,237,0.12) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(79,70,229,0.10) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(6,182,212,0.05) 0%, transparent 60%);
    animation: bgPulse 8s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
  }

  @keyframes bgPulse {
    0% { transform: translate(0, 0) rotate(0deg); }
    100% { transform: translate(2%, 2%) rotate(1deg); }
  }

  .container {
    position: relative;
    z-index: 1;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
  }

  /* HEADER */
  header {
    text-align: center;
    padding: 50px 20px 30px;
    position: relative;
    z-index: 1;
  }

  .header-icon {
    font-size: 56px;
    margin-bottom: 16px;
    display: block;
    animation: float 3s ease-in-out infinite;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
  }

  header h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
  }

  header p {
    color: var(--text-muted);
    font-size: 1.05rem;
    font-weight: 400;
  }

  .stats-bar {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 24px;
    flex-wrap: wrap;
  }

  .stat {
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 22px;
    text-align: center;
    backdrop-filter: blur(8px);
  }

  .stat-num {
    font-size: 1.5rem;
    font-weight: 700;
    color: #a78bfa;
  }

  .stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }

  /* SCREENS */
  .screen { display: none; }
  .screen.active { display: block; }

  /* SEARCH */
  .search-bar {
    margin: 20px 0;
    position: relative;
  }

  .search-bar input {
    width: 100%;
    padding: 14px 20px 14px 50px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    color: var(--text);
    font-size: 1rem;
    font-family: 'Inter', sans-serif;
    outline: none;
    transition: all 0.3s;
  }

  .search-bar input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15);
  }

  .search-icon {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
    font-size: 18px;
  }

  /* BILET GRID */
  .bilet-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 14px;
    margin-top: 20px;
  }

  .bilet-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 14px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    user-select: none;
  }

  .bilet-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    transform: scaleX(0);
    transition: transform 0.3s;
  }

  .bilet-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 12px 32px rgba(124,58,237,0.25);
    background: var(--surface);
  }

  .bilet-card:hover::before {
    transform: scaleX(1);
  }

  .bilet-card:active {
    transform: translateY(-1px) scale(0.98);
  }

  .bilet-num {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
  }

  .bilet-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .bilet-count {
    display: inline-block;
    background: rgba(124,58,237,0.15);
    color: #a78bfa;
    border-radius: 20px;
    padding: 2px 8px;
    font-size: 0.7rem;
    margin-top: 8px;
    font-weight: 600;
  }

  /* QUESTION SCREEN */
  .back-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.06);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 18px;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s;
    margin-bottom: 24px;
  }

  .back-btn:hover {
    background: rgba(255,255,255,0.1);
    color: var(--text);
    border-color: var(--accent);
  }

  .bilet-title-header {
    text-align: center;
    margin-bottom: 30px;
  }

  .bilet-title-header h2 {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .bilet-title-header p {
    color: var(--text-muted);
    margin-top: 6px;
    font-size: 0.9rem;
  }

  .questions-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .question-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
    transition: all 0.3s;
  }

  .question-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .question-header:hover {
    background: rgba(124,58,237,0.08);
  }

  .question-num {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .q-badge {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.95rem;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(124,58,237,0.35);
  }

  .q-title {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text);
    line-height: 1.4;
  }

  .q-toggle {
    color: var(--text-muted);
    font-size: 20px;
    transition: transform 0.3s;
    flex-shrink: 0;
  }

  .question-card.open .q-toggle {
    transform: rotate(180deg);
    color: var(--accent);
  }

  .question-card.open {
    border-color: rgba(124,58,237,0.4);
    box-shadow: 0 8px 32px rgba(124,58,237,0.12);
  }

  .question-body {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .question-card.open .question-body {
    max-height: 3000px;
  }

  .answer-content {
    padding: 0 24px 24px;
    border-top: 1px solid var(--border);
    padding-top: 20px;
  }

  .answer-label {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.12);
    color: #34d399;
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 14px;
  }

  .answer-text {
    color: var(--text);
    font-size: 0.95rem;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
  }

  /* NAVIGATION ARROWS */
  .bilet-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 30px;
    gap: 12px;
  }

  .nav-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px 22px;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    transition: all 0.25s;
    flex: 1;
    justify-content: center;
  }

  .nav-btn:hover:not(:disabled) {
    background: rgba(124,58,237,0.12);
    border-color: var(--accent);
    color: var(--text);
  }

  .nav-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .nav-indicator {
    color: var(--text-muted);
    font-size: 0.85rem;
    text-align: center;
    min-width: 80px;
  }

  /* PROGRESS BAR */
  .progress-container {
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    height: 4px;
    margin-bottom: 20px;
    overflow: hidden;
  }

  .progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    border-radius: 100px;
    transition: width 0.4s ease;
  }

  /* FOOTER */
  footer {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-muted);
    font-size: 0.8rem;
    position: relative;
    z-index: 1;
  }

  /* HIDDEN utility */
  .hidden { display: none !important; }

  /* RESPONSIVE */
  @media (max-width: 480px) {
    header h1 { font-size: 1.8rem; }
    .bilet-grid { grid-template-columns: repeat(3, 1fr); }
    .question-header { padding: 16px 18px; }
    .answer-content { padding: 16px 18px; }
  }
</style>
</head>
<body>

<header>
  <span class="header-icon">📚</span>
  <h1>Metodika Biletlari</h1>
  <p>Adabiyot o'qitish metodikasi — imtihon savol-javoblari</p>
  <div class="stats-bar">
    <div class="stat">
      <div class="stat-num" id="totalBilets">0</div>
      <div class="stat-label">Bilet</div>
    </div>
    <div class="stat">
      <div class="stat-num" id="totalQuestions">0</div>
      <div class="stat-label">Savol</div>
    </div>
  </div>
</header>

<!-- SCREEN 1: BILET SELECTION -->
<div class="container">
  <div id="screenBilets" class="screen active">
    <div class="search-bar">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" placeholder="Bilet raqamini qidiring..." oninput="filterBilets(this.value)">
    </div>
    <div class="bilet-grid" id="biletGrid"></div>
  </div>

  <!-- SCREEN 2: QUESTIONS -->
  <div id="screenQuestions" class="screen">
    <button class="back-btn" onclick="goBack()">← Ortga</button>
    <div class="bilet-title-header">
      <h2 id="biletHeading">Bilet 1</h2>
      <p id="biletSubheading"></p>
    </div>
    <div class="progress-container">
      <div class="progress-bar" id="progressBar" style="width:0%"></div>
    </div>
    <div class="questions-list" id="questionsList"></div>

    <div class="bilet-nav">
      <button class="nav-btn" id="prevBtn" onclick="navigateBilet(-1)">← Oldingi</button>
      <div class="nav-indicator" id="navIndicator"></div>
      <button class="nav-btn" id="nextBtn" onclick="navigateBilet(1)">Keyingi →</button>
    </div>
  </div>
</div>

<footer>
  <p>Ventoy uchun tayyor • Adabiyot o'qitish metodikasi</p>
</footer>

<script>
const BILETS_DATA = ''' + js_data + ''';

// Convert keys to numbers and sort
const biletKeys = Object.keys(BILETS_DATA).map(Number).sort((a,b)=>a-b);

let currentBiletIndex = 0;
let filteredKeys = [...biletKeys];

// Update stats
document.getElementById('totalBilets').textContent = biletKeys.length;
const totalQ = biletKeys.reduce((acc, k) => acc + BILETS_DATA[k].length, 0);
document.getElementById('totalQuestions').textContent = totalQ;

// Render bilet grid
function renderGrid(keys) {
  const grid = document.getElementById('biletGrid');
  grid.innerHTML = '';
  keys.forEach(k => {
    const qs = BILETS_DATA[k];
    const card = document.createElement('div');
    card.className = 'bilet-card';
    card.innerHTML = `
      <span class="bilet-num">${k}</span>
      <div class="bilet-label">Bilet</div>
      <span class="bilet-count">${qs.length} savol</span>
    `;
    card.onclick = () => openBilet(k);
    grid.appendChild(card);
  });
}

renderGrid(biletKeys);

function filterBilets(val) {
  val = val.trim();
  if (!val) {
    filteredKeys = [...biletKeys];
  } else {
    filteredKeys = biletKeys.filter(k => String(k).includes(val));
  }
  renderGrid(filteredKeys);
}

function openBilet(biletNum) {
  currentBiletIndex = biletKeys.indexOf(biletNum);
  showBilet(biletNum);
  document.getElementById('screenBilets').classList.remove('active');
  document.getElementById('screenQuestions').classList.add('active');
  window.scrollTo({top: 0, behavior: 'smooth'});
}

function showBilet(biletNum) {
  const qs = BILETS_DATA[biletNum] || [];
  document.getElementById('biletHeading').textContent = `${biletNum}-Bilet`;
  document.getElementById('biletSubheading').textContent = `${qs.length} ta savol`;

  const idx = biletKeys.indexOf(biletNum);
  const pct = Math.round(((idx + 1) / biletKeys.length) * 100);
  document.getElementById('progressBar').style.width = pct + '%';
  document.getElementById('navIndicator').textContent = `${idx+1} / ${biletKeys.length}`;

  document.getElementById('prevBtn').disabled = idx === 0;
  document.getElementById('nextBtn').disabled = idx === biletKeys.length - 1;

  const list = document.getElementById('questionsList');
  list.innerHTML = '';

  if (qs.length === 0) {
    list.innerHTML = '<p style="text-align:center;color:var(--text-muted);padding:40px;">Bu bilet uchun ma\\'lumot mavjud emas.</p>';
    return;
  }

  qs.forEach((q, i) => {
    const card = document.createElement('div');
    card.className = 'question-card';
    card.id = `qcard-${i}`;

    // Derive short title from content
    let title = q.title || '';
    if (!title || title === `Savol ${i}` || title.length < 5) {
      title = q.content.split('\\n')[0].slice(0, 120);
    }
    // Clean up title
    title = title.replace(/^\\d+[.\\-\\s]*(savol|javobi|javob)?[.\\-\\s]*/i, '').trim();
    if (!title) title = `${i+1}-savol javobi`;

    const contentClean = q.content;

    card.innerHTML = `
      <div class="question-header" onclick="toggleQuestion(${i})">
        <div class="question-num">
          <div class="q-badge">${i+1}</div>
          <div class="q-title">${escHtml(title)}</div>
        </div>
        <span class="q-toggle">▼</span>
      </div>
      <div class="question-body">
        <div class="answer-content">
          <span class="answer-label">✓ Javob</span>
          <div class="answer-text">${escHtml(contentClean)}</div>
        </div>
      </div>
    `;
    list.appendChild(card);
  });
}

function toggleQuestion(idx) {
  const card = document.getElementById(`qcard-${idx}`);
  card.classList.toggle('open');
}

function navigateBilet(dir) {
  const newIdx = currentBiletIndex + dir;
  if (newIdx < 0 || newIdx >= biletKeys.length) return;
  currentBiletIndex = newIdx;
  showBilet(biletKeys[currentBiletIndex]);
  window.scrollTo({top: 0, behavior: 'smooth'});
}

function goBack() {
  document.getElementById('screenQuestions').classList.remove('active');
  document.getElementById('screenBilets').classList.add('active');
  window.scrollTo({top: 0, behavior: 'smooth'});
}

function escHtml(str) {
  return String(str)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}
</script>
</body>
</html>
'''

output_path = r'D:\Farangiz\metodica\index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'index.html yaratildi: {output_path}')
print(f'Biletlar soni: {len(bilets_sorted)}')
