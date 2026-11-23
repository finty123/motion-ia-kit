// EXEMPLO COMPLETO — vídeo 'Motion com IA / Comenta MOTION' (83,5 s, 16:9)
// Usa WD (palavras da narração cortada) e BEATS. Leia junto com examples/motion-ia/README.md
// ===== Cenas v2: 1–10 =====
// ---------- S1: TU É DOOOOOOOOOIDO ----------
const S1 = (() => {
  const sz = 380, row = [];
  const chars = ['D', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'I', 'D', 'O'];
  const times = [w(2) - 0.07]; for (let i = 1; i <= 9; i++) times.push(w(2) + 0.02 + i * 0.075); times.push(1.73, 1.83, 1.94);
  return { sz, chars, times, row };
})();
function s1layout() {
  if (S1.row.length) return S1.row;
  let x = -200;
  S1.chars.forEach((ch, i) => { const cw = tw(ch, S1.sz); S1.row.push({ ch, t: S1.times[i], x: x + cw / 2, w: cw }); x += cw + 6; });
  return S1.row;
}
function S1f(ctx, t) {
  const row = s1layout(), last = row[row.length - 1];
  // câmera acompanha a cabeça da palavra
  let cx = 0; let prev = 0;
  for (const L2 of row) { const target = L2.x - 240; cx += (target - prev) * sp(t, L2.t, 0.85, 9); prev = target; }
  const fin = sp(t, 2.0, 0.9, 8); cx = lerp(cx, last.x, fin);
  const dive = P(t, 2.24, 2.96), dz = eiExp(dive) * 1290;
  setCam3({ x: cx, y: lerp(-40, 70, fin) + 20 * Math.sin(t * 3), z: 120 + dz + 60 * t, ry: 0.18 * Math.sin(t * 1.7) * (1 - fin), rz: 0.05 * Math.sin(t * 2.3) * (1 - dive) + 0.25 * eiExp(dive), rx: -0.06 });
  bgv(ctx, K, V, 0.3 + 0.2 * P(t, 0.9, 1.6));
  // streaks de velocidade (parallax)
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); const r = mulberry32(3);
  for (let i = 0; i < 28; i++) { const y = r() * H, len = 100 + r() * 400, sp2 = 0.4 + r(), x = ((r() * 4000 - cx * sp2 * 1.4) % (W + 600) + W + 600) % (W + 600) - 300; ctx.strokeStyle = rgba(i % 3 ? WH : L, 0.06 + 0.06 * (i % 3 === 0)); ctx.lineWidth = 1 + r() * 3; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + len, y); ctx.stroke(); }
  ctx.restore();
  // TU É
  W3(ctx, t, 'TU', w(0) - 0.06, { x: -150, y: -300, size: 210, from: { z: -900, rz: 0.5, ry: 0.8 }, side: SIDE, glow: 0.15 });
  W3(ctx, t, 'É', w(1) - 0.08, { x: 120, y: -300, size: 210, face: L, side: SIDE, from: { z: -900, rz: -0.5, ry: -0.9 }, glow: 0.3 });
  // D O O O ... I D O
  row.forEach((L2, i) => {
    const isLast = i === row.length - 1;
    const fr = i % 2 ? { z: 1600, ry: 1.6, rx: -0.4 } : { z: -700, rx: 1.2, rz: 0.3 };
    const op = { x: L2.x, y: 70, size: S1.sz, side: SIDE, from: fr, glow: 0.12, flash: 0.8, w: 17, depth: 70 };
    if (isLast) op.inner = (face, po) => { const hw = face.w * 0.42, hh = face.h * 0.72; const hc = TXC.get('hole') || (() => { const c = mk(200, 380); const g = c.x.createRadialGradient(100, 190, 10, 100, 190, 200); g.addColorStop(0, V); g.addColorStop(1, DV); c.x.fillStyle = g; rr(c.x, 0, 0, 200, 380, 100); c.x.fill(); TXC.set('hole', c.c); return c.c; })(); plane(ctx, hc, po, 2, hw, hh, 0.5); };
    W3(ctx, t, L2.ch, L2.t, op);
  });
  L3(ctx, t, 'rapaz', w(3) - 0.04, { x: last.x, y: 70 + 250, size: 58, col: L });
  if (dive > 0.86) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = P(dive, 0.86, 0.97); ctx.fillStyle = DV; ctx.fillRect(0, 0, W, H); ctx.restore(); }
}
cue(w(0), 'hit_small', 0.6, { sh: 0.2 }); cue(w(1), 'hit_small', 0.65, { sh: 0.25, ch: 0.3 });
S1.times.forEach((tt, i) => { if (i === 0) cue(tt + 0.07, 'boom', 0.85, { sh: 0.6, ch: 0.5, fl: 0.2 }); else if (i === S1.times.length - 1) cue(tt + 0.06, 'hit_med', 0.7, { sh: 0.4 }); else cue(tt + 0.05, i % 2 ? 'whoosh_small' : 'tick', 0.42); });
cue(w(3), 'tick', 0.5); cue(2.22, 'dive', 0.9, { bl: 0.6 });

// ---------- S2: tá de brincadeira comigo, né? ----------
function S2f(ctx, t) {
  const u = P(t, w(4), w(9));
  setCam3({ ry: lerp(0.45, -0.3, eio(u)), rx: lerp(-0.15, 0.08, u), z: lerp(-200, 250, eio(u)), rz: lerp(-0.08, 0.05, u), y: 20 * Math.sin(t * 4) });
  bgv(ctx, DV, V, 0.55, W / 2, H * 0.45); bokeh(ctx, t);
  W3(ctx, t, 'TÁ', w(4) - 0.07, { x: -130, y: -290, size: 170, side: SIDE, from: { z: -900, rx: 1.4 }, glow: 0.1 });
  W3(ctx, t, 'DE', w(5) - 0.07, { x: 130, y: -290, size: 170, side: SIDE, from: { z: -900, rx: -1.4 }, glow: 0.1 });
  W3(ctx, t, 'BRINCADEIRA', w(6) - 0.08, { x: 0, y: -30, size: 290, side: SIDE, from: { z: 2600, ry: -1.8 }, glow: 0.25, flash: 1.1, depth: 60 });
  const wc = tw('COMIGO, ', 190), wn = tw('NÉ?', 240), x0 = -(wc + wn) / 2;
  W3(ctx, t, 'COMIGO,', w(7) - 0.07, { x: x0 + tw('COMIGO,', 190) / 2, y: 260, size: 190, side: SIDE, from: { y: -500, z: 400, rx: -1.6 }, glow: 0.1 });
  W3(ctx, t, 'NÉ?', w(8) - 0.08, { x: x0 + wc + wn / 2, y: 255, size: 240, face: L, side: SIDE, from: { z: -1200, rz: 0.8 }, glow: 0.5, flash: 1.4, zeta: 0.35 });
  ring(ctx, t, w(8), L, 2400, 30, 0.7);
}
cue(w(4) - 0.04, 'whoosh_fast', 0.6); cue(w(4), 'hit_small', 0.45); cue(w(5), 'hit_small', 0.45); cue(w(6), 'impact', 0.8, { sh: 0.5, ch: 0.4 }); cue(w(7), 'hit_small', 0.55); cue(w(8), 'hit_med', 0.75, { sh: 0.45, fl: 0.15 });

// ---------- S3: congela / PERA AÍ ----------
let FREEZE2 = null;
function S3f(ctx, t) {
  if (!FREEZE2) { const c = mk(W, H); const sv = CAM3; NOPOST = true; S2f(c.x, w(9) - 0.05); NOPOST = false; CAM3 = sv; FREEZE2 = c.c; }
  const u = eo3(P(t, w(9), w(9) + 0.5));
  setCam3({ rz: -0.06 * u, ry: 0.1 * Math.sin(t * 2), z: 80 * u });
  bg(ctx, K);
  plane(ctx, FREEZE2, { z: lerp(0, 700, u), rx: lerp(0, 0.5, u), rz: lerp(0, -0.12, u), y: lerp(0, 80, u) }, 6, W, H, 0, lerp(1, 0.28, u));
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = 'rgba(255,255,255,0.04)'; for (let y = 0; y < H; y += 6) ctx.fillRect(0, y, W, 2);
  const ph = lerp(0.82, 0.3, eo3(P(t, w(9), w(9) + 0.45))); ctx.fillStyle = '#333'; ctx.fillRect(260, 1000, W - 520, 8); ctx.fillStyle = L; ctx.fillRect(260, 1000, (W - 520) * ph, 8); ctx.beginPath(); ctx.arc(260 + (W - 520) * ph, 1004, 15, 0, 7); ctx.fill(); ctx.restore();
  W3(ctx, t, 'NÃO,', w(9) - 0.06, { x: -190, y: -250, size: 150, side: SIDE, from: { z: -900, rz: 0.4 }, glow: 0.05 });
  W3(ctx, t, 'PÔ,', w(10) - 0.06, { x: 200, y: -250, size: 150, side: SIDE, from: { z: -900, rz: -0.4 }, glow: 0.05 });
  if (t >= w(11) - 0.08) {
    const k = sp(t, w(11) - 0.08, 0.45, 18), pose = { x: 0, y: 80, z: lerp(-1000, 0, k), rz: lerp(0.5, -0.05, k), ry: 0.12 * Math.sin((t - 5) * 2) };
    const tex = TXC.get('perabox') || (() => { const tt = TX('PERA AÍ', 230, K); const c = mk(tt.w + 120, tt.h + 70); c.x.fillStyle = L; rr(c.x, 0, 0, c.c.width, c.c.height, 18); c.x.fill(); c.x.drawImage(tt.c, 60, 35); TXC.set('perabox', c.c); return c.c; })();
    for (let i = 6; i >= 1; i--) plane(ctx, TXC.get('peraside') || (() => { const c = mk(tex.width, tex.height); c.x.fillStyle = '#5a7a10'; rr(c.x, 0, 0, tex.width, tex.height, 18); c.x.fill(); TXC.set('peraside', c.c); return c.c; })(), pose, 1, tex.width, tex.height, i * 6);
    plane(ctx, tex, pose, 2);
    glow(ctx, g => plane(g, tex, pose, 1), 0.35 + 0.9 * Math.exp(-(t - w(11)) * 5), 8);
  }
}
cue(w(9), 'tapestop', 0.8, { ch: 0.9 }); cue(w(9) + 0.02, 'glitch', 0.55); cue(w(9), 'hit_small', 0.4); cue(w(10), 'hit_small', 0.45); cue(w(11), 'impact', 0.85, { sh: 0.6, fl: 0.2, ch: 0.4 });

// ---------- S4: janela tipo After girando em 3D ----------
let AETEX = null, AEHALF = null;
function aeTex() {
  if (AETEX) return;
  const c = mk(1500, 800); aeWindow(c.x, 0, 0, 1500, 800, 0.8); AETEX = c.c;
  const A = [-80 + 0, 800 * 0.18], B = [1580, 800 * 0.86];
  AEHALF = [0, 1].map(s => { const h = mk(1500, 800); h.x.beginPath(); if (!s) { h.x.moveTo(A[0], A[1]); h.x.lineTo(B[0], B[1]); h.x.lineTo(1600, -10); h.x.lineTo(-100, -10); } else { h.x.moveTo(A[0], A[1]); h.x.lineTo(B[0], B[1]); h.x.lineTo(1600, 900); h.x.lineTo(-100, 900); } h.x.closePath(); h.x.clip(); h.x.drawImage(AETEX, 0, 0); return h.c; });
}
function S4f(ctx, t) {
  aeTex();
  const t0 = w(13), k = sp(t, t0, 0.62, 5.5), cut = w(20) + 0.02;
  setCam3({ ry: 0.25 * Math.sin((t - t0) * 1.1) - 0.1, rx: -0.08 + 0.06 * Math.sin((t - t0) * 0.8), x: lerp(-200, 80, P(t, t0, w(24))), z: lerp(-100, 260, P(t, t0, w(24))), rz: 0.04 * Math.sin((t - t0) * 1.5) });
  bgv(ctx, DV, V, 0.5); bokeh(ctx, t, 0.6);
  const base = { x: 0, y: 30, z: lerp(3200, 220, k), ry: lerp(3.6, 0.22, k), rx: lerp(-0.7, 0.1, k), rz: lerp(0.4, 0, k), s: 0.95 };
  if (t < cut) plane(ctx, AETEX, base, 8, 1500, 800);
  else {
    const d = t - cut;
    [[-1, 0], [1, 1]].forEach(([sg, hi]) => { const o = { ...base, x: base.x + sg * 500 * d, y: base.y + (sg > 0 ? 1400 * d * d : -500 * d), z: base.z + 600 * d, rz: sg * 0.6 * d, ry: base.ry + sg * 0.8 * d, rx: base.rx + sg * 0.5 * d }; plane(ctx, AEHALF[hi], o, 6, 1500, 800, 0, clamp(1 - d / 1.1)); });
  }
  if (t >= w(20) - 0.04 && t < cut + 0.4) {
    const p = eo3(P(t, w(20) - 0.04, w(20) + 0.06)), fade = 1 - P(t, cut + 0.1, cut + 0.4);
    const ax = 120, ay = 260, bx = W - 120, by = H - 200, ex = lerp(ax, bx, p), ey = lerp(ay, by, p);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.strokeStyle = rgba(L, fade); ctx.lineWidth = 10; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ex, ey); ctx.stroke(); ctx.restore();
    glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.strokeStyle = L; g.lineWidth = 46; g.lineCap = 'round'; g.beginPath(); g.moveTo(ax, ay); g.lineTo(ex, ey); g.stroke(); }, 1.4 * fade, 6);
  }
  W3(ctx, t, 'AFTER', w(19) - 0.08, { x: 0, y: -20, z: -250, size: 320, side: '#2b2b2b', from: { z: 1800, ry: 1.4 }, glow: 0.15, out: w(20) - 0.1, outD: 0.15 });
  W3(ctx, t, 'NENHUMA', w(20) - 0.06, { x: 0, y: -150, z: -200, size: 240, side: SIDE, from: { z: -1100, rz: 0.5 }, glow: 0.15, out: w(22) - 0.08 });
  W3(ctx, t, 'VEZ', w(21) - 0.08, { x: 0, y: 140, z: -200, size: 270, face: L, side: SIDE, from: { z: -1100, rz: -0.6 }, glow: 0.45, flash: 1.3, out: w(22) - 0.05 });
  W3(ctx, t, 'PRA FAZER', w(22) - 0.04, { x: 0, y: 0, z: -100, size: 200, side: SIDE, from: { z: 1500, ry: -1.4 }, glow: 0.1, out: w(24) - 0.1, outD: 0.12 });
}
cue(w(13), 'whoosh_long', 0.7); [0.25, 0.45, 0.62, 0.8].forEach(d => cue(w(13) + d, 'click', 0.45)); cue(w(19), 'hit_med', 0.65, { sh: 0.3 });
cue(w(20), 'slash', 0.85, { fl: 0.2, ch: 0.6 }); cue(w(20) + 0.1, 'whoosh_fall', 0.65); cue(w(21), 'impact', 0.8, { sh: 0.55 }); cue(w(22), 'whoosh_small', 0.55); cue(w(22) + 0.05, 'hit_small', 0.5);

// ---------- S4b: ESSE / VÍDEO / AQUI com troca de cor ----------
function S4bf(ctx, t) {
  const segs = [[w(24), L, K, 'ESSE', 0.07], [w(25), V, WH, 'VÍDEO', -0.08], [w(26), K, L, 'AQUI', 0.05]];
  let si = 0; segs.forEach((s, i) => { if (t >= s[0] - 0.06) si = i; });
  const [ts, bgc, fc, word, roll] = segs[si];
  setCam3({ rz: roll + 0.03 * Math.sin(t * 6), z: 150 * P(t, ts, ts + 0.4), ry: 0.2 * Math.sin((t - ts) * 3) });
  if (si > 0) { bg(ctx, segs[si - 1][1]); }
  // wipe diagonal da nova cor
  const wp = eo3(P(t, ts - 0.06, ts + 0.04));
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.beginPath(); const ex = lerp(-600, W + 600, wp); ctx.moveTo(-800, 0); ctx.lineTo(ex + 300, 0); ctx.lineTo(ex - 300, H); ctx.lineTo(-800, H); ctx.closePath(); ctx.fillStyle = bgc; ctx.fill(); if (bgc === K) radial(ctx, W / 2, H / 2, 900, V, 0.35); ctx.restore();
  W3(ctx, t, word, ts - 0.07, { size: 340, face: fc, side: fc === K ? SIDE : (fc === L ? SIDE : '#3a1a80'), from: { z: -1400, rz: roll * 8, ry: 0.6 }, glow: fc === L ? 0.6 : 0.1, flash: fc === L ? 1.4 : 0.5, depth: 60, s: si === 2 ? 1 + 0.25 * eiExp(P(t, w(27) - 0.25, w(27))) : 1 });
}
[24, 25, 26].forEach(i => { cue(w(i) - 0.06, 'whoosh_fast', 0.55); cue(w(i), 'hit_med', 0.6, { sh: 0.3, ch: 0.25 }); });

// ---------- S5: sucção dinâmica + CLAUDE letra por letra ----------
const VORT = (() => { const r = mulberry32(5), a = []; for (let i = 0; i < 300; i++) a.push({ a: r() * 6.283, r: 500 + r() * 1300, c: [L, V, WH][Math.floor(r() * 3)], w: 1 + r() * 3.5, sp: 0.6 + r() }); return a; })();
function S5f(ctx, t) {
  const tc = w(31);
  if (t < tc) {
    const u = P(t, w(27), tc), ue = ei3(u);
    setCam3({ rz: 1.6 * ue + 0.1 * Math.sin(t * 9) * u, z: 400 * ue, ry: 0.3 * Math.sin(t * 5) * (1 - u) });
    bgv(ctx, K, V, 0.25 + 0.4 * u);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.lineCap = 'round';
    for (const p of VORT) { const rr0 = p.r * (1 - eiExp(Math.min(1, u * 1.04))) + 20; const an = p.a + u * 6 * p.sp; const len = 0.25 + 0.6 * u; ctx.strokeStyle = rgba(p.c, 0.25 + 0.65 * u); ctx.lineWidth = p.w; ctx.beginPath(); ctx.arc(W / 2, H / 2, rr0, an, an + len); ctx.stroke(); }
    radial(ctx, W / 2, H / 2, 60 + 380 * ue, L, 0.2 + 0.7 * ue); ctx.restore();
    const words = [['E', 27], ['ISSO', 28], ['AQUI', 29], ['É', 30]];
    words.forEach(([s, i], j) => { const t0 = w(i) - 0.06; if (t < t0) return; const q = P(t, t0, tc), a = j * 1.7 + q * 4.5, rad = lerp(420, 0, ei3(q)); W3(ctx, t, s, t0, { x: Math.cos(a) * rad, y: Math.sin(a) * rad * 0.7, size: lerp(180, 40, ei3(q)), side: SIDE, from: { z: -800, rz: 0.6 }, rz: -a * 0.3, glow: 0.2 }); });
    return;
  }
  const d = t - tc;
  setCam3({ ry: 0.42 * Math.sin((t - tc - 0.5) * 0.9) * P(t, tc + 0.4, tc + 1.0), rx: -0.1 * Math.sin((t - tc) * 0.7), z: lerp(-150, 260, eio(P(t, tc, tc + 2.8))), rz: 0.05 * Math.sin(t * 0.8) });
  bgv(ctx, K, V, 0.5);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (d < 1.2) { ctx.lineWidth = 3; for (const p of VORT) { const r1 = 200 + d * 2600 * p.sp; ctx.strokeStyle = rgba(p.c, 0.6 * (1 - d / 1.2)); ctx.beginPath(); ctx.moveTo(W / 2 + Math.cos(p.a) * r1, H / 2 + Math.sin(p.a) * r1); ctx.lineTo(W / 2 + Math.cos(p.a) * (r1 + 200), H / 2 + Math.sin(p.a) * (r1 + 200)); ctx.stroke(); } }
  ctx.restore();
  ring(ctx, t, tc, L, 2600, 44, 0.9); ring(ctx, t, tc + 0.08, V, 1800, 24, 0.9);
  const word = 'CLAUDE', sz = 300; let tot = 0; const ws = [...word].map(ch => { const x = tw(ch, sz); tot += x + 12; return x; }); tot -= 12;
  let x = -tot / 2;
  [...word].forEach((ch, i) => {
    const t0 = tc - 0.05 + i * 0.075, cxl = x + ws[i] / 2; x += ws[i] + 12;
    const gl = P(t, tc + 0.8 + i * 0.05, tc + 1.5 + i * 0.05);
    W3(ctx, t, ch, t0, { x: cxl, y: -40, size: sz, side: SIDE, depth: 70, from: { ry: -1.57, z: 700, y: -60 }, w: 13, zeta: 0.5, glow: 0.18, flash: 1.2, glint: gl > 0 && gl < 1 ? gl : undefined, N: 3 });
  });
  L3(ctx, t, 'meu amigo', w(32) - 0.03, { y: 230, size: 56 });
  W3(ctx, t, 'É, RAPAZ', w(34) - 0.07, { y: 350, size: 120, face: L, side: SIDE, from: { z: -900, rz: 0.4 }, glow: 0.4 });
}
cue(w(27), 'suck', 1.0, {}); cue(w(28), 'whoosh_small', 0.4); cue(w(29), 'whoosh_small', 0.45); cue(w(30), 'whoosh_small', 0.5); cue(w(31) - 0.25, 'blurcue', 0, { bl: 0.5 });
cue(w(31), 'braam', 1.0, { sh: 1.0, fl: 0.9, ch: 1.0 }); for (let i = 1; i < 6; i++) cue(w(31) - 0.05 + i * 0.075, 'key', 0.45); cue(w(31) + 0.85, 'shimmer', 0.55); cue(w(34), 'hit_small', 0.6, { sh: 0.25 });

// ---------- S6: código em 3D + contagem até 0 ----------
let EDC = null;
function editorTex(t) {
  if (!EDC) EDC = mk(1180, 720); const c = EDC.x; c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, 1180, 720);
  rr(c, 0, 0, 1180, 720, 24); c.fillStyle = '#0f0f12'; c.fill(); c.strokeStyle = '#2f2f36'; c.lineWidth = 3; c.stroke();
  c.fillStyle = '#18181c'; rr(c, 0, 0, 1180, 52, [24, 24, 0, 0]); c.fill(); T(c, 'animacao.js', 590, 27, 20, '#999', { f: 'Inter' });
  const typed = Math.floor(clamp((t - w(36)) / 0.55) * CODE.length), del = P(t, w(39), w(39) + 0.4);
  const vis = Math.min(typed, Math.ceil(CODE.length * (1 - del)));
  for (let i = 0; i < vis; i++) { const y = 84 + i * 28; T(c, String(i + 1).padStart(2, ' '), 40, y, 17, '#555', { f: '"DejaVu Sans Mono"', a: 'left' }); codeLine(c, CODE[i], 96, y, 20); }
  if (del > 0 && del < 1) { c.fillStyle = rgba(V, 0.75); c.fillRect(86, 84 + vis * 28 - 14, 1060, 28); }
  return EDC.c;
}
function S6f(ctx, t) {
  const t0 = w(36), k = sp(t, t0, 0.6, 6.5), away = eiExp(P(t, w(39) + 0.15, w(39) + 0.55));
  setCam3({ ry: 0.3 * Math.sin((t - t0) * 1.2), rx: -0.08, z: lerp(0, 200, P(t, t0, w(43))), x: 60 * Math.sin((t - t0) * 0.9), rz: 0.03 * Math.sin(t * 1.4) });
  bgv(ctx, DV, V, 0.5); bokeh(ctx, t, 0.7);
  if (away < 1) plane(ctx, editorTex(t), { x: lerp(-300, 0, k), y: 40, z: lerp(2800, 250, k) + 2600 * away, ry: lerp(-1.6, 0.32, k) + 1.2 * away, rx: lerp(0.6, 0.08, k), rz: lerp(-0.3, 0, k) - 0.4 * away }, 8, 1180, 720, 0, 1 - away);
  W3(ctx, t, 'EU NÃO ESCREVI', t0 - 0.06, { y: -380, size: 120, side: SIDE, from: { z: -900, rx: 1.2 }, glow: 0.1 });
  const c0 = w(39) + 0.1, c1 = w(42) - 0.02;
  if (t >= c0 && t < c1) { const v = Math.round(1284 * (1 - eio(P(t, c0, c1)))); const pose = { y: 20, z: lerp(600, 0, eo3(P(t, c0, c0 + 0.25))), ry: 0.25 * Math.sin(t * 3), rx: 0.1 }; text3D(ctx, v.toLocaleString('pt-BR'), pose, { size: 300, side: SIDE, depth: 50 }); }
  if (t >= c1) { W3(ctx, t, '0', c1 - 0.06, { y: 20, size: 440, face: L, side: SIDE, depth: 90, from: { z: -1600, rz: 0.6 }, glow: 0.55, flash: 1.6, zeta: 0.4, drift: 0.12 }); ring(ctx, t, c1, L, 2600, 40, 0.8); }
  W3(ctx, t, 'LINHAS DE CÓDIGO', w(42) - 0.06, { y: 390, size: 100, side: SIDE, from: { z: 900, rx: -1.2 }, glow: 0.1 });
}
cue(w(36), 'whoosh_long', 0.6); for (let i = 0; i < 12; i++) cue(w(36) + 0.05 + i * 0.045, 'key', 0.3);
cue(w(39), 'rev_whoosh', 0.6); { const c0 = w(39) + 0.1, c1 = w(42) - 0.02; let tt = c0, st = 0.035; while (tt < c1 - 0.03) { cue(tt, 'tick', 0.32); tt += st; st *= 1.12; } cue(c1, 'impact', 0.95, { sh: 0.9, fl: 0.4, ch: 0.6 }); }
cue(w(40) + 0.1, 'hit_small', 0.4);

// ---------- S7: PC gamer + NASA + buraco negro ----------
function S7f(ctx, t) {
  const t0 = w(43), bh0 = w(48) + 0.55, bh1 = w(49) - 0.25, u = P(t, bh0, bh1), ue = eiExp(u);
  setCam3({ ry: lerp(-0.5, 0.45, eio(P(t, t0, bh0))), rx: -0.12 + 0.05 * Math.sin(t), z: lerp(-300, 200, P(t, t0, bh0)), rz: 0.04 * Math.sin(t * 1.2) });
  bg(ctx, K);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); radial(ctx, W / 2, H / 2 + 80, 1000, V, 0.45 * (1 - ue)); radial(ctx, W * 0.8, H * 0.2, 700, L, 0.06 * (1 - ue));
  for (const s of STARS) { const ox = (s.x - CAM3.ry * 600 * (0.3 + s.d) - t * 30 + W * 4) % W; let x = ox, y = s.y; if (u > 0) { const dx = x - W / 2, dy = y - H / 2, a = Math.atan2(dy, dx) + ue * 3, r0 = Math.hypot(dx, dy) * (1 - ue); x = W / 2 + Math.cos(a) * r0; y = H / 2 + Math.sin(a) * r0; } ctx.fillStyle = rgba(WH, 0.3 + 0.6 * s.d); ctx.fillRect(x, y, s.s * (1 + 3 * u), s.s); }
  ctx.restore();
  if (u < 1) {
    ctx.save(); if (u > 0) { ctx.translate(W / 2, H / 2); ctx.rotate(ue * 4.5); const sc = Math.max(0.001, 1 - ue); ctx.scale(sc, sc); ctx.translate(-W / 2, -H / 2); }
    const k = sp(t, t0, 0.75, 5);
    const o = { x: 0, y: 60 + 18 * Math.sin(t * 1.5), z: lerp(7000, 450, k), rx: -0.15, ry: 0.6 + (t - t0) * 1.1, rz: 0.06 };
    box3(ctx, [260, 560, 580], o, pcFace3(t, false));
    glow(ctx, g => box3(g, [260, 560, 580], o, pcFace3(t, true)), 1.1, 6);
    L3(ctx, t, 'NÃO PRECISEI DE', t0 - 0.02, { y: -430, size: 46 });
    W3(ctx, t, 'COMPUTADOR DA', w(46) - 0.07, { y: -330, z: -50, size: 120, side: SIDE, from: { z: -900, rx: 1.2 }, glow: 0.12 });
    if (t >= w(48) - 0.08) {
      const kk = sp(t, w(48) - 0.08, 0.45, 18), pose = { y: 90, z: lerp(-1300, -320, kk), rz: lerp(0.6, -0.06, kk), ry: 0.1 * Math.sin(t * 2) };
      const tex = TXC.get('nasabox') || (() => { const tt = TX('NASA', 260, WH); const c = mk(tt.w + 140, tt.h + 90); c.x.strokeStyle = WH; c.x.lineWidth = 14; rr(c.x, 7, 7, c.c.width - 14, c.c.height - 14, 20); c.x.stroke(); c.x.drawImage(tt.c, 70, 45); TXC.set('nasabox', c.c); return c.c; })();
      plane(ctx, tex, pose, 2);
      const tw2 = tex.width / 2, th2 = tex.height / 2;
      [[w(48) + 0.2, -1], [w(48) + 0.32, 1]].forEach(([tt, sg]) => { if (t < tt) return; const p = eo3(P(t, tt, tt + 0.09)); const a = P3([-tw2 * 1.05, sg * -th2 * 1.1, -2], pose), b = P3([tw2 * 1.05, sg * th2 * 1.1, -2], pose); const ex = lerp(a[0], b[0], p), ey = lerp(a[1], b[1], p); ctx.save(); ctx.strokeStyle = L; ctx.lineWidth = 30; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(ex, ey); ctx.stroke(); ctx.restore(); glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); if (u > 0) { g.translate(W / 2, H / 2); g.rotate(ue * 4.5); const sc = Math.max(0.001, 1 - ue); g.scale(sc, sc); g.translate(-W / 2, -H / 2); } g.strokeStyle = L; g.lineWidth = 50; g.lineCap = 'round'; g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(ex, ey); g.stroke(); }, 0.9, 6); });
    }
    ctx.restore();
  }
  // buraco negro
  if (t >= bh0 - 0.1) {
    const g0 = eo3(P(t, bh0 - 0.1, bh0 + 0.2)), r = (20 + ue * 1400) * g0 + 40 * g0;
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    for (let i = 0; i < 3; i++) { ctx.strokeStyle = rgba(i === 1 ? L : V, 0.55 * (1 - P(t, bh1, bh1 + 0.3))); ctx.lineWidth = 18 - i * 5; ctx.beginPath(); ctx.ellipse(W / 2, H / 2, r * (1.25 + i * 0.12), r * (0.42 + i * 0.05), 0.2 + t * 0.6, t * (3 + i), t * (3 + i) + 4.5); ctx.stroke(); }
    ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(W / 2, H / 2, r, 0, 7); ctx.fill(); ctx.restore();
    glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.strokeStyle = V; g.lineWidth = 40; g.beginPath(); g.arc(W / 2, H / 2, r * 1.05, 0, 7); g.stroke(); }, 0.8 * (1 - P(t, bh1, bh1 + 0.3)), 8);
  }
}
cue(w(43), 'drone', 0.7); cue(w(43), 'whoosh_long', 0.6); cue(w(46), 'hit_small', 0.5); cue(w(48), 'impact', 0.85, { sh: 0.6, fl: 0.2 }); cue(w(48) + 0.2, 'slash', 0.6); cue(w(48) + 0.32, 'slash', 0.6, { ch: 0.4 });
cue(w(48) + 0.5, 'blackhole', 0.95, { bl: 0.0 }); cue(w(48) + 0.5, 'muffle', w(49) - w(48) - 0.5); cue(w(49) - 0.45, 'blurcue', 0, { bl: 0.6 });

// ---------- S8: volta do buraco negro — E TU PODE PEDIR O QUE TU QUISER ----------
function S8f(ctx, t) {
  const t0 = w(49), out = w(57) - 0.4;
  setCam3({ ry: lerp(-0.4, 0.3, eio(P(t, t0, out))), z: lerp(-200, 220, P(t, t0, out)), rz: lerp(0.1, -0.04, P(t, t0, t0 + 0.6)), rx: 0.05 * Math.sin(t * 2) });
  bgv(ctx, L, '#ffffff', 0.35);
  ring(ctx, t, t0, K, 2600, 50, 0.6);
  const ow = { glow: 0, side: SIDE, out, outD: 0.2, outZ: 1300 };
  const rowW = (ws, sz) => { const tot = ws.reduce((a, s) => a + tw(s + ' ', sz), 0) - tw(' ', sz); let x = -tot / 2; return ws.map(s => { const c = x + tw(s, sz) / 2; x += tw(s + ' ', sz); return c; }); };
  const r1 = rowW(['E', 'TU', 'PODE'], 150);[['E', 49], ['TU', 50], ['PODE', 51]].forEach(([s, i], j) => W3(ctx, t, s, w(i) - 0.07, { ...ow, x: r1[j], y: -310, size: 150, face: K, from: { z: -900, rx: j % 2 ? 1.2 : -1.2 } }));
  W3(ctx, t, 'PEDIR', w(52) - 0.07, { ...ow, y: -70, size: 270, face: K, from: { z: 1800, ry: 1.6 } });
  const sz = 230, r3 = rowW(['O', 'QUE', 'TU', 'QUISER'], sz);
  [['O', 53], ['QUE', 54], ['TU', 55], ['QUISER', 56]].forEach(([s, i], j) => W3(ctx, t, s, w(i) - 0.07, { ...ow, x: r3[j], y: 230, size: sz, face: j === 3 ? V : K, side: j === 3 ? '#2a0d55' : SIDE, from: { z: -1000, rz: j % 2 ? 0.5 : -0.5 }, glow: j === 3 ? 0.15 : 0, glowCol: V }));
}
cue(w(49), 'impact', 0.95, { sh: 0.8, fl: 0.9, ch: 0.5 }); [50, 51, 53, 54, 55].forEach(i => cue(w(i), 'tick', 0.45)); cue(w(52), 'hit_small', 0.6, { sh: 0.2 }); cue(w(56), 'hit_med', 0.65, { sh: 0.3 }); cue(w(57) - 0.4, 'whoosh_fast', 0.6);

// ---------- S9: quadrado (entra antes) → cubo → voa ----------
const EXPP = [220, -210];
function S9f(ctx, t) {
  const t0 = w(57) - 0.35, v3 = w(63), fly0 = w(65), ex = w(68);
  const ext = sp(t, v3, 0.6, 9), fly = P(t, fly0, ex), fe = ei3(fly);
  setCam3({ ry: lerp(0, 0.5, ext) * (1 - fly) + 0.15 * Math.sin(t * 1.3), rx: lerp(0, -0.25, ext) * (1 - fly) - 0.15 * fly, z: lerp(0, 260, ext) * (1 - fly), y: -60 * fly, rz: 0.04 * Math.sin(t * 1.6) });
  bgv(ctx, L, '#ffffff', 0.35);
  if (fly > 0) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); const r = mulberry32(4); ctx.lineCap = 'round'; for (let i = 0; i < 60; i++) { const x = W / 2 - 700 + r() * 1400 + 200 * fe, yy = ((r() * H + t * 3000 * (0.5 + r())) % (H + 400)) - 200; ctx.strokeStyle = rgba(K, 0.15 + 0.35 * fly); ctx.lineWidth = 2 + r() * 5; ctx.beginPath(); ctx.moveTo(x, yy); ctx.lineTo(x, yy - 100 - 400 * fly); ctx.stroke(); } ctx.restore(); }
  const k = sp(t, t0, 0.55, 12), s = 300;
  const o = { x: lerp(-900, 0, k) + EXPP[0] * fe, y: lerp(-600, 30, k) + (EXPP[1] - 30) * fe, z: lerp(-400, 0, k), rz: lerp(-2.4, 0, k) + 3 * fe, rx: lerp(0, -0.55, ext) - 2.5 * fe, ry: lerp(0, 0.75, ext) + 5 * fe };
  box3(ctx, [s, s, Math.max(2, s * ext)], o, (i, li) => ({ fill: i === 0 ? '#000' : mix('#7F3AED', '#1a0a40', 1 - li), stroke: ext > 0.02 ? L : null, lw: 4 }));
  if (ext > 0.02) glow(ctx, g => box3(g, [s, s, Math.max(2, s * ext)], o, () => ({ fill: null, stroke: L, lw: 8 })), 0.7, 6);
  L3(ctx, t, 'esse quadrado aqui', w(57) - 0.03, { y: -400, size: 56, col: K, out: v3 - 0.2 });
  W3(ctx, t, 'VIRE 3D', v3 - 0.07, { y: 310, size: 150, face: K, side: SIDE, from: { z: -900, rx: 1.2 }, glow: 0, out: fly0 - 0.12, outD: 0.15 });
  W3(ctx, t, 'SAIA VOANDO', fly0 - 0.07, { y: 310, size: 150, face: K, side: SIDE, from: { z: 1500, ry: 1.5 }, glow: 0, out: ex - 0.15, outD: 0.15 });
}
cue(w(57) - 0.35, 'whoosh', 0.6); cue(w(57) - 0.1, 'click_heavy', 0.75, { sh: 0.2 }); cue(w(63), 'servo', 0.7); cue(w(63) + 0.05, 'hit_small', 0.5); cue(w(65) - 0.1, 'riser_short', 0.7); cue(w(65), 'whoosh_up', 0.7);

// ---------- S10: explosão em partículas pequenas que reconstroem o texto ----------
let PTS = null;
function partSetup() {
  if (PTS) return PTS;
  const words = 'O QUE TU ', q = 'QUISER', sz = Math.min(260, 1450 / (tw(words + q, 100) / 100));
  const full = tw(words + q, sz), x0 = W / 2 - full / 2, xq = x0 + tw(words, sz);
  const o = mk(W, H); o.x.font = `${sz}px Anton`; o.x.textBaseline = 'middle'; o.x.fillStyle = '#fff'; o.x.fillText(words + q, x0, H / 2 - 20);
  const id = o.x.getImageData(0, 0, W, H).data, tg = [];
  for (let y = 0; y < H; y += 8) for (let x = 0; x < W; x += 8) if (id[(y * W + x) * 4 + 3] > 140) tg.push([x, y, x >= xq]);
  const r = mulberry32(77); const sh = tg.map(p => { const an = r() * 6.283, s2 = 300 + r() * 1700; return { tx: p[0], ty: p[1], q: p[2], vx: Math.cos(an) * s2, vy: Math.sin(an) * s2 - 150, rz: r() * 6, w: (r() - .5) * 16, s: 4 + r() * 6, c: [L, V, WH][Math.floor(r() * 3)], d: r(), shp: [r(), r(), r()] }; });
  PTS = { sh, sz, x0, xq, words, q }; return PTS;
}
function shardPos2(p, t) { const d = Math.max(0, t - w(68)), k = 2.6, f = (1 - Math.exp(-k * d)) / k; return [W / 2 + EXPP[0] + p.vx * f, H / 2 + EXPP[1] + p.vy * f + 50 * d * d, p.rz + p.w * f]; }
const QFONTS = ['Playfair Display', 'Bebas Neue', 'Pacifico', 'Space Mono', 'Bungee', 'Abril Fatface', 'Permanent Marker'];
function S10f(ctx, t) {
  const P0 = partSetup(), te = w(68), r0 = w(69) - 0.05, r1 = w(75) - 0.25, solid = r1 + 0.05;
  const d = t - te;
  setCam3({ ry: 0.12 * Math.sin((t - te) * 0.8), rz: 0.03 * Math.sin(t), z: 120 * P(t, te, w(77)) });
  bgv(ctx, K, V, 0.45 * Math.min(1, 0.4 + d));
  ring(ctx, t, te, WH, 2200, 40, 0.8, W / 2 + EXPP[0], H / 2 + EXPP[1]);
  if (t < te + 0.6) W3(ctx, t, 'EXPLODA', te - 0.05, { y: 60, size: 330, face: L, side: SIDE, from: { z: -1500, rz: 0.4 }, glow: 0.4, flash: 1.5, out: te + 0.42, outD: 0.18 });
  const m = eio(P(t, r0, r1)), fade = 1 - P(t, solid + 0.05, solid + 0.3);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (fade > 0) for (const p of P0.sh) {
    const [x, y, rz] = shardPos2(p, t); const arc = Math.sin(Math.PI * m) * 120 * (p.d - 0.5);
    const X2 = lerp(x, p.tx, m) + arc, Y2 = lerp(y, p.ty, m) - arc * 0.5, R = lerp(rz, 0, m), S = lerp(p.s, 6, m);
    ctx.fillStyle = m > 0.6 ? (p.q ? L : WH) : p.c; ctx.globalAlpha = fade;
    ctx.save(); ctx.translate(X2, Y2); ctx.rotate(R); ctx.beginPath(); ctx.moveTo((p.shp[0] - .5) * S * 2, -S); ctx.lineTo(S, (p.shp[1] - .5) * S); ctx.lineTo((p.shp[2] - .5) * S, S); ctx.closePath(); ctx.fill(); ctx.restore();
  }
  ctx.restore();
  glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); if (fade > 0) for (const p of P0.sh) { if (!(m > 0.6 ? p.q : p.c === L)) continue; const [x, y] = shardPos2(p, t); g.fillStyle = L; g.fillRect(lerp(x, p.tx, m) - 4, lerp(y, p.ty, m) - 4, 8, 8); } }, 0.5 + 0.8 * Math.exp(-d * 1.5), 6);
  if (t >= solid) {
    const al = clamp((t - solid) / 0.12);
    const words = P0.words, wordsW = tw(words, P0.sz);
    // fonte do QUISER muda 7 vezes (clique)
    const f0 = w(75) + 0.12; let fi = Math.floor((t - f0) / 0.115); let font = 'Anton';
    if (t >= f0 && fi < QFONTS.length) font = QFONTS[fi];
    const qsz0 = font === 'Anton' ? P0.sz : P0.sz * 0.9; const qw0 = tw(P0.q, qsz0, `"${font}"`), qAnton = tw(P0.q, P0.sz), qsz = qsz0 * Math.min(1, qAnton * 1.15 / qw0);
    const qw = tw(P0.q, qsz, `"${font}"`), tot = wordsW + qw, xs0 = -tot / 2;
    text3D(ctx, words.trim(), { x: xs0 + tw(words.trim(), P0.sz) / 2, y: -20, z: 0 }, { size: P0.sz, side: SIDE, depth: 40, alpha: al });
    const qo = { x: xs0 + wordsW + qw / 2, y: -20, z: 0, rz: t >= f0 && fi < QFONTS.length ? 0.04 * ((fi % 2) * 2 - 1) : 0, s: t >= f0 && fi < QFONTS.length ? 1 + 0.08 * Math.exp(-((t - f0) % 0.115) * 30) : 1 };
    text3D(ctx, P0.q, qo, { size: qsz, font: `"${font}"`, face: L, side: SIDE, depth: 40, alpha: al });
    text3Dglow(ctx, P0.q, qo, { size: qsz, font: `"${font}"` }, 0.45 * al);
    if (fi === QFONTS.length) ring(ctx, t, f0 + QFONTS.length * 0.115, L, 2000, 26, 0.6);
  }
  L3(ctx, t, 'RAPAZ', w(76) - 0.03, { y: 230, size: 70, col: L, font: 'Anton', wt: '' });
}
cue(w(68), 'explosion', 0.85, { sh: 1.1, fl: 1.0, ch: 1.0 }); cue(w(69) - 0.1, 'rev_whoosh', 0.6); cue(w(72), 'whoosh_soft', 0.5); cue(w(75) - 0.2, 'hit_soft', 0.65, { sh: 0.25, fl: 0.15 });
for (let i = 0; i < 7; i++) cue(w(75) + 0.12 + i * 0.115, 'click', 0.6); cue(w(75) + 0.12 + 7 * 0.115, 'hit_med', 0.65, { sh: 0.35 }); cue(w(76), 'tick', 0.45);

// ===== Cenas v2: 11–24 =====
// ---------- S11: pedido genérico → resultado genérico (câmera 3D indo e voltando) ----------
function S11f(ctx, t) {
  const t0 = w(77), tv = w(86) - 0.1;
  setCam3({ ry: 0.5 * Math.sin((t - t0) * 0.75 + 0.3), x: lerp(-220, 220, (Math.sin((t - t0) * 0.5) + 1) / 2), z: lerp(-100, 250, P(t, t0, w(94))), rx: -0.08 + 0.05 * Math.sin((t - t0) * 1.1), rz: 0.03 * Math.sin(t * 1.3) });
  bgv(ctx, DV, V, 0.55); bokeh(ctx, t, 0.6);
  const k = sp(t, t0, 0.65, 6.5), out = eiExp(P(t, tv - 0.15, tv + 0.2));
  if (out < 1) plane(ctx, chatTex(t, 'Chat com IA', 'faz um vídeo bonito pro meu Instagram', t0 + 0.08, w(85) - 0.05, w(85) + 0.1, w(85) + 0.2, tv), { x: lerp(-800, 0, k) - 1300 * out, y: 20, z: lerp(2200, 200, k) + 800 * out, ry: lerp(1.3, 0, k) - 1.4 * out, rz: lerp(-0.2, 0, k) }, 6, 900, 760);
  if (t >= tv) { const kc = sp(t, tv, 0.6, 9); plane(ctx, badTex(t), { x: lerp(1300, 0, kc), y: -40, z: lerp(1600, 150, kc), ry: lerp(-1.4, -0.12, kc) + 0.1 * Math.sin(t * 1.5), rz: lerp(0.3, 0, kc) }, 6, 960, 540); }
  L3(ctx, t, 'vai receber genérico também', w(87) - 0.02, { y: 380, size: 54 });
  stamp3(ctx, t, w(92) - 0.07, 'gen', 'GENÉRICO', 170, { y: -40, z: -260, rz: -0.07 });
}
cue(w(77), 'whoosh_long', 0.6); for (let i = 0; i < 18; i++) cue(w(77) + 0.1 + i * 0.075, 'key', 0.3); cue(w(85) + 0.1, 'click', 0.65); cue(w(86) - 0.12, 'whoosh_fast', 0.65); cue(w(86), 'hum', 0.4); cue(w(92), 'impact', 0.8, { sh: 0.5, ch: 0.3 });

// ---------- S12: pedindo pro Claude ----------
function S12f(ctx, t) {
  const t0 = w(94), q = w(108) - 0.05;
  setCam3({ ry: lerp(-0.45, 0.35, eio(P(t, t0, q))), z: lerp(0, 300, P(t, t0, q)), rx: -0.06, rz: 0.04 * Math.sin(t * 1.5), x: 80 * Math.sin((t - t0) * 0.9) });
  bgv(ctx, K, V, 0.45); bokeh(ctx, t, 0.5);
  W3(ctx, t, 'AGORA,', t0 - 0.06, { y: -390, size: 110, side: SIDE, from: { z: -900, rx: 1.2 }, glow: 0.1, out: w(95) - 0.1, outD: 0.12 });
  W3(ctx, t, 'POR QUE?', w(95) - 0.06, { y: -390, size: 120, side: SIDE, from: { z: -900, rx: -1.2 }, glow: 0.1, out: q - 0.25, outD: 0.15 });
  const pc = w(98) - 0.15, k = sp(t, pc, 0.62, 7), aw = eiExp(P(t, w(110) - 0.12, w(110) + 0.18));
  if (t >= pc && aw < 1) plane(ctx, chatTex(t, 'Claude', 'faz um vídeo bom igual esse', w(100), w(106), w(106) + 0.08, w(106) + 0.12, w(107) + 0.02, 'Aqui está seu vídeo!'), { x: lerp(1200, 0, k), y: 40, z: lerp(1800, 250, k) + 2000 * aw, ry: lerp(-1.3, 0.05, k) + 1.2 * aw, rz: lerp(0.25, 0, k) }, 6, 900, 760, 0, 1 - aw);
  const tv = w(107) + 0.02;
  if (t >= tv && aw < 1) { const kc = sp(t, tv, 0.6, 10); plane(ctx, badTex(t), { x: 0, y: 30, z: lerp(-600, -60, kc) + 2000 * aw, ry: lerp(0.9, 0.05, kc) + 1 * aw, rz: lerp(-0.25, 0, kc) }, 6, 760, 427, 0, 1 - aw); }
  W3(ctx, t, 'NÃO VAI SAIR', q, { y: -300, size: 150, side: SIDE, from: { z: -900, rz: 0.5 }, glow: 0.1 });
  W3(ctx, t, '?', w(110) - 0.06, { y: 110, size: 560, face: L, side: SIDE, depth: 90, from: { z: -2200, rz: 1.2, ry: 1.5 }, glow: 0.5, flash: 1.6, zeta: 0.38, drift: 0.15 });
  ring(ctx, t, w(110), L, 2400, 34, 0.7);
}
cue(w(94), 'whoosh', 0.55); cue(w(94), 'hit_small', 0.4); cue(w(95), 'hit_small', 0.45); cue(w(98) - 0.15, 'whoosh_long', 0.55); for (let i = 0; i < 14; i++) cue(w(100) + i * ((w(106) - w(100)) / 14), 'key', 0.3); cue(w(106) + 0.08, 'click', 0.6); cue(w(107), 'whoosh_small', 0.5);
cue(w(108) - 0.05, 'glitch', 0.55, { ch: 0.7 }); cue(w(110), 'subhit', 0.9, { sh: 0.6, fl: 0.2 });

// ---------- S13: por que genérico — sequência com troca de cor ----------
const GRY = '#b9b3c9', GRYS = '#4a4458';
function S13f(ctx, t) {
  const segs = [[w(111), V], [w(118) - 0.05, K], [w(119) - 0.05, L], [w(125) - 0.05, K], [w(129) - 0.05, DV], [w(136) - 0.05, L]];
  const si = swipeBG(ctx, t, segs), ts = segs[si][0];
  const sgn = si % 2 ? 1 : -1;
  setCam3({ ry: sgn * 0.35 * (1 - sp(t, ts, 0.8, 7)) + 0.12 * Math.sin(t * 1.3), rz: sgn * 0.06 * (1 - sp(t, ts, 0.8, 7)) + 0.02 * Math.sin(t * 2), z: 180 * P(t, ts, ts + 1.2), rx: 0.05 * Math.sin(t * 1.7) });
  const sg = (i) => segs[i][0], nx = (i) => (i + 1 < segs.length ? segs[i + 1][0] : w(139)) - 0.12;
  if (si === 0) { const xs = rowX(['PORQUE', 'TU', 'TÁ'], 150);[['PORQUE', 111], ['TU', 112], ['TÁ', 113]].forEach(([s, i], j) => W3(ctx, t, s, w(i) - 0.07, { x: xs[j], y: -120, size: 150, side: '#3d1680', from: { z: -900, rx: j % 2 ? 1.3 : -1.3 }, glow: 0.05, out: nx(0) })); W3(ctx, t, 'PEDINDO', w(114) - 0.07, { y: 110, size: 220, side: '#3d1680', from: { z: 1600, ry: 1.5 }, glow: 0.1, out: nx(0) }); }
  if (si === 1) W3(ctx, t, 'GENÉRICO', w(118) - 0.07, { size: 340, face: GRY, side: GRYS, depth: 70, from: { z: -1700, rz: 0.7 }, glow: 0, out: nx(1), drift: 0.1 });
  if (si === 2) { const xs = rowX(['E', 'SE', 'TU', 'PEDIR'], 150);[['E', 119], ['SE', 120], ['TU', 121], ['PEDIR', 122]].forEach(([s, i], j) => W3(ctx, t, s, w(i) - 0.07, { x: xs[j], y: -130, size: 150, face: K, side: SIDE, from: { z: -900, rz: j % 2 ? 0.6 : -0.6 }, glow: 0, out: nx(2) })); W3(ctx, t, 'PRA IA', w(123) - 0.07, { y: 120, size: 240, face: V, side: '#2a0d55', from: { z: 1700, ry: -1.5 }, glow: 0, out: nx(2) }); }
  if (si === 3) { L3(ctx, t, 'de um jeito', sg(3) + 0.05, { y: -250, size: 56 }); W3(ctx, t, 'GENÉRICO', w(128) - 0.07, { y: 40, size: 330, face: GRY, side: GRYS, depth: 70, from: { z: -1700, rz: -0.7 }, glow: 0, out: nx(3), drift: 0.1 }); }
  if (si === 4) { L3(ctx, t, 'tu vai ter um', sg(4) + 0.05, { y: -330, size: 54 }); W3(ctx, t, 'RESULTADO', w(133) - 0.07, { y: -80, size: 230, side: '#3d1680', from: { z: 1700, ry: 1.5 }, glow: 0.1, out: nx(4) }); W3(ctx, t, 'GENÉRICO', w(134) - 0.07, { y: 170, size: 230, face: GRY, side: GRYS, from: { z: -1500, rz: 0.6 }, glow: 0, out: nx(4) }); }
  if (si === 5) W3(ctx, t, 'NÃO TEM PRA ONDE', w(136) - 0.07, { size: 190, face: K, side: SIDE, from: { z: -1700, rz: -0.5, ry: 0.8 }, glow: 0, zeta: 0.4, drift: 0.08 });
}
cue(w(111), 'whoosh_fast', 0.55);[111, 112, 113].forEach(i => cue(w(i), 'tick', 0.45)); cue(w(114), 'hit_small', 0.5);
cue(w(118) - 0.05, 'whoosh_fast', 0.6); cue(w(118), 'impact', 0.8, { sh: 0.55, ch: 0.4 }); cue(w(119) - 0.05, 'whoosh_fast', 0.6);[119, 120, 121, 122].forEach(i => cue(w(i), 'tick', 0.42)); cue(w(123), 'hit_small', 0.55, { sh: 0.2 });
cue(w(125) - 0.05, 'whoosh_fast', 0.55); cue(w(128), 'impact', 0.8, { sh: 0.5, ch: 0.4 }); cue(w(129) - 0.05, 'whoosh_fast', 0.55); cue(w(133), 'hit_med', 0.6, { sh: 0.3 }); cue(w(134), 'hit_dry', 0.65, { sh: 0.3 });
cue(w(136) - 0.05, 'whoosh_fast', 0.6); cue(w(136), 'impact', 0.85, { sh: 0.6, fl: 0.15 });

// ---------- S14: grade 3D de vídeos iguais ----------
let GRIDT = null;
function gridTexs() {
  if (GRIDT) return GRIDT;
  GRIDT = [[1, 1], [3, 2], [6, 4], [12, 8]].map(([cols, rows], lv) => { const c = mk(1600, 900), gw = 1600, gh = 900, cw = gw / cols, chh = gh / rows, pad = Math.max(6, 30 / cols * 2); for (let r = 0; r < rows; r++) for (let q = 0; q < cols; q++) badVideo(c.x, q * cw + pad / 2, r * chh + pad / 2, cw - pad, chh - pad, r * 1.3 + q, Math.max(5, 22 / Math.sqrt(cols)), cols > 3); return c.c; });
  return GRIDT;
}
function S14f(ctx, t) {
  const tg = gridTexs(), lvT = [w(139) - 0.05, w(141) - 0.05, w(144) - 0.05, w(148) - 0.08];
  let lv = 0; lvT.forEach((tt, i) => { if (t >= tt) lv = i; });
  setCam3({ ry: lerp(0.55, -0.4, eio(P(t, w(139), w(150)))), rx: -0.12, z: lerp(-300, 250, P(t, w(139), w(150))), rz: 0.04 * Math.sin(t * 2) });
  bgv(ctx, K, V, 0.4);
  const k = sp(t, lvT[lv], 0.55, 16), flip = (1 - k);
  plane(ctx, tg[lv], { y: 10, z: 200 + 300 * flip, rx: flip * 1.4, ry: 0.15, s: 1 + 0.05 * flip }, 8, 1600, 900);
  if (lv === 3) W3(ctx, t, 'TODO MUNDO', lvT[3], { z: -250, size: 260, side: SIDE, from: { z: -1500, rz: 0.5 }, glow: 0.3, flash: 1.2 });
}
cue(w(139), 'whoosh', 0.55);[141, 144].forEach(i => { for (let j = 0; j < 5; j++) cue(w(i) - 0.05 + j * 0.03, 'tick', 0.3); cue(w(i), 'whoosh_small', 0.45); }); cue(w(148), 'impact', 0.9, { sh: 0.65, fl: 0.3, ch: 0.4 });

// ---------- S15: post publicado, 0 → 3 visualizações, comentário da tia ----------
let PHC = null;
function postTex(t, t0, v) {
  if (!PHC) PHC = mk(430, 860); const c = PHC.x, pw = 430, ph = 860; c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, pw, ph);
  rr(c, 0, 0, pw, ph, 54); c.fillStyle = '#111'; c.fill(); c.lineWidth = 6; c.strokeStyle = '#2a2a2a'; c.stroke();
  c.save(); rr(c, 14, 14, pw - 28, ph - 28, 42); c.clip(); badVideo(c, 14, 14, pw - 28, ph - 28, t, 42);
  const gr = c.createLinearGradient(0, ph * 0.6, 0, ph); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, 'rgba(0,0,0,0.65)'); c.fillStyle = gr; c.fillRect(0, 0, pw, ph);
  const up = P(t, t0, t0 + 0.3);
  if (up < 1) { c.fillStyle = 'rgba(0,0,0,0.6)'; c.fillRect(0, 0, pw, ph); T(c, 'Publicando...', pw / 2, ph / 2 - 30, 28, WH, { f: 'Inter', w: 800 }); c.fillStyle = '#333'; c.fillRect(60, ph / 2 + 10, pw - 120, 10); c.fillStyle = L; c.fillRect(60, ph / 2 + 10, (pw - 120) * eo3(up), 10); }
  c.fillStyle = '#888'; c.beginPath(); c.arc(64, ph - 110, 24, 0, 7); c.fill(); T(c, 'meu_perfil', 100, ph - 112, 24, WH, { f: 'Inter', w: 800, a: 'left' });
  eyeIcon(c, 70, ph - 58, 15, WH); T(c, `${v} visualizações`, 96, ph - 58, 24, WH, { f: 'Inter', w: 800, a: 'left' });
  c.restore(); return PHC.c;
}
function S15f(ctx, t) {
  const t0 = w(150) - 0.55, vt = [t0 + 0.35, t0 + 0.6, t0 + 0.85];
  let v = 0; vt.forEach(tt => { if (t >= tt) v++; });
  setCam3({ ry: lerp(-0.45, 0.35, eio(P(t, t0, w(154)))), z: lerp(-150, 200, P(t, t0, w(154))), rx: -0.06, rz: 0.03 * Math.sin(t * 2) });
  bgv(ctx, L, '#ffffff', 0.35);
  const k = sp(t, t0, 0.6, 9);
  plane(ctx, postTex(t, t0, v), { x: 0, y: 10, z: lerp(1600, 200, k), ry: lerp(1.6, 0.1, k) + 0.08 * Math.sin(t * 2), rz: lerp(-0.3, 0, k) }, 6, 430, 860);
  if (t >= vt[0] - 0.1) { const kk = sp(t, vt[Math.max(0, v - 1)], 0.5, 22); text3D(ctx, String(v), { x: -560, y: -40, z: lerp(-500, 0, kk), rz: lerp(0.4, 0, kk) }, { size: 380, face: K, side: SIDE, depth: 60 }); L3(ctx, t, 'visualizações', vt[0], { x: -560, y: 190, size: 50, col: K }); }
  if (t >= w(153) - 0.1) {
    const cc = TXC.get('neuza') || (() => { const c = mk(600, 170); const x = c.x; rr(x, 0, 0, 600, 170, 24); x.fillStyle = '#17171a'; x.fill(); x.fillStyle = '#6b6b75'; x.beginPath(); x.arc(62, 64, 34, 0, 7); x.fill(); T(x, 'N', 62, 66, 32, WH, { f: 'Inter', w: 800 }); T(x, 'tia_neuza', 116, 46, 30, WH, { f: 'Inter', w: 800, a: 'left' }); T(x, 'agora', 116 + tw('tia_neuza ', 30, 'Inter', 800), 47, 22, '#777', { f: 'Inter', a: 'left' }); T(x, 'tá lindo, meu filho', 116, 94, 32, '#eaeaea', { f: 'Inter', w: 500, a: 'left' }); heart(x, 116 + tw('tá lindo, meu filho ', 32, 'Inter', 500) + 14, 98, 18, L); T(x, 'Responder', 116, 138, 20, '#777', { f: 'Inter', w: 600, a: 'left' }); TXC.set('neuza', c.c); return c.c; })();
    const kc = sp(t, w(153) - 0.1, 0.55, 14); plane(ctx, cc, { x: 560, y: 20, z: lerp(-700, -60, kc), rx: lerp(1.4, 0, kc), ry: -0.15 }, 3, 600, 170);
  }
}
cue(w(150) - 0.55, 'whoosh_fast', 0.6); cue(w(150) - 0.5, 'click', 0.55);[0.35, 0.6, 0.85].forEach(d => cue(w(150) - 0.55 + d, 'hit_small', 0.45, { sh: 0.15 })); cue(w(153), 'notif', 0.55);

// ---------- S16: nesse nível + 2 ----------
function S16f(ctx, t) {
  const t0 = w(154) + 0.15, t2 = w(163) - 0.08;
  setCam3({ ry: 0.35 * Math.sin((t - t0) * 0.8), z: lerp(-100, 250, P(t, t0, w(165))), rx: -0.05 + 0.05 * Math.sin(t * 1.1), rz: 0.04 * Math.sin(t * 1.6) });
  bgv(ctx, DV, V, 0.55); bokeh(ctx, t, 0.8);
  L3(ctx, t, 'pra conseguir', t0, { y: -380, size: 56, out: w(160) - 0.15 });
  W3(ctx, t, 'UM VÍDEO', w(156) - 0.07, { y: -190, size: 160, side: SIDE, from: { z: -900, rx: 1.3 }, glow: 0.1, out: w(160) - 0.1 });
  W3(ctx, t, 'NESSE NÍVEL', w(158) - 0.07, { y: 70, size: 280, face: L, side: SIDE, depth: 60, from: { z: 2200, ry: -1.6 }, glow: 0.5, flash: 1.5, out: w(160) - 0.05 });
  L3(ctx, t, 'tu precisa de', w(160) - 0.03, { y: -380, size: 56 });
  W3(ctx, t, '2', t2, { y: 0, size: 540, face: L, side: SIDE, depth: 110, from: { z: -2600, rz: -1.4, ry: 2.4 }, glow: 0.6, flash: 1.8, zeta: 0.45, w: 12, drift: 0.18, out: w(165) - 0.08, outD: 0.15, outZ: 1400 });
  ring(ctx, t, w(163), L, 2600, 44, 0.8);
  L3(ctx, t, 'COISAS', w(164) - 0.02, { y: 350, size: 70, font: 'Anton', wt: '' });
}
cue(w(156), 'hit_small', 0.5); cue(w(158), 'impact', 0.8, { sh: 0.5, ch: 0.3 }); cue(w(160) - 0.05, 'whoosh_fast', 0.5); cue(w(163) - 0.35, 'riser_short', 0.5); cue(w(163), 'boom', 0.95, { sh: 0.85, fl: 0.4, ch: 0.6 });

// ---------- S17: PROMPT + REFERÊNCIA ----------
function cardTex(key, col, title, tcol, icon) { return TXC.get(key) || (() => { const c = mk(720, 480), x = c.x; x.fillStyle = col; rr(x, 0, 0, 720, 480, 34); x.fill(); icon(x, 360, 170); const tt = TX(title, 120, tcol); x.drawImage(tt.c, 360 - tt.w / 2, 300); TXC.set(key, c.c); return c.c; })(); }
function S17f(ctx, t) {
  const t0 = w(165);
  setCam3({ ry: 0.3 * Math.sin((t - t0) * 0.9), z: lerp(0, 220, P(t, t0, w(168))), rx: -0.08 + 0.06 * Math.sin(t), rz: 0.03 * Math.sin(t * 1.4) });
  bgv(ctx, K, V, 0.45);
  const A = cardTex('cP', V, 'PROMPT', WH, (x, cx, cy) => { x.fillStyle = 'rgba(255,255,255,0.9)'; [300, 360, 240, 330].forEach((ww, i) => { rr(x, cx - 190, cy - 80 + i * 44, ww, 22, 11); x.fill(); }); });
  const B = cardTex('cR', L, 'REFERÊNCIA', K, (x, cx, cy) => { x.strokeStyle = K; x.lineWidth = 12; rr(x, cx - 150, cy - 90, 300, 170, 14); x.stroke(); for (let i = 0; i < 5; i++) { x.fillStyle = K; x.fillRect(cx - 130 + i * 60, cy - 122, 30, 16); x.fillRect(cx - 130 + i * 60, cy + 106, 30, 16); } x.beginPath(); x.moveTo(cx - 30, cy - 45); x.lineTo(cx + 45, cy - 5); x.lineTo(cx - 30, cy + 35); x.closePath(); x.fill(); });
  const sideA = TXC.get('cPs') || (() => { const c = mk(720, 480); c.x.fillStyle = '#2a0d55'; rr(c.x, 0, 0, 720, 480, 34); c.x.fill(); TXC.set('cPs', c.c); return c.c; })();
  const sideB = TXC.get('cRs') || (() => { const c = mk(720, 480); c.x.fillStyle = '#4d6610'; rr(c.x, 0, 0, 720, 480, 34); c.x.fill(); TXC.set('cRs', c.c); return c.c; })();
  [[A, sideA, t0 - 0.07, -430, 0.28, -1], [B, sideB, w(167) - 0.07, 430, -0.28, 1]].forEach(([tex, side, ta, x, ry, sg]) => {
    if (t < ta) return; const k = sp(t, ta, 0.55, 12);
    const o = { x: lerp(0, x, k), y: 30 + 14 * Math.sin(t * 1.6 + sg), z: lerp(-1200, 100, k), ry: lerp(sg * 3.2, ry, k), rz: lerp(sg * 0.5, 0, k), s: 0.95 };
    for (let i = 8; i >= 1; i--) plane(ctx, side, o, 1, 720, 480, i * 5);
    plane(ctx, tex, o, 3, 720, 480);
    glow(ctx, g => plane(g, side === sideA ? A : B, o, 1), 0.25 + 0.8 * Math.exp(-(t - ta) * 4), 9);
  });
}
cue(w(165), 'hit_med', 0.7, { sh: 0.35, ch: 0.3 }); cue(w(165) - 0.05, 'whoosh_fast', 0.5); cue(w(167), 'hit_med', 0.7, { sh: 0.35, ch: 0.3 }); cue(w(167) - 0.05, 'whoosh_fast', 0.5);

// ---------- S18: parede de prompt em 3D ----------
let WALLT = null;
function wallTex() {
  if (WALLT) return WALLT; const lh = 46, n = WALL.length * 2, c = mk(1500, n * lh + 80), x = c.x;
  x.font = '30px "DejaVu Sans Mono", monospace'; x.textAlign = 'center'; x.textBaseline = 'middle';
  for (let i = 0; i < n; i++) { const s = WALL[i % WALL.length]; x.fillStyle = s.startsWith('<') ? L : (/^\d/.test(s) ? '#b28cff' : '#e6e6e6'); x.fillText(s, 750, 40 + i * lh); }
  WALLT = c.c; return WALLT;
}
function wallScroll2(t) { const a = w(168), b = w(177), c = w(191) - 0.05, v0 = 260; if (t < b) return v0 * (t - a); const d = Math.min(t, c) - b, acc = (1500 - v0) / (c - b); return v0 * (b - a) + v0 * d + 0.5 * acc * d * d; }
function S18f(ctx, t) {
  const tex = wallTex(), s = wallScroll2(t), stop = t >= w(191) - 0.05;
  setCam3({ ry: 0.22 * Math.sin((t - w(168)) * 0.5), rz: 0.04 * Math.sin((t - w(168)) * 0.7), x: 0, z: 0, rx: 0 });
  bgv(ctx, K, V, 0.3);
  const rx = -1.3, hgt = tex.height, S = 1.7, ly = -hgt / 2 + 250 + s;
  const o = { x: 0, y: 330 - S * ly * Math.cos(rx), z: 60 - S * ly * Math.sin(rx), rx, s: S };
  plane(ctx, tex, o, 16, 1500, hgt, 0, stop ? 0.45 : 1);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); const gr = ctx.createLinearGradient(0, 0, 0, 330); gr.addColorStop(0, 'rgba(0,0,0,0.95)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = gr; ctx.fillRect(0, 0, W, 330); ctx.restore();
  L3(ctx, t, 'pra escrever um prompt', w(170) - 0.03, { y: -400, size: 56, out: w(177) - 0.1 });
  W3(ctx, t, 'SUPER COMPLEXO', w(177) - 0.07, { y: -200, z: -150, size: 210, side: SIDE, from: { z: -1500, rz: 0.5 }, glow: 0.2, flash: 1.2, out: w(179) - 0.05 });
  L3(ctx, t, 'com tudo que precisa pra sair um vídeo igual esse', w(179) - 0.02, { y: -400, size: 46, out: w(191) - 0.2 });
  if (stop) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = 'rgba(0,0,0,0.4)'; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  stamp3(ctx, t, w(191) - 0.07, 'dif', 'DIFÍCIL', 260, { y: 0, z: -200, rz: -0.05 });
}
cue(w(168), 'riser_long', 0.55); cue(w(177), 'impact', 0.75, { sh: 0.45, ch: 0.3 }); cue(w(179), 'whoosh', 0.45); cue(w(191), 'hit_big', 0.95, { sh: 1.0, fl: 0.3, ch: 0.6 });

// ---------- S19: começando do zero (contagem) ----------
function S19f(ctx, t) {
  const t0 = w(192), z0 = w(198) - 0.03;
  setCam3({ ry: 0.3 * Math.sin((t - t0) * 1.2), z: lerp(-100, 200, P(t, t0, w(199))), rz: 0.04 * Math.sin(t * 2) });
  bgv(ctx, L, '#ffffff', 0.35);
  W3(ctx, t, 'PRINCIPALMENTE', t0 - 0.07, { y: -330, size: 120, face: K, side: SIDE, from: { z: -900, rx: 1.2 }, glow: 0 });
  L3(ctx, t, 'se tu tá começando do zero', w(193) - 0.02, { y: -225, size: 52, col: K });
  const c0 = t0 + 0.25;
  if (t >= c0 && t < z0) { const v = Math.max(1, Math.round(9 * (1 - eio(P(t, c0, z0))))); text3D(ctx, String(v), { y: 90, z: 0, ry: 0.25 * Math.sin(t * 3) }, { size: 460, face: K, side: SIDE, depth: 60 }); }
  if (t >= z0) { W3(ctx, t, '0', z0 - 0.05, { y: 90, size: 520, face: V, side: '#2a0d55', depth: 100, from: { z: -1800, rz: 0.7 }, glow: 0.4, glowCol: V, flash: 1.3, zeta: 0.38, drift: 0.12 }); ring(ctx, t, z0, K, 2400, 36, 0.7); }
}
cue(w(192), 'hit_small', 0.5);{ const c0 = w(192) + 0.25, z0 = w(198) - 0.03; for (let i = 1; i <= 8; i++) cue(c0 + (z0 - c0) * (1 - Math.sqrt(1 - i / 9)), 'tick', 0.38); cue(z0, 'impact', 0.95, { sh: 0.85, fl: 0.3, ch: 0.5 }); }

// ---------- S20: LOGO MOTION IA em 3D real (respiro) ----------
function S20f(ctx, t) {
  const t0 = w(199), ti = w(209) - 0.08;
  setCam3({ ry: 0.22 * Math.sin((t - t0) * 0.45), rx: -0.06 + 0.04 * Math.sin((t - t0) * 0.4), z: lerp(-100, 200, eio(P(t, t0, w(210)))), rz: 0.02 * Math.sin((t - t0) * 0.5) });
  bgv(ctx, K, V, 0.4 + 0.08 * Math.sin(t * 2));
  L3(ctx, t, 'e isso tudo eu te ensino no curso', t0, { y: -330, size: 52 });
  const km = sp(t, t0 + 0.15, 0.75, 5), ki = t >= ti ? sp(t, ti, 0.4, 15) : 0;
  const parts = [['M', { x: 0, y: 0, z: lerp(1600, 0, km), ry: lerp(-1.4, 0, km), al: clamp((t - t0 - 0.15) / 0.3) }]];
  if (t >= ti) parts.push(['I', { x: 0, y: 0, z: lerp(-1300, 0, ki), rz: lerp(0.5, 0, ki), al: clamp((t - ti) / 0.04) }]);
  const gp = P(t, ti + 0.35, ti + 1.25);
  logo3(ctx, t, { y: 60, s: 1.05 }, parts, gp, t >= ti ? 0.35 + 1.0 * Math.exp(-(t - ti - 0.1) * 3) : 0.2);
  ring(ctx, t, w(209), L, 2400, 30, 0.8);
}
cue(w(199) + 0.15, 'whoosh_soft', 0.55); cue(w(209) - 0.9, 'riser_short', 0.55); cue(w(209), 'impact', 1.0, { sh: 0.5, fl: 0.45, ch: 0.4 }); cue(w(209) + 0.35, 'shimmer', 0.5);

// ---------- S21/S22: preço ----------
function S21f(ctx, t) {
  const t0 = w(210);
  setCam3({ z: lerp(0, 160, P(t, t0, w(217))), ry: 0.12 * Math.sin((t - t0) * 0.6), rz: 0.015 * Math.sin(t) });
  bgv(ctx, K, V, 0.2);
  L3(ctx, t, 'ele tá por', t0, { y: -240, size: 56 });
  W3(ctx, t, 'R$297', w(213) - 0.06, { y: 40, size: 340, side: '#333333', depth: 50, from: { z: -700, rx: 0.8 }, glow: 0, w: 13 });
}
cue(w(213), 'hit_dry_low', 0.85, { sh: 0.2 });
function S22f(ctx, t) {
  const t0 = w(217), st = w(228) - 0.02, fall = P(t, st + 0.12, st + 0.75), t97 = w(229) - 0.08;
  setCam3({ ry: 0.25 * Math.sin((t - t0) * 0.55), z: lerp(0, 200, P(t, t0, w(232))), rx: -0.05, rz: 0.02 * Math.sin(t * 0.8) });
  bgv(ctx, K, V, 0.15 + 0.35 * P(t, t97, t97 + 0.6));
  L3(ctx, t, 'mas só agora, nesse período de', t0, { y: -430, size: 48, out: w(223) - 0.2 });
  const m = eio(P(t, t0, t0 + 0.6)), pose = { y: lerp(40, -200, m) + 900 * ei3(fall), z: 300 * ei3(fall), rx: 1.6 * ei3(fall), rz: 0.4 * ei3(fall), s: lerp(1, 0.62, m) };
  if (fall < 1) text3D(ctx, 'R$297', pose, { size: 340, side: '#333333', depth: 50, alpha: 1 - fall });
  if (t >= st && fall < 0.6) { const p = eo3(P(t, st, st + 0.12)); const tt = TX('R$297', 340, WH); const a = P3([-tt.w / 2 - 30, 0, -5], pose), b = P3([tt.w / 2 + 30, 0, -5], pose); const ex = lerp(a[0], b[0], p), ey = lerp(a[1], b[1], p); ctx.save(); ctx.strokeStyle = L; ctx.lineWidth = 18; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(ex, ey); ctx.stroke(); ctx.restore(); glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.strokeStyle = L; g.lineWidth = 40; g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(ex, ey); g.stroke(); }, 0.9, 6); }
  stamp3(ctx, t, w(223) - 0.07, 'blk', 'BLACK', 110, { y: -370, z: -50, rz: -0.04 });
  L3(ctx, t, 'apenas', st + 0.25, { y: -230, size: 64, col: L });
  W3(ctx, t, 'R$97', t97, { y: 90, size: 440, face: L, side: SIDE, depth: 100, from: { z: -2600, rz: 0.9, ry: 1.2 }, glow: 0.45 + 0.25 * beatPulse(t), flash: 1.8, zeta: 0.42, drift: 0.14 });
  ring(ctx, t, w(229), L, 2600, 46, 0.9);
}
cue(w(223), 'impact', 0.6, { sh: 0.3 }); cue(w(228) - 0.02, 'slash', 0.7); cue(w(228) + 0.15, 'whoosh_fall', 0.5); cue(w(229), 'impact_huge', 1.0, { sh: 1.0, fl: 0.6, ch: 0.7 });

// ---------- S23: CTA comenta MOTION + simulação ----------
let PH2 = null;
function ctaPhoneTex(t, tA) {
  if (!PH2) PH2 = mk(430, 760); const c = PH2.x, sw = 430, sh = 760; c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, sw, sh);
  rr(c, 0, 0, sw, sh, 50); c.fillStyle = '#111'; c.fill(); c.strokeStyle = '#2a2a2a'; c.lineWidth = 6; c.stroke();
  c.save(); rr(c, 12, 12, sw - 24, sh - 24, 40); c.clip(); c.fillStyle = '#0c0c0e'; c.fillRect(0, 0, sw, sh); c.translate(12, 12);
  const iw = sw - 24, ih = sh - 24, typ0 = tA + 0.3, sent = tA + 0.8, notif = w(243) - 0.02, dm = notif + 0.6, msg = dm + 0.3, card = msg + 0.3, tap = card + 0.55;
  const dmE = eio(P(t, dm, dm + 0.3));
  c.save(); c.translate(-iw * dmE, 0);
  T(c, 'Comentários', iw / 2, 50, 26, WH, { f: 'Inter', w: 800 }); c.fillStyle = '#222'; c.fillRect(0, 86, iw, 2);
  const list = [['lucas.edits', 'que isso, mano'], ['bia.design', 'quero aprender'], ['rafa_motion', 'surreal demais']];
  const isSent = t >= sent, off = isSent ? 110 * sp(t, sent, .7, 14) : 0;
  if (isSent) { const yy = 112; c.fillStyle = rgba(L, 0.15); c.fillRect(0, yy - 10, iw, 100); c.fillStyle = L; c.beginPath(); c.arc(46, yy + 38, 26, 0, 7); c.fill(); T(c, 'você', 88, yy + 22, 22, WH, { f: 'Inter', w: 800, a: 'left' }); T(c, 'motion', 88, yy + 56, 30, L, { f: 'Inter', w: 800, a: 'left' }); }
  list.forEach(([u, m], i) => { const yy = 112 + off + i * 110; c.fillStyle = '#3a3a40'; c.beginPath(); c.arc(46, yy + 38, 26, 0, 7); c.fill(); T(c, u, 88, yy + 22, 22, '#bbb', { f: 'Inter', w: 700, a: 'left' }); T(c, m, 88, yy + 56, 26, WH, { f: 'Inter', w: 500, a: 'left' }); });
  c.fillStyle = '#1b1b1f'; rr(c, 16, ih - 90, iw - 32, 66, 33); c.fill();
  const nn = Math.floor(clamp((t - typ0) / 0.4) * 6);
  if (!isSent) T(c, 'motion'.slice(0, nn) + ((Math.floor(t * 3) % 2) ? '|' : ''), 44, ih - 57, 28, WH, { f: 'Inter', w: 600, a: 'left' }); else T(c, 'Adicione um comentário...', 44, ih - 57, 22, '#555', { f: 'Inter', a: 'left' });
  T(c, 'Publicar', iw - 40, ih - 57, 22, nn > 0 ? L : '#555', { f: 'Inter', w: 800, a: 'right' });
  c.restore();
  if (dmE > 0) {
    c.save(); c.translate(iw * (1 - dmE), 0); c.fillStyle = '#0c0c0e'; c.fillRect(0, 0, iw, ih);
    c.fillStyle = V; c.beginPath(); c.arc(54, 52, 28, 0, 7); c.fill(); T(c, 'ayrtonsena.stg', 96, 52, 26, WH, { f: 'Inter', w: 800, a: 'left' }); c.fillStyle = '#222'; c.fillRect(0, 100, iw, 2);
    if (t >= msg) { c.globalAlpha = clamp((t - msg) / .12); c.fillStyle = '#26262b'; rr(c, 20, 140, 360, 110, 26); c.fill(); T(c, 'Aqui está o link do curso', 44, 177, 24, WH, { f: 'Inter', w: 500, a: 'left' }); T(c, 'Motion com IA', 44, 213, 24, WH, { f: 'Inter', w: 700, a: 'left' }); c.globalAlpha = 1; }
    if (t >= card) { const lit = t >= tap; c.globalAlpha = clamp((t - card) / .12); c.fillStyle = L; rr(c, 20, 280, 370, 190, 26); c.fill(); T(c, 'MOTION COM IA', 46, 345, 52, K, { a: 'left' }); T(c, 'acessar o curso  →', 46, 415, 26, K, { f: 'Inter', w: 800, a: 'left' }); c.globalAlpha = 1; if (t >= tap - 0.25 && t < tap + 0.7) { const rp = P(t, tap, tap + 0.5), fx = 280, fy = 400; c.strokeStyle = rgba(WH, 1 - rp); c.lineWidth = 4; c.beginPath(); c.arc(fx, fy, 30 + rp * 70, 0, 7); c.stroke(); c.fillStyle = rgba(WH, 0.85 * (1 - P(t, tap + 0.3, tap + 0.7))); c.beginPath(); c.arc(fx, fy, 24, 0, 7); c.fill(); } if (lit) { c.strokeStyle = WH; c.lineWidth = 4; rr(c, 20, 280, 370, 190, 26); c.stroke(); } }
    c.restore();
  }
  if (t >= notif && t < dm + 0.2) { const kn = sp(t, notif, .7, 14), out = P(t, dm - 0.1, dm + 0.2), ny = lerp(-140, 16, kn) - 160 * ei3(out); c.fillStyle = '#1e1e22'; rr(c, 12, ny, iw - 24, 106, 22); c.fill(); eyeIcon(c, 58, ny + 53, 20, L); T(c, 'Nova mensagem', 96, ny + 36, 22, WH, { f: 'Inter', w: 800, a: 'left' }); T(c, 'Dá uma olhada no seu direct', 96, ny + 72, 21, '#cfcfcf', { f: 'Inter', w: 500, a: 'left' }); }
  c.restore();
  return { tex: PH2.c, tap };
}
function S23f(ctx, t) {
  const t0 = w(232), tA = w(234) - 0.1, up = eio(P(t, tA, tA + 0.45));
  setCam3({ ry: 0.3 * Math.sin((t - t0) * 0.6), z: lerp(-150, 150, P(t, t0, t0 + 6)), rx: -0.05 + 0.04 * Math.sin(t * 0.9), rz: 0.02 * Math.sin(t * 1.1) });
  bgv(ctx, DV, V, 0.55); bokeh(ctx, t, 0.7);
  const s1 = 72, s2 = 130, rw = tw('COMENTA ', s1) + tw('MOTION', s2), rx = -rw / 2;
  if (t >= t0 - 0.07) { const k = sp(t, t0 - 0.07, 0.55, 15); text3D(ctx, 'COMENTA', { x: lerp(0, rx + tw('COMENTA', s1) / 2, up), y: lerp(-230, -440, up), z: lerp(-900, 0, k), rx: lerp(1.2, 0, k), s: lerp(1, s1 / 150, up) }, { size: 150, side: SIDE, depth: 30 }); }
  if (t >= w(233) - 0.08) {
    const k = sp(t, w(233) - 0.08, 0.45, 15), pls = 1 + 0.04 * beatPulse(t);
    const o = { x: lerp(0, rx + tw('COMENTA ', s1) + tw('MOTION', s2) / 2, up), y: lerp(60, -440, up), z: lerp(-1800, 0, k), rz: lerp(0.7, 0, k), ry: 0.12 * Math.sin((t - t0) * 1.4) * (1 - up), s: lerp(1, s2 / 360, up) * pls };
    text3D(ctx, 'MOTION', o, { size: 360, face: L, side: SIDE, depth: 70 }); text3Dglow(ctx, 'MOTION', o, { size: 360 }, 0.4 + 0.5 * beatPulse(t) + 1.2 * Math.exp(-(t - w(233)) * 4));
  }
  if (t >= tA) { const r = ctaPhoneTex(t, tA), kp = sp(t, tA, 0.65, 9); plane(ctx, r.tex, { y: lerp(900, 80, kp), z: lerp(600, 150, kp), rx: lerp(0.9, 0.04, kp), ry: 0.18 * Math.sin((t - tA) * 0.8) }, 6, 430, 760); if (t >= r.tap) glow(ctx, g => plane(g, r.tex, { y: 80, z: 150, rx: 0.04, ry: 0.18 * Math.sin((t - tA) * 0.8) }, 2, 430, 760), 0.35 * Math.exp(-(t - r.tap) * 1.5), 10); }
}
cue(w(232), 'whoosh', 0.55); cue(w(232), 'hit_small', 0.5); cue(w(233), 'impact', 0.85, { sh: 0.5, fl: 0.25 }); cue(w(234) - 0.1, 'whoosh', 0.5); for (let i = 0; i < 6; i++) cue(w(234) + 0.2 + i * 0.067, 'key', 0.35); cue(w(234) + 0.7, 'click', 0.6); cue(w(243) - 0.02, 'notif', 0.55); cue(w(243) + 0.58, 'whoosh_small', 0.45); cue(w(243) + 1.75, 'click', 0.65);

// ---------- S24: logo final ----------
function S24f(ctx, t) {
  const t0 = END - 3.5;
  setCam3({ ry: 0.15 * Math.sin((t - t0) * 0.5), z: lerp(-200, 100, eio(P(t, t0, END))), rz: 0.015 * Math.sin(t) });
  bgv(ctx, K, V, 0.35 + 0.05 * Math.sin(t * 2));
  const k = sp(t, t0, 0.7, 6);
  logo3(ctx, t, { y: 0, s: 0.8, z: lerp(900, 0, k), ry: lerp(-0.8, 0, k) }, [['M', { x: 0 }], ['I', { x: 0 }]], P(t, t0 + 0.8, t0 + 1.8), 0.3 + 0.25 * beatPulse(t));
  const fo = P(t, END - 0.45, END); if (fo > 0) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
}
const END = 83.5;
cue(END - 3.5, 'whoosh_long', 0.5); cue(END - 3.5, 'blurcue', 0, { bl: 0.7 }); cue(END - 2.7, 'shimmer', 0.4);


// ===== registro das cenas (início, função) =====
scene(0, S1f);
scene(w(4), S2f);
scene(w(9), S3f);
scene(w(13), S4f);
scene(w(24) - 0.07, S4bf);
scene(w(27), S5f);
scene(w(36), S6f);
scene(w(43), S7f);
scene(w(49), S8f);
scene(w(57) - 0.35, S9f);
scene(w(68), S10f);
scene(w(77), S11f);
scene(w(94), S12f);
scene(w(111), S13f);
scene(w(139), S14f);
scene(w(150) - 0.55, S15f);
scene(w(154) + 0.15, S16f);
scene(w(165), S17f);
scene(w(168), S18f);
scene(w(192), S19f);
scene(w(199), S20f);
scene(w(210), S21f);
scene(w(217), S22f);
scene(w(232), S23f);
scene(END - 3.5, S24f);
