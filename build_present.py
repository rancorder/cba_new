"""Build present.html — 商談者用 左右分割ビュー。
左=台本（クリックでスライド連動）、右=顧客提示スライド（全画面トグル付き）。
slide rendering JS is reused verbatim from build_html.py so both views stay identical."""
import json, re

with open('slides_data.json', encoding='utf-8') as f:
    DATA = json.load(f)
DATA_JSON = json.dumps(DATA, ensure_ascii=False)

# --- pull the render() function + slide CSS out of build_html.py so we never diverge ---
with open('build_html.py', encoding='utf-8') as f:
    src = f.read()

# slide CSS lives between the first ":root{" block start and the "/* ---------- chrome" marker
css_match = re.search(r'(:root\{.*?)(/\* ---------- chrome)', src, re.S)
SLIDE_CSS = css_match.group(1)

# render() function body: from "function esc" through the close of "function render"
rnd_match = re.search(r'(function esc\(s\).*?function render\(s\)\{.*?\n    default: return.*?\n  \}\n\}\n)', src, re.S)
RENDER_JS = rnd_match.group(1)

HTML = r'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CBA 商談ビュー（商談者用）</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<style>
__SLIDE_CSS__
  /* ===== presenter shell ===== */
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;font-family:"Noto Serif JP",serif;background:#15100e;color:#3A2D2A;overflow:hidden}
  #app{display:flex;height:100vh}

  /* left: script */
  #script{width:38%;min-width:330px;max-width:560px;height:100vh;overflow-y:auto;background:#1a1411;
          border-right:1px solid rgba(232,221,213,.12);padding:0 0 120px}
  #script::-webkit-scrollbar{width:9px}
  #script::-webkit-scrollbar-thumb{background:rgba(232,221,213,.18);border-radius:5px}
  .sc-top{position:sticky;top:0;z-index:5;background:#0f0b09;padding:16px 22px;border-bottom:1px solid rgba(232,221,213,.12)}
  .sc-top .ttl{font-family:"Cormorant Garamond",serif;letter-spacing:.18em;font-size:15px;color:#e8ddd5}
  .sc-top .sub{font-size:11px;color:#9a8b80;letter-spacing:.08em;margin-top:3px}
  .tgt-switch{display:flex;gap:6px;margin-top:11px}
  .tgt-switch .tgt{flex:1;background:rgba(232,221,213,.08);color:#c2b1a6;border:1px solid rgba(232,221,213,.18);
                   border-radius:14px;padding:6px 4px;font-size:11px;letter-spacing:.02em;cursor:pointer;font-family:"Noto Serif JP",serif}
  .tgt-switch .tgt:hover{background:rgba(232,221,213,.16)}
  .tgt-switch .tgt.on{background:var(--accent);color:#1a1411;border-color:var(--accent);font-weight:500}
  .sc-item{padding:18px 22px;border-bottom:1px solid rgba(232,221,213,.08);cursor:pointer;transition:background .15s}
  .sc-item:hover{background:rgba(232,221,213,.04)}
  .sc-item.active{background:rgba(232,155,126,.12);border-left:3px solid var(--accent);padding-left:19px}
  .sc-head{display:flex;align-items:center;gap:10px;margin-bottom:9px}
  .sc-num{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:19px;color:var(--accent)}
  .sc-sec{font-size:10px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase}
  .sc-badge{font-size:9px;letter-spacing:.12em;background:var(--accent);color:#1a1411;padding:2px 7px;border-radius:9px}
  .sc-stitle{font-size:13px;color:#fff;opacity:.82;margin-bottom:10px;letter-spacing:.04em;line-height:1.4}
  .sc-lbl{font-size:9px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase;margin:11px 0 4px}
  .sc-talk{font-size:13.5px;line-height:1.85;letter-spacing:.02em;color:#f0e8e1}
  .sc-cue{font-size:12px;line-height:1.7;color:#c2b1a6;border-left:2px solid var(--accent);padding-left:11px;margin-top:4px}

  /* right: slide stage */
  #right{flex:1;display:flex;flex-direction:column;background:#241c1a;height:100vh}
  #rbar{height:50px;flex:0 0 50px;display:flex;align-items:center;justify-content:space-between;
        padding:0 18px;background:#1a1411;border-bottom:1px solid rgba(232,221,213,.1)}
  #rbar .pos{font-family:"Cormorant Garamond",serif;letter-spacing:.16em;font-size:14px;color:#c2b1a6}
  #rbar .btns{display:flex;gap:8px}
  #rbar button{background:rgba(232,221,213,.1);color:#e8ddd5;border:1px solid rgba(232,221,213,.22);
               border-radius:16px;padding:6px 15px;font-size:12px;letter-spacing:.06em;cursor:pointer;
               font-family:"Noto Serif JP",serif}
  #rbar button:hover{background:rgba(232,221,213,.2)}
  #rbar button.fs{background:var(--accent);color:#1a1411;border-color:var(--accent);font-weight:500}
  #custStatus{font-size:11px;letter-spacing:.06em;padding:5px 11px;border-radius:13px;align-self:center}
  #custStatus.cust-off{color:#9a8b80;border:1px solid rgba(232,221,213,.2)}
  #custStatus.cust-on{color:#1a1411;background:#9bbf8f;font-weight:500}
  #rstage{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:22px;min-height:0;position:relative}
  #rframe{position:relative;width:100%;aspect-ratio:16/9;max-height:calc(100% - 40px);max-width:calc((100vh - 134px)*1.7778);
          background:var(--bg);overflow:hidden;container-type:size;box-shadow:0 10px 40px rgba(0,0,0,.4)}
  #rhint{margin-top:14px;max-width:80%;text-align:center;font-size:11px;line-height:1.6;color:#8a7b70;letter-spacing:.03em}
  .slide{position:absolute;inset:0;opacity:0;transition:opacity .4s ease;pointer-events:none}
  .slide.active{opacity:1;pointer-events:auto}

  @media(max-width:900px){
    #app{flex-direction:column}
    #script{width:100%;max-width:none;height:42vh;border-right:none;border-bottom:1px solid rgba(232,221,213,.12)}
    #right{height:58vh}
  }
</style>
</head>
<body>
<div id="app">
  <div id="script">
    <div class="sc-top">
      <div class="ttl">PRESENTER SCRIPT</div>
      <div class="sub">台本をクリック → 右のスライドが連動します</div>
      <div class="tgt-switch">
        <button class="tgt" data-t="A" onclick="setTarget('A')">① 主婦・会社員</button>
        <button class="tgt" data-t="B" onclick="setTarget('B')">② 音楽経験者</button>
        <button class="tgt" data-t="C" onclick="setTarget('C')">③ ヨガ</button>
      </div>
    </div>
    <div id="sclist"></div>
  </div>
  <div id="right">
    <div id="rbar">
      <span class="pos" id="pos"></span>
      <div class="btns">
        <button onclick="go(-1)">‹ 前</button>
        <button onclick="go(1)">次 ›</button>
        <span id="custStatus" class="cust-off">顧客画面：未接続</span>
        <button class="fs" onclick="openCustomer()">🖥 顧客画面を別タブで開く</button>
      </div>
    </div>
    <div id="rstage"><div id="rframe"></div>
      <div id="rhint">右はプレビューです。「顧客画面を別タブで開く」を押すと、別タブに顧客用スライドが開き、この台本クリックと連動します。そのタブをZoomで共有してください。</div>
    </div>
  </div>
</div>

<script>
const DATA = __DATA__;
const S = DATA.slides, IMG = DATA.images;

/* ---- customer tab sync via BroadcastChannel ---- */
const chan = ('BroadcastChannel' in window) ? new BroadcastChannel('cba-deck-sync') : null;
let custWin = null;
function openCustomer(){
  custWin = window.open('/?customer=1&target='+TARGET,'cba_customer');
  setCustStatus(true);
  setTimeout(()=>{ broadcastTarget(); broadcastAbs(); }, 900);
}
function broadcastAbs(){ if(chan) chan.postMessage({type:'goto', abs:cur}); }
function broadcastTarget(){ if(chan) chan.postMessage({type:'target', target:TARGET}); }
function setCustStatus(on){
  const el=document.getElementById('custStatus');
  el.textContent = on ? '顧客画面：接続中' : '顧客画面：未接続';
  el.className = on ? 'cust-on' : 'cust-off';
}
if(chan) chan.onmessage = (e)=>{
  if(e.data?.type==='hello') { setCustStatus(true); broadcastTarget(); broadcastAbs(); }
  if(e.data?.type==='bye') setCustStatus(false);
};

__RENDER_JS__

/* ---- target state (A=主婦・会社員 / B=音楽経験者 / C=ヨガ) ---- */
let TARGET = (new URLSearchParams(location.search).get('target')||'B').toUpperCase();
if(!['A','B','C'].includes(TARGET)) TARGET='B';
let cur = 0;            // absolute slide index
let view = [];          // visible absolute indices for current target
let vpos = 0;           // position within view
function rebuildView(){ view = S.map((s,i)=>i).filter(i=>{const t=S[i].target||'all';return t==='all'||t===TARGET;}); }

/* ---- build right stage (all slides; visibility by active class) ---- */
const rframe = document.getElementById('rframe');
S.forEach((s,i)=>{
  const el=document.createElement('div'); el.className='slide'; el.dataset.i=i;
  el.innerHTML=render(s); rframe.appendChild(el);
});
const slideEls=[...rframe.querySelectorAll('.slide')];

/* ---- build left script (all; filtered by display) ---- */
const sclist=document.getElementById('sclist');
sclist.innerHTML=S.map((s,i)=>{
  const n=s.notes||{};
  const badge=s.badge?`<span class="sc-badge">${s.badge}</span>`:'';
  const stitle=(s.deck.title||s.deck.headline||s.deck.eyebrow||s.id).replace(/<[^>]+>/g,'');
  return `<div class="sc-item" data-i="${i}" onclick="showAbs(${i})">
    <div class="sc-head"><span class="sc-num"></span>
      <span class="sc-sec">${s.section||''}</span>${badge}</div>
    <div class="sc-stitle">${stitle}</div>
    ${n.talk?`<div class="sc-lbl">話す内容</div><div class="sc-talk">${n.talk}</div>`:''}
    ${n.cue?`<div class="sc-lbl">進行のポイント</div><div class="sc-cue">${n.cue}</div>`:''}
  </div>`;
}).join('');
const scItems=[...sclist.querySelectorAll('.sc-item')];

/* ---- target switch ---- */
function setTarget(t){
  if(!['A','B','C'].includes(t)) return;
  TARGET=t; rebuildView();
  document.querySelectorAll('.tgt').forEach(b=>b.classList.toggle('on',b.dataset.t===t));
  // filter left script items + renumber
  scItems.forEach((el)=>{
    const i=+el.dataset.i; const tt=S[i].target||'all';
    el.style.display=(tt==='all'||tt===t)?'':'none';
  });
  view.forEach((absI,p)=>{ const el=scItems[absI]; if(el) el.querySelector('.sc-num').textContent=String(p+1).padStart(2,'0'); });
  broadcastTarget();
  showView(0);
}

/* ---- navigation ---- */
function showView(p){
  vpos=Math.max(0,Math.min(view.length-1,p));
  cur=view[vpos];
  slideEls.forEach((el)=>el.classList.toggle('active',+el.dataset.i===cur));
  scItems.forEach((el)=>el.classList.toggle('active',+el.dataset.i===cur));
  document.getElementById('pos').textContent=String(vpos+1).padStart(2,'0')+' / '+String(view.length).padStart(2,'0');
  broadcastAbs();
  const a=scItems[cur];
  if(a){const r=a.getBoundingClientRect();
    if(r.top<120||r.bottom>innerHeight)a.scrollIntoView({block:'center',behavior:'smooth'});}
}
function showAbs(absI){ const p=view.indexOf(absI); if(p>=0) showView(p); }
function go(d){showView(vpos+d)}

/* ---- keys ---- */
addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){go(1);e.preventDefault()}
  if(e.key==='ArrowLeft'||e.key==='PageUp'){go(-1)}
  if(e.key==='Home')showView(0); if(e.key==='End')showView(view.length-1);
});
let tx=0;
rframe.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});
rframe.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)go(dx<0?1:-1)},{passive:true});

/* ---- init ---- */
setTarget(TARGET);
</script>
</body>
</html>'''

out = (HTML
       .replace('__SLIDE_CSS__', SLIDE_CSS)
       .replace('__RENDER_JS__', RENDER_JS)
       .replace('__DATA__', DATA_JSON))
with open('present.html','w',encoding='utf-8') as f:
    f.write(out)
print(f"Wrote present.html ({len(out)} bytes), reused {len(SLIDE_CSS)} css + {len(RENDER_JS)} render js")
