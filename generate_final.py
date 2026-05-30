import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\Farangiz\metodica\bilets_clean.json', 'r', encoding='utf-8') as f:
    bilets = json.load(f)

bilets_sorted = {int(k): v for k, v in bilets.items()}
# Safe JSON embedding — NO JS string issues
json_str = json.dumps(bilets_sorted, ensure_ascii=False, indent=None)

total_bilets = len(bilets_sorted)
total_q = sum(len(v) for v in bilets_sorted.values())
total_with_answer = sum(1 for v in bilets_sorted.values() for q in v if q['javob'] != 'Javob mavjud emas')

html = f"""<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Metodika — Imtihon Biletlari</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

<!-- JSON data embedded safely — no JS string escaping issues -->
<script type="application/json" id="biletData">{json_str}</script>

<style>
  :root {{
    --bg: #080812;
    --s1: #0f0f20;
    --s2: #14142a;
    --card: #1a1a35;
    --card-h: #1f1f3e;
    --violet: #7c3aed;
    --indigo: #4f46e5;
    --cyan: #0891b2;
    --teal: #0d9488;
    --green: #059669;
    --amber: #d97706;
    --red: #dc2626;
    --txt: #f1f5f9;
    --txt2: #cbd5e1;
    --txt3: #94a3b8;
    --txt4: #64748b;
    --border: #1e1e3a;
    --border2: #252548;
  }}
  *, *::before, *::after {{ margin:0; padding:0; box-sizing:border-box; }}
  html {{ scroll-behavior:smooth; }}

  body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--txt);
    min-height: 100vh;
    overflow-x: hidden;
  }}

  /* ─── Animated background ─── */
  .bg {{
    position: fixed; inset: 0; z-index: 0; overflow: hidden; pointer-events: none;
  }}
  .bg-blob {{
    position: absolute; border-radius: 50%; filter: blur(120px); opacity: 0.07;
    animation: drift 20s ease-in-out infinite alternate;
  }}
  .blob1 {{ width:600px; height:600px; background:#7c3aed; top:-200px; left:-200px; }}
  .blob2 {{ width:500px; height:500px; background:#0891b2; bottom:-200px; right:-200px; animation-delay:-8s; }}
  .blob3 {{ width:400px; height:400px; background:#4f46e5; top:40%; left:35%; animation-delay:-4s; }}
  @keyframes drift {{
    0% {{ transform: translate(0,0) scale(1); }}
    100% {{ transform: translate(40px, 40px) scale(1.15); }}
  }}

  /* ─── Layout ─── */
  .page {{ position: relative; z-index: 1; }}
  .container {{ max-width: 960px; margin: 0 auto; padding: 0 20px; }}

  /* ─── Header ─── */
  .header {{
    text-align: center;
    padding: 60px 20px 40px;
  }}
  .header-icon {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 72px; height: 72px; border-radius: 22px;
    background: linear-gradient(135deg, #7c3aed 0%, #0891b2 100%);
    box-shadow: 0 0 0 1px rgba(124,58,237,0.3), 0 20px 60px rgba(124,58,237,0.35);
    margin-bottom: 24px;
    animation: iconPulse 4s ease-in-out infinite;
  }}
  @keyframes iconPulse {{
    0%,100% {{ box-shadow: 0 0 0 1px rgba(124,58,237,0.3), 0 20px 60px rgba(124,58,237,0.35); }}
    50% {{ box-shadow: 0 0 0 1px rgba(124,58,237,0.5), 0 20px 80px rgba(124,58,237,0.5); }}
  }}
  .header-icon svg {{ width:34px; height:34px; color:#fff; }}

  .header h1 {{
    font-size: clamp(1.8rem, 5vw, 3rem);
    font-weight: 900;
    letter-spacing: -1.5px;
    background: linear-gradient(135deg, #c4b5fd 0%, #93c5fd 45%, #6ee7b7 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
    line-height: 1.1;
  }}
  .header p {{ color: var(--txt3); font-size: 1rem; font-weight: 400; }}

  .chips {{
    display: flex; justify-content: center; gap: 10px;
    margin-top: 28px; flex-wrap: wrap;
  }}
  .chip {{
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border2);
    border-radius: 100px;
    padding: 7px 16px;
    font-size: 0.82rem; font-weight: 500;
    backdrop-filter: blur(12px);
  }}
  .chip-dot {{
    width:7px; height:7px; border-radius:50%; flex-shrink:0;
  }}
  .chip-dot.v {{ background: #a78bfa; }}
  .chip-dot.b {{ background: #60a5fa; }}
  .chip-dot.g {{ background: #34d399; }}
  .chip span {{ color: var(--txt); font-weight: 700; }}
  .chip em {{ color: var(--txt4); font-style:normal; }}

  /* ─── Screen system ─── */
  .screen {{ display: none; }}
  .screen.active {{ display: block; }}

  /* ─── Search bar ─── */
  .searchbar {{
    position: relative; margin-bottom: 24px;
  }}
  .searchbar svg {{
    position:absolute; left:16px; top:50%;
    transform:translateY(-50%);
    color: var(--txt4); width:18px; height:18px;
    pointer-events:none;
  }}
  .searchbar input {{
    width: 100%;
    padding: 13px 16px 13px 48px;
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 14px;
    color: var(--txt);
    font-size: 0.95rem;
    font-family: inherit;
    outline: none;
    transition: border-color .25s, box-shadow .25s, background .25s;
  }}
  .searchbar input::placeholder {{ color: var(--txt4); }}
  .searchbar input:focus {{
    border-color: var(--violet);
    background: var(--card-h);
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12);
  }}

  /* ─── Bilet grid ─── */
  .bilet-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: 10px;
  }}
  .bilet-card {{
    position: relative;
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 16px;
    padding: 20px 10px 16px;
    text-align: center;
    cursor: pointer;
    transition: transform .35s cubic-bezier(.34,1.56,.64,1), border-color .25s, box-shadow .25s;
    overflow: hidden;
    user-select: none;
  }}
  .bilet-card::before {{
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, var(--violet), var(--cyan));
    transform: scaleX(0); transform-origin: left;
    transition: transform .3s ease;
  }}
  .bilet-card:hover {{ transform: translateY(-5px) scale(1.03); border-color: rgba(124,58,237,.45); box-shadow: 0 16px 40px rgba(124,58,237,.18); }}
  .bilet-card:hover::before {{ transform: scaleX(1); }}
  .bilet-card:active {{ transform: translateY(-1px) scale(.99); }}

  .bc-num {{
    display: block; font-size: 2rem; font-weight: 900; line-height: 1;
    background: linear-gradient(135deg, #c4b5fd, #67e8f9);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 3px;
  }}
  .bc-lbl {{
    display: block; font-size: .6rem; color: var(--txt4);
    text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600;
    margin-bottom: 8px;
  }}
  .bc-tag {{
    display: inline-flex; align-items: center; gap: 3px;
    background: rgba(124,58,237,.13); border: 1px solid rgba(124,58,237,.18);
    color: #a78bfa; border-radius: 100px;
    padding: 2px 9px; font-size:.62rem; font-weight:700;
  }}

  /* ─── Empty state ─── */
  .empty {{
    text-align: center; padding: 60px 20px; color: var(--txt4);
  }}
  .empty svg {{ width:48px; height:48px; margin-bottom:12px; opacity:.4; }}
  .hidden {{ display:none !important; }}

  /* ─── Questions screen ─── */
  .topbar {{
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 24px; flex-wrap: wrap;
  }}
  .btn-back {{
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(255,255,255,.04);
    border: 1px solid var(--border2);
    border-radius: 10px;
    padding: 9px 16px;
    color: var(--txt3);
    cursor: pointer;
    font-size: .86rem; font-family: inherit; font-weight: 500;
    transition: all .2s;
    white-space: nowrap; flex-shrink: 0;
  }}
  .btn-back svg {{ width:15px; height:15px; }}
  .btn-back:hover {{ background: rgba(124,58,237,.1); color: var(--txt); border-color: var(--violet); }}

  .bilet-info {{ flex:1; text-align:center; }}
  .bilet-info h2 {{
    font-size: 1.7rem; font-weight:900; letter-spacing:-0.5px;
    background: linear-gradient(135deg, #c4b5fd, #67e8f9);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .bilet-info p {{ color: var(--txt4); font-size:.82rem; margin-top:2px; }}

  /* Progress */
  .progress {{
    height:3px; background:var(--border2); border-radius:100px;
    margin-bottom:24px; overflow:hidden;
  }}
  .progress-bar {{
    height:100%;
    background: linear-gradient(90deg, #7c3aed, #0891b2);
    border-radius:100px;
    transition: width .5s ease;
  }}

  /* ─── Question cards ─── */
  .q-list {{ display:flex; flex-direction:column; gap:10px; }}

  .qcard {{
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 18px; overflow:hidden;
    transition: border-color .3s, box-shadow .3s;
  }}
  .qcard.open {{
    border-color: rgba(124,58,237,.35);
    box-shadow: 0 8px 40px rgba(124,58,237,.1);
  }}

  .qcard-header {{
    display: flex; align-items: center; gap: 12px;
    padding: 18px 20px; cursor:pointer;
    transition: background .2s;
    user-select: none;
  }}
  .qcard-header:hover {{ background: rgba(124,58,237,.05); }}

  .q-badge {{
    width:38px; height:38px; border-radius:11px; flex-shrink:0;
    background: linear-gradient(135deg, var(--violet), var(--indigo));
    display:flex; align-items:center; justify-content:center;
    font-size:.9rem; font-weight:800;
    box-shadow: 0 4px 14px rgba(124,58,237,.4);
  }}

  .q-title {{
    flex:1; font-size:.92rem; font-weight:600; color:var(--txt);
    line-height:1.4;
  }}

  .no-ans-tag {{
    display:inline-flex; align-items:center; gap:5px;
    background: rgba(220,38,38,.1); border:1px solid rgba(220,38,38,.2);
    color:#f87171; border-radius:100px;
    padding: 3px 10px; font-size:.68rem; font-weight:700;
    white-space:nowrap; flex-shrink:0;
  }}
  .no-ans-tag svg {{ width:11px; height:11px; }}

  .q-chevron {{
    color: var(--txt4); flex-shrink:0;
    transition: transform .35s cubic-bezier(.34,1.56,.64,1), color .2s;
  }}
  .q-chevron svg {{ width:18px; height:18px; display:block; }}
  .qcard.open .q-chevron {{ transform:rotate(180deg); color:var(--violet); }}

  /* Answer body */
  .qcard-body {{
    max-height:0; overflow:hidden;
    transition: max-height .5s cubic-bezier(.4,0,.2,1);
  }}
  .qcard.open .qcard-body {{ max-height:5000px; }}

  .qcard-answer {{
    border-top:1px solid var(--border2);
    padding: 18px 20px 22px;
  }}

  .ans-label {{
    display: inline-flex; align-items: center; gap:6px;
    background: rgba(5,150,105,.1); border:1px solid rgba(5,150,105,.2);
    color:#34d399; border-radius:8px;
    padding:4px 12px; font-size:.68rem; font-weight:700;
    text-transform:uppercase; letter-spacing:.8px;
    margin-bottom:14px;
  }}
  .ans-label svg {{ width:12px; height:12px; }}

  .ans-text {{
    color:var(--txt2); font-size:.91rem; line-height:1.9;
    white-space:pre-wrap; word-break:break-word;
  }}

  .no-ans-msg {{
    display:flex; align-items:center; gap:8px;
    color:var(--txt4); font-size:.88rem; font-style:italic;
  }}
  .no-ans-msg svg {{ width:16px; height:16px; flex-shrink:0; color:#f87171; }}

  /* ─── Navigation ─── */
  .navrow {{
    display:flex; align-items:center; justify-content:space-between;
    gap:12px; margin-top:28px; padding-bottom:48px;
  }}
  .nav-btn {{
    display:flex; align-items:center; gap:7px;
    background: var(--card); border:1px solid var(--border2);
    border-radius:12px; padding:11px 20px;
    color:var(--txt3); cursor:pointer;
    font-size:.86rem; font-family:inherit; font-weight:600;
    transition: all .25s;
  }}
  .nav-btn svg {{ width:16px; height:16px; }}
  .nav-btn:hover:not(:disabled) {{ background:rgba(124,58,237,.1); border-color:var(--violet); color:var(--txt); }}
  .nav-btn:disabled {{ opacity:.2; cursor:default; pointer-events:none; }}

  .nav-info {{
    font-size:.84rem; color:var(--txt4); text-align:center; min-width:80px;
  }}
  .nav-info strong {{ color:var(--txt); font-weight:700; }}

  /* ─── Footer ─── */
  footer {{
    text-align:center; padding:28px 20px 40px;
    position:relative; z-index:1;
    border-top: 1px solid var(--border);
    margin-top: 20px;
  }}
  .footer-name {{
    font-size:.95rem; font-weight:700; color:var(--txt2); margin-bottom:4px;
    letter-spacing:.3px;
  }}
  .footer-sub {{
    font-size:.75rem; color:var(--txt4);
  }}

  /* ─── Responsive ─── */
  @media (max-width:600px) {{
    .bilet-grid {{ grid-template-columns: repeat(4, 1fr); gap:8px; }}
    .bilet-card {{ padding:14px 6px 12px; border-radius:12px; }}
    .bc-num {{ font-size:1.6rem; }}
    .bc-tag {{ font-size:.55rem; }}
    .qcard-header {{ padding:14px 14px; }}
    .qcard-answer {{ padding:14px 14px 18px; }}
    .nav-btn {{ padding:9px 12px; font-size:.8rem; }}
    .header h1 {{ font-size:1.9rem; }}
  }}
  @media (max-width:380px) {{
    .bilet-grid {{ grid-template-columns: repeat(3, 1fr); }}
  }}
</style>
</head>
<body>

<div class="bg">
  <div class="bg-blob blob1"></div>
  <div class="bg-blob blob2"></div>
  <div class="bg-blob blob3"></div>
</div>

<div class="page">

<!-- ░░░ HEADER ░░░ -->
<header class="header">
  <div class="header-icon">
    <!-- Book + Graduation cap icon -->
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
    </svg>
  </div>
  <h1>Metodika Biletlari</h1>
  <p>Adabiyot o&#x2bc;qitish metodikasi &mdash; imtihon savol-javoblari</p>
  <div class="chips">
    <div class="chip"><span class="chip-dot v"></span><span>{total_bilets}</span><em>Bilet</em></div>
    <div class="chip"><span class="chip-dot b"></span><span>{total_q}</span><em>Savol</em></div>
    <div class="chip"><span class="chip-dot g"></span><span>{total_with_answer}</span><em>Javob</em></div>
  </div>
</header>

<div class="container">

<!-- ░░░ SCREEN 1 — BILET LIST ░░░ -->
<div id="s1" class="screen active">
  <div class="searchbar">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
    </svg>
    <input type="text" id="searchInput" placeholder="Bilet raqamini qidiring..." oninput="filterBilets(this.value)">
  </div>

  <div class="bilet-grid" id="biletGrid"></div>

  <div id="emptyMsg" class="empty hidden">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
      <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
      <path d="M8 11h6M11 8v6"/>
    </svg>
    <p>Bunday bilet topilmadi</p>
  </div>
</div>

<!-- ░░░ SCREEN 2 — QUESTIONS ░░░ -->
<div id="s2" class="screen">
  <div class="topbar">
    <button class="btn-back" onclick="goBack()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 12H5M5 12l7-7M5 12l7 7"/>
      </svg>
      Ortga
    </button>
    <div class="bilet-info">
      <h2 id="biletTitle">—</h2>
      <p id="biletSub">—</p>
    </div>
    <div style="width:80px; flex-shrink:0;"></div>
  </div>

  <div class="progress"><div class="progress-bar" id="pBar" style="width:0%"></div></div>

  <div class="q-list" id="qList"></div>

  <div class="navrow">
    <button class="nav-btn" id="prevBtn" onclick="navigate(-1)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
      Oldingi
    </button>
    <div class="nav-info" id="navInfo"><strong>1</strong> / 30</div>
    <button class="nav-btn" id="nextBtn" onclick="navigate(1)">
      Keyingi
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
    </button>
  </div>
</div>

</div><!-- /container -->

<!-- ░░░ FOOTER ░░░ -->
<footer>
  <div class="footer-name">
    <svg style="width:14px;height:14px;vertical-align:middle;margin-right:5px;color:#a78bfa;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
    Farangiz Ulkanova
  </div>
  <div class="footer-sub">Adabiyot o&#x2bc;qitish metodikasi &nbsp;&bull;&nbsp; Ventoy uchun tayyor &nbsp;&bull;&nbsp; Offline ishlaydi</div>
</footer>

</div><!-- /page -->

<script>
// ── Load data from embedded JSON (safe — no JS string escaping) ──
const DATA = JSON.parse(document.getElementById('biletData').textContent);
const KEYS = Object.keys(DATA).map(Number).sort((a,b) => a - b);
let curIdx = 0;

// ── Icon SVGs ──
const icons = {{
  check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
  warn:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
  info:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
  down:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>',
}};

// ── Render bilet grid ──
function renderGrid(keys) {{
  const grid = document.getElementById('biletGrid');
  const empty = document.getElementById('emptyMsg');
  grid.innerHTML = '';
  if (!keys.length) {{ empty.classList.remove('hidden'); return; }}
  empty.classList.add('hidden');
  keys.forEach(k => {{
    const qs = DATA[k];
    const card = document.createElement('div');
    card.className = 'bilet-card';
    card.innerHTML =
      '<span class="bc-num">' + k + '</span>' +
      '<span class="bc-lbl">bilet</span>' +
      '<span class="bc-tag">' + qs.length + ' savol</span>';
    card.onclick = () => openBilet(k);
    grid.appendChild(card);
  }});
}}
renderGrid(KEYS);

function filterBilets(v) {{
  v = v.trim();
  renderGrid(v ? KEYS.filter(k => String(k).includes(v)) : KEYS);
}}

function openBilet(num) {{
  curIdx = KEYS.indexOf(num);
  renderBilet(num);
  document.getElementById('s1').classList.remove('active');
  document.getElementById('s2').classList.add('active');
  window.scrollTo({{top:0, behavior:'smooth'}});
}}

function renderBilet(num) {{
  const qs = DATA[num] || [];
  document.getElementById('biletTitle').textContent = num + '-Bilet';
  const withAns = qs.filter(q => q.javob !== 'Javob mavjud emas').length;
  document.getElementById('biletSub').textContent =
    qs.length + ' ta savol \u2022 ' + withAns + ' ta javob mavjud';

  const pct = Math.round(((curIdx + 1) / KEYS.length) * 100);
  document.getElementById('pBar').style.width = pct + '%';
  document.getElementById('navInfo').innerHTML =
    '<strong>' + (curIdx + 1) + '</strong> / ' + KEYS.length;
  document.getElementById('prevBtn').disabled = curIdx === 0;
  document.getElementById('nextBtn').disabled = curIdx === KEYS.length - 1;

  const list = document.getElementById('qList');
  list.innerHTML = '';

  if (!qs.length) {{
    list.innerHTML =
      '<div class="empty">' + icons.info + '<p>Bu bilet uchun ma\u02bcluomot yo\u02bcq.</p></div>';
    return;
  }}

  qs.forEach(function(q, i) {{
    const hasAns = q.javob !== 'Javob mavjud emas';
    const card = document.createElement('div');
    card.className = 'qcard';
    card.id = 'qc' + i;

    const savol = esc(q.savol || ('Savol ' + q.savol_raqami));

    let noTag = hasAns ? '' :
      '<span class="no-ans-tag">' + icons.warn + 'Javob yo\u02bcq</span>';

    let bodyHtml = '';
    if (hasAns) {{
      bodyHtml =
        '<span class="ans-label">' + icons.check + 'Javob</span>' +
        '<div class="ans-text">' + esc(q.javob) + '</div>';
    }} else {{
      bodyHtml =
        '<div class="no-ans-msg">' + icons.warn +
        '<span>Bu savol uchun javob hozircha kiritilmagan.</span></div>';
    }}

    card.innerHTML =
      '<div class="qcard-header" onclick="toggle(' + i + ')">' +
        '<div class="q-badge">' + q.savol_raqami + '</div>' +
        '<div class="q-title">' + savol + '</div>' +
        noTag +
        '<div class="q-chevron">' + icons.down + '</div>' +
      '</div>' +
      '<div class="qcard-body">' +
        '<div class="qcard-answer">' + bodyHtml + '</div>' +
      '</div>';

    list.appendChild(card);
  }});
}}

function toggle(i) {{
  document.getElementById('qc' + i).classList.toggle('open');
}}

function navigate(dir) {{
  const ni = curIdx + dir;
  if (ni < 0 || ni >= KEYS.length) return;
  curIdx = ni;
  renderBilet(KEYS[curIdx]);
  window.scrollTo({{top:0, behavior:'smooth'}});
}}

function goBack() {{
  document.getElementById('s2').classList.remove('active');
  document.getElementById('s1').classList.add('active');
  window.scrollTo({{top:0, behavior:'smooth'}});
}}

function esc(s) {{
  return String(s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}}
</script>
</body>
</html>"""

with open(r'D:\Farangiz\metodica\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

size = len(html.encode('utf-8'))
print(f'index.html yaratildi! ({size//1024} KB)')
print(f'Biletlar: {total_bilets} | Savollar: {total_q} | Javoblar: {total_with_answer}')
