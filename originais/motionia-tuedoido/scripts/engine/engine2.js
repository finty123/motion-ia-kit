// ===== núcleo 3D v2 =====
const DV = '#1a0636', DV2 = '#2a0d55';
const F3 = 1300;
let CAM3 = { x: 0, y: 0, z: 0, rx: 0, ry: 0, rz: 0 };
function setCam3(c) { CAM3 = Object.assign({ x: 0, y: 0, z: 0, rx: 0, ry: 0, rz: 0 }, c); }
function xf(p, o) { const s = o.s ?? 1; let q = [p[0] * s, p[1] * s, p[2] * s]; q = rot3(q, o.rx || 0, o.ry || 0, o.rz || 0); q = [q[0] + (o.x || 0), q[1] + (o.y || 0), q[2] + (o.z || 0)]; return o.parent ? xf(q, o.parent) : q; }
function view(p) { let q = [p[0] - CAM3.x, p[1] - CAM3.y, p[2] - CAM3.z]; q = rot3(q, 0, 0, -CAM3.rz); q = rot3(q, 0, -CAM3.ry, 0); q = rot3(q, -CAM3.rx, 0, 0); return q; }
function pj(p) { const z = p[2] + F3; const k = F3 / Math.max(1, z); return [W / 2 + p[0] * k, H / 2 + p[1] * k, z, k]; }
const P3 = (p, o) => pj(view(xf(p, o)));

function tri(ctx, img, x0, y0, x1, y1, x2, y2, u0, v0, u1, v1, u2, v2) {
  const cx = (x0 + x1 + x2) / 3, cy = (y0 + y1 + y2) / 3, ex = (x, y) => { const dx = x - cx, dy = y - cy, l = Math.hypot(dx, dy) || 1; return [x + dx / l * 0.9, y + dy / l * 0.9]; };
  const a0 = ex(x0, y0), a1 = ex(x1, y1), a2 = ex(x2, y2);
  const du1 = u1 - u0, dv1 = v1 - v0, du2 = u2 - u0, dv2 = v2 - v0, det = du1 * dv2 - du2 * dv1; if (!det) return;
  const dx1 = x1 - x0, dy1 = y1 - y0, dx2 = x2 - x0, dy2 = y2 - y0;
  const a = (dx1 * dv2 - dx2 * dv1) / det, b = (dy1 * dv2 - dy2 * dv1) / det, c = (dx2 * du1 - dx1 * du2) / det, d = (dy2 * du1 - dy1 * du2) / det;
  ctx.save(); ctx.beginPath(); ctx.moveTo(a0[0], a0[1]); ctx.lineTo(a1[0], a1[1]); ctx.lineTo(a2[0], a2[1]); ctx.closePath(); ctx.clip();
  ctx.transform(a, b, c, d, x0 - a * u0 - c * v0, y0 - b * u0 - d * v0); ctx.drawImage(img, 0, 0); ctx.restore();
}
// textured plane in 3D. tex = canvas/image. local size w x h (world units), lz local z offset
function plane(ctx, tex, o, N = 4, w, h, lz = 0, alpha = 1) {
  const img = tex.c || tex; w = w ?? img.width; h = h ?? img.height;
  const G = [];
  let bad = 0; for (let j = 0; j <= N; j++) for (let i = 0; i <= N; i++) { const p = P3([-w / 2 + w * i / N, -h / 2 + h * j / N, lz], o); if (p[2] < 30) { bad++; G.push(null); } else G.push(p); } if (bad === G.length) return;
  const iw = img.width, ih = img.height;
  ctx.save(); ctx.globalAlpha *= alpha;
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
    const A = G[j * (N + 1) + i], B = G[j * (N + 1) + i + 1], Cc = G[(j + 1) * (N + 1) + i + 1], D = G[(j + 1) * (N + 1) + i]; if (!A || !B || !Cc || !D) continue;
    const u0 = iw * i / N, u1 = iw * (i + 1) / N, v0 = ih * j / N, v1 = ih * (j + 1) / N;
    tri(ctx, img, A[0], A[1], B[0], B[1], Cc[0], Cc[1], u0, v0, u1, v0, u1, v1);
    tri(ctx, img, A[0], A[1], Cc[0], Cc[1], D[0], D[1], u0, v0, u1, v1, u0, v1);
  }
  ctx.restore();
}
function facing(o, w, h) { const a = P3([-w / 2, -h / 2, 0], o), b = P3([w / 2, -h / 2, 0], o), c = P3([-w / 2, h / 2, 0], o); return ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) > 0; }

// text textures (cached)
const TXC = new Map();
function TX(s, sz, col, font = 'Anton', wt = '') {
  const key = s + '|' + sz + '|' + col + '|' + font + '|' + wt; if (TXC.has(key)) return TXC.get(key);
  const t = mk(4, 4); t.x.font = `${wt} ${sz}px ${font}`; const m = t.x.measureText(s);
  const asc = m.actualBoundingBoxAscent, desc = m.actualBoundingBoxDescent, pad = Math.ceil(sz * 0.08);
  const w = Math.ceil(Math.max(m.width, m.actualBoundingBoxRight + m.actualBoundingBoxLeft) + pad * 2), h = Math.ceil(asc + desc + pad * 2);
  const c = mk(w, h); c.x.font = `${wt} ${sz}px ${font}`; c.x.fillStyle = col; c.x.textBaseline = 'alphabetic'; c.x.fillText(s, pad + (m.actualBoundingBoxLeft || 0), pad + asc);
  const r = { c: c.c, w, h }; if (TXC.size > 900) TXC.clear(); TXC.set(key, r); return r;
}
// extruded 3D text with real perspective
function text3D(ctx, s, o, op = {}) {
  const sz = op.size || 200, f = op.font || 'Anton', wt = op.wt || '';
  const face = TX(s, sz, op.face || WH, f, wt), side = TX(s, sz, op.side || '#3d1680', f, wt), sideD = TX(s, sz, op.sideD || mix(op.side || '#3d1680', '#000000', 0.6).replace(/rgb\((\d+),(\d+),(\d+)\)/, (m, r, g, b) => '#' + [r, g, b].map(v => (+v).toString(16).padStart(2, '0')).join('')), f, wt);
  const d = op.depth ?? sz * 0.16, n = op.layers ?? Math.max(3, Math.min(12, Math.round(d / 5)));
  const N = op.N ?? 2, al = op.alpha ?? 1;
  if (al <= 0) return;
  const front = facing(o, face.w, face.h);
  if (front) { for (let i = n; i >= 1; i--) plane(ctx, i > n * 0.45 ? sideD : side, o, 1, face.w, face.h, d * i / n, al); if (op.inner) op.inner(face, o); plane(ctx, face, o, N, face.w, face.h, 0, al); }
  else { plane(ctx, face, o, N, face.w, face.h, 0, al); for (let i = 1; i <= n; i++) plane(ctx, i > n * 0.45 ? sideD : side, o, 1, face.w, face.h, d * i / n, al); }
  if (op.glint !== undefined && op.glint > 0 && op.glint < 1 && front) {
    // reflexo especular: faixa de luz passando pela face
    const gk = 'glint|' + s + sz + f; let gc = TXC.get(gk);
    if (!gc) { gc = mk(face.w, face.h); TXC.set(gk, gc); }
    gc.x.setTransform(1, 0, 0, 1, 0, 0); gc.x.globalCompositeOperation = 'source-over'; gc.x.clearRect(0, 0, face.w, face.h); gc.x.drawImage(face.c, 0, 0);
    gc.x.globalCompositeOperation = 'source-in'; const gx = lerp(-face.w * 0.3, face.w * 1.3, op.glint);
    const gr = gc.x.createLinearGradient(gx - face.h * 0.5, 0, gx + face.h * 0.1, face.h); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(0.45, 'rgba(255,255,255,0)'); gr.addColorStop(0.5, 'rgba(255,255,255,1)'); gr.addColorStop(0.58, 'rgba(198,255,52,0.9)'); gr.addColorStop(0.62, 'rgba(255,255,255,0)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    gc.x.fillStyle = gr; gc.x.fillRect(0, 0, face.w, face.h);
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; plane(ctx, gc.c, o, N, face.w, face.h, -0.5, al); ctx.restore();
  }
}
function text3Dglow(ctx, s, o, op, amt, blur = 7) { if (amt <= 0.01) return; glow(ctx, g => plane(g, TX(s, op.size || 200, op.glowCol || L, op.font || 'Anton', op.wt || ''), o, 1), amt, blur); }

// word3: palavra 3D que entra com giro e IMPACTO
function W3(ctx, t, s, t0, o) {
  if (t < t0) return null;
  const k = sp(t, t0, o.zeta ?? 0.52, o.w ?? 15), fr = o.from || { z: -900, ry: 0.0, rx: 0.0, rz: 0.25 };
  const pose = { x: (o.x || 0) + (fr.x || 0) * (1 - k), y: (o.y || 0) + (fr.y || 0) * (1 - k), z: (o.z || 0) + (fr.z ?? -900) * (1 - k), rx: (o.rx || 0) + (fr.rx || 0) * (1 - k), ry: (o.ry || 0) + (fr.ry || 0) * (1 - k), rz: (o.rz || 0) + (fr.rz || 0) * (1 - k), s: o.s ?? 1 };
  let al = clamp((t - t0) / 0.04);
  if (o.out !== undefined && t > o.out) { const u = eiExp(P(t, o.out, o.out + (o.outD || 0.22))); pose.z -= u * (o.outZ ?? 1100); pose.ry += u * (o.outRy || 0); pose.y += u * (o.outY || 0); pose.x += u * (o.outX || 0); al *= 1 - u; }
  if (al <= 0) return pose;
  if (o.drift) { pose.ry += o.drift * Math.sin((t - t0) * 1.3); pose.rx += o.drift * 0.4 * Math.sin((t - t0) * 0.9); }
  text3D(ctx, s, pose, { ...o, alpha: al });
  const land = Math.exp(-Math.max(0, t - t0 - 0.05) * 5);
  if (o.glow !== 0) text3Dglow(ctx, s, pose, o, (o.glow ?? 0.25) * al + (o.flash ?? 0.9) * land * al);
  return pose;
}
// texto 2D plano com impacto (para linhas pequenas) – posicionado em 3D sem extrusão
function L3(ctx, t, s, t0, o) {
  if (t < t0) return; const k = sp(t, t0, 0.7, 16), al = clamp((t - t0) / 0.08) * (o.out !== undefined ? 1 - P(t, o.out, o.out + 0.15) : 1);
  if (al <= 0) return;
  const tx = TX(s, o.size || 48, o.col || WH, o.font || 'Inter', o.wt || '800');
  plane(ctx, tx, { x: o.x || 0, y: (o.y || 0) + 40 * (1 - k), z: o.z || 0, rx: (o.rx || 0) + 0.6 * (1 - k), ry: o.ry || 0, rz: o.rz || 0 }, 1, undefined, undefined, 0, al);
}
// caixa 3D com a câmera global
function box3(ctx, size, o, faceStyle) {
  const [w, h, d] = size.map(v => v / 2);
  const V0 = [[-w, -h, -d], [w, -h, -d], [w, h, -d], [-w, h, -d], [-w, -h, d], [w, -h, d], [w, h, d], [-w, h, d]];
  const Vw = V0.map(p => view(xf(p, o))); const Pp = Vw.map(pj);
  if (Pp.some(p => p[2] < 30)) return;
  const F = [[0, 1, 2, 3, size[0], size[1]], [5, 4, 7, 6, size[0], size[1]], [4, 0, 3, 7, size[2], size[1]], [1, 5, 6, 2, size[2], size[1]], [4, 5, 1, 0, size[0], size[2]], [3, 2, 6, 7, size[0], size[2]]];
  const list = [];
  F.forEach((fc, i) => {
    const a = Pp[fc[0]], b = Pp[fc[1]], c = Pp[fc[3]];
    const cr = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]);
    if (cr <= 0) return;
    const A = Vw[fc[0]], B = Vw[fc[1]], Cv = Vw[fc[3]]; const u = [B[0] - A[0], B[1] - A[1], B[2] - A[2]], v = [Cv[0] - A[0], Cv[1] - A[1], Cv[2] - A[2]];
    const n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]], nl = Math.hypot(...n) || 1;
    const light = clamp(0.3 + 0.7 * Math.max(0, (-n[0] * 0.35 - n[1] * 0.55 - n[2] * 0.75) / nl));
    const zc = [0, 1, 2, 3].reduce((s2, k) => s2 + Vw[fc[k]][2], 0) / 4;
    list.push({ i, z: zc, fc, light });
  });
  list.sort((p, q) => q.z - p.z);
  for (const it of list) {
    const pts = it.fc.slice(0, 4).map(k => Pp[k]); const st = faceStyle(it.i, it.light);
    ctx.save(); ctx.beginPath(); pts.forEach((p, k) => k ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath();
    if (st.fill) { ctx.fillStyle = st.fill; ctx.fill(); }
    if (st.stroke) { ctx.strokeStyle = st.stroke; ctx.lineWidth = st.lw || 2; ctx.lineJoin = 'round'; ctx.stroke(); }
    if (st.draw) { ctx.clip(); const fw = it.fc[4], fh = it.fc[5], p0 = pts[0], p1 = pts[1], p3 = pts[3]; ctx.transform((p1[0] - p0[0]) / fw, (p1[1] - p0[1]) / fw, (p3[0] - p0[0]) / fh, (p3[1] - p0[1]) / fh, p0[0], p0[1]); st.draw(ctx, fw, fh, it.light); }
    ctx.restore();
  }
}
// desfoque gaussiano de uma camada (renderiza em 1/4, desfoca, sobe)
const BLA = mk(480, 270), BLB = mk(480, 270);
function blurDraw(ctx, fn, px = 4, amt = 1) {
  if (NOPOST || ctx !== X) { fn(ctx); return; }
  const g = BLA.x; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, 480, 270); g.setTransform(.25, 0, 0, .25, 0, 0); camApply(g, CUR_T); fn(g);
  const h = BLB.x; h.setTransform(1, 0, 0, 1, 0, 0); h.clearRect(0, 0, 480, 270); h.filter = `blur(${px}px)`; h.drawImage(BLA.c, 0, 0); h.filter = 'none';
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = amt; X.drawImage(BLB.c, 0, 0, W, H); X.restore();
}
function bgv(ctx, base, glowCol = V, ga = 0.45, gx = W / 2, gy = H / 2) { bg(ctx, base); ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); radial(ctx, gx, gy, 1100, glowCol, ga); ctx.restore(); }
function ring(ctx, t, t0, col = L, sp2 = 2200, wmax = 36, dur = 0.8, x = W / 2, y = H / 2) { const d = t - t0; if (d < 0 || d > dur) return; ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.strokeStyle = rgba(col, 1 - d / dur); ctx.lineWidth = wmax * (1 - d / dur) + 2; ctx.beginPath(); ctx.arc(x, y, 40 + d * sp2, 0, 7); ctx.stroke(); ctx.restore(); }
// partículas bokeh desfocadas ao fundo
const BOKEH = (() => { const r = mulberry32(55), a = []; for (let i = 0; i < 40; i++) a.push({ x: r() * W, y: r() * H, s: 6 + r() * 26, d: r(), c: r() < .5 ? L : V, ph: r() * 6 }); return a; })();
function bokeh(ctx, t, amt = 1) { blurDraw(ctx, c => { c.save(); c.setTransform(c.getTransform()); for (const b of BOKEH) { const x = (b.x + t * 40 * (b.d - .5) * 3 + W) % W, y = b.y + Math.sin(t + b.ph) * 30; c.fillStyle = rgba(b.c, 0.35 * amt); c.beginPath(); c.arc(x, y, b.s, 0, 7); c.fill(); } c.restore(); }, 5, 1); }
