// ===== kit_musica.js — motion music (lyric/motion estilo After Effects) =====
// Carregado depois de engine/engine2/helpers/kit. Tudo é função pura do tempo t (seek em qualquer quadro).
// Nomes escolhidos pra não colidir com o que os scenes.js antigos definem (sx, rowG, fit).

// ---------- utilidades ----------
function scr(fn) { X.save(); X.setTransform(1, 0, 0, 1, 0, 0); fn(X); X.restore(); }          // desenho em coordenada de tela
function rowGap(ws, sz, gap, font = 'Anton') { const wd = ws.map(s => tw(s, sz, font)), tot = wd.reduce((a, b) => a + b, 0) + gap * (ws.length - 1); let x = -tot / 2; return wd.map(v => { const c = x + v / 2; x += v + gap; return c; }); }
function fitSize(s, wmax, hmax, font = 'Anton') { return Math.min(hmax, wmax / (tw(s, 100, font) / 100)); }
function beatNear(t) { let b = BEATS[0] || 0; for (const x of BEATS) if (Math.abs(x - t) < Math.abs(b - t)) b = x; return b; }
function beatsBetween(a, b) { return BEATS.filter(x => x >= a && x < b); }
// clarão estourado (transição de luz entre blocos): flash curto + blur. Flash bom = 2 quadros, sem cauda cinza.
function clarao(t, forca = 0.7) { cue(t, 'v', 0, { fl: forca, bl: 0.7 }); }
function scramble(s, t, t0, dur = 0.35, seed = 7) {
  if (t >= t0 + dur) return s; const r = mulberry32(seed + Math.floor(t * 30)), k = clamp((t - t0) / dur), CH = 'ABCDEFGHJKMNPQRSTUVWXYZ#%&@*';
  return [...s].map((c, i) => (c === ' ' || i / s.length < k) ? c : CH[Math.floor(r() * CH.length)]).join('');
}

// ---------- pós-efeitos globais (ligue no scenes.js: RITMO.fisheye = 0.18 etc. ou função de t) ----------
const RITMO = { fisheye: 0, halftone: 0, halftoneCol: '#000000', vazamento: 0 };
const POSTFX = [];
(function () { const base = window.seek; window.seek = function (t) { base(t); if (NOPOST) return; for (const f of POSTFX) f(t); }; })();
const rval = (v, t) => typeof v === 'function' ? v(t) : v;
const LBUF = mk(W, H);
// lente olho de peixe: centro aumenta, bordas comprimem (malha de triângulos, sem shader)
POSTFX.push(t => {
  const k = rval(RITMO.fisheye, t); if (!k || k < 0.002) return;
  LBUF.x.setTransform(1, 0, 0, 1, 0, 0); LBUF.x.drawImage(C, 0, 0);
  const NX = 28, NY = Math.max(8, Math.round(28 * H / W)), asp = W / H, zoom = 1 + k * 0.35;
  const src = (dx, dy) => { const px = dx * asp, r2 = (px * px + dy * dy) / (asp * asp), f = (1 - k * (1 - r2)) / zoom; return [clamp(dx * f, -1, 1), clamp(dy * f, -1, 1)]; };
  const G = []; for (let j = 0; j <= NY; j++) for (let i = 0; i <= NX; i++) { const dx = -1 + 2 * i / NX, dy = -1 + 2 * j / NY, s = src(dx, dy); G.push([(dx + 1) / 2 * W, (dy + 1) / 2 * H, (s[0] + 1) / 2 * W, (s[1] + 1) / 2 * H]); }
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0);
  for (let j = 0; j < NY; j++) for (let i = 0; i < NX; i++) {
    const A = G[j * (NX + 1) + i], B = G[j * (NX + 1) + i + 1], Cc = G[(j + 1) * (NX + 1) + i + 1], D = G[(j + 1) * (NX + 1) + i];
    tri(X, LBUF.c, A[0], A[1], B[0], B[1], Cc[0], Cc[1], A[2], A[3], B[2], B[3], Cc[2], Cc[3]);
    tri(X, LBUF.c, A[0], A[1], Cc[0], Cc[1], D[0], D[1], A[2], A[3], Cc[2], Cc[3], D[2], D[3]);
  }
  X.restore();
});
// retícula (halftone) por cima: cara de impressão / colagem
const HT = (() => { const c = mk(12, 12); c.x.fillStyle = '#000'; c.x.beginPath(); c.x.arc(6, 6, 2.3, 0, 7); c.x.fill(); return c.c; })();
POSTFX.push(t => {
  const a = rval(RITMO.halftone, t); if (!a) return;
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = a; X.globalCompositeOperation = 'multiply';
  const p = X.createPattern(HT, 'repeat'); X.fillStyle = p; X.fillRect(0, 0, W, H); X.restore();
});
// vazamento de luz quente andando devagar (estilo filme)
POSTFX.push(t => {
  const a = rval(RITMO.vazamento, t); if (!a) return;
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'screen';
  radial(X, W * (0.15 + 0.2 * Math.sin(t * 0.37)), H * (0.2 + 0.1 * Math.cos(t * 0.29)), W * 0.6, '#ff8a3d', 0.35 * a);
  radial(X, W * (0.9 + 0.1 * Math.sin(t * 0.21)), H * 0.85, W * 0.5, '#ff3d6e', 0.25 * a); X.restore();
});

// ---------- texto escrito à mão (write-on) com neon ----------
// o script aparece da esquerda pra direita com a ponta da caneta brilhando. o: {x,y,z,rx,ry,rz,size,font,col,glowCol,glow,out}
const WOC = new Map();
function writeOn(ctx, t, s, t0, dur, o = {}) {
  if (t < t0) return; const size = o.size || 140, font = o.font || 'Pacifico', col = o.col || WH, tx = TX(s, size, col, font, o.wt || '');
  let al = 1; if (o.out !== undefined && t > o.out) al = 1 - P(t, o.out, o.out + (o.outD || 0.25)); if (al <= 0) return;
  const key = s + size + font; let c = WOC.get(key); if (!c) { c = mk(tx.w, tx.h); WOC.set(key, c); }
  const p = eio(clamp((t - t0) / dur)), fe = tx.w * 0.06, ex = -fe + (tx.w + fe * 2) * p;
  c.x.setTransform(1, 0, 0, 1, 0, 0); c.x.globalCompositeOperation = 'source-over'; c.x.clearRect(0, 0, tx.w, tx.h); c.x.drawImage(tx.c, 0, 0);
  if (p < 1) { const g = c.x.createLinearGradient(ex - fe, 0, ex, 0); g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)'); c.x.globalCompositeOperation = 'destination-in'; c.x.fillStyle = g; c.x.fillRect(0, 0, tx.w, tx.h); }
  const pose = { x: o.x || 0, y: o.y || 0, z: o.z || 0, rx: o.rx || 0, ry: o.ry || 0, rz: o.rz || 0, s: o.s ?? 1 };
  plane(ctx, c.c, pose, 2, tx.w, tx.h, 0, al);
  glow(ctx, g => plane(g, c.c, pose, 1, tx.w, tx.h), (o.glow ?? 0.9) * al, o.blur || 6);
  if (p > 0 && p < 1) { const q = P3([ex - tx.w / 2 - fe * 0.5, 0, -1], pose); scr(c2 => { c2.globalCompositeOperation = 'lighter'; radial(c2, q[0], q[1], 60 * q[3], o.glowCol || col, 0.9 * al); }); }
}

// ---------- pílula/etiqueta com sombra longa e texto que troca ----------
// o: {x,y,z,rx,ry,rz, size, font, bg, fg, sombra, textos:[[t,'texto'],...], t0, out, padX, padY, raio}
function pill(ctx, t, o) {
  const t0 = o.t0 ?? o.textos[0][0]; if (t < t0) return;
  const size = o.size || 90, font = o.font || 'Anton', padX = o.padX ?? size * 0.45, padY = o.padY ?? size * 0.22, R = o.raio ?? size * 0.32;
  let i = 0; o.textos.forEach((x, j) => { if (t >= x[0]) i = j; });
  const cur = o.textos[i][1], prev = i ? o.textos[i - 1][1] : null, ts = o.textos[i][0], sw = clamp((t - ts) / 0.16);
  const wCur = tw(cur, size, font), wPrev = prev ? tw(prev, size, font) : wCur, bw = lerp(wPrev, wCur, eo3(sw)) + padX * 2, bh = size * 1.18 + padY * 2;
  const sh = o.sombra === false ? 0 : (o.sombraLen ?? size * 1.4), cw = Math.ceil(bw + sh + 8), ch = Math.ceil(bh + sh + 8);
  const key = 'pill' + (o.id || ''); let c = WOC.get(key); if (!c || c.c.width < cw || c.c.height < ch) { c = mk(Math.max(cw, c ? c.c.width : 0), Math.max(ch, c ? c.c.height : 0)); WOC.set(key, c); }
  const x = c.x; x.setTransform(1, 0, 0, 1, 0, 0); x.clearRect(0, 0, c.c.width, c.c.height);
  if (sh) { // sombra longa diagonal: desenha opaca num canvas à parte e aplica com transparência (não acumula)
    let sc = WOC.get(key + 's'); if (!sc || sc.c.width < c.c.width || sc.c.height < c.c.height) { sc = mk(c.c.width, c.c.height); WOC.set(key + 's', sc); }
    sc.x.setTransform(1, 0, 0, 1, 0, 0); sc.x.clearRect(0, 0, sc.c.width, sc.c.height); sc.x.fillStyle = o.sombraCol || mix(o.bg || V, '#000000', 0.35);
    for (let k = sh; k > 0; k -= 2) { rr(sc.x, 4 + k, 4 + k, bw, bh, R); sc.x.fill(); }
    x.globalAlpha = o.sombraAlpha ?? 0.32; x.drawImage(sc.c, 0, 0); x.globalAlpha = 1; }
  x.fillStyle = o.bg || V; rr(x, 4, 4, bw, bh, R); x.fill();
  x.save(); rr(x, 4, 4, bw, bh, R); x.clip(); x.font = `${o.wt || ''} ${size}px ${font}`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = o.fg || WH;
  if (prev && sw < 1) { x.globalAlpha = 1 - sw; x.fillText(prev, 4 + bw / 2, 4 + bh / 2 - sw * bh * 0.7); x.globalAlpha = sw; x.fillText(cur, 4 + bw / 2, 4 + bh / 2 + (1 - sw) * bh * 0.7); }
  else x.fillText(o.scramble ? scramble(cur, t, ts, o.scramble) : cur, 4 + bw / 2, 4 + bh / 2 + size * 0.04);
  x.restore();
  const k = sp(t, t0 - 0.06, 0.5, 15); let al = clamp((t - t0 + 0.06) / 0.05); if (o.out !== undefined && t > o.out) al *= 1 - P(t, o.out, o.out + 0.2);
  const pose = { x: (o.x || 0) + (c.c.width / 2 - 4 - bw / 2), y: (o.y || 0) + (c.c.height / 2 - 4 - bh / 2), z: (o.z || 0) + (1 - k) * -500, rx: o.rx || 0, ry: o.ry || 0, rz: (o.rz || 0) + (1 - k) * 0.5, s: lerp(0.3, 1, Math.min(1.2, k)) };
  plane(ctx, c.c, pose, 2, c.c.width, c.c.height, 0, al);
}

// ---------- texto em círculo girando (o "ooooh" do Juno) ----------
// o: {x,y,z,r,size,font,col,spin,stagger,glow}
function circleText(ctx, t, s, t0, o = {}) {
  if (t < t0) return; const r = o.r || 360, size = o.size || 110, chars = [...s], n = chars.length, rot = (o.spin ?? 0.9) * (t - t0) + (o.a0 || -Math.PI / 2);
  chars.forEach((ch, i) => {
    const ta = t0 + i * (o.stagger ?? 0.04); if (t < ta) return; const k = sp(t, ta, 0.5, 16), a = rot + i / n * Math.PI * 2;
    const pose = { x: (o.x || 0) + Math.cos(a) * r, y: (o.y || 0) + Math.sin(a) * r, z: o.z || 0, rz: a + Math.PI / 2, s: Math.min(1.25, k) };
    const tx = TX(ch, size, o.col || WH, o.font || 'Anton'); plane(ctx, tx, pose, 1);
  });
  if (o.glow) glow(ctx, g => chars.forEach((ch, i) => { if (t < t0 + i * (o.stagger ?? 0.04)) return; const a = rot + i / n * Math.PI * 2; plane(g, TX(ch, size, o.glowCol || o.col || WH, o.font || 'Anton'), { x: (o.x || 0) + Math.cos(a) * r, y: (o.y || 0) + Math.sin(a) * r, z: o.z || 0, rz: a + Math.PI / 2 }, 1); }), o.glow, 6);
}

// ---------- sílaba esticada = letra repetida num caminho (Foreverrrr / DOOOIDO / IIII) ----------
// times: instantes de cada letra (ex.: a cada meia batida). path(i) -> {x,y,z,rz}.
// Ordem na cena: h = trailHead(t, times, path) -> setCam3 seguindo h -> fundo -> letterTrail(...).
function trailHead(t, times, path) { let i = 0; times.forEach((ti, j) => { if (t >= ti) i = j; }); const a = path(Math.max(0, i - 1)), b = path(i), k = sp(t, times[i], 0.85, 9); return { x: lerp(a.x, b.x, k), y: lerp(a.y, b.y, k), z: lerp(a.z || 0, b.z || 0, k), i }; }
function letterTrail(ctx, t, ch, times, path, o = {}) {
  let head = path(0);
  times.forEach((ti, i) => { if (t < ti) return; const p = path(i); head = p; W3(ctx, t, ch, ti, { size: o.size || 300, face: o.face || WH, side: o.side || SIDE, x: p.x, y: p.y, z: p.z || 0, rz: p.rz || 0, from: o.from || (i % 2 ? { z: 1400, ry: 1.5 } : { z: -800, rx: 1.2 }), glow: o.glow ?? 0.15, flash: o.flash ?? 0.8, depth: o.depth, w: 17 }); });
  return head;
}

// ---------- transições ----------
// íris: forma cresce do centro e cobre a tela com a cor da PRÓXIMA cena (forma: 'circulo' | 'coracao' | 'estrela')
function iris(ctx, t, t0, dur, cor, forma = 'circulo', cx = W / 2, cy = H / 2) {
  if (t < t0 || t > t0 + dur + 0.05) return; const p = ei3(clamp((t - t0) / dur)), R = p * Math.hypot(W, H) * (forma === 'circulo' ? 0.6 : 0.9);
  scr(c => {
    c.fillStyle = cor; c.beginPath();
    if (forma === 'coracao') { c.translate(cx, cy); c.scale(R / 100, R / 100); c.moveTo(0, 35); c.bezierCurveTo(-100, -30, -50, -100, 0, -45); c.bezierCurveTo(50, -100, 100, -30, 0, 35); }
    else if (forma === 'estrela') { for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr2 = i % 2 ? R * 0.45 : R; c.lineTo(cx + Math.cos(a) * rr2, cy + Math.sin(a) * rr2); } }
    else c.arc(cx, cy, R, 0, 7);
    c.closePath(); c.fill();
  });
}
// objeto passando colado na lente (abelha do Tyler): atravessa a tela gigante e desfocado; o corte de cena vai no meio (t0+dur/2)
// desenho(c, x, y, s): desenha o objeto centrado em (x,y) com escala s. Padrão: emoji.
function lensPass(ctx, t, t0, dur, desenho, o = {}) {
  if (t < t0 || t > t0 + dur) return; const p = clamp((t - t0) / dur), dir = o.dir || 1;
  const x = W / 2 + dir * lerp(-W * 0.9, W * 0.9, eio(p)), y = H / 2 + (o.dy || 0) + Math.sin(p * Math.PI) * -60, s = (o.s || 1) * (0.9 + Math.sin(p * Math.PI) * 1.6);
  const draw = typeof desenho === 'string' ? (c, X0, Y0, S) => { c.font = `${Math.round(700 * S)}px "Segoe UI Emoji","Apple Color Emoji",sans-serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(desenho, X0, Y0); } : desenho;
  blurDraw(ctx, c => { c.save(); c.setTransform(0.25, 0, 0, 0.25, 0, 0); draw(c, x, y, s); c.restore(); }, o.blur ?? 5, 1);
}
// explosão de quadrinho (starburst) atrás da pessoa/palavra, batendo junto da palavra
const SBC = new Map();
function starburst(ctx, t, t0, o = {}) {
  if (t < t0) return; const col = o.col || '#fff3c4', R = o.r || 420, n = o.pontas || 16, key = col + R + n;
  let c = SBC.get(key); if (!c) { c = mk(R * 2 + 20, R * 2 + 20); const x = c.x, rnd = mulberry32(n); x.fillStyle = col; x.beginPath(); for (let i = 0; i < n * 2; i++) { const a = i / (n * 2) * Math.PI * 2, rr2 = i % 2 ? R * (0.55 + 0.1 * rnd()) : R * (0.9 + 0.1 * rnd()); x.lineTo(R + 10 + Math.cos(a) * rr2, R + 10 + Math.sin(a) * rr2); } x.closePath(); x.fill(); SBC.set(key, c); }
  const k = sp(t, t0 - 0.05, 0.4, 18); let al = 1; if (o.out !== undefined && t > o.out) al = 1 - P(t, o.out, o.out + 0.15);
  const pose = { x: o.x || 0, y: o.y || 0, z: o.z ?? 200, rz: (o.giro ?? 0.25) * (t - t0), s: Math.min(1.15, k) * (1 + 0.05 * beatPulse(t)) };
  plane(ctx, c.c, pose, 2, c.c.width, c.c.height, 0, al);
  glow(ctx, g => plane(g, c.c, pose, 1, c.c.width, c.c.height), (o.glow ?? 0.25) * al, 8);
}

// ---------- cenário ----------
// chão de grade em perspectiva (Juno): linhas no plano y = yChao, rolando na direção da câmera
function gridFloor(ctx, t, o = {}) {
  const yC = o.y ?? 380, step = o.step || 160, n = o.n || 18, col = o.col || rgba(WH, 0.45), sc = ((t * (o.vel ?? 220)) % step);
  ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = o.lw || 2;
  for (let i = -n; i <= n; i++) { const a = P3([i * step, yC, -200], {}), b = P3([i * step, yC, n * step * 2], {}); if (a[2] < 30 || b[2] < 30) continue; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); }
  for (let j = 0; j < n * 2; j++) { const z = j * step - sc, a = P3([-n * step, yC, z], {}), b = P3([n * step, yC, z], {}); if (a[2] < 30 || b[2] < 30) continue; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); }
  ctx.restore();
}
// chuva/nuvem de objetos do universo da música (beijos, corações, abelhas, emoji) em profundidade, os de perto desfocados
// desenho: string emoji OU canvas/imagem. o: {n, seed, area, vel, tam, desfoque}
const PROPC = new Map();
function propsField(ctx, t, t0, desenho, o = {}) {
  if (t < t0) return; const n = o.n || 24, r = mulberry32(o.seed || 9), ar = o.area || 1600, list = [];
  let img = typeof desenho === 'string' ? PROPC.get(desenho) : desenho;
  if (!img) { const c = mk(256, 256); c.x.font = '200px "Segoe UI Emoji","Apple Color Emoji",sans-serif'; c.x.textAlign = 'center'; c.x.textBaseline = 'middle'; c.x.fillText(desenho, 128, 140); PROPC.set(desenho, c.c); img = c.c; }
  for (let i = 0; i < n; i++) list.push({ x: (r() - 0.5) * ar * 1.6, y: (r() - 0.5) * ar, z: -600 + r() * 2600, rz: (r() - 0.5) * 1.2, s: (o.tam || 0.8) * (0.5 + r()), d: r(), ta: t0 + r() * (o.espalha ?? 0.4) });
  list.sort((a, b) => b.z - a.z);
  for (const p of list) {
    if (t < p.ta) continue; const k = sp(t, p.ta, 0.55, 14), y = p.y - (o.vel ?? 40) * (t - t0) * (0.5 + p.d), pose = { x: p.x, y, z: p.z, rz: p.rz + 0.3 * Math.sin(t + p.d * 6), s: p.s * Math.min(1.1, k) };
    if (p.z < -200 && (o.desfoque ?? true)) blurDraw(ctx, c => plane(c, img, pose, 1), 4, 0.9); else plane(ctx, img, pose, 1);
  }
}

// ---------- peças prontas do Training Season (aprovadas) ----------
// barra "LOADING 000%" que enche nos marcos [[t, fração], ...]
function loadingBar(ctx, t, marcos, o = {}) {
  const fim = o.fim ?? marcos[marcos.length - 1][0], al = 1 - P(t, fim + 0.15, fim + 0.4); if (al <= 0) return;
  let p = 0; marcos.forEach(([tt, v], i) => { if (t >= tt) p = lerp(i ? marcos[i - 1][1] : 0, v, sp(t, tt, 0.8, 16)); }); p = clamp(p);
  const bw = o.w || 560, x0 = W / 2 - bw / 2, y0 = o.y ?? H - 120, col = o.col || WH;
  scr(c => { c.globalAlpha = al; c.fillStyle = rgba(col, 0.16); c.fillRect(x0, y0, bw, 6); c.fillStyle = col; c.fillRect(x0, y0, bw * p, 6);
    T(c, o.label || 'LOADING', x0, y0 - 30, 28, rgba(col, 0.75), { f: '"Space Mono"', w: 700, a: 'left' }); T(c, String(Math.round(p * 100)).padStart(3, '0') + '%', x0 + bw, y0 - 30, 28, col, { f: '"Space Mono"', w: 700, a: 'right' }); });
  glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.globalAlpha = al; g.fillStyle = col; g.fillRect(x0, y0 - 2, bw * p, 8); }, 0.9, 5);
}
// buraco negro VERMELHO que cresce sugando e fecha em t1 (miolo escuro, borda vermelha, disco de acreção)
function redHole(ctx, t, t0, t1, o = {}) {
  if (t < t0 || t > t1) return; const u = P(t, t0, t1), col = 1 - eiExp(P(t, t1 - 0.22, t1)), r = (o.r0 ?? 24) + (o.r1 ?? 230) * eo3(P(t, t0, t1 - 0.3)) * (1 + 0.06 * beatPulse(t)) * col;
  const RIM = o.cor || '#ff2d55', MID = o.meio || '#3a0410';
  scr(c => {
    for (let i = 0; i < 4; i++) { c.strokeStyle = rgba(i % 2 ? '#ff8fa5' : RIM, 0.7 * col); c.lineWidth = 12 - i * 2.5; c.beginPath(); c.ellipse(W / 2, H / 2, r * (1.45 + i * 0.16), r * (0.4 + i * 0.05), 0.25 + t * 0.6, t * (3 + i), t * (3 + i) + 4.6); c.stroke(); }
    const g = c.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, Math.max(1, r)); g.addColorStop(0, '#0a0002'); g.addColorStop(0.55, MID); g.addColorStop(0.85, o.borda || '#e8173f'); g.addColorStop(1, RIM);
    c.fillStyle = g; c.beginPath(); c.arc(W / 2, H / 2, Math.max(0, r), 0, 7); c.fill();
  });
  glow(ctx, g => { g.setTransform(.25, 0, 0, .25, 0, 0); g.strokeStyle = RIM; g.lineWidth = 50; g.beginPath(); g.arc(W / 2, H / 2, r * 1.04, 0, 7); g.stroke(); }, (0.9 + 0.6 * beatPulse(t)) * col, 8);
  return u;
}
// assinatura final: pequena, branca, glow, centralizada, PARADA e sem fade out
// txt = o @ que a PESSOA informou (ex.: 'by @fulano'). Sem txt nao desenha nada: nunca assine com um @ que ela nao deu.
function assinatura(ctx, t, t0, txt = '', o = {}) {
  if (!txt) return;
  // desenhada em coordenada de TELA: não gira nem treme com a câmera da cena
  if (t < t0) return; const al = clamp((t - t0) / (o.fadeIn ?? 0.6)), tx = TX(txt, o.size || 46, o.col || WH, o.font || 'Inter', o.wt || '700');
  const x0 = W / 2 - tx.w / 2, y0 = H / 2 + (o.y || 0) - tx.h / 2;
  scr(c => { c.globalAlpha = al; c.drawImage(tx.c, x0, y0); });
  if (!NOPOST) { const g = GA.x; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, 480, 270); g.drawImage(tx.c, x0 / 4, y0 / 4, tx.w / 4, tx.h / 4); const h = GB.x; h.setTransform(1, 0, 0, 1, 0, 0); h.clearRect(0, 0, 480, 270); h.filter = 'blur(7px)'; h.drawImage(GA.c, 0, 0); h.filter = 'none';
    scr(c => { c.globalCompositeOperation = 'lighter'; c.globalAlpha = clamp((o.glow ?? 0.75) * al); c.drawImage(GB.c, 0, 0, W, H); }); }
}
