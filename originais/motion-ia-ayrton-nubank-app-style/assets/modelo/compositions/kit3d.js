// Kit 3D compartilhado pelas cenas: palco com luz de estúdio, moeda roxa e iPhone realistas,
// e as telas do app desenhadas em canvas (texturas da tela do celular).
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";
export { THREE };

export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const seg = (t, a, b) => clamp((t - a) / (b - a));
export const ease = {
  outExpo: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
  outQuart: (x) => 1 - Math.pow(1 - x, 4),
  inOut: (x) => (x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2),
  inCubic: (x) => x * x * x,
  // mola amortecida (0.75) em forma fechada: qualquer quadro sai sozinho
  spring: (x) => (x >= 1 ? 1 : 1 - Math.exp(-6 * x) * Math.cos(9 * x)),
};
export const lerp = (a, b, k) => a + (b - a) * k;

export const IMG = {};
function loadImg(key, src) {
  return new Promise((res) => { const im = new Image(); im.onload = () => { IMG[key] = im; res(); }; im.onerror = () => res(); im.src = src; });
}
export async function ready() {
  if (!IMG.nu) await loadImg("nu", "assets/nu-branco.png");
  await Promise.all(
    ["700 100px Outfit", "600 100px Outfit", "500 100px Outfit", "400 40px Inter", "600 40px Inter", "700 40px Inter"].map((f) => document.fonts.load(f)),
  );
}

// ------------------------------------------------------------------ palco
// Ambiente de estúdio: domo neutro + softboxes em faixa; é ele que dá o reflexo realista no metal e no vidro.
function studioEnv(renderer) {
  const s = new THREE.Scene();
  s.add(new THREE.Mesh(new THREE.SphereGeometry(20, 32, 16), new THREE.MeshBasicMaterial({ side: THREE.BackSide, color: 0x6f6a7c })));
  const box = (w, h, color, k, pos) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(k), side: THREE.DoubleSide }));
    m.position.set(...pos);
    m.lookAt(0, 0, 0);
    s.add(m);
  };
  box(12, 3, "#fff3e8", 7, [0, 9, 5]); // faixa principal em cima, quente
  box(2.2, 14, "#ece6ff", 5, [-10, 2, 3]); // faixa lateral fria
  box(2.2, 14, "#ffffff", 4, [10, 1, -4]); // recorte (rim)
  box(16, 5, "#cdb6ff", 1.4, [0, -7, 5]); // rebatida lilás do chão
  const pm = new THREE.PMREMGenerator(renderer);
  const tex = pm.fromScene(s, 0.03).texture;
  pm.dispose();
  return tex;
}

export function makeStage(canvas, { fov = 30, w = 1920, h = 1080, shadow = true, exposure = 1 } = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(w, h, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = exposure;
  renderer.shadowMap.enabled = shadow;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0x000000, 0);
  const scene = new THREE.Scene();
  scene.environment = studioEnv(renderer);
  const camera = new THREE.PerspectiveCamera(fov, w / h, 0.05, 100);
  camera.position.set(0, 0, 10);
  const key = new THREE.DirectionalLight(0xfff0e4, 1.5);
  key.position.set(3, 6, 5);
  key.castShadow = shadow;
  key.shadow.mapSize.set(2048, 2048);
  Object.assign(key.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 0.5, far: 30 });
  key.shadow.bias = -0.0004;
  scene.add(key, key.target);
  const fill = new THREE.HemisphereLight(0xf4eeff, 0xd6c8ff, 0.35);
  scene.add(fill);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: 0.16 }));
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  ground.visible = false;
  scene.add(ground);
  return { renderer, scene, camera, key, fill, ground, render: () => renderer.render(scene, camera) };
}

// ------------------------------------------------------------------ moeda roxa
// Face em grade polar deslocada por um mapa de altura (borda alta, campo baixo, cifrão em relevo);
// normais calculadas da geometria, então o relevo pega luz de verdade. Borda serrilhada.
export function makeCoin({ R = 1, T = 0.16, color = "#7a2bd3", glyph = "$" } = {}) {
  const N = 512, c = document.createElement("canvas");
  c.width = c.height = N;
  const g = c.getContext("2d"), m = N / 2;
  g.fillStyle = "#000"; g.fillRect(0, 0, N, N);
  g.fillStyle = "#fff"; g.beginPath(); g.arc(m, m, m, 0, 7); g.fill();
  g.filter = "blur(4px)";
  g.fillStyle = "#262626"; g.beginPath(); g.arc(m, m, m * 0.83, 0, 7); g.fill();
  g.strokeStyle = "#4a4a4a"; g.lineWidth = 6; g.beginPath(); g.arc(m, m, m * 0.73, 0, 7); g.stroke();
  g.filter = "blur(5px)";
  g.fillStyle = "#ececec"; g.font = "700 310px Outfit"; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillText(glyph, m, m + 14);
  g.filter = "none";
  const img = g.getImageData(0, 0, N, N).data;
  const H = (u, v) => {
    const x = clamp((u * 0.5 + 0.5) * (N - 1), 0, N - 1), y = clamp((0.5 - v * 0.5) * (N - 1), 0, N - 1);
    const x0 = Math.floor(x), y0 = Math.floor(y), x1 = Math.min(N - 1, x0 + 1), y1 = Math.min(N - 1, y0 + 1), fx = x - x0, fy = y - y0;
    const p = (xx, yy) => img[(yy * N + xx) * 4] / 255;
    return (p(x0, y0) * (1 - fx) + p(x1, y0) * fx) * (1 - fy) + (p(x0, y1) * (1 - fx) + p(x1, y1) * fx) * fy;
  };
  const NR = 150, NS = 256, relief = 0.05 * R;
  function face(sign) {
    const pos = [], idx = [];
    for (let i = 0; i <= NR; i++) {
      const r = i / NR, rr = i === NR ? 1.007 : r;
      for (let j = 0; j <= NS; j++) {
        const a = (j / NS) * Math.PI * 2, u = r * Math.cos(a), v = r * Math.sin(a);
        pos.push(rr * Math.cos(a) * R, rr * Math.sin(a) * R, sign * (T / 2 + H(sign > 0 ? u : -u, v) * relief));
      }
    }
    for (let i = 0; i < NR; i++)
      for (let j = 0; j < NS; j++) {
        const a = i * (NS + 1) + j, b = a + NS + 1;
        if (sign > 0) idx.push(a, b, a + 1, b, b + 1, a + 1);
        else idx.push(a, a + 1, b, b, a + 1, b + 1);
      }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
    geo.setIndex(idx);
    geo.computeVertexNormals();
    return geo;
  }
  const eg = new THREE.CylinderGeometry(R, R, T + 2 * relief, 720, 1, true);
  const p = eg.attributes.position;
  for (let k = 0; k < p.count; k++) {
    const x = p.getX(k), z = p.getZ(k), s = 1 + 0.006 * Math.cos(Math.atan2(z, x) * 180);
    p.setX(k, x * s); p.setZ(k, z * s);
  }
  eg.computeVertexNormals();
  eg.rotateX(Math.PI / 2);
  const mat = new THREE.MeshPhysicalMaterial({ color, metalness: 1, roughness: 0.3, clearcoat: 0.7, clearcoatRoughness: 0.12 });
  const edgeMat = mat.clone();
  edgeMat.roughness = 0.4;
  const grp = new THREE.Group();
  for (const mesh of [new THREE.Mesh(face(1), mat), new THREE.Mesh(face(-1), mat), new THREE.Mesh(eg, edgeMat)]) {
    mesh.castShadow = true;
    grp.add(mesh);
  }
  return grp;
}

// ------------------------------------------------------------------ iPhone
function rrShape(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y); s.absarc(x + w - r, y + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x + w, y + h - r); s.absarc(x + w - r, y + h - r, r, 0, Math.PI / 2, false);
  s.lineTo(x + r, y + h); s.absarc(x + r, y + h - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x, y + r); s.absarc(x + r, y + r, r, Math.PI, Math.PI * 1.5, false);
  return s;
}
function shapeGeo(w, h, r, uv = false) {
  const geo = new THREE.ShapeGeometry(rrShape(w, h, r), 48);
  if (uv) {
    const p = geo.attributes.position, a = geo.attributes.uv;
    for (let i = 0; i < p.count; i++) a.setXY(i, (p.getX(i) + w / 2) / w, (p.getY(i) + h / 2) / h);
  }
  return geo;
}

export const SCREEN = { w: 600, h: 1278 };

export function makePhone({ frame = "#3e3448", backColor = "#4a3f56" } = {}) {
  const W = 0.715, H = 1.466, D = 0.0825, rad = 0.115, bev = 0.014;
  const grp = new THREE.Group();
  const metal = new THREE.MeshPhysicalMaterial({ color: frame, metalness: 1, roughness: 0.3, clearcoat: 0.4, clearcoatRoughness: 0.2 });
  const body = new THREE.Mesh(
    new THREE.ExtrudeGeometry(rrShape(W - 2 * bev, H - 2 * bev, rad - bev), { depth: D - 2 * bev, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 8, curveSegments: 48 }),
    metal,
  );
  body.geometry.translate(0, 0, -(D - 2 * bev) / 2);
  body.castShadow = true;
  grp.add(body);
  const z = D / 2 + bev * 0.0;
  const glass = new THREE.Mesh(shapeGeo(W - 0.012, H - 0.012, rad - 0.006), new THREE.MeshPhysicalMaterial({ color: "#040406", roughness: 0.05, clearcoat: 1, clearcoatRoughness: 0.03 }));
  glass.position.z = z + 0.0006;
  grp.add(glass);
  const cv = document.createElement("canvas");
  cv.width = SCREEN.w; cv.height = SCREEN.h;
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  const sw = W - 0.052, sh = H - 0.052;
  const screen = new THREE.Mesh(shapeGeo(sw, sh, rad - 0.026, true), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false }));
  screen.position.z = z + 0.0012;
  grp.add(screen);
  // camada de reflexo do vidro: só o especular soma por cima da tela
  const refl = new THREE.Mesh(
    shapeGeo(W - 0.012, H - 0.012, rad - 0.006),
    new THREE.MeshPhysicalMaterial({ color: 0x000000, roughness: 0.07, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, envMapIntensity: 1.3 }),
  );
  refl.position.z = z + 0.0018;
  grp.add(refl);
  const back = new THREE.Mesh(shapeGeo(W - 0.012, H - 0.012, rad - 0.006), new THREE.MeshPhysicalMaterial({ color: backColor, roughness: 0.55, metalness: 0.15 }));
  back.rotation.y = Math.PI;
  back.position.z = -z - 0.0006;
  grp.add(back);
  // bloco de câmeras (canto superior direito visto de frente = esquerdo visto de trás)
  const bump = new THREE.Mesh(
    new THREE.ExtrudeGeometry(rrShape(0.31, 0.31, 0.075), { depth: 0.008, bevelEnabled: true, bevelThickness: 0.004, bevelSize: 0.004, bevelSegments: 4, curveSegments: 32 }),
    new THREE.MeshPhysicalMaterial({ color: backColor, roughness: 0.25, metalness: 0.1, clearcoat: 1 }),
  );
  const bx = W / 2 - 0.035 - 0.155, by = H / 2 - 0.035 - 0.155;
  bump.position.set(bx, by, -z - 0.012);
  grp.add(bump);
  const ringG = new THREE.CylinderGeometry(0.06, 0.06, 0.022, 48).rotateX(Math.PI / 2);
  const lensG = new THREE.CylinderGeometry(0.046, 0.046, 0.024, 48).rotateX(Math.PI / 2);
  const lensM = new THREE.MeshPhysicalMaterial({ color: "#05040a", roughness: 0.04, clearcoat: 1, iridescence: 0.6 });
  for (const [dx, dy] of [[0.072, 0.072], [0.072, -0.072], [-0.07, 0]]) {
    const r = new THREE.Mesh(ringG, metal); r.position.set(bx + dx, by + dy, -z - 0.026); grp.add(r);
    const l = new THREE.Mesh(lensG, lensM); l.position.set(bx + dx, by + dy, -z - 0.027); grp.add(l);
  }
  const btn = (w, h, x, y) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.03), metal); b.position.set(x, y, 0); grp.add(b); };
  btn(0.012, 0.17, W / 2 + 0.003, 0.24);
  btn(0.012, 0.11, -W / 2 - 0.003, 0.33);
  btn(0.012, 0.11, -W / 2 - 0.003, 0.19);
  btn(0.012, 0.06, -W / 2 - 0.003, 0.47);
  return { group: grp, canvas: cv, ctx: cv.getContext("2d"), texture: tex, update: () => (tex.needsUpdate = true) };
}

// ------------------------------------------------------------------ telas do app (canvas 600 x 1278)
export const NU = { roxo: "#820AD1", roxoEsc: "#4A0A8C", lilas: "#C9A3FF", ink: "#17121F", cinza: "#F2F0F5" };

function rr(g, x, y, w, h, r) {
  g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath();
}
function statusBar(g, color, time = "9:41") {
  g.fillStyle = color; g.font = "600 30px Inter"; g.textAlign = "left"; g.textBaseline = "middle";
  g.fillText(time, 66, 52);
  // sinal, wi-fi e bateria simplificados
  g.fillRect(452, 46, 6, 14); g.fillRect(462, 42, 6, 18); g.fillRect(472, 38, 6, 22);
  rr(g, 492, 38, 46, 22, 6); g.strokeStyle = color; g.lineWidth = 2.5; g.stroke(); rr(g, 496, 42, 34, 14, 3); g.fill();
  g.fillStyle = "#000"; rr(g, 205, 22, 190, 56, 28); g.fill(); // ilha dinâmica
}
const money = (v) => "R$ " + v.toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, ".");
export { money };

// Tela inicial (redesenhada da referência que o Ayrton mandou)
export function drawHome(g, { saldo = 8742.36, nome = "Ana" } = {}) {
  const { w, h } = SCREEN;
  g.fillStyle = "#fff"; g.fillRect(0, 0, w, h);
  g.fillStyle = NU.roxo; g.fillRect(0, 0, w, 330);
  statusBar(g, "#fff");
  g.fillStyle = "rgba(255,255,255,.22)"; g.beginPath(); g.arc(86, 150, 38, 0, 7); g.fill();
  g.strokeStyle = "#fff"; g.lineWidth = 3; g.beginPath(); g.arc(86, 142, 11, 0, 7); g.stroke(); g.beginPath(); g.arc(86, 172, 18, Math.PI * 1.1, Math.PI * 1.9); g.stroke();
  for (const x of [408, 466, 524]) { g.strokeStyle = "#fff"; g.lineWidth = 3; g.beginPath(); g.arc(x, 150, 15, 0, 7); g.stroke(); }
  g.fillStyle = "#fff"; g.font = "600 36px Inter"; g.textAlign = "left"; g.fillText(`Olá, ${nome}`, 50, 250);
  g.fillStyle = "#fff"; rr(g, 0, 300, w, h - 300, 34); g.fill();
  g.fillStyle = NU.ink; g.font = "600 30px Inter"; g.fillText("Conta  ›", 50, 380);
  g.font = "700 50px Inter"; g.fillText(money(saldo), 50, 448);
  g.fillStyle = NU.cinza; rr(g, 50, 490, 290, 46, 23); g.fill();
  g.fillStyle = "#1db954"; g.beginPath(); g.arc(76, 513, 8, 0, 7); g.fill();
  g.fillStyle = NU.ink; g.font = "500 22px Inter"; g.fillText("Rendendo todo dia  ›", 94, 514);
  const items = [["Pix", "◆"], ["Pagar", "▥"], ["Transferir", "⇄"], ["Caixinhas", "◎"], ["Cartão", "▭"], ["Investir", "▮"], ["Recarga", "▯"], ["Mais", "•••"]];
  items.forEach(([lab, ic], i) => {
    const cx = 100 + (i % 4) * 133, cy = 630 + Math.floor(i / 4) * 190;
    g.fillStyle = NU.cinza; g.beginPath(); g.arc(cx, cy, 50, 0, 7); g.fill();
    g.fillStyle = NU.ink; g.font = "600 34px Inter"; g.textAlign = "center"; g.fillText(ic, cx, cy + 2);
    g.font = "500 22px Inter"; g.fillText(lab, cx, cy + 82);
  });
  g.textAlign = "left";
  g.fillStyle = NU.cinza; rr(g, 50, 1030, 500, 90, 22); g.fill();
  g.fillStyle = NU.ink; g.font = "600 28px Inter"; g.fillText("▭   Meus cartões", 80, 1076);
  g.fillStyle = "rgba(0,0,0,.85)"; rr(g, 200, h - 30, 200, 9, 5); g.fill();
}

// Caixinha recém-criada, saldo subindo
export function drawCaixinha(g, { valor = 0, prog = 0, nome = "Minha caixinha" } = {}) {
  const { w, h } = SCREEN;
  g.fillStyle = "#fff"; g.fillRect(0, 0, w, h);
  statusBar(g, NU.ink);
  g.fillStyle = NU.ink; g.font = "600 34px Inter"; g.textAlign = "left"; g.fillText("‹", 50, 150);
  g.font = "700 46px Inter"; g.fillText(nome, 50, 250);
  const gr = g.createLinearGradient(0, 300, w, 640); gr.addColorStop(0, NU.roxoEsc); gr.addColorStop(1, "#A54BFF");
  g.fillStyle = gr; rr(g, 40, 300, w - 80, 340, 36); g.fill();
  g.fillStyle = "rgba(255,255,255,.75)"; g.font = "500 26px Inter"; g.fillText("Saldo guardado", 80, 370);
  g.fillStyle = "#fff"; g.font = "700 62px Inter"; g.fillText(money(valor), 80, 450);
  g.fillStyle = "rgba(255,255,255,.2)"; rr(g, 80, 510, w - 160, 16, 8); g.fill();
  g.fillStyle = "#fff"; rr(g, 80, 510, Math.max(16, (w - 160) * prog), 16, 8); g.fill();
  g.fillStyle = "rgba(255,255,255,.85)"; g.font = "500 24px Inter"; g.fillText(`Meta: viagem · ${Math.round(prog * 100)}%`, 80, 580);
  g.fillStyle = NU.cinza; rr(g, 40, 690, w - 80, 70, 35); g.fill();
  g.fillStyle = "#1db954"; g.beginPath(); g.arc(80, 725, 9, 0, 7); g.fill();
  g.fillStyle = NU.ink; g.font = "600 26px Inter"; g.fillText("Rendendo todo dia", 104, 726);
  const rows = [["Hoje", "+ R$ 0,47"], ["Ontem", "+ R$ 0,46"], ["Seg", "+ R$ 0,46"]];
  rows.forEach(([a, b], i) => {
    const y = 840 + i * 92;
    g.fillStyle = "#8a8494"; g.font = "500 26px Inter"; g.fillText(a, 50, y);
    g.fillStyle = "#1a9e4a"; g.textAlign = "right"; g.font = "600 28px Inter"; g.fillText(b, w - 50, y); g.textAlign = "left";
    g.fillStyle = "#ece9f0"; g.fillRect(50, y + 36, w - 100, 2);
  });
  g.fillStyle = NU.roxo; rr(g, 40, h - 170, w - 80, 96, 48); g.fill();
  g.fillStyle = "#fff"; g.font = "600 30px Inter"; g.textAlign = "center"; g.fillText("Guardar dinheiro", w / 2, h - 121); g.textAlign = "left";
  g.fillStyle = "rgba(0,0,0,.85)"; rr(g, 200, h - 30, 200, 9, 5); g.fill();
}

// Tela de bloqueio: dia, noite ou fim de semana (k: 0 dia → 1 noite)
export function drawLock(g, { hora = "09:41", data = "quinta-feira, 23 de outubro", k = 0, notif = "Seu dinheiro rendeu R$ 0,47 hoje" } = {}) {
  const { w, h } = SCREEN;
  const top = lerpColor("#B58CFF", "#1B0B3A", k), bot = lerpColor("#F3D9FF", "#4A0A8C", k);
  const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, top); gr.addColorStop(1, bot);
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  statusBar(g, "#fff", "");
  g.fillStyle = "#fff"; g.textAlign = "center"; g.font = "500 30px Inter"; g.fillText(data, w / 2, 200);
  g.font = "600 170px Outfit"; g.fillText(hora, w / 2, 330);
  g.fillStyle = `rgba(255,255,255,${0.55 - 0.25 * k})`; rr(g, 34, 470, w - 68, 130, 34); g.fill();
  g.fillStyle = NU.roxo; rr(g, 58, 500, 70, 70, 18); g.fill();
  g.fillStyle = "#fff"; g.font = "700 36px Outfit"; g.fillText("$", 93, 537);
  g.textAlign = "left"; g.fillStyle = k > 0.5 ? "#fff" : NU.ink; g.font = "700 26px Inter"; g.fillText("Nubank", 148, 518);
  g.font = "500 24px Inter"; g.fillText(notif, 148, 556);
  g.fillStyle = "rgba(255,255,255,.9)"; rr(g, 200, h - 30, 200, 9, 5); g.fill();
}

// "No automático" com toggle (ponte entre a cena da lista e a do celular)
export function drawAuto(g, { on = 1 } = {}) {
  const { w, h } = SCREEN;
  g.fillStyle = "#fff"; g.fillRect(0, 0, w, h);
  statusBar(g, NU.ink);
  g.fillStyle = NU.ink; g.font = "700 46px Inter"; g.textAlign = "left"; g.fillText("Caixinhas", 50, 210);
  const rows = ["Guardar todo dia", "Render no automático", "Arredondar compras"];
  rows.forEach((r, i) => {
    const y = 300 + i * 130;
    g.fillStyle = NU.cinza; rr(g, 40, y, w - 80, 104, 28); g.fill();
    g.fillStyle = NU.ink; g.font = "600 28px Inter"; g.fillText(r, 70, y + 54);
    const kk = i === 1 ? on : 1;
    g.fillStyle = lerpColor("#d4d0da", NU.roxo, kk); rr(g, w - 170, y + 27, 100, 50, 25); g.fill();
    g.fillStyle = "#fff"; g.beginPath(); g.arc(w - 145 + 50 * kk, y + 52, 21, 0, 7); g.fill();
  });
  g.fillStyle = "rgba(0,0,0,.85)"; rr(g, 200, h - 30, 200, 9, 5); g.fill();
}

export function lerpColor(a, b, k) {
  const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
  const c = [16, 8, 0].map((s) => Math.round(lerp((pa >> s) & 255, (pb >> s) & 255, clamp(k))));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
