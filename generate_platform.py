import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\Farangiz\metodica\bilets_clean.json', 'r', encoding='utf-8') as f:
    bilets = json.load(f)

bilets_sorted = {int(k): v for k, v in bilets.items()}
json_str = json.dumps(bilets_sorted, ensure_ascii=False)

total_bilets = len(bilets_sorted)
total_q = sum(len(v) for v in bilets_sorted.values())

html = f"""<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Metodika — Ta'lim Platformasi</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap" rel="stylesheet">
<script type="application/json" id="biletData">{json_str}</script>
<style>
/* ════════════════════════════════════════
   DESIGN TOKENS
════════════════════════════════════════ */
:root {{
  --bg:        #070711;
  --bg2:       #0d0d1e;
  --bg3:       #111128;
  --surface:   #161630;
  --surface2:  #1c1c3a;
  --surface3:  #212145;
  --border:    #1e1e3f;
  --border2:   #272752;
  --violet:    #6366f1;
  --violet-d:  #4f52c4;
  --violet-l:  #818cf8;
  --sky:       #0ea5e9;
  --sky-l:     #38bdf8;
  --teal:      #14b8a6;
  --green:     #22c55e;
  --green-d:   #16a34a;
  --amber:     #f59e0b;
  --red:       #ef4444;
  --txt:       #f1f5f9;
  --txt2:      #cbd5e1;
  --txt3:      #94a3b8;
  --txt4:      #64748b;
  --txt5:      #475569;
  --r-sm:      8px;
  --r-md:      12px;
  --r-lg:      16px;
  --r-xl:      22px;
  --shadow:    0 4px 24px rgba(0,0,0,.4);
  --shadow-lg: 0 12px 48px rgba(0,0,0,.5);
}}

/* ════════════════════════════════════════
   RESET & BASE
════════════════════════════════════════ */
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{
  font-family:'Inter',system-ui,sans-serif;
  background:var(--bg);
  color:var(--txt);
  min-height:100vh;
  overflow-x:hidden;
  font-size:15px;
  line-height:1.6;
}}
button{{cursor:pointer;font-family:inherit;border:none;background:none;}}
input{{font-family:inherit;}}

/* ════════════════════════════════════════
   ANIMATED BACKGROUND
════════════════════════════════════════ */
.bg-art{{
  position:fixed;inset:0;z-index:0;
  overflow:hidden;pointer-events:none;
}}
.glow{{
  position:absolute;border-radius:50%;
  filter:blur(100px);opacity:.055;
  animation:glow-drift 18s ease-in-out infinite alternate;
}}
.g1{{width:700px;height:700px;background:#6366f1;top:-200px;left:-200px;}}
.g2{{width:600px;height:600px;background:#0ea5e9;bottom:-200px;right:-200px;animation-delay:-7s;}}
.g3{{width:450px;height:450px;background:#14b8a6;top:30%;left:30%;animation-delay:-3s;}}
@keyframes glow-drift{{
  0%{{transform:translate(0,0) scale(1);}}
  100%{{transform:translate(50px,30px) scale(1.2);}}
}}

/* ════════════════════════════════════════
   LAYOUT WRAPPER
════════════════════════════════════════ */
.app{{position:relative;z-index:1;}}

/* ════════════════════════════════════════
   PAGE: LOGIN
════════════════════════════════════════ */
#page-login{{
  display:flex;align-items:center;justify-content:center;
  min-height:100vh;padding:20px;
}}
.login-box{{
  width:100%;max-width:420px;
  background:var(--surface);
  border:1px solid var(--border2);
  border-radius:var(--r-xl);
  padding:40px;
  box-shadow:var(--shadow-lg);
  animation:fadeUp .5s ease both;
}}
.login-logo{{
  display:flex;align-items:center;justify-content:center;
  width:64px;height:64px;border-radius:18px;
  background:linear-gradient(135deg,#6366f1,#0ea5e9);
  margin:0 auto 24px;
  box-shadow:0 8px 32px rgba(99,102,241,.4);
}}
.login-logo svg{{width:30px;height:30px;color:#fff;}}
.login-box h2{{
  text-align:center;font-size:1.5rem;font-weight:800;
  margin-bottom:6px;letter-spacing:-0.3px;
}}
.login-box .sub{{
  text-align:center;color:var(--txt4);font-size:.88rem;
  margin-bottom:32px;
}}
.form-group{{margin-bottom:18px;}}
.form-label{{
  display:block;font-size:.82rem;font-weight:600;
  color:var(--txt3);margin-bottom:7px;letter-spacing:.3px;
  text-transform:uppercase;
}}
.form-input{{
  width:100%;padding:12px 16px;
  background:var(--surface2);
  border:1.5px solid var(--border2);
  border-radius:var(--r-md);
  color:var(--txt);font-size:.95rem;outline:none;
  transition:border-color .2s,box-shadow .2s,background .2s;
}}
.form-input:focus{{
  border-color:var(--violet);
  background:var(--surface3);
  box-shadow:0 0 0 3px rgba(99,102,241,.15);
}}
.form-input::placeholder{{color:var(--txt5);}}
.btn-primary{{
  width:100%;padding:13px;
  background:linear-gradient(135deg,var(--violet),var(--sky));
  border:none;border-radius:var(--r-md);
  color:#fff;font-size:.95rem;font-weight:700;
  letter-spacing:.3px;
  transition:opacity .2s,transform .15s,box-shadow .2s;
  box-shadow:0 4px 20px rgba(99,102,241,.4);
}}
.btn-primary:hover{{opacity:.9;box-shadow:0 6px 28px rgba(99,102,241,.5);}}
.btn-primary:active{{transform:scale(.98);}}
.btn-primary:disabled{{opacity:.4;cursor:not-allowed;transform:none;}}

.users-prev{{margin-top:28px;}}
.users-prev-label{{
  font-size:.75rem;color:var(--txt4);font-weight:600;
  text-transform:uppercase;letter-spacing:.5px;
  margin-bottom:10px;display:block;
}}
.user-prev-list{{display:flex;flex-direction:column;gap:8px;}}
.user-prev-item{{
  display:flex;align-items:center;gap:10px;
  padding:10px 14px;
  background:var(--bg3);border:1px solid var(--border);
  border-radius:var(--r-md);cursor:pointer;
  transition:border-color .2s,background .2s;
}}
.user-prev-item:hover{{border-color:var(--violet-l);background:var(--surface2);}}
.user-av-sm{{
  width:32px;height:32px;border-radius:9px;
  display:flex;align-items:center;justify-content:center;
  font-size:.8rem;font-weight:800;color:#fff;flex-shrink:0;
}}
.user-prev-name{{font-size:.88rem;font-weight:600;color:var(--txt);flex:1;}}
.user-prev-stats{{font-size:.74rem;color:var(--txt4);}}

/* ════════════════════════════════════════
   PAGE: MAIN APP
════════════════════════════════════════ */
#page-app{{display:none;flex-direction:column;min-height:100vh;}}

/* ── TOPBAR ── */
.topbar{{
  position:sticky;top:0;z-index:100;
  background:rgba(7,7,17,.88);
  backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);
  padding:0 24px;
  height:62px;
  display:flex;align-items:center;gap:16px;
}}
.topbar-brand{{
  display:flex;align-items:center;gap:10px;flex-shrink:0;
}}
.topbar-icon{{
  width:36px;height:36px;border-radius:10px;
  background:linear-gradient(135deg,#6366f1,#0ea5e9);
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 2px 12px rgba(99,102,241,.35);
}}
.topbar-icon svg{{width:18px;height:18px;color:#fff;}}
.topbar-brand-name{{
  font-size:1.05rem;font-weight:800;
  background:linear-gradient(135deg,#818cf8,#38bdf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}}
.topbar-spacer{{flex:1;}}

/* Back button in topbar */
.topbar-back{{
  display:none;align-items:center;gap:7px;
  padding:7px 14px;
  background:var(--surface2);border:1px solid var(--border2);
  border-radius:var(--r-sm);
  color:var(--txt3);font-size:.85rem;font-weight:600;
  transition:all .2s;
}}
.topbar-back:hover{{border-color:var(--violet-l);color:var(--txt);}}
.topbar-back svg{{width:15px;height:15px;}}
.topbar-back.visible{{display:flex;}}

.topbar-right{{display:flex;align-items:center;gap:10px;}}

/* User avatar */
.user-pill{{
  display:flex;align-items:center;gap:8px;
  padding:5px 12px 5px 5px;
  background:var(--surface2);border:1px solid var(--border2);
  border-radius:100px;cursor:pointer;
  transition:all .2s;
  position:relative;
}}
.user-pill:hover{{border-color:var(--violet-l);}}
.user-av{{
  width:28px;height:28px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:.72rem;font-weight:800;color:#fff;flex-shrink:0;
}}
.user-name{{font-size:.82rem;font-weight:600;color:var(--txt2);max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}}

/* User dropdown */
.user-menu{{
  position:absolute;top:calc(100% + 8px);right:0;
  background:var(--surface);border:1px solid var(--border2);
  border-radius:var(--r-lg);
  width:220px;
  box-shadow:var(--shadow-lg);
  padding:8px;
  display:none;z-index:200;
  animation:fadeDown .2s ease;
}}
.user-menu.open{{display:block;}}
@keyframes fadeDown{{from{{opacity:0;transform:translateY(-8px);}}to{{opacity:1;transform:translateY(0);}}}}
.user-menu-header{{
  padding:10px 12px 12px;
  border-bottom:1px solid var(--border);
  margin-bottom:6px;
}}
.user-menu-name{{font-size:.9rem;font-weight:700;color:var(--txt);}}
.user-menu-sub{{font-size:.75rem;color:var(--txt4);margin-top:2px;}}
.menu-item{{
  display:flex;align-items:center;gap:10px;
  padding:9px 12px;border-radius:var(--r-sm);
  color:var(--txt3);font-size:.85rem;font-weight:500;
  cursor:pointer;transition:all .15s;
}}
.menu-item:hover{{background:var(--surface2);color:var(--txt);}}
.menu-item svg{{width:15px;height:15px;flex-shrink:0;}}
.menu-item.danger{{color:#f87171;}}
.menu-item.danger:hover{{background:rgba(239,68,68,.1);color:#f87171;}}

/* ── MAIN CONTENT ── */
.main{{flex:1;padding:28px 24px 60px;max-width:1100px;margin:0 auto;width:100%;}}

/* ════════════════════════════════════════
   VIEW: DASHBOARD
════════════════════════════════════════ */
#view-dashboard{{}}

/* Hero greeting */
.hero{{
  background:var(--surface);
  border:1px solid var(--border2);
  border-radius:var(--r-xl);
  padding:28px 32px;
  margin-bottom:24px;
  display:flex;align-items:center;gap:24px;
  overflow:hidden;position:relative;
}}
.hero::before{{
  content:'';position:absolute;right:-60px;top:-60px;
  width:300px;height:300px;border-radius:50%;
  background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(14,165,233,.08));
  pointer-events:none;
}}
.hero-avatar{{
  width:60px;height:60px;border-radius:16px;
  display:flex;align-items:center;justify-content:center;
  font-size:1.4rem;font-weight:900;color:#fff;flex-shrink:0;
  box-shadow:0 8px 24px rgba(99,102,241,.35);
}}
.hero-text h2{{
  font-size:1.25rem;font-weight:800;
  margin-bottom:3px;letter-spacing:-.3px;
}}
.hero-text p{{color:var(--txt4);font-size:.88rem;}}
.hero-progress{{
  margin-left:auto;text-align:right;flex-shrink:0;
}}
.hero-pct{{
  font-size:2rem;font-weight:900;
  background:linear-gradient(135deg,#818cf8,#38bdf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;line-height:1;
}}
.hero-pct-lbl{{font-size:.75rem;color:var(--txt4);margin-top:3px;}}

/* Stats row */
.stats-row{{
  display:grid;grid-template-columns:repeat(4,1fr);
  gap:12px;margin-bottom:28px;
}}
.stat-card{{
  background:var(--surface);border:1px solid var(--border2);
  border-radius:var(--r-lg);padding:18px 20px;
  transition:border-color .2s,transform .2s;
}}
.stat-card:hover{{border-color:var(--border2);transform:translateY(-2px);}}
.stat-icon{{
  width:36px;height:36px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  margin-bottom:12px;
}}
.stat-icon svg{{width:18px;height:18px;}}
.si-violet{{background:rgba(99,102,241,.15);color:var(--violet-l);}}
.si-sky{{background:rgba(14,165,233,.15);color:var(--sky-l);}}
.si-green{{background:rgba(34,197,94,.15);color:#4ade80;}}
.si-amber{{background:rgba(245,158,11,.15);color:#fbbf24;}}
.stat-val{{font-size:1.6rem;font-weight:900;line-height:1;margin-bottom:4px;}}
.stat-lbl{{font-size:.75rem;color:var(--txt4);font-weight:500;}}

/* Progress bar */
.overall-progress{{
  background:var(--surface);border:1px solid var(--border2);
  border-radius:var(--r-lg);padding:20px 24px;margin-bottom:28px;
}}
.op-header{{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:14px;
}}
.op-title{{font-size:.9rem;font-weight:700;color:var(--txt2);}}
.op-val{{font-size:.9rem;font-weight:700;color:var(--violet-l);}}
.pbar-track{{
  height:8px;background:var(--surface3);border-radius:100px;overflow:hidden;
}}
.pbar-fill{{
  height:100%;border-radius:100px;
  background:linear-gradient(90deg,var(--violet),var(--sky));
  transition:width .8s cubic-bezier(.4,0,.2,1);
}}
.pbar-milestones{{
  display:flex;justify-content:space-between;
  margin-top:8px;
}}
.pbar-m{{font-size:.7rem;color:var(--txt5);}}

/* Filter tabs */
.filter-tabs{{
  display:flex;align-items:center;gap:8px;
  margin-bottom:20px;flex-wrap:wrap;
}}
.filter-label{{
  font-size:.82rem;font-weight:700;color:var(--txt4);
  margin-right:4px;text-transform:uppercase;letter-spacing:.5px;
}}
.ftab{{
  padding:6px 16px;border-radius:100px;
  border:1.5px solid var(--border2);
  background:transparent;
  color:var(--txt4);font-size:.82rem;font-weight:600;
  transition:all .2s;cursor:pointer;
}}
.ftab.active{{
  background:var(--violet);border-color:var(--violet);
  color:#fff;
  box-shadow:0 2px 12px rgba(99,102,241,.35);
}}
.ftab:not(.active):hover{{border-color:var(--violet-l);color:var(--txt);}}

.search-filter{{
  margin-left:auto;
  position:relative;
}}
.search-filter input{{
  padding:7px 14px 7px 36px;
  background:var(--surface2);border:1.5px solid var(--border2);
  border-radius:100px;color:var(--txt);font-size:.82rem;
  outline:none;width:180px;
  transition:all .2s;
}}
.search-filter input:focus{{
  border-color:var(--violet);width:220px;
  box-shadow:0 0 0 3px rgba(99,102,241,.12);
}}
.search-filter input::placeholder{{color:var(--txt5);}}
.search-filter svg{{
  position:absolute;left:11px;top:50%;transform:translateY(-50%);
  width:15px;height:15px;color:var(--txt4);pointer-events:none;
}}

/* Bilet grid */
.bilet-grid{{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(220px,1fr));
  gap:12px;
}}
.bcard{{
  background:var(--surface);border:1.5px solid var(--border2);
  border-radius:var(--r-lg);padding:20px;
  cursor:pointer;
  transition:all .3s cubic-bezier(.34,1.56,.64,1);
  position:relative;overflow:hidden;
}}
.bcard::after{{
  content:'';position:absolute;inset:0;
  border-radius:var(--r-lg);
  background:linear-gradient(135deg,rgba(99,102,241,.06),rgba(14,165,233,.03));
  opacity:0;transition:opacity .2s;
}}
.bcard:hover{{
  transform:translateY(-4px);
  border-color:rgba(99,102,241,.4);
  box-shadow:0 12px 36px rgba(99,102,241,.15);
}}
.bcard:hover::after{{opacity:1;}}
.bcard:active{{transform:translateY(-1px) scale(.99);}}

/* Status indicator */
.bcard-status{{
  position:absolute;top:14px;right:14px;
  display:flex;align-items:center;gap:5px;
  padding:3px 9px;border-radius:100px;
  font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.5px;
}}
.status-read{{background:rgba(34,197,94,.12);color:#4ade80;border:1px solid rgba(34,197,94,.2);}}
.status-unread{{background:rgba(99,102,241,.1);color:#818cf8;border:1px solid rgba(99,102,241,.15);}}
.status-partial{{background:rgba(245,158,11,.1);color:#fbbf24;border:1px solid rgba(245,158,11,.15);}}

.bcard-num{{
  font-size:2.2rem;font-weight:900;line-height:1;
  background:linear-gradient(135deg,#c4b5fd,#67e8f9);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin-bottom:4px;
}}
.bcard-lbl{{
  font-size:.65rem;color:var(--txt5);
  text-transform:uppercase;letter-spacing:1.5px;font-weight:600;
  margin-bottom:14px;
}}

/* Mini progress bar on card */
.bcard-bar{{
  height:3px;background:var(--surface3);border-radius:100px;
  overflow:hidden;margin-bottom:10px;
}}
.bcard-bar-fill{{
  height:100%;border-radius:100px;
  background:linear-gradient(90deg,var(--violet),var(--sky));
  transition:width .4s ease;
}}
.bcard-meta{{
  display:flex;align-items:center;justify-content:space-between;
}}
.bcard-q-count{{
  display:flex;align-items:center;gap:5px;
  font-size:.75rem;color:var(--txt4);font-weight:500;
}}
.bcard-q-count svg{{width:13px;height:13px;}}
.bcard-time{{
  font-size:.7rem;color:var(--txt5);
}}

/* Empty */
.empty-grid{{
  grid-column:1/-1;text-align:center;
  padding:60px 20px;color:var(--txt4);
}}
.empty-grid svg{{width:48px;height:48px;opacity:.3;margin-bottom:12px;}}

/* ════════════════════════════════════════
   VIEW: BILET READER
════════════════════════════════════════ */
#view-bilet{{display:none;}}

.reader-header{{
  background:var(--surface);border:1px solid var(--border2);
  border-radius:var(--r-xl);padding:24px 28px;
  margin-bottom:20px;
  display:flex;align-items:center;gap:20px;
}}
.reader-num{{
  width:56px;height:56px;border-radius:16px;
  background:linear-gradient(135deg,var(--violet),var(--sky));
  display:flex;align-items:center;justify-content:center;
  font-size:1.3rem;font-weight:900;color:#fff;flex-shrink:0;
  box-shadow:0 6px 20px rgba(99,102,241,.35);
}}
.reader-info{{flex:1;}}
.reader-info h2{{font-size:1.2rem;font-weight:800;margin-bottom:3px;}}
.reader-info p{{font-size:.82rem;color:var(--txt4);}}
.reader-status-badge{{
  display:flex;align-items:center;gap:7px;
  padding:7px 14px;border-radius:100px;
  font-size:.8rem;font-weight:700;
}}
.rsb-read{{background:rgba(34,197,94,.12);color:#4ade80;border:1px solid rgba(34,197,94,.2);}}
.rsb-unread{{background:rgba(99,102,241,.1);color:#818cf8;border:1px solid rgba(99,102,241,.15);}}
.rsb-read svg,.rsb-unread svg{{width:14px;height:14px;}}

/* Bilet navigation strip */
.bilet-nav-strip{{
  display:flex;align-items:center;gap:10px;
  margin-bottom:20px;
}}
.nav-strip-btn{{
  display:flex;align-items:center;gap:6px;
  padding:9px 18px;
  background:var(--surface);border:1px solid var(--border2);
  border-radius:var(--r-md);
  color:var(--txt3);font-size:.84rem;font-weight:600;
  transition:all .2s;
}}
.nav-strip-btn:hover:not(:disabled){{border-color:var(--violet-l);color:var(--txt);}}
.nav-strip-btn:disabled{{opacity:.25;cursor:default;}}
.nav-strip-btn svg{{width:15px;height:15px;}}
.nav-strip-center{{flex:1;text-align:center;}}
.nav-strip-pips{{
  display:flex;justify-content:center;gap:5px;flex-wrap:wrap;
  max-width:400px;margin:0 auto;
}}
.pip{{
  width:28px;height:28px;border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:.7rem;font-weight:700;cursor:pointer;
  border:1.5px solid var(--border2);
  color:var(--txt4);transition:all .2s;
  background:var(--surface);
}}
.pip:hover{{border-color:var(--violet-l);color:var(--txt);}}
.pip.current{{background:var(--violet);border-color:var(--violet);color:#fff;}}
.pip.done{{background:rgba(34,197,94,.15);border-color:rgba(34,197,94,.3);color:#4ade80;}}

/* Questions */
.q-list{{display:flex;flex-direction:column;gap:10px;margin-bottom:20px;}}

.qcard{{
  background:var(--surface);border:1.5px solid var(--border2);
  border-radius:var(--r-lg);overflow:hidden;
  transition:border-color .25s,box-shadow .25s;
}}
.qcard.open{{
  border-color:rgba(99,102,241,.35);
  box-shadow:0 6px 32px rgba(99,102,241,.1);
}}
.qcard-head{{
  display:flex;align-items:flex-start;gap:14px;
  padding:18px 20px;cursor:pointer;
  transition:background .15s;user-select:none;
}}
.qcard-head:hover{{background:rgba(99,102,241,.04);}}
.q-num{{
  width:36px;height:36px;border-radius:10px;flex-shrink:0;
  background:linear-gradient(135deg,var(--violet),var(--violet-d));
  display:flex;align-items:center;justify-content:center;
  font-size:.85rem;font-weight:800;
  box-shadow:0 3px 12px rgba(99,102,241,.35);
}}
.q-title{{flex:1;font-size:.9rem;font-weight:600;color:var(--txt);line-height:1.45;padding-top:1px;}}
.q-tags{{display:flex;align-items:center;gap:7px;flex-shrink:0;}}
.q-no-ans{{
  display:flex;align-items:center;gap:4px;
  padding:2px 9px;border-radius:100px;
  background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);
  color:#f87171;font-size:.65rem;font-weight:700;
}}
.q-no-ans svg,.q-read-tag svg{{width:10px;height:10px;}}
.q-read-tag{{
  display:flex;align-items:center;gap:4px;
  padding:2px 9px;border-radius:100px;
  background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);
  color:#4ade80;font-size:.65rem;font-weight:700;
}}
.q-chevron{{
  color:var(--txt5);flex-shrink:0;margin-top:2px;
  transition:transform .3s cubic-bezier(.34,1.56,.64,1),color .2s;
}}
.q-chevron svg{{width:17px;height:17px;display:block;}}
.qcard.open .q-chevron{{transform:rotate(180deg);color:var(--violet-l);}}

.qcard-body{{
  max-height:0;overflow:hidden;
  transition:max-height .45s cubic-bezier(.4,0,.2,1);
}}
.qcard.open .qcard-body{{max-height:6000px;}}
.qcard-inner{{
  border-top:1px solid var(--border2);
  padding:20px 20px 24px 20px;
}}
.ans-tag{{
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(20,184,166,.1);border:1px solid rgba(20,184,166,.2);
  color:#2dd4bf;border-radius:var(--r-sm);
  padding:4px 12px;font-size:.68rem;font-weight:700;
  text-transform:uppercase;letter-spacing:.8px;margin-bottom:14px;
}}
.ans-tag svg{{width:11px;height:11px;}}
.ans-text{{
  color:var(--txt2);font-size:.9rem;line-height:1.95;
  white-space:pre-wrap;word-break:break-word;
}}
.no-ans-box{{
  display:flex;align-items:center;gap:10px;
  padding:14px 16px;
  background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.12);
  border-radius:var(--r-md);
  color:#f87171;font-size:.86rem;
}}
.no-ans-box svg{{width:16px;height:16px;flex-shrink:0;}}

/* Mark read button */
.mark-read-row{{
  display:flex;justify-content:flex-end;margin-top:14px;
}}
.btn-mark{{
  display:flex;align-items:center;gap:7px;
  padding:9px 18px;border-radius:var(--r-md);
  font-size:.82rem;font-weight:700;
  transition:all .2s;
  border:1.5px solid transparent;
}}
.btn-mark-done{{
  background:linear-gradient(135deg,#059669,#0d9488);
  color:#fff;border-color:transparent;
  box-shadow:0 3px 14px rgba(5,150,105,.3);
}}
.btn-mark-done:hover{{box-shadow:0 5px 18px rgba(5,150,105,.4);}}
.btn-mark-undo{{
  background:transparent;
  color:var(--txt4);border-color:var(--border2);
}}
.btn-mark-undo:hover{{border-color:var(--red);color:#f87171;}}
.btn-mark svg{{width:15px;height:15px;}}

/* ════════════════════════════════════════
   UTILITIES & ANIMATIONS
════════════════════════════════════════ */
.hidden{{display:none!important;}}
@keyframes fadeUp{{
  from{{opacity:0;transform:translateY(20px);}}
  to{{opacity:1;transform:translateY(0);}}
}}
@keyframes fadeIn{{
  from{{opacity:0;}}to{{opacity:1;}}
}}
.fade-in{{animation:fadeIn .3s ease both;}}
.fade-up{{animation:fadeUp .35s ease both;}}

/* ════════════════════════════════════════
   RESPONSIVE
════════════════════════════════════════ */
@media(max-width:900px){{
  .stats-row{{grid-template-columns:repeat(2,1fr);}}
  .bilet-grid{{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));}}
}}
@media(max-width:600px){{
  .topbar{{padding:0 14px;}}
  .main{{padding:18px 14px 48px;}}
  .hero{{padding:20px;flex-wrap:wrap;}}
  .hero-progress{{margin-left:0;}}
  .stats-row{{grid-template-columns:repeat(2,1fr);gap:8px;}}
  .bilet-grid{{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;}}
  .reader-header{{flex-wrap:wrap;padding:18px;}}
  .nav-strip-pips{{max-width:280px;}}
  .search-filter input{{width:130px;}}
  .search-filter input:focus{{width:160px;}}
  .user-name{{display:none;}}
  .login-box{{padding:28px 24px;}}
}}
</style>
</head>
<body>
<div class="bg-art">
  <div class="glow g1"></div>
  <div class="glow g2"></div>
  <div class="glow g3"></div>
</div>

<!-- ════════════════════════════════════
     PAGE: LOGIN
════════════════════════════════════ -->
<div class="app" id="page-login">
  <div class="login-box">
    <div class="login-logo">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
      </svg>
    </div>
    <h2>Metodika Platformasi</h2>
    <p class="sub">Ismingizni kiriting va o&#x2bc;rganishni boshlang</p>

    <div class="form-group">
      <label class="form-label" for="nameInput">To&#x2bc;liq ismingiz</label>
      <input class="form-input" type="text" id="nameInput" placeholder="Masalan: Aziza Karimova" autocomplete="off" maxlength="50">
    </div>
    <button class="btn-primary" id="loginBtn" onclick="doLogin()" disabled>
      Kirish
      <svg style="width:15px;height:15px;margin-left:6px;vertical-align:middle;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12h14M12 5l7 7-7 7"/>
      </svg>
    </button>

    <div class="users-prev" id="prevUsersList"></div>
  </div>
</div>

<!-- ════════════════════════════════════
     PAGE: APP
════════════════════════════════════ -->
<div class="app" id="page-app">

  <!-- TOPBAR -->
  <nav class="topbar">
    <div class="topbar-brand">
      <div class="topbar-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
          <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
        </svg>
      </div>
      <span class="topbar-brand-name">Metodika</span>
    </div>

    <button class="topbar-back" id="topbarBack" onclick="showDashboard()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M5 12l7-7M5 12l7 7"/></svg>
      Barcha biletlar
    </button>

    <div class="topbar-spacer"></div>

    <div class="topbar-right">
      <div class="user-pill" onclick="toggleUserMenu()">
        <div class="user-av" id="topbarAv"></div>
        <span class="user-name" id="topbarName"></span>
        <svg style="width:13px;height:13px;color:var(--txt4);margin-left:2px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        <div class="user-menu" id="userMenu">
          <div class="user-menu-header">
            <div class="user-menu-name" id="menuName"></div>
            <div class="user-menu-sub" id="menuSub"></div>
          </div>
          <div class="menu-item" onclick="resetProgress()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.5"/></svg>
            Progressni tozalash
          </div>
          <div class="menu-item danger" onclick="switchUser()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Boshqa foydalanuvchi
          </div>
        </div>
      </div>
    </div>
  </nav>

  <!-- MAIN -->
  <main class="main">

    <!-- ─── DASHBOARD VIEW ─── -->
    <div id="view-dashboard">

      <!-- Hero -->
      <div class="hero fade-up">
        <div class="hero-avatar" id="heroAv"></div>
        <div class="hero-text">
          <h2 id="heroGreet">Xush kelibsiz!</h2>
          <p id="heroSub"></p>
        </div>
        <div class="hero-progress">
          <div class="hero-pct" id="heroPct">0%</div>
          <div class="hero-pct-lbl">o&#x2bc;qildi</div>
        </div>
      </div>

      <!-- Stats -->
      <div class="stats-row fade-up" style="animation-delay:.05s">
        <div class="stat-card">
          <div class="stat-icon si-violet">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
          </div>
          <div class="stat-val" id="st-total">{total_bilets}</div>
          <div class="stat-lbl">Jami biletlar</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon si-green">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
          <div class="stat-val" id="st-read">0</div>
          <div class="stat-lbl">O&#x2bc;qilgan</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon si-amber">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <div class="stat-val" id="st-left">0</div>
          <div class="stat-lbl">Qolgan</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon si-sky">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          </div>
          <div class="stat-val" id="st-streak">0</div>
          <div class="stat-lbl">Bugun o&#x2bc;qildi</div>
        </div>
      </div>

      <!-- Progress bar -->
      <div class="overall-progress fade-up" style="animation-delay:.1s">
        <div class="op-header">
          <span class="op-title">Umumiy progress</span>
          <span class="op-val" id="opVal">0 / {total_bilets}</span>
        </div>
        <div class="pbar-track">
          <div class="pbar-fill" id="mainPbar" style="width:0%"></div>
        </div>
        <div class="pbar-milestones">
          <span class="pbar-m">Boshlang&#x2bc;ich</span>
          <span class="pbar-m">25%</span>
          <span class="pbar-m">50%</span>
          <span class="pbar-m">75%</span>
          <span class="pbar-m">Yakuniy</span>
        </div>
      </div>

      <!-- Filters & search -->
      <div class="filter-tabs fade-up" style="animation-delay:.15s">
        <span class="filter-label">Ko&#x2bc;rish:</span>
        <button class="ftab active" data-filter="all" onclick="setFilter('all',this)">Hammasi</button>
        <button class="ftab" data-filter="unread" onclick="setFilter('unread',this)">O&#x2bc;qilmagan</button>
        <button class="ftab" data-filter="read" onclick="setFilter('read',this)">O&#x2bc;qilgan</button>
        <div class="search-filter">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input type="text" id="gridSearch" placeholder="Bilet raqami..." oninput="applyFilters()">
        </div>
      </div>

      <!-- Grid -->
      <div class="bilet-grid fade-up" id="biletGrid" style="animation-delay:.2s"></div>
    </div>

    <!-- ─── BILET READER VIEW ─── -->
    <div id="view-bilet">

      <div class="reader-header fade-up">
        <div class="reader-num" id="rNum"></div>
        <div class="reader-info">
          <h2 id="rTitle"></h2>
          <p id="rSub"></p>
        </div>
        <div class="reader-status-badge" id="rStatusBadge"></div>
      </div>

      <!-- Nav strip -->
      <div class="bilet-nav-strip">
        <button class="nav-strip-btn" id="prevBiletBtn" onclick="navigateBilet(-1)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>
          Oldingi
        </button>
        <div class="nav-strip-center">
          <div class="nav-strip-pips" id="navPips"></div>
        </div>
        <button class="nav-strip-btn" id="nextBiletBtn" onclick="navigateBilet(1)">
          Keyingi
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M9 18l6-6-6-6"/></svg>
        </button>
      </div>

      <!-- Questions -->
      <div class="q-list" id="qList"></div>

      <!-- Mark read action -->
      <div class="mark-read-row" id="markReadRow"></div>

    </div>

  </main>
</div>

<script>
// ═══════════════════════════════
// DATA
// ═══════════════════════════════
const BILETS = JSON.parse(document.getElementById('biletData').textContent);
const KEYS = Object.keys(BILETS).map(Number).sort((a,b)=>a-b);
const TOTAL = KEYS.length;

// ═══════════════════════════════
// STATE
// ═══════════════════════════════
let currentUser = null;
let progress = {{}};   // {{biletNum: {{read:bool, readAt: ts, openedAt: ts}}}}
let allUsers = [];     // [{{name, joinedAt, color}}]
let currentBilet = null;
let currentFilter = 'all';

// ═══════════════════════════════
// COLORS for avatars
// ═══════════════════════════════
const COLORS = ['#6366f1','#0ea5e9','#14b8a6','#f59e0b','#ec4899','#8b5cf6','#22c55e','#f97316'];
function colorFor(name) {{
  let h = 0;
  for(let i=0;i<name.length;i++) h = (h*31 + name.charCodeAt(i)) & 0xffffffff;
  return COLORS[Math.abs(h) % COLORS.length];
}}
function initials(name) {{
  return name.trim().split(' ').slice(0,2).map(w=>w[0]||'').join('').toUpperCase() || name[0].toUpperCase();
}}

// ═══════════════════════════════
// STORAGE
// ═══════════════════════════════
const SK_USERS     = 'mtk_users';
const SK_CUR_USER  = 'mtk_current';
function getProgress(userName) {{
  return JSON.parse(localStorage.getItem('mtk_prog_' + userName) || '{{}}');
}}
function saveProgress(userName, prog) {{
  localStorage.setItem('mtk_prog_' + userName, JSON.stringify(prog));
}}
function loadAllUsers() {{
  return JSON.parse(localStorage.getItem(SK_USERS) || '[]');
}}
function saveAllUsers(list) {{
  localStorage.setItem(SK_USERS, JSON.stringify(list));
}}

// ═══════════════════════════════
// LOGIN
// ═══════════════════════════════
document.getElementById('nameInput').addEventListener('input', function() {{
  document.getElementById('loginBtn').disabled = this.value.trim().length < 2;
}});
document.getElementById('nameInput').addEventListener('keydown', function(e) {{
  if(e.key==='Enter' && this.value.trim().length >= 2) doLogin();
}});

function showLoginPage() {{
  document.getElementById('page-login').style.display='flex';
  document.getElementById('page-app').style.display='none';
  renderPrevUsers();
}}

function renderPrevUsers() {{
  allUsers = loadAllUsers();
  const container = document.getElementById('prevUsersList');
  if(!allUsers.length) {{ container.innerHTML=''; return; }}
  const prog_items = allUsers.map(u => {{
    const p = getProgress(u.name);
    const readCount = KEYS.filter(k=>p[k]&&p[k].read).length;
    return {{...u, readCount}};
  }});
  container.innerHTML = `
    <span class="users-prev-label">
      <svg style="width:12px;height:12px;vertical-align:middle;margin-right:4px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      Oldingi foydalanuvchilar
    </span>
    <div class="user-prev-list">
      ${{prog_items.map(u=>`
        <div class="user-prev-item" onclick="loginAs('${{esc(u.name)}}')">
          <div class="user-av-sm" style="background:${{u.color}}">${{initials(u.name)}}</div>
          <div class="user-prev-name">${{esc(u.name)}}</div>
          <div class="user-prev-stats">${{u.readCount}}/${{TOTAL}} bilet</div>
        </div>
      `).join('')}}
    </div>
  `;
}}

function doLogin() {{
  const name = document.getElementById('nameInput').value.trim();
  if(name.length < 2) return;
  loginAs(name);
}}

function loginAs(name) {{
  allUsers = loadAllUsers();
  let user = allUsers.find(u=>u.name===name);
  if(!user) {{
    user = {{name, joinedAt: Date.now(), color: colorFor(name)}};
    allUsers.push(user);
    saveAllUsers(allUsers);
  }}
  localStorage.setItem(SK_CUR_USER, name);
  currentUser = user;
  progress = getProgress(name);
  enterApp();
}}

function enterApp() {{
  document.getElementById('page-login').style.display='none';
  document.getElementById('page-app').style.display='flex';
  document.getElementById('page-app').style.flexDirection='column';
  setupTopbar();
  showDashboard();
}}

// ═══════════════════════════════
// TOPBAR / USER MENU
// ═══════════════════════════════
function setupTopbar() {{
  const col = currentUser.color;
  const ini = initials(currentUser.name);
  document.getElementById('topbarAv').textContent = ini;
  document.getElementById('topbarAv').style.background = col;
  document.getElementById('topbarName').textContent = currentUser.name;
  document.getElementById('menuName').textContent = currentUser.name;
  const joined = new Date(currentUser.joinedAt);
  document.getElementById('menuSub').textContent = 
    "Qo'shilgan: " + joined.toLocaleDateString('uz-UZ');
}}

let menuOpen = false;
function toggleUserMenu() {{
  menuOpen = !menuOpen;
  document.getElementById('userMenu').classList.toggle('open', menuOpen);
}}
document.addEventListener('click', function(e) {{
  if(!e.target.closest('.user-pill')) {{
    menuOpen = false;
    document.getElementById('userMenu').classList.remove('open');
  }}
}});

function switchUser() {{
  localStorage.removeItem(SK_CUR_USER);
  document.getElementById('nameInput').value='';
  document.getElementById('loginBtn').disabled=true;
  showLoginPage();
}}

function resetProgress() {{
  if(!confirm('Progressingizni tozalashni tasdiqlaysizmi?')) return;
  progress = {{}};
  saveProgress(currentUser.name, progress);
  showDashboard();
  menuOpen=false;
  document.getElementById('userMenu').classList.remove('open');
}}

// ═══════════════════════════════
// DASHBOARD
// ═══════════════════════════════
function getStats() {{
  const readKeys = KEYS.filter(k => progress[k] && progress[k].read);
  const today = new Date(); today.setHours(0,0,0,0);
  const todayKeys = readKeys.filter(k => {{
    if(!progress[k].readAt) return false;
    const d = new Date(progress[k].readAt); d.setHours(0,0,0,0);
    return d.getTime()===today.getTime();
  }});
  return {{
    total: TOTAL,
    read: readKeys.length,
    left: TOTAL - readKeys.length,
    today: todayKeys.length,
    pct: Math.round((readKeys.length/TOTAL)*100)
  }};
}}

function showDashboard() {{
  document.getElementById('view-dashboard').style.display='block';
  document.getElementById('view-bilet').style.display='none';
  document.getElementById('topbarBack').classList.remove('visible');
  currentBilet = null;
  updateDashboard();
}}

function updateDashboard() {{
  const s = getStats();
  // Hero
  const now = new Date().getHours();
  const greet = now<12?'Xayrli tong':'now<17?'Xayrli kun':'Xayrli kech';
  document.getElementById('heroGreet').textContent = greet + ', ' + currentUser.name.split(' ')[0] + '!';
  document.getElementById('heroSub').textContent = s.read + ' ta bilet o\u02bcqildi, ' + s.left + ' ta qoldi.';
  document.getElementById('heroPct').textContent = s.pct + '%';
  document.getElementById('heroAv').textContent = initials(currentUser.name);
  document.getElementById('heroAv').style.background = currentUser.color;
  // Stats
  document.getElementById('st-read').textContent = s.read;
  document.getElementById('st-left').textContent = s.left;
  document.getElementById('st-streak').textContent = s.today;
  // Progress bar
  document.getElementById('mainPbar').style.width = s.pct + '%';
  document.getElementById('opVal').textContent = s.read + ' / ' + s.total;
  // Grid
  renderGrid();
}}

function setFilter(f, btn) {{
  currentFilter = f;
  document.querySelectorAll('.ftab').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  renderGrid();
}}

function applyFilters() {{
  renderGrid();
}}

function renderGrid() {{
  const search = document.getElementById('gridSearch').value.trim();
  const grid = document.getElementById('biletGrid');
  grid.innerHTML = '';

  let keys = KEYS.filter(k => {{
    if(search && !String(k).includes(search)) return false;
    const isRead = !!(progress[k] && progress[k].read);
    if(currentFilter==='read' && !isRead) return false;
    if(currentFilter==='unread' && isRead) return false;
    return true;
  }});

  if(!keys.length) {{
    grid.innerHTML = '<div class="empty-grid">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>' +
      '<p>Bilet topilmadi</p></div>';
    return;
  }}

  keys.forEach(k => {{
    const qs = BILETS[k];
    const prog = progress[k] || {{}};
    const isRead = !!prog.read;
    const openedAt = prog.openedAt ? new Date(prog.openedAt).toLocaleDateString('uz-UZ') : null;

    let statusClass, statusIcon, statusText;
    if(isRead) {{
      statusClass='status-read';
      statusIcon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:9px;height:9px"><polyline points="20 6 9 17 4 12"/></svg>';
      statusText="O'qildi";
    }} else if(openedAt) {{
      statusClass='status-partial';
      statusIcon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:9px;height:9px"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';
      statusText='Jarayonda';
    }} else {{
      statusClass='status-unread';
      statusIcon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:9px;height:9px"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>';
      statusText="O'qilmagan";
    }}

    const readPct = isRead ? 100 : (openedAt ? 40 : 0);

    const card = document.createElement('div');
    card.className = 'bcard';
    card.onclick = () => openBilet(k);
    card.innerHTML =
      '<div class="bcard-status ' + statusClass + '">' + statusIcon + statusText + '</div>' +
      '<div class="bcard-num">' + k + '</div>' +
      '<div class="bcard-lbl">Bilet</div>' +
      '<div class="bcard-bar"><div class="bcard-bar-fill" style="width:' + readPct + '%"></div></div>' +
      '<div class="bcard-meta">' +
        '<div class="bcard-q-count"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>' + qs.length + ' savol</div>' +
        (openedAt ? '<div class="bcard-time">' + openedAt + '</div>' : '') +
      '</div>';
    grid.appendChild(card);
  }});
}}

// ═══════════════════════════════
// BILET READER
// ═══════════════════════════════
function openBilet(num) {{
  currentBilet = num;
  // Track: mark as opened (not fully read yet)
  if(!progress[num]) progress[num] = {{}};
  if(!progress[num].openedAt) progress[num].openedAt = Date.now();
  saveProgress(currentUser.name, progress);

  document.getElementById('view-dashboard').style.display='none';
  document.getElementById('view-bilet').style.display='block';
  document.getElementById('topbarBack').classList.add('visible');
  renderReader(num);
}}

function renderReader(num) {{
  const qs = BILETS[num] || [];
  const prog = progress[num] || {{}};
  const isRead = !!prog.read;

  document.getElementById('rNum').textContent = num;
  document.getElementById('rTitle').textContent = num + '-Bilet';
  const withAns = qs.filter(q=>q.javob!=='Javob mavjud emas').length;
  document.getElementById('rSub').textContent = qs.length + ' ta savol \u2022 ' + withAns + ' ta javob mavjud';

  const badge = document.getElementById('rStatusBadge');
  if(isRead) {{
    badge.className='reader-status-badge rsb-read';
    badge.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:14px;height:14px"><polyline points="20 6 9 17 4 12"/></svg>O\u02bcqildi';
  }} else {{
    badge.className='reader-status-badge rsb-unread';
    badge.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:14px;height:14px"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>O\u02bcqilmagan';
  }}

  // Pips
  const pips = document.getElementById('navPips');
  pips.innerHTML = '';
  KEYS.slice(0, 30).forEach((k,i) => {{
    const isReadK = !!(progress[k] && progress[k].read);
    const pip = document.createElement('div');
    pip.className='pip' + (k===num?' current':'') + (isReadK?' done':'');
    pip.textContent = k;
    pip.title = 'Bilet ' + k;
    pip.onclick = () => {{ currentBilet=k; renderReader(k); }};
    pips.appendChild(pip);
  }});

  document.getElementById('prevBiletBtn').disabled = KEYS.indexOf(num)===0;
  document.getElementById('nextBiletBtn').disabled = KEYS.indexOf(num)===KEYS.length-1;

  // Questions
  const qList = document.getElementById('qList');
  qList.innerHTML = '';
  qs.forEach(function(q,i){{
    const hasAns = q.javob!=='Javob mavjud emas';
    const card = document.createElement('div');
    card.className='qcard';
    card.id='qc'+i;

    const noAnsTag = hasAns ? '' :
      '<span class="q-no-ans"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>Javob yo\u02bcq</span>';

    let bodyHtml;
    if(hasAns) {{
      bodyHtml = '<span class="ans-tag"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:11px;height:11px"><polyline points="20 6 9 17 4 12"/></svg>Javob</span>' +
        '<div class="ans-text">' + esc(q.javob) + '</div>';
    }} else {{
      bodyHtml = '<div class="no-ans-box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>' +
        'Bu savol uchun javob kiritilmagan.</div>';
    }}

    card.innerHTML =
      '<div class="qcard-head" onclick="toggleQ('+i+')">' +
        '<div class="q-num">'+q.savol_raqami+'</div>' +
        '<div class="q-title">'+esc(q.savol||'Savol '+q.savol_raqami)+'</div>' +
        '<div class="q-tags">' + noAnsTag + '</div>' +
        '<div class="q-chevron"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg></div>' +
      '</div>' +
      '<div class="qcard-body"><div class="qcard-inner">' + bodyHtml + '</div></div>';
    qList.appendChild(card);
  }});

  // Mark read button
  renderMarkReadBtn(num);
}}

function renderMarkReadBtn(num) {{
  const row = document.getElementById('markReadRow');
  const isRead = !!(progress[num] && progress[num].read);
  if(isRead) {{
    row.innerHTML =
      '<button class="btn-mark btn-mark-undo" onclick="markBilet('+num+',false)">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:15px;height:15px"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.5"/></svg>' +
        'O\u02bcqilmagan deb belgilash' +
      '</button>';
  }} else {{
    row.innerHTML =
      '<button class="btn-mark btn-mark-done" onclick="markBilet('+num+',true)">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:15px;height:15px"><polyline points="20 6 9 17 4 12"/></svg>' +
        'O\u02bcqildi deb belgilash' +
      '</button>';
  }}
}}

function markBilet(num, isRead) {{
  if(!progress[num]) progress[num]={{}};
  progress[num].read = isRead;
  if(isRead) progress[num].readAt = Date.now();
  else delete progress[num].readAt;
  saveProgress(currentUser.name, progress);
  renderReader(num);
}}

function toggleQ(i) {{
  document.getElementById('qc'+i).classList.toggle('open');
}}

function navigateBilet(dir) {{
  const idx = KEYS.indexOf(currentBilet);
  const ni = idx + dir;
  if(ni<0||ni>=KEYS.length) return;
  currentBilet = KEYS[ni];
  if(!progress[currentBilet]) progress[currentBilet]={{}};
  if(!progress[currentBilet].openedAt) progress[currentBilet].openedAt=Date.now();
  saveProgress(currentUser.name,progress);
  renderReader(currentBilet);
  window.scrollTo({{top:0,behavior:'smooth'}});
}}

// ═══════════════════════════════
// HELPERS
// ═══════════════════════════════
function esc(s) {{
  return String(s||'')
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}}

// ═══════════════════════════════
// INIT
// ═══════════════════════════════
(function init() {{
  const savedUser = localStorage.getItem(SK_CUR_USER);
  if(savedUser) {{
    allUsers = loadAllUsers();
    const user = allUsers.find(u=>u.name===savedUser);
    if(user) {{
      currentUser = user;
      progress = getProgress(savedUser);
      enterApp();
      return;
    }}
  }}
  showLoginPage();
}})();
</script>
</body>
</html>"""

# Fix the greeting ternary (Python f-string issue)
html = html.replace("now<12?'Xayrli tong':'now<17?'Xayrli kun':'Xayrli kech'", 
                    "now<12?'Xayrli tong':now<17?'Xayrli kun':'Xayrli kech'")

with open(r'D:\Farangiz\metodica\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = len(html.encode('utf-8')) // 1024
print(f'index.html yaratildi! ({size_kb} KB)')
