import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="BioElectrio NanoLab", layout="wide")

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>BioElectrio NanoLab: Microbial Electrolysis Cell</title>
<meta name="color-scheme" content="dark">
<style>
:root{--bg:#060b16;--panel:#0c1424;--line:#1f2d45;--ink:#eaf0fa;--mute:#93a3bd;--accent:#38bdf8;--gold:#facc15;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:dark}
html{scroll-padding-top:env(safe-area-inset-top,0px)}*,*::before,*::after{box-sizing:inherit}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:20px}
.wrap{max-width:1040px;margin:0 auto}
.hd{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:12px}.hd h1{color:#2dd4bf;margin:0 0 2px;font-size:1.3rem;font-weight:650}
.logo{width:46px;height:46px;border-radius:12px;background:linear-gradient(135deg,#2dd4bf,#38bdf8);display:grid;place-items:center;font-size:1.4rem}
.pill{margin-left:auto;border:1px solid #1d5f6b;background:#0b2b36;color:#67e8f9;border-radius:999px;padding:6px 14px;font-size:.85rem}
.mut{color:var(--mute);font-size:.8rem}.sub{color:var(--mute);margin:0 0 14px;max-width:74ch}
canvas{display:block;width:100%;aspect-ratio:1000/520;background:#030712;border:1px solid var(--line);border-radius:10px}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;margin:10px 2px 14px;color:var(--mute);font-size:.85rem}
.legend i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin-bottom:14px}
.lbl{display:block;color:var(--mute);font-size:.85rem;margin-bottom:8px}
.mats{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}
button{font:inherit;color:var(--ink);cursor:pointer}
button:focus-visible,input:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.mc{display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-start;text-align:left;padding:11px 13px;border-radius:10px;background:#0a1220;border:1px solid var(--line)}
.mc b{display:block;font-size:.93rem;margin-bottom:2px}.mc span{color:var(--mute);font-size:.8rem}
.mc[aria-pressed=true]{border-color:var(--c);background:#0d2236}.mc[aria-pressed=true] b{color:var(--c)}
.controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.controls label{display:block;color:var(--mute);font-size:.85rem;margin-bottom:6px}.controls b{color:var(--ink)}
input[type=range]{width:100%;accent-color:var(--accent)}
#pp{background:#101b30;border:1px solid #2a3b5a;border-radius:8px;padding:7px 14px;align-self:end}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:14px}
.metrics .panel{margin:0}.k{color:var(--mute);font-size:.82rem}.v{font-size:1.45rem;font-weight:650;color:var(--accent);margin-top:2px}.s{color:var(--mute);font-size:.78rem}
.row{display:grid;grid-template-columns:170px 1fr 70px;gap:10px;align-items:center;font-size:.88rem;margin-bottom:8px}
.row .nm{color:var(--mute)}.row.on .nm{color:var(--ink);font-weight:600}
.track{height:10px;background:#0a1220;border-radius:5px;overflow:hidden}.fill{height:100%;border-radius:5px;transition:width .25s}
.ev{display:grid;grid-template-columns:minmax(150px,1fr) 2.4fr;gap:8px 18px;font-size:.86rem}
.ev span:nth-child(odd){font-weight:600}.ev span:nth-child(even){color:var(--mute)}
.note{color:var(--mute);font-size:.8rem;margin:10px 0 0}
@media(max-width:600px){.row{grid-template-columns:110px 1fr 56px}.ev{grid-template-columns:1fr}.ev span:nth-child(even){margin-bottom:6px}}
</style>
</head>
<body>
<div class="wrap">
<header class="hd"><div class="logo">⚡</div><div><h1>BioElectrio NanoLab: Microbial Electrolysis Cell (MEC)</h1><div class="mut">Interactive molecular and systems-level digital twin simulator</div></div><span class="pill" id="live">● Live molecular simulation active</span></header>
<p class="sub">Bacteria on the anode swallow waste molecules (yellow) and release electrons, protons and CO₂. Each electron dot stands in for the 8 that one acetate molecule yields. The anode sets how many electrons flow, and the cathode catalyst decides what share of them become hydrogen. All figures come from the article “Nanomaterials Are Supercharging Bio-Hydrogen Fuel. Can It Leave the Lab?”</p>

<canvas id="sim" aria-label="Animated microbial electrolysis cell"></canvas>
<div class="legend">
<span><i style="background:#4ade80"></i>Bacteria</span><span><i style="background:#fde68a"></i>Organic waste</span>
<span><i style="background:#facc15"></i>Electron (e⁻)</span><span><i style="background:#fb7185"></i>Proton (H⁺)</span>
<span><i style="background:#38bdf8"></i>Hydrogen bubble</span><span><i style="background:#94a3b8"></i>Electron that did not become H₂</span><span><i style="background:#c084fc"></i>H₂ leaked to methanogens</span><span><i style="background:#a8a29e"></i>CO₂ released when bacteria eat</span>
</div>

<div class="panel">
<span class="lbl">Anode: where the bacteria live</span><div class="mats" id="an"></div>
<span class="lbl" style="margin-top:14px">Cathode catalyst: where hydrogen forms</span><div class="mats" id="ca"></div>
<span class="lbl" style="margin-top:14px">Reactor design</span><div class="mats" id="dz"></div>
</div>

<div class="panel controls">
<div><label for="vs">Applied voltage: <b id="vv">0.6 V</b></label><input type="range" id="vs" min="0.2" max="0.9" step="0.1" value="0.6"><div class="mut">The article gives 0.2–0.9 V for MECs, against 1.23–1.8 V for water electrolysis</div></div>
<div><label for="cs">Waste strength (COD): <b id="cv">2500 mg/L</b></label><input type="range" id="cs" min="500" max="5000" step="100" value="2500"></div>
<div><label for="ts">Sim speed: <b id="tv">1×</b></label><input type="range" id="ts" min="0.25" max="2" step="0.25" value="1"></div>
<div style="display:flex"><button id="pp" aria-pressed="false">Pause</button></div>
</div>

<div class="metrics">
<div class="panel"><div class="k">Hydrogen output vs plain felt</div><div class="v" id="rel">–</div><div class="s">same voltage and waste; felt anode + felt cathode in a double-chamber cell = 1×</div></div>
<div class="panel"><div class="k">Hydrogen conversion efficiency</div><div class="v" id="cvn">–</div><div class="s">share of electrons the cathode turns into H₂</div></div>
<div class="panel"><div class="k">Electrons reaching cathode</div><div class="v" id="ems">–</div><div class="s">per second, measured in the animation</div></div>
<div class="panel"><div class="k">Share that became H₂</div><div class="v" id="sh">–</div><div class="s">measured; grey fizzles and purple leaks are the rest</div></div>
<div class="panel"><div class="k">Reported catalyst stability</div><div class="v" id="stb">–</div><div class="s">how long the cited study stayed stable</div></div>
</div>

<div class="panel"><span class="lbl">Hydrogen output for each cathode catalyst, with your chosen anode</span><div id="cmp"></div>
<p class="note">The anode multipliers are current density, not litres of hydrogen. Here the extra electrons are multiplied by the cathode’s conversion efficiency, so treat the gold and iron bars as upper bounds. Single-chamber hydrogen loss follows Call & Logan (2008): about 2% of the gas was methane at 0.3–0.8 V, but 28% at 0.2 V when cycles ran long. The membrane’s 10% current penalty is a placeholder, because measured membrane resistances vary widely and no single figure fits.</p></div>

<div class="panel"><span class="lbl">Why platinum converts the most hydrogen</span>
<p class="note" style="margin:0 0 10px;color:var(--ink)">Platinum is the best-known catalyst for the hydrogen-forming step itself, while the other options are less active metals or plain carbon that barely helps.</p>
<div class="ev">
<span>It binds hydrogen “just right”</span><span>The classic explanation is the Sabatier volcano: the best catalysts hold hydrogen neither too weakly nor too strongly, and platinum sits near that sweet spot. More recent calculations say the full story is subtler, with unusually low reaction barriers on platinum.</span>
<span>It needs almost no extra push</span><span>In acidic solution platinum starts making hydrogen very close to the reaction’s equilibrium voltage and speeds up steeply with voltage (a Tafel slope near 30 mV per decade). It is described as the most efficient known electrocatalyst.</span>
<span>Metals beat carbon</span><span>In the 2019 MEC test, metal-loaded cathodes did better than carbon nanoparticles and nanotubes, which landed close to plain felt. Carbon helps as a conductive support, not as a catalyst.</span>
<span>Nickel is close behind</span><span>Ni/C reached 73.0% against 80.6% for Pt/C, with stability and current density almost comparable in that study.</span>
<span>Not always first</span><span>A review lists a nickel–cobalt–phosphide catalyst at 90.3% in a different study. Platinum tops one comparison, not every one, and different labs measure efficiency differently.</span>
<span>The catch</span><span>Platinum is rare and expensive, and sulfides and cyanides in real wastewater damage it, so it works better as a benchmark than a practical choice.</span>
</div>
<p class="note">Sources: Lindgren, Kastlunger &amp; Peterson (2019, arXiv:1903.09903, ACS Catal.); the 2019 platinum-substitutes study (Int. J. Hydrogen Energy 44:2258–2265), whose efficiencies I checked against its abstract; the 2022 Nanomaterials review (12:1316).</p></div>

<div class="panel"><span class="lbl">What the article reports</span>
<div class="ev">
<span>Gold anode</span><span>Up to 20× the current density of plain graphite, measured with Shewanella oneidensis (Fan et al. 2011). That is current, not hydrogen, and gold is costly at scale.</span>
<span>Palladium anode</span><span>50–150% more current density than plain graphite (Fan et al. 2011). The simulator uses the 2× midpoint.</span>
<span>Iron anode</span><span>Up to 5.89× the current density of plain graphite (Xu et al. 2012), with a much cheaper metal than gold.</span>
<span>Electrodeposited nickel cathode</span><span>Up to 5.4 L of hydrogen per litre of reactor per day with no membrane, stable for over a month, with under 5% methane (Hrapovic et al. 2010).</span>
<span>Nickel phosphide cathode</span><span>0.29 L of hydrogen per litre in 24 hours, the same as nickel, with 14× nickel’s current density, stable for 11 days (Kim et al. 2019). The simulator gives it nickel’s conversion efficiency. A review lists 65.5% cathodic hydrogen recovery for Ni₂P, measured a different way, so the two are not directly comparable.</span>
<span>Single vs double chamber</span><span>Single-chamber cells are cheaper with lower resistance, but hydrogen drifts to the anode where methanogens consume it. A membrane stops that but adds cost, resistance, pH gradients and biofouling.</span>
<span>Main barriers</span><span>Membrane fouling (silver nanoparticles help but disturb proton transport); real wastewater with varying pH and sulfides or cyanides that poison platinum, while most labs use clean acetate; trade-offs such as gold’s cost and nickel dissolving; and falling current density and hydrogen rate as reactors grow.</span>
<span>Cathode catalysts (2019 comparison)</span><span>Overall hydrogen conversion efficiency: platinum 80.6%, nickel-based 73.0%, carbon nanoparticles 47.0%, carbon nanotubes 38.9%, plain carbon felt 38.7%.</span>
<span>Voltage</span><span>MECs run on about 0.2–0.9 V because the bacteria supply part of the energy. Water electrolysis needs about 1.23 V in theory and 1.8 V in practice.</span>
<span>Durability</span><span>Electrodeposited nickel stayed stable for over a month and nickel phosphide for 11 days. A commercial plant would need years.</span>
<span>Scale-up</span><span>A 2024 pilot using nickel foam cathodes ran over 80 days on industrial wastewater and reported the highest pilot-scale hydrogen production recorded.</span>
<span>Cost context</span><span>About 95% of hydrogen is grey, from natural gas, at roughly $1.50/kg and 10–12 kg CO₂ per kg. Green hydrogen costs about $4–6/kg.</span>
<span>The article’s verdict</span><span>Not yet, and maybe not everywhere. The likeliest early use is on-site treatment of food-processing and municipal wastewater, with hydrogen as a bonus.</span>
</div>
<p class="note">Source: the article above, which draws on Fan et al. (2011), Xu et al. (2012), Hrapovic et al. (2010), Kim et al. (2019) and a 2019 platinum-alternatives study. This simulator is a teaching model, not a prediction of real reactor output.</p></div>
</div>

<script>
(function(){
const W=1000,H=520,$=id=>document.getElementById(id);
const AN={felt:{name:'Plain graphite felt',mult:1,sub:'1× current (baseline)',col:'#7c8798'},
 au:{name:'Gold-nanoparticle anode',mult:20,sub:'Up to 20× current density | costly',col:'#e0a82e'},
 pd:{name:'Palladium-nanoparticle anode',mult:2,sub:'50–150% more current (2× midpoint used)',col:'#a5b4fc'},
 fe:{name:'Iron-nanoparticle anode',mult:5.89,sub:'Up to 5.89× current density | cheaper metal',col:'#f87171'}};
const CA={felt:{name:'Plain carbon felt',eff:.387,col:'#94a3b8'},cnt:{name:'Carbon nanotubes',eff:.389,col:'#38bdf8'},
 cnp:{name:'Carbon nanoparticles',eff:.47,col:'#c084fc'},ni:{name:'Nickel-based catalyst',eff:.73,col:'#fb923c',stab:'over a month'},
 nip:{name:'Nickel phosphide',eff:.73,col:'#f472b6',stab:'11 days'},
 pt:{name:'Platinum (benchmark)',eff:.806,col:'#e2e8f0'}};
const S={V:.6,cod:2500,an:'felt',ca:'ni',dz:'double',paused:false,ts:1};
const DZ={double:{name:'Double-chamber (membrane)',col:'#34d399',sub:'Blocks H₂ leakage | costlier, more resistance, fouling'},single:{name:'Single-chamber (no membrane)',col:'#f59e0b',sub:'Cheaper, lower resistance | H₂ can leak to methanogens'}};
const RES={double:.9,single:1};
const leakF=()=>S.V<=.21?.28:.02; // single-chamber: methane was 28% of the gas at 0.2 V and about 2% at 0.3–0.8 V (Call & Logan 2008)
const cv=$('sim'),ctx=cv.getContext('2d');let sc=1;
function fit(){const r=cv.getBoundingClientRect(),d=window.devicePixelRatio||1;cv.width=Math.round(r.width*d);cv.height=Math.round(r.width*H/W*d);sc=cv.width/W}
window.addEventListener('resize',fit);fit();
const X={top:70,bot:440,wy:28};
let film=[],free=[],sub=[],E=[],P=[],B=[],L=[],G=[],arr=[],conv=[],simT=0,acc=0;
const pv=()=>.1+.9*(S.V-.2)/.7, mo=()=>S.cod/(S.cod+1500);
function build(){film=[];for(let i=0;i<12;i++)film.push({x:112+Math.random()*6,y:X.top+22+(X.bot-X.top-44)*(i+.5)/12,ph:Math.random()*6,fl:0,cd:Math.random()*1.5,tg:null});E=[];P=[];B=[];L=[];G=[];arr=[];conv=[];for(const s of sub)s.tg=null}
function mkFree(){free=[];for(let i=0;i<5;i++)free.push({x:200+Math.random()*230,y:80+Math.random()*340,a:Math.random()*6.28,t:Math.random()*2})}
function syncSub(){const n=Math.round(S.cod/60);while(sub.length<n)sub.push({x:170+Math.random()*280,y:70+Math.random()*360});sub.length=n}
build();mkFree();syncSub();

function card(g,k,x,s){return '<button class="mc" data-g="'+g+'" data-k="'+k+'" aria-pressed="'+(S[g]===k)+'" style="--c:'+x.col+'"><b>'+x.name+'</b><span>'+s+'</span></button>'}
function cards(){
 $('an').innerHTML=Object.keys(AN).map(k=>card('an',k,AN[k],AN[k].sub)).join('');
 $('ca').innerHTML=Object.keys(CA).map(k=>card('ca',k,CA[k],(CA[k].eff*100).toFixed(1)+'% hydrogen conversion'+(CA[k].stab?' | stable '+CA[k].stab:''))).join('');
 $('dz').innerHTML=Object.keys(DZ).map(k=>card('dz',k,DZ[k],DZ[k].sub)).join('');
}
cards();
document.addEventListener('click',e=>{const b=e.target.closest('.mc');if(!b)return;S[b.dataset.g]=b.dataset.k;cards();build();metrics()});

function spawn(b){
 if(E.length<450)E.push({x:b.x,y:b.y,i:0,pts:[[75,b.y],[75,X.wy],[925,X.wy],[925,90+Math.random()*340]]});
 if(P.length<250)P.push({x:b.x+6,y:b.y+(Math.random()-.5)*10});
}
const cdm=()=>2/(mo()*pv()*AN[S.an].mult*RES[S.dz]); // seconds between meals per bacterium (the pace the anode and voltage allow)
function eat(b,s){b.tg=null;b.fl=.45;b.cd=cdm()*(.6+.8*Math.random());s.tg=null;s.x=150+Math.random()*305;s.y=70+Math.random()*360;G.push({x:b.x+8,y:b.y,t:0});spawn(b)}
function step(dt){
 simT+=dt;const v=pv(),eff=CA[S.ca].eff;
 for(const b of film){
  if(b.tg&&sub.indexOf(b.tg)<0)b.tg=null;
  if(b.tg){const s=b.tg,dx=b.x-s.x,dy=b.y-s.y,d=Math.hypot(dx,dy),m=450*dt;if(d<=m+8)eat(b,s);else{s.x+=dx/d*m;s.y+=dy/d*m}}
  else{b.cd-=dt;if(b.cd<=0){const fr=sub.filter(s=>!s.tg),best=fr[Math.floor(Math.random()*fr.length)];if(best){best.tg=b;b.tg=best}else b.cd=.2}}
 }
 const sp=360*(.6+.4*v)*dt;
 for(let i=E.length-1;i>=0;i--){
  const e=E[i],p=e.pts[e.i],dx=p[0]-e.x,dy=p[1]-e.y,d=Math.hypot(dx,dy);
  if(sp>=d){e.x=p[0];e.y=p[1];e.i++;
   if(e.i>=e.pts.length){arr.push(simT);
    if(Math.random()<eff){const lk=S.dz==='single'&&Math.random()<leakF();B.push({x:918,bx:918,y:e.y,r:2.5+Math.random()*3,vy:30+Math.random()*30,ph:Math.random()*6,lk});if(!lk)conv.push(simT)}
    else L.push({x:918,y:e.y,t:0});
    E.splice(i,1)}
  }else{e.x+=dx/d*sp;e.y+=dy/d*sp}
 }
 for(let i=P.length-1;i>=0;i--){const q=P[i];q.x+=(90+220*v)*dt;q.y+=(Math.random()-.5)*90*dt;q.y=Math.max(70,Math.min(430,q.y));if(q.x>905)P.splice(i,1)}
 for(let i=B.length-1;i>=0;i--){const b=B[i];if(b.lk){b.x-=90*dt;b.y-=b.vy*.2*dt;if(b.x<150||b.y<64)B.splice(i,1);continue}b.y-=b.vy*dt;b.x=b.bx+Math.sin(b.y*.06+b.ph)*5;b.r+=dt*.4;if(b.y<64)B.splice(i,1)}
 for(let i=L.length-1;i>=0;i--){L[i].t+=dt;if(L[i].t>.7)L.splice(i,1)}
 for(let i=G.length-1;i>=0;i--){G[i].t+=dt;G[i].y-=14*dt;G[i].x+=8*dt;if(G[i].t>1.2)G.splice(i,1)}
 for(const f of free){f.t-=dt;if(f.t<=0){f.t=1+Math.random()*1.5;f.a=Math.random()*6.28}
  f.x+=Math.cos(f.a)*26*dt;f.y+=Math.sin(f.a)*26*dt;
  if(f.x<180||f.x>450){f.a=Math.PI-f.a;f.x=Math.max(180,Math.min(450,f.x))}
  if(f.y<70||f.y>430){f.a=-f.a;f.y=Math.max(70,Math.min(430,f.y))}}
 for(const s of sub){if(s.tg)continue;s.x+=(Math.random()-.5)*70*dt;s.y+=(Math.random()-.5)*70*dt;s.x=Math.max(150,Math.min(455,s.x));s.y=Math.max(62,Math.min(438,s.y))}
 for(const b of film)if(b.fl>0)b.fl-=dt;
 while(arr.length&&arr[0]<simT-5)arr.shift();while(conv.length&&conv[0]<simT-5)conv.shift();
}
function rod(x,y,a,len,w,col,glow){
 ctx.save();ctx.translate(x,y);ctx.rotate(a);
 if(glow>0){ctx.fillStyle='rgba(250,204,21,'+(glow*1.6)+')';ctx.beginPath();ctx.ellipse(0,0,len+5,w+5,0,0,6.28);ctx.fill()}
 ctx.fillStyle=col;ctx.beginPath();ctx.ellipse(0,0,len,w,0,0,6.28);ctx.fill();ctx.restore();
}
function dot(x,y,r,c){ctx.fillStyle=c;ctx.beginPath();ctx.arc(x,y,r,0,6.28);ctx.fill()}
function draw(){
 ctx.setTransform(sc,0,0,sc,0,0);ctx.fillStyle='#030712';ctx.fillRect(0,0,W,H);
 const a=AN[S.an],c=CA[S.ca];
 for(const x of[30,530]){ctx.fillStyle='rgba(18,32,58,.55)';ctx.fillRect(x,50,440,400);ctx.strokeStyle='#2c4064';ctx.lineWidth=2;ctx.strokeRect(x,50,440,400);
  ctx.strokeStyle='rgba(56,189,248,.25)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x,62);ctx.lineTo(x+440,62);ctx.stroke()}
 const dbl=S.dz==='double';ctx.fillStyle=dbl?'#22314d':'#0b1528';ctx.fillRect(dbl?470:466,50,dbl?60:68,400);if(dbl){ctx.fillStyle='#050b16';for(let y=62;y<445;y+=14)ctx.fillRect(494,y,12,5)}
 ctx.save();ctx.translate(488,250);ctx.rotate(-Math.PI/2);ctx.fillStyle='#93a3bd';ctx.font='12px system-ui';ctx.textAlign='center';ctx.fillText(dbl?'Proton exchange membrane':'No membrane: one shared tank',0,0);ctx.restore();
 // anode
 ctx.fillStyle='#7c8798';ctx.globalAlpha=.9;ctx.fillRect(60,X.top,30,X.bot-X.top);ctx.globalAlpha=1;
 for(let y=X.top;y<X.bot;y+=18)ctx.fillRect(90,y,6+((y*7)%6),10);
 if(S.an!=='felt'){ctx.fillStyle=a.col;for(let i=0;i<80;i++){ctx.beginPath();ctx.arc(88+((i*37)%16),X.top+4+(i*4.7)%360,2.4,0,6.28);ctx.fill()}}
 // cathode
 ctx.fillStyle=c.col;ctx.globalAlpha=.85;ctx.fillRect(910,X.top,30,X.bot-X.top);ctx.globalAlpha=1;
 if(S.ca==='felt'){for(let y=X.top;y<X.bot;y+=18)ctx.fillRect(898,y,12,8)}
 else if(S.ca==='cnt'){ctx.strokeStyle='#7dd3fc';ctx.lineWidth=2;ctx.lineCap='round';for(let i=0;i<30;i++){const y=X.top+i*12;ctx.beginPath();ctx.moveTo(910,y);ctx.quadraticCurveTo(902,y+Math.sin(simT+i)*3,892,y+3);ctx.stroke()}}
 else{const r=S.ca==='ni'?3.2:2.2;for(let i=0;i<70;i++){ctx.beginPath();ctx.arc(896+(i*37)%14,X.top+4+(i*5.1)%360,r,0,6.28);ctx.fill()}}
 // wire + source
 ctx.strokeStyle='#cbd5e1';ctx.lineWidth=3;ctx.lineCap='butt';ctx.beginPath();ctx.moveTo(75,X.top);ctx.lineTo(75,X.wy);ctx.lineTo(925,X.wy);ctx.lineTo(925,X.top);ctx.stroke();
 ctx.fillStyle='#0c1424';ctx.fillRect(470,10,60,36);ctx.strokeRect(470,10,60,36);ctx.fillStyle='#38bdf8';ctx.font='bold 15px system-ui';ctx.textAlign='center';ctx.fillText(S.V.toFixed(1)+' V',500,34);
 ctx.fillStyle='#93a3bd';ctx.font='13px system-ui';ctx.textAlign='left';ctx.fillText('Anode (−): '+a.name,40,478);
 ctx.textAlign='right';ctx.fillText('Cathode (+): '+c.name,960,478);
 for(const s of sub)dot(s.x,s.y,s.tg?3.6:2.8,s.tg?'#fde047':'rgba(253,230,138,.85)');
 for(const f of free)rod(f.x,f.y,f.a,9,4,'#22c55e',0);
 for(const b of film)rod(b.x,b.y,Math.PI/2+Math.sin(simT*2+b.ph)*.35,9,4.5,'#4ade80',Math.max(0,b.fl));
 for(const g of G)dot(g.x,g.y,2.4,'rgba(168,162,158,'+((1-g.t/1.2)*.9)+')');
 for(const q of P)dot(q.x,q.y,2.8,'#fb7185');
 for(const e of E){dot(e.x,e.y,4.5,'rgba(250,204,21,.25)');dot(e.x,e.y,2.8,'#facc15')}
 for(const l of L){ctx.strokeStyle='rgba(148,163,184,'+(1-l.t/.7)+')';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(l.x,l.y,3+l.t*14,0,6.28);ctx.stroke();dot(l.x,l.y,2,'rgba(148,163,184,'+(1-l.t/.7)+')')}
 for(const b of B){ctx.fillStyle=b.lk?'rgba(192,132,252,.25)':'rgba(56,189,248,.22)';ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,6.28);ctx.fill();ctx.strokeStyle=b.lk?'#c084fc':'#7dd3fc';ctx.lineWidth=1;ctx.stroke()}
}
const out=k=>AN[S.an].mult*CA[k].eff*RES[S.dz]*(S.dz==='single'?1-leakF():1),rel=k=>out(k)/(CA.felt.eff*RES.double);
function metrics(){
 const w=Math.min(5,Math.max(simT,1));
 $('rel').textContent=rel(S.ca).toFixed(1)+'×';
 $('cvn').textContent=(CA[S.ca].eff*100).toFixed(1)+'%';
 $('stb').textContent=CA[S.ca].stab?'Stable '+CA[S.ca].stab:'Not reported';
 $('ems').textContent=(arr.length/w).toFixed(1)+' /s';
 $('sh').textContent=arr.length>8?Math.round(conv.length/arr.length*100)+'%':'–';
 const ks=Object.keys(CA),mx=Math.max(...ks.map(rel));
 $('cmp').innerHTML=ks.map(k=>'<div class="row'+(k===S.ca?' on':'')+'"><span class="nm">'+CA[k].name+'</span><div class="track"><div class="fill" style="width:'+(rel(k)/mx*100).toFixed(0)+'%;background:'+CA[k].col+'"></div></div><span>'+rel(k).toFixed(1)+'×</span></div>').join('');
}
let last=performance.now(),lastM=0;
function frame(now){const d=Math.min(.05,(now-last)/1000);last=now;if(!S.paused)step(d*S.ts);draw();if(now-lastM>250){lastM=now;metrics()}requestAnimationFrame(frame)}
$('vs').addEventListener('input',e=>{S.V=parseFloat(e.target.value);$('vv').textContent=S.V.toFixed(1)+' V'});
$('cs').addEventListener('input',e=>{S.cod=parseInt(e.target.value);$('cv').textContent=S.cod+' mg/L';syncSub()});
$('ts').addEventListener('input',e=>{S.ts=parseFloat(e.target.value);$('tv').textContent=S.ts+'×'});
$('pp').addEventListener('click',e=>{S.paused=!S.paused;e.target.setAttribute('aria-pressed',S.paused);e.target.textContent=S.paused?'Resume':'Pause';$('live').textContent=S.paused?'● Simulation paused':'● Live molecular simulation active'});
metrics();requestAnimationFrame(frame);
})();
</script>
</body>
</html>
"""

components.html(HTML, height=2300, scrolling=True)
