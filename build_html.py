"""Generate a single self-contained index.html from slides_data.json.
Data-driven: adding a slide = adding one object to slides_data.json's 'slides' array."""
import json

with open('slides_data.json', encoding='utf-8') as f:
    DATA = json.load(f)

DATA_JSON = json.dumps(DATA, ensure_ascii=False)

HTML = r'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>CBA アーティスト・インストラクター育成講座</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#FBF6F1; --band:#F8D7CA; --accent:#E89B7E; --ink:#3A2D2A;
    --sub:#5C4A45; --gold:#B89968; --hair:rgba(184,153,104,.55);
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#241c1a;font-family:"Noto Serif JP",serif;color:var(--ink);-webkit-font-smoothing:antialiased}
  .en,.eyebrow,.num{font-family:"Cormorant Garamond",serif}

  /* ---------- stage ---------- */
  #stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#241c1a}
  .slide-frame{position:relative;width:100vw;height:56.25vw;max-height:100vh;max-width:177.78vh;background:var(--bg);overflow:hidden}
  .slide{position:absolute;inset:0;opacity:0;transition:opacity .55s ease;pointer-events:none;
         /* base canvas 1280x720, everything scales via container query units */}
  .slide.active{opacity:1;pointer-events:auto}

  /* scale text to frame: use cqw if available, fallback vw via JS-set --u */
  .slide-frame{container-type:size}
  .u{font-size:1cqw}

  /* ---------- shared atoms ---------- */
  .eyebrow{letter-spacing:.4em;color:var(--gold);text-transform:uppercase;text-align:center}
  .hair{height:1px;background:var(--gold);margin:0 auto}
  .band{position:absolute;top:0;left:0;right:0;background:var(--band);display:flex;align-items:center}
  em{font-style:normal;background:linear-gradient(transparent 62%,var(--band) 62%);padding:0 .12em}
  .accent{color:var(--accent)}

  /* ---------- layout per type (all sizes in cqw/cqh) ---------- */
  .pad{position:absolute;inset:0;padding:7cqh 9cqw}

  /* cover */
  .cv-logo{position:absolute;top:4cqh;left:3cqw;width:9cqw;height:9cqw;border-radius:50%;object-fit:cover;z-index:3}
  .cv-hero{position:absolute;top:4.5cqh;left:50%;transform:translateX(-50%);width:82cqw;height:52cqh;object-fit:cover}
  .cv-badge{position:absolute;top:7cqh;left:50%;transform:translateX(-50%);z-index:3;background:rgba(251,246,241,.55);
            padding:.5cqh 2cqw;font-size:2cqw;letter-spacing:.15em}
  .cv-tb{position:absolute;bottom:9cqh;left:0;right:0;text-align:center}
  .cv-lead{font-size:1.9cqw;letter-spacing:.22em;color:var(--sub);margin-bottom:1.6cqh}
  .cv-title{font-size:3cqw;letter-spacing:.16em;color:var(--ink)}
  .cv-sub{margin-top:2.2cqh;font-size:1.15cqw;letter-spacing:.18em;color:var(--sub)}
  .cv-sub .en{font-style:italic;margin-left:1.4cqw;letter-spacing:.06em}
  .cv-sep{color:var(--gold);margin:0 .2cqw}

  /* ===== plantable: comparison table ===== */
  .pt-tbl{position:absolute;top:17cqh;bottom:5cqh;left:6cqw;right:6cqw;display:flex;flex-direction:column}
  .pt-row{display:flex;align-items:center;flex:1;border-radius:.5cqw}
  .pt-row.pt-alt{background:rgba(184,153,104,.07)}
  .pt-head{flex:0 0 auto;margin-bottom:.6cqh}
  .pt-c0{flex:0 0 38cqw;padding:0 1.5cqw;font-size:1.15cqw;letter-spacing:.04em;color:var(--ink)}
  .pt-c{flex:1;text-align:center;font-size:1.1cqw;letter-spacing:.03em;color:var(--sub)}
  .pt-main-h{background:var(--accent);color:#fff;border-radius:.6cqw;padding:1.2cqh 0;font-size:1.35cqw;letter-spacing:.1em}
  .pt-sub-h{background:rgba(248,215,202,.5);color:var(--ink);border-radius:.6cqw;padding:1.2cqh 0;font-size:1.35cqw;letter-spacing:.1em}
  .pt-head .pt-c0{font-size:1cqw}
  .pt-chk{display:inline-flex;align-items:center;justify-content:center;width:2.4cqw;height:2.4cqw;border-radius:50%;
          background:var(--accent);color:#fff;font-size:1.2cqw}

  /* ===== plancompare: main 110 vs sub 77 ===== */
  .pc-wrap{position:absolute;top:18cqh;bottom:13cqh;left:8cqw;right:8cqw;display:flex;gap:3cqw;align-items:stretch}
  .pc-main,.pc-sub{flex:1;padding:3.5cqh 2.6cqw;display:flex;flex-direction:column;position:relative}
  .pc-main{background:rgba(248,215,202,.32);border:1.5px solid var(--accent);border-radius:1cqw}
  .pc-sub{background:rgba(251,246,241,.6);border:1px solid var(--hair);border-radius:1cqw}
  .pc-tag{position:absolute;top:-1.6cqh;left:2.6cqw;background:var(--accent);color:#fff;font-size:1cqw;
          letter-spacing:.14em;padding:.5cqh 1.4cqw;border-radius:1cqh}
  .pc-name{font-size:1.5cqw;letter-spacing:.16em;color:var(--sub);margin-bottom:1.2cqh}
  .pc-price{font-size:3.4cqw;letter-spacing:.03em;color:var(--accent);margin-bottom:.4cqh}
  .pc-price-sub{color:var(--ink);opacity:.75;font-size:2.8cqw}
  .pc-tax{font-size:1.1cqw;letter-spacing:.06em;margin-left:.4cqw;color:var(--sub)}
  .pc-for{font-size:1.2cqw;letter-spacing:.06em;color:var(--ink);margin-bottom:2cqh;line-height:1.5;min-height:3.4cqh}
  .pc-points{border-top:1px solid var(--hair);padding-top:1.8cqh}
  .pc-pt{font-size:1.15cqw;letter-spacing:.05em;line-height:1.6;margin-bottom:1.2cqh;display:flex;gap:.7cqw;color:var(--sub)}
  .pc-dot{color:var(--gold)}
  .pc-foot{position:absolute;bottom:7.5cqh;left:0;right:0;text-align:center;font-size:1.25cqw;letter-spacing:.1em;color:var(--ink)}

  /* ===== photo-driven types ===== */
  /* photo: full-bleed hero */
  .ph-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .ph-scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(40,28,24,.05) 0%,rgba(40,28,24,.15) 45%,rgba(40,28,24,.62) 100%)}
  .ph-scrim-deep{background:linear-gradient(180deg,rgba(30,22,20,.45),rgba(30,22,20,.55))}
  .ph-cap{position:absolute;left:7cqw;right:7cqw;bottom:8cqh;color:#fff;text-shadow:0 1px 12px rgba(0,0,0,.4)}
  .ph-eyebrow{font-family:"Cormorant Garamond",serif;letter-spacing:.4em;font-size:1.2cqw;color:#f3e4d8;margin-bottom:1.5cqh;text-transform:uppercase}
  .ph-title{font-size:3cqw;letter-spacing:.14em;line-height:1.5;font-weight:400}
  .ph-title em{font-style:normal;background:linear-gradient(transparent 62%,rgba(232,155,126,.85) 62%);padding:0 .1em}
  .ph-sub{margin-top:2cqh;font-size:1.35cqw;letter-spacing:.12em;color:#f0e0d4;line-height:1.7}

  /* photogrid */
  .pg-grid{position:absolute;top:18cqh;bottom:6cqh;left:5cqw;right:5cqw;display:grid;gap:1.6cqw}
  .pg-2{grid-template-columns:1fr 1fr}
  .pg-3{grid-template-columns:1fr 1fr 1fr}
  .pg-4{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}
  .pg-6{grid-template-columns:1fr 1fr 1fr;grid-template-rows:1fr 1fr}
  .pg-cell{position:relative;overflow:hidden;border-radius:.6cqw}
  .pg-cell img{width:100%;height:100%;object-fit:cover;display:block}
  .pg-lbl{position:absolute;left:0;right:0;bottom:0;padding:1.6cqh 1cqw .9cqh;color:#fff;font-size:1.05cqw;
          letter-spacing:.08em;text-align:center;background:linear-gradient(transparent,rgba(40,28,24,.75))}

  /* split: half photo half text */
  .sp-img{position:absolute;top:0;bottom:0;width:46cqw;object-fit:cover}
  .sp-img.sp-l{left:0} .sp-img.sp-r{right:0}
  .sp-text{position:absolute;top:0;bottom:0;width:54cqw;padding:0 6cqw;display:flex;flex-direction:column;justify-content:center}
  .sp-text.sp-tl{left:0} .sp-text.sp-tr{right:0}
  .sp-title{font-size:2.5cqw;letter-spacing:.14em;line-height:1.5;margin-bottom:3cqh}
  .sp-title em{font-style:normal;background:linear-gradient(transparent 62%,var(--band) 62%);padding:0 .1em}
  .sp-body{font-size:1.3cqw;letter-spacing:.06em;line-height:2;color:var(--sub)}
  .sp-list{margin-top:1cqh}
  .sp-li{font-size:1.35cqw;letter-spacing:.08em;line-height:1.7;margin-bottom:1.8cqh;color:var(--ink);display:flex;gap:.8cqw}
  .sp-dot{color:var(--gold)}

  /* photoquote: portrait + testimonial */
  .pq-portrait{position:absolute;left:0;top:0;bottom:0;width:40cqw;object-fit:cover}
  .pq-body{position:absolute;right:0;top:0;bottom:0;width:60cqw;padding:0 6cqw;display:flex;flex-direction:column;justify-content:center}
  .pq-meta{font-size:1.3cqw;letter-spacing:.16em;color:var(--sub);margin-bottom:2cqh}
  .pq-headline{font-size:2.2cqw;letter-spacing:.1em;color:var(--accent);line-height:1.5;padding-bottom:2.5cqh;
               margin-bottom:2.5cqh;border-bottom:1px solid var(--hair)}
  .pq-quote{font-size:1.2cqw;letter-spacing:.06em;line-height:1.95;color:var(--ink)}
  .pq-quote p{margin-bottom:1.3cqh}
  .pq-quote p:first-child:before{content:"「";color:var(--gold)}
  .pq-quote p:last-child:after{content:"」";color:var(--gold)}

  /* photostat: hero + big numbers */
  .ps-wrap{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff}
  .ps-wrap .ph-eyebrow{color:#f3e4d8;margin-bottom:5cqh}
  .ps-stats{display:flex;gap:6cqw}
  .ps-stat{text-align:center}
  .ps-num{font-family:"Cormorant Garamond",serif;font-size:5cqw;color:#fff;line-height:1;text-shadow:0 2px 16px rgba(0,0,0,.4)}
  .ps-lbl{margin-top:1.5cqh;font-size:1.2cqw;letter-spacing:.14em;color:#f0e0d4}

  /* statement */
  .st{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center}
  .st .eyebrow{font-size:1.25cqw;margin-bottom:4.5cqh}
  .st .hair{width:5cqw;margin-bottom:4.5cqh}
  .st h1{font-weight:400;font-size:3.2cqw;letter-spacing:.16em;line-height:2}
  .st .foot-mark{position:absolute;bottom:4cqh;right:5cqw;font-size:.85cqw;letter-spacing:.25em;color:var(--gold);font-style:italic}

  /* agenda / reflect / cards / closing share heading */
  .head-band{height:13cqh;padding-left:6cqw;background:var(--band);display:flex}
  .head-band h2{font-weight:400;font-size:2.5cqw;letter-spacing:.2em;align-self:center}

  /* flexpage: vertically-centered content block (fixes overlap + balance) */
  .flexpage{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
            justify-content:center;padding:9cqh 9cqw;text-align:center}
  .fp-eyebrow{font-size:1.15cqw;letter-spacing:.4em;margin-bottom:1.8cqh}
  .fp-hair{width:5cqw;margin-bottom:3.2cqh}
  .fp-title{font-weight:400;font-size:2.8cqw;letter-spacing:.16em;line-height:1.55;margin-bottom:5cqh}
  .fp-list{width:100%;max-width:72cqw;text-align:left}
  .fp-list .row{display:flex;align-items:flex-start;margin-bottom:3cqh}
  .fp-list .row:last-child{margin-bottom:0}
  .fp-list .n{flex:0 0 5cqw;font-style:italic;font-size:2cqw;color:var(--accent);padding-top:.3cqh}
  .fp-list .t{flex:1;font-size:1.55cqw;letter-spacing:.1em;line-height:1.85}
  .fp-foot{margin-top:5cqh;font-size:1.35cqw;letter-spacing:.16em;color:var(--sub)}
  .close-c-flow{margin-top:5cqh;font-size:1.45cqw;letter-spacing:.16em;color:var(--sub);line-height:1.9}
  .center-eyebrow{font-size:1.15cqw;margin-bottom:2.2cqh}
  .center-title{text-align:center;font-weight:400;font-size:2.8cqw;letter-spacing:.16em;line-height:1.55}

  .lst{position:absolute;top:34cqh;left:14cqw;right:14cqw}
  .lst .row{display:flex;align-items:flex-start;margin-bottom:3.4cqh}
  .lst .n{flex:0 0 5cqw;font-style:italic;font-size:2.2cqw;color:var(--accent)}
  .lst .t{flex:1;font-size:1.65cqw;letter-spacing:.1em;line-height:1.9}
  .foot{position:absolute;bottom:7cqh;left:0;right:0;text-align:center;font-size:1.35cqw;letter-spacing:.16em;color:var(--sub)}

  /* curator / diagnostic */
  .blk{position:absolute;top:36cqh;left:14cqw;right:14cqw}
  .blk .row{display:flex;align-items:flex-start;margin-bottom:3cqh}
  .blk .n{flex:0 0 5cqw;font-style:italic;font-size:2cqw;color:var(--accent);padding-top:.4cqh}
  .blk .t{flex:1;font-size:1.5cqw;letter-spacing:.1em;line-height:1.85}
  .sign{position:absolute;bottom:4.5cqh;right:6cqw;font-size:1.05cqw;letter-spacing:.18em;color:var(--sub)}
  .lead-c{text-align:center;font-size:1.4cqw;letter-spacing:.2em;color:var(--sub);margin-top:2cqh}
  .close-c{position:absolute;bottom:7cqh;left:0;right:0;text-align:center;font-size:1.45cqw;letter-spacing:.16em;color:var(--sub);line-height:1.9}

  /* testimonial */
  .tm-meta{position:absolute;top:20cqh;left:9cqw;font-size:1.35cqw;letter-spacing:.16em;color:var(--sub)}
  .tm-hl{position:absolute;top:27cqh;left:9cqw;right:9cqw;text-align:center;color:var(--accent);font-size:2.5cqw;letter-spacing:.14em;padding:2cqh 0}
  .tm-hl .hair{width:5cqw;background:var(--accent)}
  .tm-q{position:absolute;top:44cqh;left:16cqw;right:16cqw;font-size:1.4cqw;letter-spacing:.08em;line-height:2.1;text-align:justify}
  .tm-q p{margin-bottom:1.6cqh}
  .tm-q p:first-child:before{content:"「";color:var(--gold)}
  .tm-q p:last-child:after{content:"」";color:var(--gold)}

  /* service */
  .sv{position:absolute;top:28cqh;left:11cqw;right:11cqw}
  .sv .row{display:flex;align-items:flex-start;margin-bottom:2.8cqh;padding-bottom:2.8cqh;border-bottom:1px solid var(--hair)}
  .sv .row:last-child{border-bottom:none}
  .sv .n{flex:0 0 4cqw;font-style:italic;font-size:1.8cqw;color:var(--accent)}
  .sv .c{flex:1}
  .sv .ti{font-size:1.7cqw;letter-spacing:.12em;margin-bottom:.6cqh}
  .sv .de{font-size:1.2cqw;letter-spacing:.06em;color:var(--sub);line-height:1.6}
  /* dense: 5+ items → 2 columns, tighter */
  .sv.sv-dense{top:19cqh;left:8cqw;right:8cqw;display:grid;grid-template-columns:1fr 1fr;column-gap:4cqw;row-gap:0}
  .sv.sv-dense .row{margin-bottom:1.8cqh;padding-bottom:1.8cqh}
  .sv.sv-dense .n{flex:0 0 3.2cqw;font-size:1.4cqw}
  .sv.sv-dense .ti{font-size:1.32cqw;margin-bottom:.3cqh;letter-spacing:.08em}
  .sv.sv-dense .de{font-size:1.02cqw;line-height:1.5}
  .sv.sv-dense .row:nth-last-child(-n+1):nth-child(odd){border-bottom:none}

  /* cards */
  .cards{position:absolute;top:32cqh;left:9cqw;right:9cqw;display:flex;gap:3cqw;justify-content:center}
  .card{flex:1;border:1px solid var(--hair);padding:5cqh 2.5cqw;text-align:center;font-size:1.5cqw;
        letter-spacing:.1em;line-height:1.7;display:flex;align-items:center;justify-content:center;min-height:24cqh}

  /* price */
  .pr{position:absolute;top:30cqh;left:14cqw;right:14cqw;display:flex;gap:4cqw}
  .pr .plan{flex:1;border:1px solid var(--hair);padding:5cqh 2cqw;text-align:center}
  .pr .pn{font-size:1.5cqw;letter-spacing:.16em;color:var(--sub);margin-bottom:2cqh}
  .pr .pp{font-size:3.4cqw;letter-spacing:.05em;color:var(--accent);margin-bottom:1.5cqh}
  .pr .pd{font-size:1.1cqw;letter-spacing:.08em;color:var(--sub)}
  .pr-note{position:absolute;bottom:11cqh;left:0;right:0;text-align:center;font-size:1.2cqw;letter-spacing:.12em;color:var(--sub)}

  /* special */
  .sp{position:absolute;top:30cqh;left:11cqw;right:11cqw;display:flex;gap:3cqw}
  .sp .opt{flex:1;background:rgba(248,215,202,.35);padding:4.5cqh 2.5cqw;text-align:center}
  .sp .ol{font-style:italic;font-size:1.6cqw;color:var(--accent);letter-spacing:.1em;margin-bottom:2cqh}
  .sp .ot{font-size:1.5cqw;letter-spacing:.08em;line-height:1.6;margin-bottom:1.5cqh}
  .sp .od{font-size:1.1cqw;color:var(--sub);letter-spacing:.06em;line-height:1.5}

  /* contract */
  /* contract — vertically centered, coral numbers, soft dividers */
  .ct{position:absolute;top:17cqh;bottom:7cqh;left:11cqw;right:11cqw;display:flex;flex-direction:column;justify-content:center}
  .ct .crow{display:flex;align-items:flex-start;padding:2.3cqh 0;border-bottom:1px solid var(--hair)}
  .ct .crow:last-child{border-bottom:none}
  .ct .ck{flex:0 0 24cqw;font-size:1.45cqw;letter-spacing:.1em;display:flex;align-items:baseline;gap:.7cqw}
  .ct .cnum{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:1.5cqw;color:var(--accent)}
  .ct .cv{flex:1;font-size:1.2cqw;letter-spacing:.05em;color:var(--sub);line-height:1.7}
  .ct .crow.warn .ck,.ct .crow.warn .cv{color:var(--accent)}
  .ct .crow.warn .cnum{color:var(--accent)}

  /* concern — reassuring card grid (warm, not a data table) */
  .concern-grid{display:flex;gap:2.8cqw;width:100%;max-width:80cqw;justify-content:center}
  .concern-card{flex:1;background:rgba(248,215,202,.22);border-radius:1cqw;padding:3.5cqh 2.2cqw;
                display:flex;flex-direction:column}
  .concern-card .cc-q{font-size:1.5cqw;letter-spacing:.08em;color:var(--ink);margin-bottom:2cqh;
                      line-height:1.5;display:flex;align-items:baseline;gap:.5cqw}
  .concern-card .cc-mark{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:1.9cqw;color:var(--accent)}
  .concern-card .cc-a{font-size:1.15cqw;letter-spacing:.04em;color:var(--sub);line-height:1.8}

  /* revenue */
  .rev{position:absolute;top:24cqh;left:10cqw;right:10cqw}
  .rev .rrow{display:flex;align-items:center;padding:1.7cqh 0;border-bottom:1px solid var(--hair)}
  .rev .rrow:last-child{border-bottom:none}
  .rev .rk{flex:0 0 32cqw;font-size:1.4cqw;letter-spacing:.08em}
  .rev .rm{flex:1;font-size:1.15cqw;color:var(--sub);letter-spacing:.04em}
  .rev .rv{flex:0 0 20cqw;text-align:right;font-size:1.6cqw;color:var(--accent);letter-spacing:.04em}

  /* closing */
  .cl{position:absolute;top:34cqh;left:18cqw;right:18cqw}
  .cl .row{display:flex;align-items:flex-start;margin-bottom:2.8cqh}
  .cl .n{flex:0 0 4cqw;font-style:italic;font-size:1.8cqw;color:var(--accent)}
  .cl .t{flex:1;font-size:1.55cqw;letter-spacing:.1em;line-height:1.7}

  /* ---------- chrome ---------- */
  #ui{position:fixed;left:0;right:0;bottom:0;height:46px;display:flex;align-items:center;justify-content:center;
      gap:18px;background:rgba(36,28,26,.0);z-index:50;opacity:0;transition:opacity .3s}
  body:hover #ui,#ui:hover{opacity:1}
  #ui button{background:rgba(251,246,241,.12);color:#FBF6F1;border:1px solid rgba(251,246,241,.25);
             border-radius:20px;padding:5px 14px;font-size:12px;letter-spacing:.08em;cursor:pointer;font-family:"Cormorant Garamond",serif}
  #ui button:hover{background:rgba(251,246,241,.22)}
  #prog{position:fixed;top:0;left:0;height:3px;background:var(--accent);z-index:60;transition:width .4s}
  #counter{position:fixed;top:10px;right:16px;color:rgba(251,246,241,.5);font-family:"Cormorant Garamond",serif;
           font-size:14px;letter-spacing:.15em;z-index:60}
  #dots{position:fixed;top:10px;left:16px;z-index:60;font-family:"Cormorant Garamond",serif;font-size:11px;
        letter-spacing:.2em;color:rgba(251,246,241,.5);text-transform:uppercase}

  /* ---------- presenter notes ---------- */
  #notes{position:fixed;inset:0;background:#1a1411;color:#e8ddd5;z-index:200;display:none;overflow-y:auto;
         font-family:"Noto Serif JP",serif}
  #notes.show{display:block}
  .nt-wrap{max-width:1100px;margin:0 auto;padding:40px 32px 80px}
  .nt-head{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid rgba(232,221,213,.2);
           padding-bottom:16px;margin-bottom:30px}
  .nt-head h1{font-size:20px;font-weight:500;letter-spacing:.1em}
  .nt-head .x{cursor:pointer;color:var(--accent);font-size:14px;letter-spacing:.1em}
  .nt-card{border:1px solid rgba(232,221,213,.16);border-radius:8px;padding:22px 26px;margin-bottom:18px;background:rgba(255,255,255,.02)}
  .nt-card .meta{display:flex;align-items:center;gap:12px;margin-bottom:14px}
  .nt-card .idx{font-family:"Cormorant Garamond",serif;font-size:22px;color:var(--accent);font-style:italic}
  .nt-card .sec{font-size:11px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase}
  .nt-card .badge{font-size:10px;letter-spacing:.15em;background:var(--accent);color:#1a1411;padding:2px 8px;border-radius:10px}
  .nt-card .stitle{font-size:15px;color:#fff;margin-bottom:14px;letter-spacing:.06em;opacity:.85}
  .nt-card .lbl{font-size:10px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase;margin:14px 0 6px}
  .nt-card .talk{font-size:15px;line-height:1.9;letter-spacing:.03em;color:#f0e8e1}
  .nt-card .cue{font-size:13px;line-height:1.75;letter-spacing:.03em;color:#c9b8ad;border-left:2px solid var(--accent);padding-left:14px;margin-top:6px}
  .nt-bar{position:fixed;top:0;left:0;right:0;height:48px;background:#0f0b09;display:flex;align-items:center;
          justify-content:space-between;padding:0 20px;z-index:210}
  .nt-bar .t{font-family:"Cormorant Garamond",serif;letter-spacing:.2em;font-size:14px;color:#e8ddd5}
  .nt-bar .toggle{font-size:12px;color:var(--accent);cursor:pointer;letter-spacing:.1em;border:1px solid rgba(232,221,213,.25);
                  padding:5px 12px;border-radius:14px}
  #notes .nt-wrap{padding-top:70px}

  /* customer-mode: synced receiver tab — clean, chrome hidden, fills screen */
  body.customer-mode #ui,
  body.customer-mode #counter,
  body.customer-mode #dots,
  body.customer-mode #prog{display:none!important}
  body.customer-mode #stage{background:#241c1a}
  body.customer-mode .slide-frame{box-shadow:none}

  @media (max-width:768px){
    .slide-frame{height:auto;aspect-ratio:16/9}
  }
</style>
</head>
<body>
<div id="prog"></div>
<div id="dots"></div>
<div id="counter"></div>
<div id="stage"><div class="slide-frame" id="frame"></div></div>
<div id="ui">
  <button onclick="go(-1)">‹ 前へ</button>
  <button onclick="toggleNotes()">商談メモ</button>
  <button onclick="toggleFs()">全画面</button>
  <button onclick="go(1)">次へ ›</button>
</div>

<div id="notes">
  <div class="nt-bar">
    <span class="t">PRESENTER NOTES — 商談者専用（聴衆には表示されません）</span>
    <span class="toggle" onclick="toggleNotes()">✕ 閉じてプレゼンに戻る</span>
  </div>
  <div class="nt-wrap" id="nt-wrap"></div>
</div>

<script>
const DATA = __DATA__;
const S = DATA.slides, IMG = DATA.images;
let cur = 0;

/* ---------- renderers ---------- */
function esc(s){return s==null?'':s}
function roman(i){return ['i','ii','iii','iv','v','vi','vii','viii'][i]||(i+1)}

function render(s){
  const d = s.deck;
  switch(s.type){
    case 'plantable': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="pt-tbl">
        <div class="pt-row pt-head">
          <div class="pt-c0"></div>
          <div class="pt-c pt-main-h">プレミアム</div>
          <div class="pt-c pt-sub-h">ベーシック</div>
        </div>
        ${d.rows.map((r,i)=>`<div class="pt-row${i%2?' pt-alt':''}">
          <div class="pt-c0">${r[0]}</div>
          <div class="pt-c">${r[1]==='✓'?'<span class="pt-chk">✓</span>':r[1]}</div>
          <div class="pt-c">${r[2]==='✓'?'<span class="pt-chk">✓</span>':r[2]}</div>
        </div>`).join('')}
      </div>`;
    case 'plancompare': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="pc-wrap">
        <div class="pc-main">
          <div class="pc-tag">${d.main.tag}</div>
          <div class="pc-name">${d.main.name}</div>
          <div class="pc-price">${d.main.price}<span class="pc-tax">${d.main.tax}</span></div>
          <div class="pc-for">${d.main.for}</div>
          <div class="pc-points">${d.main.points.map(t=>`<div class="pc-pt"><span class="pc-dot">◇</span>${t}</div>`).join('')}</div>
        </div>
        <div class="pc-sub">
          <div class="pc-name">${d.sub.name}</div>
          <div class="pc-price pc-price-sub">${d.sub.price}<span class="pc-tax">${d.sub.tax}</span></div>
          <div class="pc-for">${d.sub.for}</div>
          <div class="pc-points">${d.sub.points.map(t=>`<div class="pc-pt"><span class="pc-dot">◇</span>${t}</div>`).join('')}</div>
        </div>
      </div>
      <div class="pc-foot">${d.foot}</div>
      <div class="foot" style="bottom:3cqh">${d.note}</div>`;
    case 'photo': return `
      <img class="ph-bg" src="${IMG[d.img]}">
      <div class="ph-scrim"></div>
      <div class="ph-cap">
        ${d.eyebrow?`<div class="ph-eyebrow">${d.eyebrow}</div>`:''}
        <div class="ph-title">${d.title}</div>
        ${d.sub?`<div class="ph-sub">${d.sub}</div>`:''}
      </div>`;
    case 'photogrid': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="pg-grid pg-${d.imgs.length}">
        ${d.imgs.map((g,i)=>`<div class="pg-cell"><img src="${IMG[g.img]}"><div class="pg-lbl">${g.cap}</div></div>`).join('')}
      </div>
      ${d.foot?`<div class="foot" style="bottom:3cqh">${d.foot}</div>`:''}`;
    case 'split': return `
      <img class="sp-img ${d.side==='left'?'sp-l':'sp-r'}" src="${IMG[d.img]}">
      <div class="sp-text ${d.side==='left'?'sp-tr':'sp-tl'}">
        ${d.eyebrow?`<div class="eyebrow" style="text-align:left;font-size:1.1cqw">${d.eyebrow}</div><div class="hair" style="margin:1.2cqh 0 2.4cqh;width:4cqw"></div>`:''}
        <div class="sp-title">${d.title}</div>
        ${d.body?`<div class="sp-body">${d.body}</div>`:''}
        ${d.list?`<div class="sp-list">${d.list.map(t=>`<div class="sp-li"><span class="sp-dot">◇</span>${t}</div>`).join('')}</div>`:''}
      </div>`;
    case 'photoquote': return `
      <img class="pq-portrait" src="${IMG[d.img]}">
      <div class="pq-body">
        <div class="pq-meta">${d.meta}</div>
        <div class="pq-headline">${d.headline}</div>
        <div class="pq-quote">${d.quote.map(p=>`<p>${p}</p>`).join('')}</div>
      </div>`;
    case 'photostat': return `
      <img class="ph-bg" src="${IMG[d.img]}">
      <div class="ph-scrim ph-scrim-deep"></div>
      <div class="ps-wrap">
        <div class="ph-eyebrow" style="text-align:center">${d.eyebrow||''}</div>
        <div class="ps-stats">
          ${d.stats.map(s=>`<div class="ps-stat"><div class="ps-num">${s[0]}</div><div class="ps-lbl">${s[1]}</div></div>`).join('')}
        </div>
      </div>`;
    case 'cover': return `
      <img class="cv-logo" src="${IMG[d.logo]}">
      <img class="cv-hero" src="${IMG[d.hero]}">
      <div class="cv-badge">【20周年記念 特別プログラム】</div>
      <div class="cv-tb">
        <div class="cv-lead">${d.lead}</div>
        <div class="cv-title">${d.title}</div>
        <div class="cv-sub">${d.sub.replace(/◇/g,'<span class="cv-sep">◇</span>')}<span class="en">— ${d.en}</span></div>
      </div>`;
    case 'statement': return `
      <div class="st">
        ${d.eyebrow?`<div class="eyebrow">${d.eyebrow}</div><div class="hair"></div>`:''}
        <h1>${d.title}</h1>
        <div class="foot-mark">Crystal Singing Bowl Beauty Academy</div>
      </div>`;
    case 'agenda': return `
      <div class="flexpage">
        <div class="fp-title">${d.title}</div>
        <div class="fp-list">
          ${d.items.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
        </div>
        <div class="fp-foot">${d.foot}</div>
      </div>`;
    case 'curator': return `
      <div class="flexpage">
        <div class="eyebrow fp-eyebrow">${d.eyebrow}</div><div class="hair fp-hair"></div>
        <div class="fp-title">${d.title}</div>
        <div class="fp-list">
          ${d.reasons.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
        </div>
        <div class="sign">${d.sign}</div>
      </div>`;
    case 'reflect': return `
      <div class="flexpage">
        <div class="eyebrow fp-eyebrow">${d.eyebrow}</div><div class="hair fp-hair"></div>
        <div class="fp-title">${d.title}</div>
        <div class="fp-list">
          ${d.lines.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
        </div>
        <div class="fp-foot">${d.foot}</div>
      </div>`;
    case 'testimonial': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="tm-meta">${d.meta}</div>
      <div class="tm-hl"><div class="hair"></div><div style="padding:1.4cqh 0">${d.headline}</div><div class="hair"></div></div>
      <div class="tm-q">${d.quote.map(p=>`<p>${p}</p>`).join('')}</div>`;
    case 'service': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="sv ${d.items.length>=5?'sv-dense':''}">
        ${d.items.map((it,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="c"><div class="ti">${it[0]}</div><div class="de">${it[1]}</div></div></div>`).join('')}
      </div>
      <div class="foot" style="bottom:3cqh">${d.foot}</div>`;
    case 'cards': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="cards">${d.cards.map(c=>`<div class="card">${c}</div>`).join('')}</div>
      <div class="foot">${d.foot}</div>`;
    case 'diagnostic': return `
      <div class="flexpage">
        <div class="eyebrow fp-eyebrow">${d.eyebrow}</div><div class="hair fp-hair"></div>
        <div class="fp-title">${d.title}</div>
        <div class="lead-c">${d.lead}</div>
        <div class="fp-list" style="margin-top:3cqh">
          ${d.questions.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
        </div>
        <div class="close-c-flow">${d.close}</div>
      </div>`;
    case 'revenue': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="rev">
        ${d.rows.map(r=>`<div class="rrow"><div class="rk">${r[0]}</div><div class="rm">${r[1]}</div><div class="rv">${r[2]}</div></div>`).join('')}
      </div>
      <div class="foot" style="bottom:4cqh">${d.foot}</div>`;
    case 'price': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="pr">
        ${d.plans.map(p=>`<div class="plan"><div class="pn">${p[0]}</div><div class="pp">${p[1]}</div><div class="pd">${p[2]}</div></div>`).join('')}
      </div>
      <div class="pr-note">${d.note}</div>
      <div class="foot" style="bottom:6cqh">${d.foot}</div>`;
    case 'special': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div style="position:absolute;top:22cqh;left:0;right:0;text-align:center;font-size:1.3cqw;letter-spacing:.16em;color:var(--sub)">${d.lead}</div>
      <div class="sp">
        ${d.options.map(o=>`<div class="opt"><div class="ol">${o[0]}</div><div class="ot">${o[1]}</div><div class="od">${o[2]}</div></div>`).join('')}
      </div>`;
    case 'concern': return `
      <div class="flexpage">
        ${d.eyebrow?`<div class="eyebrow fp-eyebrow">${d.eyebrow}</div><div class="hair fp-hair"></div>`:''}
        <div class="fp-title" style="margin-bottom:6cqh">${d.title}</div>
        <div class="concern-grid">
          ${d.points.map((p,i)=>`<div class="concern-card">
            <div class="cc-q"><span class="cc-mark">Q.</span>${p[0]}</div>
            <div class="cc-a">${p[1]}</div>
          </div>`).join('')}
        </div>
        ${d.foot?`<div class="fp-foot">${d.foot}</div>`:''}
      </div>`;
    case 'contract': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="ct">
        ${d.points.map((p,i)=>{const w=p[0].includes('返金')?' warn':'';return `<div class="crow${w}">
          <div class="ck"><span class="cnum">${roman(i)}.</span>${p[0]}</div>
          <div class="cv">${p[1]}</div></div>`}).join('')}
      </div>`;
    case 'closing': return `
      <div style="position:absolute;top:11cqh;left:0;right:0;text-align:center">
        <div class="eyebrow center-eyebrow">${d.eyebrow}</div><div class="hair" style="width:5cqw"></div>
      </div>
      <div style="position:absolute;top:18cqh;left:0;right:0"><div class="center-title">${d.title}</div></div>
      <div class="cl">
        ${d.steps.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
      </div>
      <div class="foot">${d.foot}</div>`;
    default: return `<div class="st"><h1>${s.id}</h1></div>`;
  }
}

/* ---------- build slides ---------- */
const frame = document.getElementById('frame');
S.forEach((s,i)=>{
  const el = document.createElement('div');
  el.className = 'slide';
  el.dataset.i = i;
  el.innerHTML = render(s);
  frame.appendChild(el);
});
const slideEls = [...frame.querySelectorAll('.slide')];

/* ---------- target filtering (A=主婦・会社員 / B=音楽経験者 / C=ヨガ) ---------- */
let TARGET = (new URLSearchParams(location.search).get('target')||'B').toUpperCase();
if(!['A','B','C'].includes(TARGET)) TARGET='B';
let view = [];           // array of slide indices visible for current target
function rebuildView(){
  view = S.map((s,i)=>i).filter(i=>{const t=S[i].target||'all'; return t==='all'||t===TARGET;});
}
rebuildView();
let vpos = 0;            // position within view

/* dots / sections */
function showView(p){
  vpos = Math.max(0, Math.min(view.length-1, p));
  cur = view[vpos];
  slideEls.forEach((el,k)=>el.classList.toggle('active',k===cur));
  document.getElementById('prog').style.width = ((vpos+1)/view.length*100)+'%';
  document.getElementById('counter').textContent = String(vpos+1).padStart(2,'0')+' / '+String(view.length).padStart(2,'0');
  document.getElementById('dots').textContent = S[cur].section || '';
  location.hash = vpos+1;
}
// show(i) kept for compatibility: treat i as a view position
function show(i){ showView(i); }
function go(d){showView(vpos+d)}
function setTarget(t){ if(['A','B','C'].includes(t)){ TARGET=t; rebuildView(); showView(0);} }

/* keyboard / swipe */
addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){go(1);e.preventDefault()}
  if(e.key==='ArrowLeft'||e.key==='PageUp'){go(-1)}
  if(e.key==='Home')show(0);
  if(e.key==='End')show(S.length-1);
  if(e.key.toLowerCase()==='n')toggleNotes();
  if(e.key.toLowerCase()==='f')toggleFs();
});
let tx=0;
addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});
addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)go(dx<0?1:-1)},{passive:true});
frame.addEventListener('click',e=>{const r=frame.getBoundingClientRect();(e.clientX-r.left)/r.width>.5?go(1):go(-1)});

function toggleFs(){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}

/* ---------- presenter notes ---------- */
function buildNotes(){
  const w = document.getElementById('nt-wrap');
  w.innerHTML = S.map((s,i)=>{
    const n=s.notes||{};
    const badge = s.badge?`<span class="badge">${s.badge}</span>`:'';
    const title = (s.deck.title||s.deck.headline||(s.deck.title)||s.id);
    return `<div class="nt-card" id="nt-${i}">
      <div class="meta"><span class="idx">${String(i+1).padStart(2,'0')}</span><span class="sec">${s.section||''}</span>${badge}</div>
      <div class="stitle">${(s.deck.title||s.deck.headline||(s.deck.title)||s.id).replace(/<[^>]+>/g,'')}</div>
      ${n.talk?`<div class="lbl">話す内容</div><div class="talk">${n.talk}</div>`:''}
      ${n.cue?`<div class="lbl">進行のポイント</div><div class="cue">${n.cue}</div>`:''}
    </div>`;
  }).join('');
}
function toggleNotes(){
  const n=document.getElementById('notes');
  n.classList.toggle('show');
  if(n.classList.contains('show')){
    const c=document.getElementById('nt-'+cur);
    if(c)c.scrollIntoView({block:'center'});
  }
}

buildNotes();
const start = parseInt(location.hash.replace('#',''))||1;
showView(start-1);

/* ---- customer mode: synced receiver tab (opened from present.html) ---- */
(function(){
  const isCustomer = new URLSearchParams(location.search).get('customer')==='1';
  if(!isCustomer) return;
  document.body.classList.add('customer-mode');
  const chan = ('BroadcastChannel' in window) ? new BroadcastChannel('cba-deck-sync') : null;
  // jump to an ABSOLUTE slide index (robust across target differences)
  function gotoAbs(absIdx){
    const t=S[absIdx]?.target||'all';
    if(t!=='all' && t!==TARGET){ TARGET=t; rebuildView(); }
    const p=view.indexOf(absIdx);
    if(p>=0) showView(p);
  }
  if(chan){
    chan.onmessage = (e)=>{
      if(e.data?.type==='goto' && typeof e.data.abs==='number') gotoAbs(e.data.abs);
      if(e.data?.type==='target'){ TARGET=e.data.target; rebuildView(); showView(0); }
    };
    chan.postMessage({type:'hello'});
    addEventListener('beforeunload',()=>chan.postMessage({type:'bye'}));
  }
})();
</script>
</body>
</html>'''

out = HTML.replace('__DATA__', DATA_JSON)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(out)
print(f"Wrote index.html ({len(out)} bytes)")
