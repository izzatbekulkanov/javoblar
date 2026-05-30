import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\Farangiz\metodica\bilets_clean.json', 'r', encoding='utf-8') as f:
    bilets = json.load(f)

bilets_sorted = {int(k): v for k, v in bilets.items()}
js_data = json.dumps(bilets_sorted, ensure_ascii=False)

# Count stats
total_bilets = len(bilets_sorted)
total_q = sum(len(v) for v in bilets_sorted.values())
total_with_answer = sum(1 for v in bilets_sorted.values() for q in v if q['javob'] != 'Javob mavjud emas')

html = '''<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Metodika — Imtihon Biletlari</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0d0d1a;
    --surface: #13132b;
    --card: #1a1a35;
    --card2: #1f1f3d;
    --accent: #7c3aed;
    --accent2: #4f46e5;
    --accent3: #06b6d4;
    --green: #10b981;
    --yellow: #f59e0b;
    --red: #ef4444;
    --text: #e2e8f0;
    --text2: #cbd5e1;
    --muted: #64748b;
    --border: #252550;
    --border2: #2d2d60;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  html { scroll-behavior: smooth; }

  body {
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Animated bg orbs */
  .bg-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.12;
    pointer-events: none;
    z-index: 0;
    animation: orbFloat 12s ease-in-out infinite alternate;
  }
  .bg-orb-1 { width: 500px; height: 500px; background: #7c3aed; top: -100px; left: -100px; }
  .bg-orb-2 { width: 400px; height: 400px; background: #06b6d4; bottom: -100px; right: -100px; animation-delay: -5s; }
  .bg-orb-3 { width: 300px; height: 300px; background: #4f46e5; top: 50%; left: 50%; animation-delay: -3s; }

  @keyframes orbFloat {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(30px, 30px) scale(1.1); }
  }

  .wrap { position: relative; z-index: 1; max-width: 960px; margin: 0 auto; padding: 0 20px; }

  /* ===== HEADER ===== */
  header {
    text-align: center;
    padding: 56px 20px 36px;
    position: relative;
    z-index: 1;
  }

  .logo-ring {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 80px; height: 80px;
    border-radius: 24px;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    font-size: 36px;
    margin-bottom: 20px;
    box-shadow: 0 0 40px rgba(124,58,237,0.4);
    animation: pulse 3s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 40px rgba(124,58,237,0.4); }
    50% { box-shadow: 0 0 60px rgba(124,58,237,0.6); }
  }

  header h1 {
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #c4b5fd 0%, #93c5fd 50%, #6ee7b7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
  }

  header p { color: var(--muted); font-size: 1rem; font-weight: 400; }

  .stat-row {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 28px;
    flex-wrap: wrap;
  }

  .stat-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border2);
    border-radius: 100px;
    padding: 8px 18px;
    font-size: 0.85rem;
    backdrop-filter: blur(12px);
  }

  .stat-pill .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
  }
  .dot-purple { background: #a78bfa; }
  .dot-blue { background: #60a5fa; }
  .dot-green { background: #34d399; }

  .stat-pill strong { color: var(--text); font-weight: 700; }
  .stat-pill span { color: var(--muted); }

  /* ===== SCREEN SWITCHER ===== */
  .screen { display: none; }
  .screen.active { display: block; }

  /* ===== SEARCH ===== */
  .search-wrap {
    position: relative;
    margin-bottom: 24px;
  }

  .search-wrap svg {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--muted);
    width: 18px; height: 18px;
  }

  .search-wrap input {
    width: 100%;
    padding: 14px 18px 14px 48px;
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 14px;
    color: var(--text);
    font-size: 1rem;
    font-family: 'Inter', sans-serif;
    outline: none;
    transition: all 0.25s;
  }

  .search-wrap input::placeholder { color: var(--muted); }

  .search-wrap input:focus {
    border-color: var(--accent);
    background: var(--card2);
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12);
  }

  /* ===== BILET GRID ===== */
  .bilet-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 12px;
  }

  .bilet-card {
    position: relative;
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 18px;
    padding: 22px 12px 18px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    overflow: hidden;
    user-select: none;
  }

  .bilet-card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(6,182,212,0.04));
    opacity: 0;
    transition: opacity 0.3s;
  }

  .bilet-card:hover { 
    transform: translateY(-6px) scale(1.02);
    border-color: rgba(124,58,237,0.5);
    box-shadow: 0 20px 40px rgba(124,58,237,0.2);
  }
  .bilet-card:hover::after { opacity: 1; }
  .bilet-card:active { transform: translateY(-2px) scale(0.99); }

  .bc-num {
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #c4b5fd, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    display: block;
    margin-bottom: 4px;
  }

  .bc-label {
    font-size: 0.65rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-bottom: 10px;
    display: block;
  }

  .bc-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.2);
    color: #a78bfa;
    border-radius: 100px;
    padding: 3px 10px;
    font-size: 0.68rem;
    font-weight: 600;
  }

  /* ===== QUESTIONS SCREEN ===== */
  .top-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 28px;
    flex-wrap: wrap;
  }

  .btn-back {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border2);
    border-radius: 10px;
    padding: 10px 16px;
    color: var(--muted);
    cursor: pointer;
    font-size: 0.88rem;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    transition: all 0.2s;
    white-space: nowrap;
  }
  .btn-back:hover { background: rgba(255,255,255,0.09); color: var(--text); border-color: var(--accent); }

  .bilet-title {
    flex: 1;
    text-align: center;
  }
  .bilet-title h2 {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #c4b5fd, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .bilet-title p { color: var(--muted); font-size: 0.85rem; margin-top: 2px; }

  /* Progress */
  .progress-line {
    height: 3px;
    background: var(--border2);
    border-radius: 100px;
    margin-bottom: 24px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    border-radius: 100px;
    transition: width 0.5s ease;
  }

  /* ===== QUESTION CARDS ===== */
  .q-list { display: flex; flex-direction: column; gap: 12px; }

  .q-card {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 20px;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
  }

  .q-card.open {
    border-color: rgba(124,58,237,0.4);
    box-shadow: 0 8px 40px rgba(124,58,237,0.1);
  }

  .q-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 20px 22px;
    cursor: pointer;
    transition: background 0.2s;
    user-select: none;
  }
  .q-header:hover { background: rgba(124,58,237,0.05); }

  .q-num {
    width: 40px; height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-weight: 800;
    font-size: 0.95rem;
    flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(124,58,237,0.4);
  }

  .q-text {
    flex: 1;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text);
    line-height: 1.4;
  }

  .q-arrow {
    color: var(--muted);
    font-size: 16px;
    flex-shrink: 0;
    transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .q-card.open .q-arrow {
    transform: rotate(180deg);
    color: var(--accent);
  }

  /* NO ANSWER badge */
  .no-answer-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.2);
    color: #f87171;
    border-radius: 100px;
    padding: 2px 10px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-left: auto;
    flex-shrink: 0;
  }

  /* Body of question */
  .q-body {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .q-card.open .q-body { max-height: 4000px; }

  .q-answer {
    border-top: 1px solid var(--border2);
    padding: 20px 22px 24px;
  }

  .answer-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.2);
    color: #34d399;
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 14px;
  }

  .answer-text {
    color: var(--text2);
    font-size: 0.93rem;
    line-height: 1.85;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .no-answer-text {
    color: var(--muted);
    font-size: 0.9rem;
    font-style: italic;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* ===== NAVIGATION ===== */
  .nav-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 28px;
    padding-bottom: 40px;
  }

  .nav-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 12px;
    padding: 12px 22px;
    color: var(--muted);
    cursor: pointer;
    font-size: 0.88rem;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    transition: all 0.25s;
  }
  .nav-btn:hover:not(:disabled) {
    background: rgba(124,58,237,0.1);
    border-color: var(--accent);
    color: var(--text);
  }
  .nav-btn:disabled { opacity: 0.25; cursor: default; }

  .nav-center {
    font-size: 0.85rem;
    color: var(--muted);
    text-align: center;
    min-width: 100px;
  }
  .nav-center strong { color: var(--text); font-weight: 700; }

  /* ===== FOOTER ===== */
  footer {
    text-align: center;
    padding: 30px 20px;
    color: var(--muted);
    font-size: 0.78rem;
    position: relative;
    z-index: 1;
  }

  /* ===== RESPONSIVE ===== */
  @media (max-width: 600px) {
    header h1 { font-size: 2rem; }
    .bilet-grid { grid-template-columns: repeat(4, 1fr); gap: 10px; }
    .bilet-card { padding: 16px 8px 14px; }
    .bc-num { font-size: 1.7rem; }
    .q-header { padding: 16px 16px; }
    .q-answer { padding: 16px 16px 20px; }
    .nav-btn { padding: 10px 14px; font-size: 0.82rem; }
  }

  @media (max-width: 420px) {
    .bilet-grid { grid-template-columns: repeat(3, 1fr); }
  }

  /* Empty state */
  .empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--muted);
  }
  .empty-state .icon { font-size: 48px; margin-bottom: 12px; }
</style>
</head>
<body>

<!-- Background orbs -->
<div class="bg-orb bg-orb-1"></div>
<div class="bg-orb bg-orb-2"></div>
<div class="bg-orb bg-orb-3"></div>

<!-- HEADER -->
<header>
  <div class="logo-ring">📚</div>
  <h1>Metodika Biletlari</h1>
  <p>Adabiyot o'qitish metodikasi — imtihon savol-javoblari</p>
  <div class="stat-row">
    <div class="stat-pill">
      <div class="dot dot-purple"></div>
      <strong>''' + str(total_bilets) + '''</strong>
      <span>Bilet</span>
    </div>
    <div class="stat-pill">
      <div class="dot dot-blue"></div>
      <strong>''' + str(total_q) + '''</strong>
      <span>Savol</span>
    </div>
    <div class="stat-pill">
      <div class="dot dot-green"></div>
      <strong>''' + str(total_with_answer) + '''</strong>
      <span>Javob mavjud</span>
    </div>
  </div>
</header>

<div class="wrap">

  <!-- SCREEN 1: BILET LIST -->
  <div id="s1" class="screen active">
    <div class="search-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
      </svg>
      <input type="text" id="searchInput" placeholder="Bilet raqamini kiriting..." oninput="filterBilets(this.value)">
    </div>
    <div class="bilet-grid" id="biletGrid"></div>
    <div id="emptyState" class="empty-state hidden">
      <div class="icon">🔎</div>
      <p>Bunday bilet topilmadi</p>
    </div>
  </div>

  <!-- SCREEN 2: QUESTIONS -->
  <div id="s2" class="screen">
    <div class="top-bar">
      <button class="btn-back" onclick="goBack()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M19 12H5M5 12l7-7M5 12l7 7"/>
        </svg>
        Ortga
      </button>
      <div class="bilet-title">
        <h2 id="biletTitle">—</h2>
        <p id="biletSub">—</p>
      </div>
      <div style="width:80px"></div><!-- spacer -->
    </div>

    <div class="progress-line">
      <div class="progress-fill" id="progressFill" style="width:0%"></div>
    </div>

    <div class="q-list" id="qList"></div>

    <div class="nav-row">
      <button class="nav-btn" id="prevBtn" onclick="navigate(-1)">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M15 18l-6-6 6-6"/>
        </svg>
        Oldingi
      </button>
      <div class="nav-center" id="navCenter">—</div>
      <button class="nav-btn" id="nextBtn" onclick="navigate(1)">
        Keyingi
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M9 18l6-6-6-6"/>
        </svg>
      </button>
    </div>
  </div>

</div>

<footer>Ventoy uchun tayyor &nbsp;•&nbsp; Adabiyot o'qitish metodikasi &nbsp;•&nbsp; Offline ishlaydi</footer>

<script>
const DATA = ''' + js_data + ''';
const KEYS = Object.keys(DATA).map(Number).sort((a,b)=>a-b);
let curIdx = 0;

// Build grid
function renderGrid(keys) {
  const grid = document.getElementById('biletGrid');
  const empty = document.getElementById('emptyState');
  grid.innerHTML = '';
  if (!keys.length) { empty.classList.remove('hidden'); return; }
  empty.classList.add('hidden');
  keys.forEach(k => {
    const qs = DATA[k];
    const withAns = qs.filter(q => q.javob !== 'Javob mavjud emas').length;
    const card = document.createElement('div');
    card.className = 'bilet-card';
    card.innerHTML = `
      <span class="bc-num">${k}</span>
      <span class="bc-label">bilet</span>
      <span class="bc-badge">${qs.length} savol</span>
    `;
    card.onclick = () => openBilet(k);
    grid.appendChild(card);
  });
}
renderGrid(KEYS);

function filterBilets(v) {
  v = v.trim();
  const filtered = v ? KEYS.filter(k => String(k).includes(v)) : KEYS;
  renderGrid(filtered);
}

function openBilet(num) {
  curIdx = KEYS.indexOf(num);
  renderBilet(num);
  document.getElementById('s1').classList.remove('active');
  document.getElementById('s2').classList.add('active');
  window.scrollTo({top:0, behavior:'smooth'});
}

function renderBilet(num) {
  const qs = DATA[num] || [];
  document.getElementById('biletTitle').textContent = num + '-Bilet';
  const withAns = qs.filter(q => q.javob !== 'Javob mavjud emas').length;
  document.getElementById('biletSub').textContent = `${qs.length} ta savol • ${withAns} ta javob mavjud`;

  const pct = Math.round(((curIdx+1)/KEYS.length)*100);
  document.getElementById('progressFill').style.width = pct+'%';
  document.getElementById('navCenter').innerHTML = `<strong>${curIdx+1}</strong> / ${KEYS.length}`;
  document.getElementById('prevBtn').disabled = curIdx === 0;
  document.getElementById('nextBtn').disabled = curIdx === KEYS.length-1;

  const list = document.getElementById('qList');
  list.innerHTML = '';

  if (!qs.length) {
    list.innerHTML = '<div class="empty-state"><div class="icon">📭</div><p>Bu bilet uchun ma\'lumot mavjud emas.</p></div>';
    return;
  }

  qs.forEach((q, i) => {
    const hasAns = q.javob !== 'Javob mavjud emas';
    const card = document.createElement('div');
    card.className = 'q-card';
    card.id = 'qc'+i;

    const savol = esc(q.savol || ('Savol ' + q.savol_raqami));

    let headerExtra = '';
    if (!hasAns) {
      headerExtra = '<span class="no-answer-badge">⚠ Javob yo\'q</span>';
    }

    let bodyContent = '';
    if (hasAns) {
      bodyContent = `<span class="answer-tag">✓ Javob</span><div class="answer-text">${esc(q.javob)}</div>`;
    } else {
      bodyContent = `<div class="no-answer-text">⚠ Bu savol uchun hozircha javob kiritilmagan.</div>`;
    }

    card.innerHTML = `
      <div class="q-header" onclick="toggle(${i})">
        <div class="q-num">${q.savol_raqami}</div>
        <div class="q-text">${savol}</div>
        ${headerExtra}
        <div class="q-arrow">▼</div>
      </div>
      <div class="q-body">
        <div class="q-answer">${bodyContent}</div>
      </div>
    `;
    list.appendChild(card);
  });
}

function toggle(i) {
  document.getElementById('qc'+i).classList.toggle('open');
}

function navigate(dir) {
  const ni = curIdx + dir;
  if (ni < 0 || ni >= KEYS.length) return;
  curIdx = ni;
  renderBilet(KEYS[curIdx]);
  window.scrollTo({top:0, behavior:'smooth'});
}

function goBack() {
  document.getElementById('s2').classList.remove('active');
  document.getElementById('s1').classList.add('active');
  window.scrollTo({top:0, behavior:'smooth'});
}

function esc(s) {
  return String(s||'')
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}
</script>
</body>
</html>
'''

with open(r'D:\Farangiz\metodica\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('index.html yangilandi!')
print(f'Biletlar: {total_bilets}, Savollar: {total_q}, Javoblar: {total_with_answer}')
