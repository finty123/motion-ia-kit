// TRAINING SEASON — motion na batida (16:9), v3 APROVADA em 21/10/2026. Paleta: preto / vermelho escuro (V) / branco (L = WH).
// WD = marcadores das palavras-chave (words.json, medidos na voz). BEATS = batidas da música (123 BPM).
// Som: só a música + o close-up do final (mix_musica.py ignora as outras cues; elas ficam só pro visual).
const RED = V, DRED = '#2a030b', SD = '#4a0512', GLR = '#ff2d55', RT = '#e8173f';
// linha centrada com espaço fixo entre palavras (o espaço do Anton é estreito demais)
function rowG(ws, sz, gap) { const wd = ws.map(s => tw(s, sz)), tot = wd.reduce((a, b) => a + b, 0) + gap * (ws.length - 1); let x = -tot / 2; return wd.map(v => { const c = x + v / 2; x += v + gap; return c; }); }
const fit = (s, wmax, hmax) => Math.min(hmax, wmax / (tw(s, 100) / 100));
const sx = f => { const c = X; c.save(); c.setTransform(1, 0, 0, 1, 0, 0); f(c); c.restore(); };

// ---------- A: carregando → YOU / SHOULD / KNOW (uma por vez, tela cheia) → o I sobe, câmera acompanha e mergulha ----------
const LOADP = [[0, 0.04], [w(0), 0.31], [w(1), 0.58], [w(2), 0.83], [w(3), 1]];
function loadAt(t) { let p = 0; LOADP.forEach(([tt, v], i) => { if (t >= tt) p = lerp(i ? LOADP[i - 1][1] : 0, v, sp(t, tt, 0.8, 16)); }); return p; }
function loading(ctx, t) {
  const al = 1 - P(t, w(3) + 0.15, w(3) + 0.4); if (al <= 0) return;
  const p = clamp(loadAt(t)), bw = 560, x0 = W / 2 - bw / 2, y0 = H - 120;
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = al;
  ctx.fillStyle = rgba(WH, 0.16); ctx.fillRect(x0, y0, bw, 6); ctx.fillStyle = WH; ctx.fillRect(x0, y0, bw * p, 6);
  T(ctx, 'LOADING', x0, y0 - 30, 28, rgba(WH, 0.75), { f: '"Space Mono"', w: 700, a: 'left' });
  T(ctx, String(Math.round(p * 100)).padStart(3, '0') + '%', x0 + bw, y0 - 30, 28, WH, { f: '"Space Mono"', w: 700, a: 'right' });
  ctx.restore();
  glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.globalAlpha = al; g.fillStyle = WH; g.fillRect(x0, y0 - 2, bw * p, 8); }, 0.9, 5);
}
function iHeight(t) { if (t < w(3) - 0.07) return 0; return 420 * sp(t, w(3) - 0.07, 0.7, 10) + 640 * Math.max(0, t - w(3)); }
function SAf(ctx, t) {
  const tI = w(3), dv = P(t, 4.55, 5.35), de = ei3(dv), IW = 210, base = 440;
  const hI = iHeight(t), topY = base - hI, folY = t < tI ? 0 : lerp(0, topY + 260, eo3(P(t, tI, tI + 0.45)));
  const intro = P(t, 0, w(3));
  setCam3({ x: 40 * Math.sin(t * 1.7) * (1 - de), y: folY, z: lerp(-120, 80, intro) + de * 1240, ry: 0.22 * Math.sin(t * 1.3) * (1 - de), rx: (t > tI ? 0.1 : 0) * (1 - de), rz: 0.05 * Math.sin(t * 2.1) * (1 - de) });
  bgv(ctx, RED, GLR, 0.1 + 0.1 * beatPulse(t), W / 2, H * 0.55);
  // poeira e régua de altura passando (sensação de subida contínua junto com o I)
  sx(c => { const r = mulberry32(3); for (let i = 0; i < 40; i++) { const x = r() * W, y = ((r() * H * 3 + folY * (0.4 + r()) * 0.6) % (H + 200) + H + 200) % (H + 200) - 100; c.fillStyle = rgba(WH, 0.1 + 0.18 * r()); c.fillRect(x, y, 2, 14 + r() * 40); }
    if (t > tI) for (let k = -12; k < 40; k++) { const yy = H / 2 + (k * 140 - folY) * 1.05; if (yy < -20 || yy > H + 20) continue; c.fillStyle = rgba(WH, k % 5 ? 0.18 : 0.45); c.fillRect(W / 2 + 330, yy, k % 5 ? 26 : 56, 3); c.fillRect(W / 2 - 330 - (k % 5 ? 26 : 56), yy, k % 5 ? 26 : 56, 3); if (k % 5 === 0) T(c, String(k * 10).padStart(3, '0'), W / 2 + 400, yy, 22, rgba(WH, 0.5), { f: '"Space Mono"', w: 700, a: 'left' }); } });
  // uma palavra por vez, quase a tela inteira
  [['YOU', 0, { z: -1600, rz: 0.7 }], ['SHOULD', 1, { z: 2600, ry: -1.8 }], ['KNOW', 2, { z: -1600, rx: 1.4 }]].forEach(([s, i, fr]) => {
    const sz = fit(s, 1500, 720), nx = w(i + 1);
    W3(ctx, t, s, w(i) - 0.07, { y: 10, size: sz, side: SD, depth: sz * 0.12, from: fr, glow: 0.25, glowCol: WH, flash: 1.4, zeta: 0.45, w: 16, out: nx - 0.08, outD: 0.12, outZ: 1600 });
  });
  // o I: barra 3D branca subindo sem parar; no fim a câmera chega nele e a tela fica branca
  if (hI > 1) {
    const o = { x: 0, y: base - hI / 2, z: 0 }, dims = [IW, hI, 110];
    box3(ctx, dims, o, (i, li) => ({ fill: i === 0 ? WH : mix(SD, '#000000', 0.2 + 0.5 * (1 - li)) }));
    if (de < 0.9) glow(ctx, g => box3(g, dims, o, i => ({ fill: i === 0 ? WH : null })), 0.45 + 0.8 * Math.exp(-(t - tI) * 4), 7);
  }
  loading(ctx, t);
  if (dv > 0.6) sx(c => { c.fillStyle = `rgba(255,255,255,${P(dv, 0.6, 0.95)})`; c.fillRect(0, 0, W, H); });
}
cue(w(0), 'v', 0, { sh: 0.35, ch: 0.3 }); cue(w(1), 'v', 0, { sh: 0.35, ch: 0.3 }); cue(w(2), 'v', 0, { sh: 0.4, ch: 0.4 }); cue(w(3), 'v', 0, { sh: 0.5, ch: 0.4 });

// ---------- B: tela branca escurecendo, sugada por um buraco negro VERMELHO até o HOLD ----------
const VORT = (() => { const r = mulberry32(5), a = []; for (let i = 0; i < 360; i++) a.push({ a: r() * 6.283, r: 500 + r() * 1300, red: r() < 0.5, w: 1 + r() * 3.5, sp: 0.5 + r(), ph: r() }); return a; })();
function SBf(ctx, t) {
  const t0 = 5.46, tc = w(4) - 0.07, u = P(t, t0, tc), dk = eio(P(t, t0 + 0.05, 7.6)), col = 1 - eiExp(P(t, tc - 0.22, tc));
  setCam3({ rz: 0.25 * (t - t0) + 0.6 * ei3(u), z: 380 * ei3(u), ry: 0.12 * Math.sin(t * 1.3), rx: 0.05 * Math.sin(t * 0.9) });
  bg(ctx, mix(WH, '#0b0003', dk));
  sx(c => radial(c, W / 2, H / 2, 1000, GLR, 0.12 + 0.25 * u));
  // fluxo contínuo sendo sugado pro centro
  sx(c => {
    c.lineCap = 'round';
    for (const p of VORT) {
      const fr = ((t - t0) * (0.35 + 0.5 * u) * p.sp + p.ph) % 1, rr0 = 60 + p.r * Math.pow(1 - fr, 1.6), an = p.a + fr * 5 * p.sp + (t - t0) * 0.6, len = 0.15 + 0.5 * fr;
      c.strokeStyle = p.red ? rgba(GLR, 0.35 + 0.5 * fr) : rgba(dk < 0.5 ? '#3a0410' : '#ffffff', (0.15 + 0.45 * fr) * Math.abs(dk - 0.5) * 2);
      c.lineWidth = p.w * (0.5 + fr); c.beginPath(); c.arc(W / 2, H / 2, rr0, an, an + len); c.stroke();
    }
  });
  // buraco negro vermelho: miolo escuro, borda vermelha brilhando, disco de acreção girando
  const r = (24 + 230 * eo3(P(t, t0, tc - 0.3))) * (1 + 0.06 * beatPulse(t)) * col;
  sx(c => {
    for (let i = 0; i < 4; i++) { c.strokeStyle = rgba(i % 2 ? '#ff8fa5' : GLR, 0.7 * col); c.lineWidth = 12 - i * 2.5; c.beginPath(); c.ellipse(W / 2, H / 2, r * (1.45 + i * 0.16), r * (0.4 + i * 0.05), 0.25 + t * 0.6, t * (3 + i), t * (3 + i) + 4.6); c.stroke(); }
    const g = c.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, Math.max(1, r)); g.addColorStop(0, '#0a0002'); g.addColorStop(0.55, '#3a0410'); g.addColorStop(0.85, RT); g.addColorStop(1, GLR);
    c.fillStyle = g; c.beginPath(); c.arc(W / 2, H / 2, Math.max(0, r), 0, 7); c.fill();
  });
  glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.strokeStyle = GLR; g.lineWidth = 50; g.beginPath(); g.arc(W / 2, H / 2, r * 1.04, 0, 7); g.stroke(); }, (0.9 + 0.6 * beatPulse(t)) * col, 8);
  L3(ctx, t, 'TRAINING SEASON', 7.1, { y: 360, size: 44, col: WH, font: '"Space Mono"', wt: '700', out: 9.0 });
  L3(ctx, t, 'dua lipa', 7.4, { y: 415, size: 32, col: GLR, font: '"Space Mono"', wt: '700', out: 9.0 });
}
cue(w(4) - 0.3, 'blurcue', 0, { bl: 0.7 });

// ---------- C: HOLD (impacto máximo) ME CLOSE (abraço) + DEEPER (espelho infinito) ----------
function arcsClose(ctx, t, t0) {
  if (t < t0 - 0.25) return; const k = sp(t, t0 - 0.25, 0.55, 12), gap = lerp(1150, 800, k), al = 1 - P(t, w(7) - 0.12, w(7));
  if (al <= 0) return;
  const draw = (c, lw) => { c.lineCap = 'round'; c.lineWidth = lw; [-1, 1].forEach(sg => { const a0 = sg > 0 ? 0 : Math.PI; c.beginPath(); c.arc(W / 2 + sg * (gap - 520), H / 2, 520, a0 - 0.7, a0 + 0.7); c.stroke(); }); };
  sx(c => { c.globalAlpha = al; c.strokeStyle = WH; draw(c, 10); });
  glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.globalAlpha = al; g.strokeStyle = GLR; draw(g, 40); }, 1.1 + 0.8 * Math.exp(-(t - t0) * 4), 7);
}
function burst(ctx, t, t0, dur, seed) {
  const d = t - t0; if (d < 0 || d > dur) return;
  sx(c => { const r = mulberry32(seed); c.lineCap = 'round'; for (let i = 0; i < 110; i++) { const a = r() * 6.283, r0 = 60 + d * (1700 + r() * 2000), l = 90 + r() * 300; c.strokeStyle = rgba(i % 3 ? GLR : WH, 0.95 * (1 - d / dur)); c.lineWidth = 2 + r() * 5; c.beginPath(); c.moveTo(W / 2 + Math.cos(a) * r0, H / 2 + Math.sin(a) * r0); c.lineTo(W / 2 + Math.cos(a) * (r0 + l), H / 2 + Math.sin(a) * (r0 + l)); c.stroke(); } });
}
function frame3(c, z, rz, fw, fh, col, lw) {
  const o = { z, rz }, pts = [[-fw / 2, -fh / 2], [fw / 2, -fh / 2], [fw / 2, fh / 2], [-fw / 2, fh / 2]].map(p => P3([p[0], p[1], 0], o));
  if (pts.some(p => p[2] < 60)) return; c.strokeStyle = col; c.lineWidth = lw * pts[0][3]; c.lineJoin = 'round'; c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.closePath(); c.stroke();
}
const MIRC = ['#ffffff', '#b80e2c', '#7a0820', '#560616', '#3a040f', '#26020a', '#1a0107', '#120105'];
function SCf(ctx, t) {
  const th = w(4), td = w(7);
  if (t < td - 0.06) {
    const big = eio(P(t, w(5) - 0.2, w(5) - 0.02));
    setCam3({ ry: lerp(0.35, -0.12, eio(P(t, th, td))), z: lerp(-120, 180, P(t, th, td)), rz: 0.05 * Math.sin(t * 3) + 0.03 * beatPulse(t), rx: -0.05 });
    bgv(ctx, K, GLR, 0.22 + 0.15 * beatPulse(t) + 0.4 * Math.exp(-(t - th) * 3)); bokeh(ctx, t, 0.5);
    ring(ctx, t, th, WH, 2900, 70, 0.75); ring(ctx, t, th + 0.06, GLR, 2200, 40, 0.75); burst(ctx, t, th, 0.55, 9);
    const sz = 200, xs = rowG(['HOLD', 'ME', 'CLOSE'], sz, 150);
    W3(ctx, t, 'HOLD', th - 0.07, { x: lerp(0, xs[0], big), y: 0, size: sz, s: lerp(2.6, 1, big), side: SD, depth: 50, from: { z: -2200, rz: 0.9, ry: 1.2 }, glow: 0.35, glowCol: WH, flash: 2.0, zeta: 0.36, w: 17 });
    W3(ctx, t, 'ME', w(5) - 0.07, { x: xs[1], y: 0, size: sz, side: SD, from: { x: 900, z: -900, ry: -1.4 }, glow: 0.2 });
    W3(ctx, t, 'CLOSE', w(6) - 0.07, { x: xs[2], y: 0, size: sz, face: RT, side: DRED, glowCol: GLR, from: { z: -1300, rz: 0.6 }, glow: 0.9, flash: 1.8, zeta: 0.38 });
    arcsClose(ctx, t, w(6));
    return;
  }
  // espelho infinito: cópias de DEEPER com moldura neon, escurecendo na profundidade, fluindo na direção da câmera
  const d = t - td, flow = 1500 * d;
  setCam3({ rz: 0.12 * Math.sin(d * 1.2) + 0.08 * d, ry: 0.16 * Math.sin(d * 1.6), rx: 0.07 * Math.sin(d * 1.1), z: 0 });
  bgv(ctx, K, GLR, 0.12 + 0.1 * beatPulse(t));
  const SP = 820, NL = 11, wrap = Math.floor(flow / SP), off = flow - wrap * SP, list = [];
  for (let i = NL; i >= 0; i--) { const id = i + wrap, z = i * SP - off - 60; list.push({ id, z, lvl: Math.min(MIRC.length - 1, i) }); }
  const glw = [];
  for (const L2 of list) {
    const a0 = clamp((L2.z + 420) / 260), ent = sp(t, td - 0.07 + Math.max(0, L2.id) * 0.03, 0.55, 14);
    if (a0 <= 0 || L2.id < 0) continue;
    const pose = { z: L2.z + (1 - ent) * 1500, rz: L2.id * 0.11, s: 1 }, col = MIRC[L2.lvl];
    text3D(ctx, 'DEEPER', pose, { size: 300, face: col, side: L2.lvl < 2 ? SD : '#140105', depth: L2.lvl < 2 ? 50 : 24, alpha: a0 * clamp(ent * 3) });
    sx(c => { c.globalAlpha = a0 * clamp(ent * 3) * (L2.lvl < 6 ? 0.9 : 0.5); frame3(c, pose.z, pose.rz, 1400, 560, L2.lvl < 1 ? WH : GLR, 6); });
    if (L2.lvl < 2) glw.push([pose, L2.lvl, a0]);
  }
  for (const [pose, lvl, a0] of glw) text3Dglow(ctx, 'DEEPER', pose, { size: 300, glowCol: lvl ? GLR : WH }, (lvl ? 0.3 : 0.55 + 0.9 * Math.exp(-d * 4)) * a0);
  glow(ctx, g => { list.forEach(L2 => { if (L2.id < 0 || L2.lvl > 5) return; frame3(g, L2.z, L2.id * 0.11, 1400, 560, GLR, 14); }); }, 0.8, 6);
}
cue(w(4), 'v', 0, { sh: 1.2, fl: 0.7, ch: 1.1 }); cue(w(5), 'v', 0, { sh: 0.3 }); cue(w(6), 'v', 0, { sh: 0.6, ch: 0.5 });
cue(w(7) - 0.1, 'blurcue', 0, { bl: 0.6 }); cue(w(7), 'v', 0, { sh: 0.55, ch: 0.6, fl: 0.15 }); [11.75, 12.24, 12.72].forEach(b => cue(b, 'v', 0, { sh: 0.18, ch: 0.25 }));

// ---------- D: FEELS LIKE A RODEO (vermelho escuro, letras pulando, laço girando) ----------
function lasso(ctx, t, t0, a) {
  if (a <= 0) return; const pts = [], R = 880, ang = (t - t0) * 7.5, n = 90, tilt = 0.32 + 0.08 * Math.sin(t * 3);
  for (let i = 0; i <= n; i++) { const th = i / n * 6.283; pts.push(P3([Math.cos(th) * R * (1 + 0.04 * Math.sin(th * 3 + t * 6)), -40 + 30 * Math.sin(th * 2 + t * 5), Math.sin(th) * R * 0.5], { rx: tilt, ry: ang, y: 20 })); }
  const draw = (c, lw) => { c.lineWidth = lw; c.lineCap = 'round'; c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.stroke(); };
  ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = WH; draw(ctx, 9); ctx.restore();
  glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.globalAlpha = a; g.strokeStyle = WH; draw(g, 28); }, 0.8 * a, 6);
}
function SDf(ctx, t) {
  const t0 = 13.21, tr = w(10), bk = beatPulse(t);
  setCam3({ rz: 0.09 * Math.sin(t * 6.4) * (t > tr) + 0.06 * bk * (Math.floor(t / 0.488) % 2 ? 1 : -1), ry: 0.3 * Math.sin((t - t0) * 1.1), z: lerp(-150, 250, P(t, t0, 16.2)) + 60 * bk, rx: -0.06 + 0.05 * bk, y: -30 * bk });
  bgv(ctx, RED, GLR, 0.1 + 0.18 * bk);
  ring(ctx, t, t0, WH, 2600, 50, 0.7); ring(ctx, t, tr, WH, 2400, 40, 0.7);
  const xs = rowX(['FEELS', 'LIKE', 'A'], 130);
  [['FEELS', 0], ['LIKE', 1], ['A', 2]].forEach(([s, j]) => W3(ctx, t, s, t0 - 0.07 + j * 0.16, { x: xs[j], y: -360, size: 130, side: SD, from: { z: -900, rx: j % 2 ? 1.3 : -1.3 }, glow: 0.15 }));
  const word = 'RODEO', sz = 330; let tot = 0; const ws = [...word].map(ch => { const x = tw(ch, sz); tot += x + 16; return x; }); tot -= 16;
  let x = -tot / 2;
  [...word].forEach((ch, i) => {
    const ta = tr - 0.07 + i * 0.06, cxl = x + ws[i] / 2; x += ws[i] + 16;
    let jump = 0, rot = 0;
    for (const b of BEATS) { if (b < tr + 0.2 || b > t) continue; const d = t - b - i * 0.03; if (d > 0 && d < 0.45) { jump += Math.sin(Math.PI * d / 0.45) * 120 * (i % 2 ? 1 : 0.7); rot += Math.sin(Math.PI * d / 0.45) * 0.25 * (i % 2 ? 1 : -1); } }
    W3(ctx, t, ch, ta, { x: cxl, y: 60 - jump, rz: rot, size: sz, face: WH, side: SD, depth: 80, from: { y: -700, rx: -1.8, rz: (i % 2 ? 1 : -1) * 0.8 }, w: 14, zeta: 0.4, glow: 0.3, flash: 1.3, N: 3 });
  });
  lasso(ctx, t, tr, P(t, tr + 0.25, tr + 0.6) * (1 - P(t, 16.0, 16.2)));
}
cue(13.21, 'v', 0, { sh: 0.8, fl: 0.25, ch: 0.6 }); cue(w(10), 'v', 0, { sh: 0.7, ch: 0.5 });
[14.70, 15.19, 15.67].forEach(b => cue(b, 'v', 0, { sh: 0.3 }));

// ---------- E: TAKE CONTROL (branco, mira travando) ----------
function SEf(ctx, t) {
  const t0 = w(11) - 0.12, tc = w(12), lock = sp(t, tc, 0.7, 12);
  setCam3({ ry: lerp(0.45, 0.04, lock) + 0.03 * Math.sin(t * 2), rz: lerp(-0.12, 0, lock) + 0.01 * Math.sin(t * 3), z: lerp(-100, 150, P(t, t0, 17.3)), rx: -0.04 });
  bgv(ctx, '#f2f0ee', '#ffffff', 0.4);
  W3(ctx, t, 'TAKE', w(11) - 0.07, { y: -260, size: 140, face: K, side: '#bdbdbd', from: { z: -900, rx: 1.3 }, glow: 0 });
  W3(ctx, t, 'CONTROL', tc - 0.07, { y: 40, size: 300, face: K, side: '#9a9a9a', depth: 60, from: { z: -1800, rz: 0.7, ry: 1.2 }, glow: 0, zeta: 0.42 });
  if (t >= tc - 0.1) {
    const k = sp(t, tc - 0.1, 0.55, 13), gw = lerp(1600, 1120, k), gh = lerp(820, 440, k), cyy = 40;
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.strokeStyle = RT; ctx.lineWidth = 9; ctx.lineCap = 'square';
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sx2, sy]) => { const x0 = W / 2 + sx2 * gw / 2, y0 = H / 2 + cyy + sy * gh / 2; ctx.beginPath(); ctx.moveTo(x0, y0 - sy * 70); ctx.lineTo(x0, y0); ctx.lineTo(x0 - sx2 * 70, y0); ctx.stroke(); });
    const ul = eo3(P(t, tc + 0.05, tc + 0.3)); ctx.fillStyle = RT; ctx.fillRect(W / 2 - 330 * ul, H / 2 + cyy + 200, 660 * ul, 12);
    ctx.beginPath(); ctx.arc(W / 2 - gw / 2 + 30, H / 2 + cyy - gh / 2 - 40, 9, 0, 7); ctx.fill(); T(ctx, 'REC', W / 2 - gw / 2 + 50, H / 2 + cyy - gh / 2 - 38, 26, K, { f: '"Space Mono"', w: 700, a: 'left' });
    ctx.restore();
    glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.fillStyle = GLR; g.fillRect(W / 2 - 330 * ul, H / 2 + cyy + 200, 660 * ul, 12); }, 0.8, 5);
  }
}
cue(w(11), 'v', 0, { sh: 0.2 }); cue(w(12), 'v', 0, { sh: 0.6, ch: 0.3 });

// ---------- F: VULNERABLE — estilhaça em vidro e os mesmos cacos voltam ----------
let GLS = null;
function glassSetup() {
  if (GLS) return GLS; const sz = 260, o = mk(W, H); o.x.font = `${sz}px Anton`; o.x.textAlign = 'center'; o.x.textBaseline = 'middle'; o.x.fillStyle = '#fff'; o.x.fillText('VULNERABLE', W / 2, H / 2);
  const id = o.x.getImageData(0, 0, W, H).data, r = mulberry32(91), sh = [];
  for (let y = 0; y < H; y += 7) for (let x = 0; x < W; x += 7) if (id[(y * W + x) * 4 + 3] > 140) {
    const hx = x - W / 2, hy = y - H / 2, an = Math.atan2(hy + (r() - 0.5) * 200, hx + (r() - 0.5) * 200), s2 = 300 + r() * 1300;
    sh.push({ hx, hy, vx: Math.cos(an) * s2, vy: Math.sin(an) * s2 * 0.8 - 200, vz: -(r() * 2400) + 600, spin: (r() - 0.5) * 18, s: 3 + r() * 7, p: [r(), r(), r(), r()], br: r(), ph: r() * 6 });
  }
  GLS = sh; return sh;
}
function SFf(ctx, t) {
  const t0 = 17.3, tv = w(13), cut = w(14), back = 20.29, home = 20.74, red = 20.78, bk = beatPulse(t);
  setCam3({ ry: 0.32 * Math.sin((t - t0) * 0.9), rx: -0.06 + 0.04 * Math.sin(t * 1.4), z: lerp(-200, 200, P(t, t0, 21.2)) + 40 * bk, rz: 0.04 * Math.sin(t * 1.7) });
  bgv(ctx, K, GLR, 0.16 + 0.15 * bk + 0.2 * (t > red)); bokeh(ctx, t, 0.6);
  BEATS.forEach(b => { if (b >= 17.3 && b < 21.25) ring(ctx, t, b, GLR, 1500, 7, 0.45); });
  W3(ctx, t, 'WHEN I\'M', 17.62 - 0.07, { y: 0, size: 170, side: SD, from: { z: -1000, rx: 1.2 }, glow: 0.2, out: tv - 0.12, outD: 0.12 });
  if (t < tv - 0.07) return;
  const base = { y: 0 };
  if (t < cut) {
    const shiv = 5 * Math.sin(t * 90) * P(t, tv + 0.3, cut);
    W3(ctx, t, 'VULNERABLE', tv - 0.07, { x: shiv, size: 260, side: SD, depth: 50, from: { z: -1300, rz: 0.5, ry: 1.1 }, glow: 0.25, flash: 1.2 });
    return;
  }
  const sh = glassSetup(), dx = Math.min(t, back) - cut, kk = 2.4, f = (1 - Math.exp(-kk * dx)) / kk, m = eio(P(t, back, home));
  if (t < home) {
    const pts = [];
    sx(c => {
      for (const p of sh) {
        let ox = p.vx * f, oy = p.vy * f + 260 * dx * dx, oz = p.vz * f, rot = p.spin * f;
        ox *= 1 - m; oy *= 1 - m; oz *= 1 - m; rot *= 1 - m;
        const q = P3([p.hx + ox, p.hy + oy, oz], base); if (q[2] < 60) continue;
        const S = p.s * q[3] * lerp(1, 0.9, m), fl = 0.55 + 0.45 * Math.sin(t * 14 + p.ph);
        c.fillStyle = p.br < 0.15 ? rgba(GLR, 0.9) : `rgba(255,${235 + Math.round(20 * fl)},${240 + Math.round(15 * fl)},${0.55 + 0.45 * fl})`;
        c.save(); c.translate(q[0], q[1]); c.rotate(rot); c.beginPath(); c.moveTo((p.p[0] - .5) * S * 2, -S); c.lineTo(S, (p.p[1] - .5) * S); c.lineTo((p.p[2] - .5) * S, S); c.lineTo(-S, (p.p[3] - .5) * S); c.closePath(); c.fill(); c.restore();
        if (p.br > 0.82) pts.push([q[0], q[1], S]);
      }
    });
    glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.fillStyle = WH; for (const [x, y, S] of pts) g.fillRect(x - S, y - S, S * 2, S * 2); }, 0.9 + 0.8 * Math.exp(-(t - cut) * 4), 5);
    if (t - cut < 0.25) sx(c => radial(c, W / 2, H / 2, 900, WH, 0.5 * (1 - (t - cut) / 0.25)));
    ring(ctx, t, cut, WH, 2600, 40, 0.6);
    return;
  }
  const kr = sp(t, home, 0.45, 16), o = { s: lerp(1.15, 1, kr), ry: 0.06 * Math.sin(t * 2) };
  text3D(ctx, 'VULNERABLE', o, { size: 260, face: t >= red - 0.03 ? RT : WH, side: DRED, depth: 50 });
  text3Dglow(ctx, 'VULNERABLE', o, { size: 260, glowCol: GLR }, 0.6 + 1.3 * Math.exp(-(t - red) * 4) * (t > red) + 0.4 * bk);
  ring(ctx, t, red, GLR, 2600, 44, 0.8);
}
cue(w(13), 'v', 0, { sh: 0.5, ch: 0.5 }); cue(w(14), 'v', 0, { sh: 1.0, fl: 0.35, ch: 0.9 }); cue(19.81, 'v', 0, { sh: 0.2 });
cue(20.29, 'v', 0, { sh: 0.25, bl: 0.3 }); cue(20.78, 'v', 0, { sh: 0.7, fl: 0.2, ch: 0.6 });

// ---------- G: CONVERSATION OVERLOAD — balões de chat se multiplicando ----------
const BUBS = (() => { const r = mulberry32(12), a = []; for (let i = 0; i < 40; i++) a.push({ x: (r() - 0.5) * 1800, y: (r() - 0.5) * 900, z: -200 + r() * 900, ry: (r() - 0.5) * 0.9, rz: (r() - 0.5) * 0.3, me: r() < 0.4, w: 2 + Math.floor(r() * 4), red: r() < 0.25 }); return a; })();
function bubTex(i) {
  const b = BUBS[i], key = 'bub' + i; return TXC.get(key) || (() => {
    const bw = 220 + b.w * 70, c = mk(bw + 20, 150), x = c.x; x.fillStyle = b.red ? RT : (b.me ? '#f2f2f2' : '#1d1d22'); rr(x, 10, 10, bw, 110, 40); x.fill();
    x.beginPath(); if (b.me) { x.moveTo(bw - 30, 110); x.lineTo(bw + 10, 140); x.lineTo(bw - 70, 112); } else { x.moveTo(50, 110); x.lineTo(14, 140); x.lineTo(90, 112); } x.fill();
    x.fillStyle = b.red ? 'rgba(255,255,255,0.85)' : (b.me ? 'rgba(0,0,0,0.55)' : 'rgba(255,255,255,0.55)');
    for (let l = 0; l < 2; l++) { rr(x, 44, 38 + l * 34, (bw - 90) * (l ? 0.6 : 1), 16, 8); x.fill(); }
    TXC.set(key, c.c); return c.c;
  })();
}
function SGf(ctx, t) {
  const t0 = w(15) - 0.1, tol = w(16);
  setCam3({ ry: 0.4 * Math.sin((t - t0) * 1.4), rz: 0.05 * Math.sin(t * 2.2) + (t > tol ? 0.06 * Math.sin(t * 30) * Math.exp(-(t - tol) * 3) : 0), z: lerp(-250, 120, P(t, t0, 23.1)), x: 50 * Math.sin((t - t0) * 0.9), rx: -0.05 });
  bgv(ctx, DRED, GLR, 0.22 + 0.15 * beatPulse(t));
  const n = Math.floor(clamp((t - t0) / (tol + 0.4 - t0)) * BUBS.length);
  for (let i = 0; i < n; i++) {
    const b = BUBS[i], ta = t0 + i * ((tol + 0.4 - t0) / BUBS.length), k = sp(t, ta, 0.55, 15), tex = bubTex(i);
    plane(ctx, tex, { x: b.x, y: b.y + 10 * Math.sin(t * 2 + i), z: lerp(b.z + 1400, b.z, k), ry: b.ry, rz: b.rz + lerp(0.5, 0, k) }, 2, tex.width, tex.height, 0, 0.55 + 0.45 * k);
  }
  sx(c => { c.fillStyle = 'rgba(0,0,0,0.35)'; c.fillRect(0, 0, W, H); });
  W3(ctx, t, 'CONVERSATION', w(15) - 0.07, { y: -140, z: -300, size: 190, side: SD, from: { z: 2200, ry: -1.6 }, glow: 0.25, flash: 1.0, depth: 50, out: 23.1, outD: 0.12 });
  stamp3(ctx, t, tol - 0.07, 'ovl', 'OVERLOAD', 190, { y: 150, z: -320, rz: -0.06, bg: RT, fc: WH, out: 23.1 });
}
cue(w(15), 'v', 0, { sh: 0.4, ch: 0.3 }); cue(w(16), 'v', 0, { sh: 0.75, fl: 0.2, ch: 0.9 });

// ---------- H: TRAINING SEASON'S + contagem de treino 3-2-1 ----------
function SHf(ctx, t) {
  const t0 = w(17) - 0.12, cd = 24.24, bk = beatPulse(t);
  setCam3({ ry: (t < cd ? 0.3 : -0.25) * Math.sin((t - t0) * 1.5), rz: 0.04 * Math.sin(t * 2.5) + (t > cd ? 0.03 * Math.sin(t * 13) : 0), z: lerp(-150, 260, P(t, t0, 25.1)), rx: -0.05 });
  if (t < cd - 0.05) {
    bgv(ctx, '#f2f0ee', '#ffffff', 0.4);
    W3(ctx, t, 'TRAINING', w(17) - 0.07, { y: -130, size: 250, face: K, side: '#9a9a9a', depth: 60, from: { z: -1500, rz: -0.6 }, glow: 0, zeta: 0.42 });
    W3(ctx, t, 'SEASON\'S', w(18) - 0.07, { y: 140, size: 250, face: RT, side: DRED, depth: 60, from: { z: 2000, ry: 1.6 }, glow: 0.3, glowCol: GLR, flash: 1.0 });
    return;
  }
  bgv(ctx, K, GLR, 0.14 + 0.25 * P(t, cd, 25.15));
  const marks = [[cd, '3'], [24.68, '2'], [24.92, '1']];
  let mi = 0; marks.forEach((m, i) => { if (t >= m[0] - 0.06) mi = i; });
  const [tm, s] = marks[mi], nx = mi < 2 ? marks[mi + 1][0] : w(19), prog = P(t, cd, w(19));
  sx(c => {
    c.lineCap = 'round'; c.strokeStyle = rgba(WH, 0.12); c.lineWidth = 14; c.beginPath(); c.arc(W / 2, H / 2 + 10, 380, 0, 7); c.stroke();
    c.strokeStyle = GLR; c.lineWidth = 18; c.beginPath(); c.arc(W / 2, H / 2 + 10, 380, -Math.PI / 2, -Math.PI / 2 + 6.283 * prog); c.stroke();
    for (let i = 0; i < 60; i++) { const a = i / 60 * 6.283, l = i % 5 ? 14 : 30; c.strokeStyle = rgba(WH, i % 5 ? 0.25 : 0.6); c.lineWidth = i % 5 ? 2 : 4; c.beginPath(); c.moveTo(W / 2 + Math.cos(a) * 430, H / 2 + 10 + Math.sin(a) * 430); c.lineTo(W / 2 + Math.cos(a) * (430 + l), H / 2 + 10 + Math.sin(a) * (430 + l)); c.stroke(); }
  });
  glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.strokeStyle = GLR; g.lineWidth = 40; g.lineCap = 'round'; g.beginPath(); g.arc(W / 2, H / 2 + 10, 380, -Math.PI / 2, -Math.PI / 2 + 6.283 * prog); g.stroke(); }, 1.0, 6);
  W3(ctx, t, s, tm - 0.06, { y: 20, size: 460, face: mi === 2 ? RT : WH, side: mi === 2 ? DRED : SD, glowCol: mi === 2 ? GLR : WH, depth: 90, from: { z: -1600, rz: 0.7 * (mi % 2 ? -1 : 1) }, glow: 0.3, flash: 1.3, zeta: 0.4, out: nx - 0.08, outD: 0.08, outZ: 1300 });
}
cue(w(17), 'v', 0, { sh: 0.5, ch: 0.3 }); cue(w(18), 'v', 0, { sh: 0.45, ch: 0.4 });
cue(24.24, 'v', 0, { sh: 0.4 }); cue(24.68, 'v', 0, { sh: 0.45 }); cue(24.92, 'v', 0, { sh: 0.5, ch: 0.4 });

// ---------- I: OVER (impacto máximo) + buraco negro sugando tudo (close-up) ----------
const PARTS = (() => { const r = mulberry32(41), a = []; for (let i = 0; i < 260; i++) a.push({ a: r() * 6.283, r: 200 + r() * 1300, s: 2 + r() * 6, c: r() < 0.5 ? GLR : WH, sp: 0.5 + r() }); return a; })();
const V1 = 27.42;
function SIf(ctx, t) {
  const to = w(19), v0 = w(20), u = P(t, v0, V1), ue = eiExp(u), bk = beatPulse(t), cu = eiExp(P(t, V1 - 0.38, V1));
  setCam3({ rz: 0.05 * Math.sin(t * 2) + 2.2 * ei3(u), ry: 0.3 * Math.sin((t - to) * 1.2) * (1 - u), z: lerp(-150, 200, P(t, to, v0)) + 420 * ue + 380 * cu, rx: -0.05 });
  if (t < v0) bgv(ctx, RED, GLR, 0.12 + 0.2 * bk); else { bg(ctx, mix(RED, '#000000', clamp(u * 2.2))); sx(c => radial(c, W / 2, H / 2, 1000, GLR, 0.25 * (1 - u))); }
  ring(ctx, t, to, WH, 2800, 60, 0.9); ring(ctx, t, to + 0.08, K, 2000, 30, 0.8);
  BEATS.forEach(b => { if (b > to + 0.1 && b < v0) ring(ctx, t, b, WH, 1800, 20, 0.5); });
  sx(c => {
    for (const p of PARTS) {
      const d = Math.max(0, t - to), out = p.r * (1 - Math.exp(-d * 3)), rr0 = out * (1 - ue) + 2, an = p.a + ue * 7 * p.sp + d * 0.3;
      c.fillStyle = rgba(p.c, 0.8 * clamp(d * 4)); c.fillRect(W / 2 + Math.cos(an) * rr0 - p.s / 2, H / 2 + Math.sin(an) * rr0 * 0.75 - p.s / 2, p.s * (1 + 3 * u), p.s);
    }
  });
  if (u < 0.97) {
    const sc = Math.max(0.001, 1 - eiExp(Math.min(1, u * 1.05))), pls = 1 + 0.06 * bk * (t < v0);
    W3(ctx, t, 'OVER', to - 0.08, { size: 520, s: sc * pls, rz: -ue * 5, face: WH, side: SD, depth: 110, from: { z: -2600, rz: 1.2, ry: 2.4 }, glow: 0.45 + 0.4 * bk, flash: 1.8, zeta: 0.4, w: 12, drift: 0.08 * (1 - u) });
  }
  if (t >= v0 - 0.1) {
    const g0 = eo3(P(t, v0 - 0.1, v0 + 0.3)), col = 1 - eiExp(P(t, V1 - 0.22, V1)), r = (30 + 260 * eo3(u)) * g0 * col;
    sx(c => {
      for (let i = 0; i < 4; i++) { c.strokeStyle = rgba(i % 2 ? WH : GLR, 0.6 * col); c.lineWidth = 16 - i * 3; c.beginPath(); c.ellipse(W / 2, H / 2, r * (1.35 + i * 0.14), r * (0.42 + i * 0.05), 0.2 + t * 0.7, t * (4 + i), t * (4 + i) + 4.4); c.stroke(); }
      c.fillStyle = '#000'; c.beginPath(); c.arc(W / 2, H / 2, r, 0, 7); c.fill();
    });
    glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.strokeStyle = GLR; g.lineWidth = 50; g.beginPath(); g.arc(W / 2, H / 2, r * 1.08, 0, 7); g.stroke(); }, 1.2 * col, 8);
  }
  if (t > V1 - 0.08) sx(c => { c.fillStyle = `rgba(0,0,0,${P(t, V1 - 0.08, V1 + 0.04)})`; c.fillRect(0, 0, W, H); });
}
cue(w(19), 'v', 0, { sh: 1.1, fl: 0.6, ch: 0.9 }); cue(w(19) - 0.25, 'blurcue', 0, { bl: 0.5 });
[25.66, 26.15].forEach(b => cue(b, 'v', 0, { sh: 0.3 })); cue(V1 - 0.3, 'blurcue', 0, { bl: 0.5 }); cue(V1, 'v', 0, { sh: 0.5, ch: 0.6 });

// ---------- J: assinatura parada, minimalista (sem subir e sem fade out) ----------
function SJf(ctx, t) {
  const ti = V1 + 0.45;
  setCam3({ z: 0 });
  bg(ctx, K);
  if (t >= ti) {
    const al = clamp((t - ti) / 0.6);
    const tx = TX('by @ayrtonsena.stg', 46, WH, 'Inter', '700'), o = { y: 0 };
    plane(ctx, tx, o, 1, tx.w, tx.h, 0, al);
    glow(ctx, g => plane(g, tx, o, 1, tx.w, tx.h), 0.75 * al, 7);
  }
}
const END = 31.0;

// ===== registro das cenas =====
scene(0, SAf);
scene(5.46, SBf);
scene(w(4) - 0.07, SCf);
scene(13.21 - 0.07, SDf);
scene(w(11) - 0.12, SEf);
scene(17.3, SFf);
scene(w(15) - 0.1, SGf);
scene(w(17) - 0.12, SHf);
scene(w(19) - 0.08, SIf);
scene(V1, SJf);
