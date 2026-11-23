// ===== Motion IA — motor (Canvas2D, deterministic, window.seek) =====
const W = 1920, H = 1080;
const K = '#000000', V = '#7F3AED', L = '#C6FF34', WH = '#FFFFFF';
const C = document.getElementById('c'); C.width = W; C.height = H;
const X = C.getContext('2d');
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return { c, x: c.getContext('2d') }; }
const BUF = mk(W, H), BUF2 = mk(W, H), GA = mk(480, 270), GB = mk(480, 270);
let NOPOST = false;

// ---------- math ----------
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const P = (t, a, b) => clamp((t - a) / (b - a));
const eo3 = t => 1 - Math.pow(1 - t, 3);
const ei3 = t => t * t * t;
const eio = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const eoExp = t => t >= 1 ? 1 : 1 - Math.pow(2, -10 * t);
const eiExp = t => t <= 0 ? 0 : Math.pow(2, 10 * t - 10);
function spring(t, z = 0.62, w = 15) {
  if (t <= 0) return 0;
  const wd = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t));
}
const sp = (t, t0, z, w) => spring(t - t0, z, w);
function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function hex2rgb(h) { const n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function mix(a, b, t) { const A = hex2rgb(a), B = hex2rgb(b); return `rgb(${A.map((v, i) => Math.round(lerp(v, B[i], t))).join(',')})`; }
function rgba(h, a) { const [r, g, b] = hex2rgb(h); return `rgba(${r},${g},${b},${a})`; }

// ---------- text ----------
function T(ctx, s, x, y, sz, col, o = {}) {
  ctx.save();
  ctx.font = `${o.w || ''} ${sz}px ${o.f || 'Anton'}`;
  ctx.fillStyle = col; ctx.textAlign = o.a || 'center'; ctx.textBaseline = o.b || 'middle';
  ctx.letterSpacing = (o.ls || 0) + 'px';
  if (o.al !== undefined) ctx.globalAlpha *= o.al;
  if (o.sc !== undefined || o.r) { ctx.translate(x, y); if (o.r) ctx.rotate(o.r); const s2 = o.sc ?? 1; ctx.scale(s2, s2); x = 0; y = 0; }
  if (o.stroke) { ctx.lineWidth = o.stroke; ctx.strokeStyle = col; ctx.lineJoin = 'round'; ctx.strokeText(s, x, y); }
  else ctx.fillText(s, x, y);
  ctx.restore();
}
function tw(s, sz, f = 'Anton', w = '') { X.save(); X.font = `${w} ${sz}px ${f}`; const m = X.measureText(s).width; X.restore(); return m; }
// pseudo-3D extruded text
function T3(ctx, s, x, y, sz, o = {}) {
  const d = o.depth ?? sz * 0.14, ry = o.ry || 0, rx = o.rx || 0, sc = o.sc ?? 1;
  const n = Math.max(6, Math.min(34, Math.round(d / 2.2)));
  ctx.save(); ctx.translate(x, y);
  if (o.rz) ctx.rotate(o.rz);
  ctx.scale(sc * Math.max(.05, Math.cos(ry)), sc * Math.max(.05, Math.cos(rx)));
  ctx.transform(1, Math.sin(ry) * 0.16, -Math.sin(rx) * 0.16, 1, 0, 0);
  ctx.font = `${sz}px ${o.f || 'Anton'}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.letterSpacing = (o.ls || 0) + 'px';
  if (o.al !== undefined) ctx.globalAlpha *= o.al;
  const dx = d * (0.18 - Math.sin(ry) * 1.1), dy = d * (0.26 + Math.sin(rx) * 1.1);
  const side = o.side || '#4a1f99', face = o.face || WH;
  for (let i = n; i >= 1; i--) { const k = i / n; ctx.fillStyle = mix(side, '#000000', k * 0.75); ctx.fillText(s, dx * k, dy * k); }
  ctx.fillStyle = face; ctx.fillText(s, 0, 0);
  if (o.sweep !== undefined) { // light sweep across the face
    ctx.globalCompositeOperation = 'source-atop';
    const w = tw(s, sz, o.f || 'Anton'); const gx = lerp(-w, w, o.sweep);
    const g = ctx.createLinearGradient(gx - 140, 0, gx + 140, 0);
    g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(.5, 'rgba(198,255,52,0.85)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = g; ctx.fillRect(-w, -sz, 2 * w, 2 * sz);
  }
  ctx.restore();
}

// ---------- camera / glow / post ----------
function cam(ctx, c) { ctx.translate(W / 2, H / 2); if (c.r) ctx.rotate(c.r); const z = c.z ?? 1; ctx.scale(z, z); ctx.translate(-W / 2 - (c.x || 0), -H / 2 - (c.y || 0)); }
function glow(ctx, fn, amt = 1, blur = 7) {
  if (NOPOST || ctx !== X) return;
  const g = GA.x; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, 480, 270); g.setTransform(.25, 0, 0, .25, 0, 0); camApply(g, CUR_T);
  fn(g);
  const h = GB.x; h.setTransform(1, 0, 0, 1, 0, 0); h.clearRect(0, 0, 480, 270); h.filter = `blur(${blur}px)`; h.drawImage(GA.c, 0, 0); h.filter = 'none';
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'lighter';
  X.globalAlpha = clamp(amt, 0, 1); X.drawImage(GB.c, 0, 0, W, H);
  if (amt > 1) { X.globalAlpha = clamp(amt - 1, 0, 1); X.drawImage(GB.c, 0, 0, W, H); }
  X.restore();
}
function bg(ctx, col) { ctx.save(); ctx.fillStyle = col; ctx.fillRect(-W, -H, W * 3, H * 3); ctx.restore(); }
function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
function radial(ctx, x, y, r, col, a) { const g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, rgba(col, a)); g.addColorStop(1, rgba(col, 0)); ctx.fillStyle = g; ctx.fillRect(x - r, y - r, 2 * r, 2 * r); }

// noise tile
const NT = mk(256, 256); { const r = mulberry32(7), id = NT.x.createImageData(256, 256); for (let i = 0; i < id.data.length; i += 4) { const v = r() * 255; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; } NT.x.putImageData(id, 0, 0); }

function envAt(t, key) { // sum of decaying impulses from CUES
  let s = 0; for (const c of CUES) { const a = c[key]; if (!a) continue; const d = t - c.t; if (d >= 0 && d < 0.6) s += a * Math.exp(-d * (key === 'flash' ? 14 : 9)); } return s;
}
function smearAt(t) { for (const s of SMEARS) if (t >= s[0] && t < s[1]) { const k = Math.sin(Math.PI * P(t, s[0], s[1])); return [s[2] * k, s[3] * k]; } return null; }
function post(t) {
  X.setTransform(1, 0, 0, 1, 0, 0);
  // smear (directional motion blur)
  const sm = smearAt(t);
  if (sm) { BUF.x.setTransform(1, 0, 0, 1, 0, 0); BUF.x.clearRect(0, 0, W, H); BUF.x.drawImage(C, 0, 0); X.save(); for (let i = 1; i <= 6; i++) { X.globalAlpha = 0.22; X.drawImage(BUF.c, sm[0] * i / 6, sm[1] * i / 6); X.globalAlpha = 0.22; X.drawImage(BUF.c, -sm[0] * i / 6, -sm[1] * i / 6); } X.restore(); }
  // chroma
  const ch = Math.min(1.2, envAt(t, 'chroma'));
  if (ch > 0.03) {
    BUF.x.setTransform(1, 0, 0, 1, 0, 0); BUF.x.globalCompositeOperation = 'source-over'; BUF.x.drawImage(C, 0, 0);
    BUF.x.globalCompositeOperation = 'multiply'; BUF.x.fillStyle = V; BUF.x.fillRect(0, 0, W, H); BUF.x.globalCompositeOperation = 'source-over';
    BUF2.x.setTransform(1, 0, 0, 1, 0, 0); BUF2.x.globalCompositeOperation = 'source-over'; BUF2.x.drawImage(C, 0, 0);
    BUF2.x.globalCompositeOperation = 'multiply'; BUF2.x.fillStyle = L; BUF2.x.fillRect(0, 0, W, H); BUF2.x.globalCompositeOperation = 'source-over';
    X.save(); X.globalCompositeOperation = 'lighter'; X.globalAlpha = 0.45 * ch; X.drawImage(BUF.c, -14 * ch, 0); X.drawImage(BUF2.c, 14 * ch, 0); X.restore();
  }
  // shake (global)
  const shv = envAt(t, 'shake');
  if (shv > 0.02) {
    const a = shv * 26, dx = Math.sin(t * 97.1) * a + Math.sin(t * 61.3) * a * .5, dy = Math.cos(t * 83.7) * a * .8;
    BUF.x.setTransform(1, 0, 0, 1, 0, 0); BUF.x.drawImage(C, 0, 0);
    X.save(); X.translate(W / 2 + dx, H / 2 + dy); X.rotate(Math.sin(t * 47) * 0.006 * shv); X.scale(1.04, 1.04); X.drawImage(BUF.c, -W / 2, -H / 2); X.restore();
  }
  // flash
  const fl = Math.min(1, envAt(t, 'flash'));
  if (fl > 0.01) { X.save(); X.globalCompositeOperation = 'lighter'; X.fillStyle = `rgba(255,255,255,${fl * 0.85})`; X.fillRect(0, 0, W, H); X.restore(); }
  // vignette
  X.save(); const g = X.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0.42)'); X.fillStyle = g; X.fillRect(0, 0, W, H); X.restore();
  // grain
  X.save(); X.globalAlpha = 0.06; X.globalCompositeOperation = 'overlay'; const pat = X.createPattern(NT.c, 'repeat'); const o = Math.floor(t * 30) * 37 % 256; X.translate(-o, -(o * 3 % 256)); X.fillStyle = pat; X.fillRect(0, 0, W + 256, H + 256); X.restore();
}

// ---------- mini 3D ----------
function rot3(p, ax, ay, az) {
  let [x, y, z] = p, c, s;
  c = Math.cos(ax); s = Math.sin(ax); [y, z] = [y * c - z * s, y * s + z * c];
  c = Math.cos(ay); s = Math.sin(ay); [x, z] = [x * c + z * s, -x * s + z * c];
  c = Math.cos(az); s = Math.sin(az); [x, y] = [x * c - y * s, x * s + y * c];
  return [x, y, z];
}
function proj(p, cx, cy, f = 1500) { const z = p[2] + f; const k = f / Math.max(60, z); return [cx + p[0] * k, cy + p[1] * k, z]; }
// box: size [w,h,d], rotation, position; faces callback(faceIndex) -> {fill, draw(ctx,w,h)}
function box(ctx, cx, cy, size, rot, pos, faceStyle, f = 1500) {
  const [w, h, d] = size.map(v => v / 2);
  const V0 = [[-w, -h, -d], [w, -h, -d], [w, h, -d], [-w, h, -d], [-w, -h, d], [w, -h, d], [w, h, d], [-w, h, d]];
  const Vt = V0.map(p => { const r = rot3(p, rot[0], rot[1], rot[2]); return [r[0] + pos[0], r[1] + pos[1], r[2] + pos[2]]; });
  const Pp = Vt.map(p => proj(p, cx, cy, f));
  // faces: front(z-), back, left, right, top, bottom ; vertex order TL,TR,BR,BL ; dims
  const F = [[0, 1, 2, 3, size[0], size[1]], [5, 4, 7, 6, size[0], size[1]], [4, 0, 3, 7, size[2], size[1]], [1, 5, 6, 2, size[2], size[1]], [4, 5, 1, 0, size[0], size[2]], [3, 2, 6, 7, size[0], size[2]]];
  const list = [];
  F.forEach((fc, i) => {
    const a = Vt[fc[0]], b = Vt[fc[1]], c3 = Vt[fc[3]];
    const u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [c3[0] - a[0], c3[1] - a[1], c3[2] - a[2]];
    const n = [-(u[1] * v[2] - u[2] * v[1]), -(u[2] * v[0] - u[0] * v[2]), -(u[0] * v[1] - u[1] * v[0])];
    const ctr = [0, 1, 2, 3].map(k => Vt[fc[k]]).reduce((s, p) => [s[0] + p[0] / 4, s[1] + p[1] / 4, s[2] + p[2] / 4], [0, 0, 0]);
    const viewv = [ctr[0], ctr[1], ctr[2] + f];
    const dot = n[0] * viewv[0] + n[1] * viewv[1] + n[2] * viewv[2];
    if (dot >= 0) return;
    const nl = Math.hypot(...n); const light = clamp(0.35 + 0.65 * Math.max(0, (-n[0] * 0.4 - n[1] * 0.6 - n[2] * 0.7) / nl));
    list.push({ i, z: ctr[2], fc, light });
  });
  list.sort((p, q) => q.z - p.z);
  for (const it of list) {
    const pts = it.fc.slice(0, 4).map(k => Pp[k]);
    const st = faceStyle(it.i, it.light);
    ctx.save(); ctx.beginPath(); pts.forEach((p, k) => k ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath();
    ctx.fillStyle = st.fill; ctx.fill();
    if (st.stroke) { ctx.strokeStyle = st.stroke; ctx.lineWidth = st.lw || 2; ctx.stroke(); }
    if (st.draw) { ctx.clip(); const fw = it.fc[4], fh = it.fc[5]; const p0 = pts[0], p1 = pts[1], p3 = pts[3]; ctx.transform((p1[0] - p0[0]) / fw, (p1[1] - p0[1]) / fw, (p3[0] - p0[0]) / fh, (p3[1] - p0[1]) / fh, p0[0], p0[1]); st.draw(ctx, fw, fh, it.light); }
    ctx.restore();
  }
  return Pp;
}

// ---------- shared drawables ----------
function eye(ctx, x, y, r, open, lx, ly) {
  ctx.save(); ctx.translate(x, y);
  const h = r * 0.62 * open;
  ctx.beginPath(); ctx.moveTo(-r, 0); ctx.quadraticCurveTo(0, -h * 1.6, r, 0); ctx.quadraticCurveTo(0, h * 1.6, -r, 0); ctx.closePath();
  ctx.fillStyle = '#0d0d0d'; ctx.fill(); ctx.lineWidth = r * 0.09; ctx.strokeStyle = WH; ctx.stroke();
  ctx.clip();
  ctx.fillStyle = L; ctx.beginPath(); ctx.arc(lx * r * .35, ly * r * .2, r * 0.42, 0, 7); ctx.fill();
  ctx.fillStyle = K; ctx.beginPath(); ctx.arc(lx * r * .38, ly * r * .22, r * 0.2, 0, 7); ctx.fill();
  ctx.fillStyle = WH; ctx.beginPath(); ctx.arc(lx * r * .38 - r * .12, ly * r * .22 - r * .12, r * 0.07, 0, 7); ctx.fill();
  ctx.restore();
}
function star5(ctx, x, y, r, a, col) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.beginPath();
  for (let i = 0; i < 10; i++) { const rr2 = i % 2 ? r * 0.45 : r; const an = i * Math.PI / 5 - Math.PI / 2; ctx.lineTo(Math.cos(an) * rr2, Math.sin(an) * rr2); }
  ctx.closePath(); ctx.fillStyle = col; ctx.fill(); ctx.lineWidth = r * 0.08; ctx.strokeStyle = '#222'; ctx.stroke(); ctx.restore();
}
// deliberately bad "generic" video (lives only inside its card)
function badVideo(ctx, x, y, w, h, t, rad = 18, simple = false) {
  ctx.save(); rr(ctx, x, y, w, h, rad); ctx.clip();
  const g = ctx.createLinearGradient(x, y, x + w, y + h);
  g.addColorStop(0, '#ff6f91'); g.addColorStop(.35, '#ffc75f'); g.addColorStop(.7, '#4fd1c5'); g.addColorStop(1, '#5b8def');
  ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
  if (!simple) {
    ctx.globalAlpha = 0.55 + 0.45 * Math.sin(t * 1.3);
    ctx.font = `italic ${Math.round(h * 0.13)}px "DejaVu Serif", serif`; ctx.fillStyle = '#ffffff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('Meu Vídeo', x + w / 2, y + h * 0.42);
    ctx.font = `${Math.round(h * 0.06)}px "DejaVu Serif", serif`; ctx.fillText('confira!!', x + w / 2, y + h * 0.58);
    ctx.globalAlpha = 1;
    star5(ctx, x + w * 0.2, y + h * 0.78, h * 0.09, t * 0.8, '#ffe14d');
    star5(ctx, x + w * 0.82, y + h * 0.2, h * 0.06, -t * 0.6, '#ffe14d');
  } else {
    ctx.fillStyle = 'rgba(255,255,255,0.85)'; ctx.fillRect(x + w * 0.25, y + h * 0.4, w * 0.5, h * 0.08);
    star5(ctx, x + w * 0.22, y + h * 0.75, h * 0.1, t, '#ffe14d');
  }
  ctx.restore();
}
function phone(ctx, x, y, w, h) { // returns screen rect
  ctx.save(); rr(ctx, x, y, w, h, 54); ctx.fillStyle = '#111'; ctx.fill(); ctx.lineWidth = 6; ctx.strokeStyle = '#2a2a2a'; ctx.stroke(); ctx.restore();
  return [x + 14, y + 14, w - 28, h - 28];
}
function heart(ctx, x, y, s, col) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.beginPath(); ctx.moveTo(0, 0.35); ctx.bezierCurveTo(-1, -0.3, -0.5, -1, 0, -0.45); ctx.bezierCurveTo(0.5, -1, 1, -0.3, 0, 0.35); ctx.fillStyle = col; ctx.fill(); ctx.restore(); }
function eyeIcon(ctx, x, y, s, col) { ctx.save(); ctx.translate(x, y); ctx.strokeStyle = col; ctx.lineWidth = s * 0.12; ctx.beginPath(); ctx.moveTo(-s, 0); ctx.quadraticCurveTo(0, -s * 0.9, s, 0); ctx.quadraticCurveTo(0, s * 0.9, -s, 0); ctx.stroke(); ctx.fillStyle = col; ctx.beginPath(); ctx.arc(0, 0, s * 0.3, 0, 7); ctx.fill(); ctx.restore(); }
function stampBox(ctx, s, x, y, sz, t, t0, o = {}) {
  if (t < t0) return; const k = sp(t, t0, 0.55, 22); const sc = lerp(1.7, 1, k);
  ctx.save(); ctx.translate(x, y); ctx.rotate(o.r || 0); ctx.scale(sc, sc); ctx.globalAlpha *= clamp((t - t0) / 0.05);
  const w = tw(s, sz) + sz * 0.5, h = sz * 1.45;
  rr(ctx, -w / 2, -h / 2 - sz * 0.08, w, h, 10); ctx.fillStyle = o.bg || L; ctx.fill();
  T(ctx, s, 0, sz * 0.04, sz, o.col || K);
  ctx.restore();
}
