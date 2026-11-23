// ===== kit de cenas reutilizáveis =====
const w = i => WD[i][0];
const CUES = [];
function cue(t, sfx, v = 1, o = {}) { CUES.push({ t: +t.toFixed(3), sfx, v, shake: o.sh || 0, flash: o.fl || 0, chroma: o.ch || 0, blur: o.bl || 0 }); }
const SIDE = '#3d1680';


const STARS = (() => { const r = mulberry32(31), a = []; for (let i = 0; i < 320; i++) a.push({ x: r() * W, y: r() * H, s: 0.6 + r() * 2.2, d: r() }); return a; })();
function pcFace3(t, em) {
  return (i, li) => {
    const glass = i === 3 || i === 2;
    if (em) return { fill: null, draw: glass ? (c, w2, h2) => fans(c, w2, h2, t, true) : (i === 0 ? (c, w2, h2) => { c.fillStyle = L; c.fillRect(w2 * 0.82, h2 * 0.08, 10, h2 * 0.84); } : null) };
    if (i === 0) return { fill: mix('#1a1a1a', '#000000', 1 - li), stroke: '#3a3a3a', draw: (c, w2, h2) => { c.fillStyle = L; c.fillRect(w2 * 0.82, h2 * 0.08, 10, h2 * 0.84); c.fillStyle = '#2c2c2c'; for (let k = 0; k < 14; k++) c.fillRect(w2 * 0.12, h2 * 0.1 + k * h2 * 0.055, w2 * 0.55, 4); c.strokeStyle = L; c.lineWidth = 4; c.beginPath(); c.arc(w2 * 0.4, h2 * 0.92, 14, 0, 7); c.stroke(); } };
    if (glass) return { fill: mix('#1d0e3a', '#000000', 0.5 - li * 0.4), stroke: '#666', draw: (c, w2, h2) => { fans(c, w2, h2, t, false); c.fillStyle = 'rgba(255,255,255,0.07)'; c.beginPath(); c.moveTo(0, 0); c.lineTo(w2 * 0.45, 0); c.lineTo(0, h2 * 0.55); c.fill(); } };
    return { fill: mix('#2a2a2a', '#050505', 1 - li), stroke: '#3a3a3a' };
  };
}

let BADC = null;
function badTex(t, cw = 960, ch = 540) { if (!BADC || BADC.c.width !== cw) BADC = mk(cw, ch); BADC.x.setTransform(1, 0, 0, 1, 0, 0); BADC.x.clearRect(0, 0, cw, ch); badVideo(BADC.x, 0, 0, cw, ch, t, 22); return BADC.c; }
function stampTex(key, s, sz, bgc, fc) { return TXC.get(key) || (() => { const tt = TX(s, sz, fc); const c = mk(tt.w + sz * 0.5, tt.h + sz * 0.32); c.x.fillStyle = bgc; rr(c.x, 0, 0, c.c.width, c.c.height, 16); c.x.fill(); c.x.drawImage(tt.c, sz * 0.25, sz * 0.16); TXC.set(key, c.c); return c.c; })(); }
function stamp3(ctx, t, t0, key, s, sz, o = {}) {
  if (t < t0) return; const tex = stampTex(key, s, sz, o.bg || L, o.fc || K);
  const k = sp(t, t0, 0.45, 17); const pose = { x: o.x || 0, y: o.y || 0, z: lerp(-1300, o.z || -150, k), rz: lerp(0.6, o.rz ?? -0.05, k), ry: 0.1 * Math.sin((t - t0) * 2.5), rx: 0.05 };
  let al = clamp((t - t0) / 0.04); if (o.out && t > o.out) { const u = eiExp(P(t, o.out, o.out + 0.2)); pose.z -= 1200 * u; al *= 1 - u; }
  const side = TXC.get(key + 's') || (() => { const c = mk(tex.width, tex.height); c.x.fillStyle = mix(o.bg || L, '#000000', 0.55); rr(c.x, 0, 0, tex.width, tex.height, 16); c.x.fill(); TXC.set(key + 's', c.c); return c.c; })();
  for (let i = 6; i >= 1; i--) plane(ctx, side, pose, 1, tex.width, tex.height, i * 7, al);
  plane(ctx, tex, pose, 2, tex.width, tex.height, 0, al);
  glow(ctx, g => plane(g, tex, pose, 1), (0.3 + 1.0 * Math.exp(-(t - t0) * 5)) * al, 8);
}
// painel de chat
let CHC = null;
function chatTex(t, title, msg, ty0, ty1, send, dots0, dots1, reply) {
  if (!CHC) CHC = mk(900, 760); const c = CHC.x, pw = 900, ph = 760; c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, pw, ph);
  rr(c, 0, 0, pw, ph, 30); c.fillStyle = '#111114'; c.fill(); c.strokeStyle = '#2e2e34'; c.lineWidth = 3; c.stroke();
  c.fillStyle = '#1a1a1e'; rr(c, 0, 0, pw, 74, [30, 30, 0, 0]); c.fill();
  if (title === 'Claude') { c.fillStyle = '#d97757'; c.beginPath(); c.arc(pw / 2 - tw(title, 30, 'Inter', 800) / 2 - 30, 37, 11, 0, 7); c.fill(); }
  T(c, title, pw / 2, 38, 30, WH, { f: 'Inter', w: 800 });
  const n = Math.floor(clamp((t - ty0) / (ty1 - ty0)) * msg.length), sent = t >= send;
  c.fillStyle = '#1d1d22'; rr(c, 30, ph - 112, pw - 60, 82, 41); c.fill();
  if (!sent) T(c, msg.slice(0, n) + ((Math.floor(t * 3) % 2) ? '|' : ''), 70, ph - 70, 30, '#e8e8e8', { f: 'Inter', w: 500, a: 'left' });
  else T(c, 'Pergunte qualquer coisa', 70, ph - 70, 26, '#555', { f: 'Inter', a: 'left' });
  c.fillStyle = n > 0 ? L : '#333'; c.beginPath(); c.arc(pw - 80, ph - 71, 27, 0, 7); c.fill();
  c.strokeStyle = K; c.lineWidth = 5; c.beginPath(); c.moveTo(pw - 80, ph - 58); c.lineTo(pw - 80, ph - 84); c.moveTo(pw - 92, ph - 73); c.lineTo(pw - 80, ph - 86); c.lineTo(pw - 68, ph - 73); c.stroke();
  if (sent) { const kb = sp(t, send, 0.7, 14), by = lerp(ph - 160, 110, kb); c.font = '600 28px Inter'; const bw = Math.min(pw - 80, c.measureText(msg).width + 52); c.fillStyle = V; rr(c, pw - 40 - bw, by, bw, 66, 26); c.fill(); T(c, msg, pw - 40 - bw + 26, by + 34, 28, WH, { f: 'Inter', w: 600, a: 'left' }); }
  if (t >= dots0 && t < dots1) { c.fillStyle = '#222'; rr(c, 40, 220, 130, 60, 26); c.fill(); for (let i = 0; i < 3; i++) { c.fillStyle = rgba(WH, 0.3 + 0.6 * (Math.floor(t * 8 + i) % 3 === 0)); c.beginPath(); c.arc(80 + i * 26, 250, 8, 0, 7); c.fill(); } }
  if (t >= dots1 && reply) { c.fillStyle = '#222'; rr(c, 40, 220, 400, 60, 26); c.fill(); T(c, reply, 66, 251, 25, '#ddd', { f: 'Inter', w: 500, a: 'left' }); }
  return CHC.c;
}
function swipeBG(ctx, t, segs) { // segs: [[t0,color]], wipe diagonal
  let i = 0; segs.forEach((s, j) => { if (t >= s[0] - 0.07) i = j; });
  if (i > 0) bg(ctx, segs[i - 1][1]); const p = eo3(P(t, segs[i][0] - 0.07, segs[i][0] + 0.04)), ex = lerp(-600, W + 600, p);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.beginPath(); ctx.moveTo(-800, 0); ctx.lineTo(ex + 320, 0); ctx.lineTo(ex - 320, H); ctx.lineTo(-800, H); ctx.closePath(); ctx.fillStyle = segs[i][1]; ctx.fill();
  if (segs[i][1] === K || segs[i][1] === DV) radial(ctx, W / 2, H / 2, 1000, V, 0.4); if (segs[i][1] === L) radial(ctx, W / 2, H / 2, 1000, '#ffffff', 0.3); ctx.restore();
  return i;
}


function rowX(ws, sz) { const tot = ws.reduce((a, s) => a + tw(s + ' ', sz), 0) - tw(' ', sz); let x = -tot / 2; return ws.map(s => { const c = x + tw(s, sz) / 2; x += tw(s + ' ', sz); return c; }); }

// divide o logo em 2 partes pela maior coluna vazia (ex.: MOTION | IA). Sem vão -> parte 2 vazia.
function logoSplit(img) {
  const c = mk(img.width, img.height); c.x.drawImage(img, 0, 0); const d = c.x.getImageData(0, 0, img.width, img.height).data, wd = img.width, ht = img.height;
  const col = new Array(wd).fill(0); for (let x = 0; x < wd; x++) for (let y = 0; y < ht; y += 2) if (d[(y * wd + x) * 4 + 3] > 20) { col[x] = 1; break; }
  let best = null, s = null; for (let x = Math.floor(wd * 0.3); x < Math.floor(wd * 0.85); x++) { if (!col[x] && s === null) s = x; if (col[x] && s !== null) { if (!best || x - s > best[1] - best[0]) best = [s, x]; s = null; } }
  return best && best[1] - best[0] >= wd * 0.02 ? Math.round((best[0] + best[1]) / 2) : wd - 1;
}

let LGT = null;
function logoTex() {
  if (LGT) return LGT; const img = LOGO_IMG, wd = img.width, ht = img.height, sp2 = (typeof LOGO_SPLIT === 'number') ? LOGO_SPLIT : logoSplit(img);
  const part = (x0, x1, col) => { const c = mk(x1 - x0, ht); c.x.drawImage(img, x0, 0, x1 - x0, ht, 0, 0, x1 - x0, ht); if (col) { c.x.globalCompositeOperation = 'source-in'; c.x.fillStyle = col; c.x.fillRect(0, 0, x1 - x0, ht); } return c.c; };
  LGT = { M: part(0, sp2), I: part(sp2, wd), Ms: part(0, sp2, '#3a1580'), Is: part(sp2, wd, '#3a1580'), Md: part(0, sp2, '#12062b'), Id: part(sp2, wd, '#12062b'), Ml: part(0, sp2, L), Il: part(sp2, wd, L), wd, ht, sp2 };
  return LGT;
}
let GLC = null;
function glintTex(src, p) { if (!GLC || GLC.c.width < src.width) GLC = mk(src.width, src.height); const g = GLC.x; g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, GLC.c.width, GLC.c.height); g.drawImage(src, 0, 0); g.globalCompositeOperation = 'source-in'; const gx = lerp(-src.width * 0.3, src.width * 1.3, p); const gr = g.createLinearGradient(gx - 160, 0, gx + 60, src.height); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(0.45, 'rgba(255,255,255,0)'); gr.addColorStop(0.52, 'rgba(255,255,255,1)'); gr.addColorStop(0.6, 'rgba(198,255,52,0.9)'); gr.addColorStop(0.66, 'rgba(255,255,255,0)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, src.width, src.height); return GLC.c; }
function logo3(ctx, t, o, parts, glintP, glowAmt) {
  const L2 = logoTex(), sc = o.s ?? 1;
  parts.forEach(([which, po]) => {
    const face = L2[which], side = L2[which + 's'], dark = L2[which + 'd'], lime = L2[which + 'l'], fw = face.width, fh = face.height;
    const cx = which === 'M' ? -L2.wd / 2 + fw / 2 : -L2.wd / 2 + L2.sp2 + fw / 2;
    const ob = { ...po, parent: { ...o, s: sc } }; ob.x = (po.x || 0) + cx;
    const front = facing(ob, fw, fh), n = 10, d = 44;
    if (front) { for (let i = n; i >= 1; i--) plane(ctx, i > 4 ? dark : side, ob, 1, fw, fh, d * i / n, po.al ?? 1); plane(ctx, face, ob, 3, fw, fh, 0, po.al ?? 1); if (glintP > 0 && glintP < 1) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; plane(ctx, glintTex(face, glintP), ob, 3, fw, fh, -0.5, po.al ?? 1); ctx.restore(); } }
    else { plane(ctx, face, ob, 3, fw, fh, 0, po.al ?? 1); for (let i = 1; i <= n; i++) plane(ctx, side, ob, 1, fw, fh, d * i / n, po.al ?? 1); }
    if (glowAmt > 0) glow(ctx, g => plane(g, lime, ob, 2, fw, fh), glowAmt * (po.al ?? 1), 8);
  });
}

function beatPulse(t) { let best = 9; for (const b of BEATS) { const d = t - b; if (d >= 0 && d < best) best = d; } return Math.exp(-best * 6); }



// ===== runtime: registro de cenas, câmera de impacto, blur de transição, seek/frame =====
const SCENES = [];
function scene(t0, fn) { SCENES.push([t0, fn]); }
function finalizeScenes() { SCENES.sort((a, b) => a[0] - b[0]); SCENES.forEach(([a], i) => { if (i > 0) cue(a, 'blurcue', 0, { bl: 0.35 }); }); }
function sceneAt(t) { let f = SCENES[0][1]; for (const [a, fn] of SCENES) if (t >= a) f = fn; return f; }
function camApply(ctx, t) { if (NOPOST) return; const p = Math.min(1, envAt(t, 'shake')); const z = 1 + 0.05 * p; ctx.translate(W / 2, H / 2); ctx.rotate(0.012 * p * Math.sin(t * 40)); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2); }
let CUR_T = 0;
const PBA = mk(480, 270), PBB = mk(480, 270);
function blurAt(t) { let s = 0; for (const c of CUES) { if (!c.blur) continue; const d = (t - c.t) / 0.09; if (Math.abs(d) < 3) s += c.blur * Math.exp(-d * d); } return Math.min(1, s); }
function post2(t) {
  const b = blurAt(t);
  if (b > 0.02) { PBA.x.setTransform(1, 0, 0, 1, 0, 0); PBA.x.drawImage(C, 0, 0, 480, 270); PBB.x.setTransform(1, 0, 0, 1, 0, 0); PBB.x.clearRect(0, 0, 480, 270); PBB.x.filter = `blur(${2 + 6 * b}px)`; PBB.x.drawImage(PBA.c, 0, 0); PBB.x.filter = 'none'; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = Math.min(1, b * 1.3); X.drawImage(PBB.c, 0, 0, W, H); X.restore(); }
  post(t);
}
window.seek = function (t) {
  CUR_T = t; X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1; X.globalCompositeOperation = 'source-over'; X.filter = 'none';
  X.fillStyle = '#000'; X.fillRect(0, 0, W, H);
  X.save(); camApply(X, t); sceneAt(t)(X, t); X.restore();
  post2(t);
};
const ACC = mk(W, H);
window.frame = function (t, sub) { window.seek(t); if (!sub) return; ACC.x.setTransform(1, 0, 0, 1, 0, 0); ACC.x.globalAlpha = 1; ACC.x.drawImage(C, 0, 0); window.seek(t + sub); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 0.5; X.drawImage(ACC.c, 0, 0); X.globalAlpha = 1; };
