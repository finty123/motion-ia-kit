// Extras do kit 3D: logo "nu", tela do app no estilo da foto da mão, caixinha roxa, escudo e moeda leve.
import { THREE, IMG, NU, SCREEN, money } from "./kit3d.js";

function rr(g, x, y, w, h, r) {
  g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath();
}
function rrShape(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y); s.absarc(x + w - r, y + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x + w, y + h - r); s.absarc(x + w - r, y + h - r, r, 0, Math.PI / 2, false);
  s.lineTo(x + r, y + h); s.absarc(x + r, y + h - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x, y + r); s.absarc(x + r, y + r, r, Math.PI, Math.PI * 1.5, false);
  return s;
}

// Logo "nu" (PNG branco do Ayrton) desenhado em canvas, com cor opcional
export function drawNu(g, x, y, h, color = "#fff") {
  const im = IMG.nu; if (!im) return;
  const w = (h * im.width) / im.height;
  if (color === "#fff") { g.drawImage(im, x, y, w, h); return; }
  const c = document.createElement("canvas"); c.width = Math.ceil(w); c.height = Math.ceil(h);
  const k = c.getContext("2d"); k.drawImage(im, 0, 0, w, h); k.globalCompositeOperation = "source-in"; k.fillStyle = color; k.fillRect(0, 0, w, h);
  g.drawImage(c, x, y);
}

function statusBar(g, color) {
  g.fillStyle = color; g.font = "600 30px Inter"; g.textAlign = "left"; g.textBaseline = "middle";
  g.fillText("9:41", 66, 52);
  g.fillRect(452, 46, 6, 14); g.fillRect(462, 42, 6, 18); g.fillRect(472, 38, 6, 22);
  rr(g, 492, 38, 46, 22, 6); g.strokeStyle = color; g.lineWidth = 2.5; g.stroke(); rr(g, 496, 42, 34, 14, 3); g.fill();
  g.fillStyle = "#000"; rr(g, 205, 22, 190, 56, 28); g.fill();
}

// Tela inicial no estilo da foto da mão: header roxo com logo, card da conta, Pix/Pagar/Transferir, acesso rápido, abas
export function drawHome2(g, { saldo = 2450 } = {}) {
  const { w, h } = SCREEN;
  g.fillStyle = "#f7f6f9"; g.fillRect(0, 0, w, h);
  g.fillStyle = NU.roxo; g.fillRect(0, 0, w, 330);
  statusBar(g, "#fff");
  drawNu(g, 48, 118, 46);
  g.strokeStyle = "#fff"; g.lineWidth = 3.5;
  g.beginPath(); g.arc(470, 140, 14, Math.PI, 0); g.lineTo(484, 156); g.lineTo(456, 156); g.closePath(); g.stroke();
  g.beginPath(); g.arc(534, 142, 17, 0, 7); g.stroke();
  g.fillStyle = "#ff3b5c"; g.beginPath(); g.arc(548, 126, 8, 0, 7); g.fill();
  const gr = g.createLinearGradient(30, 210, 560, 470); gr.addColorStop(0, "#9a2ff0"); gr.addColorStop(1, "#7a0cc9");
  g.fillStyle = gr; rr(g, 30, 205, 520, 268, 34); g.fill();
  g.fillStyle = "rgba(210,190,235,.55)"; rr(g, 568, 225, 60, 230, 26); g.fill();
  g.fillStyle = "rgba(255,255,255,.85)"; g.font = "500 26px Inter"; g.textAlign = "left"; g.textBaseline = "middle"; g.fillText("Conta", 66, 258);
  g.fillStyle = "#fff"; g.font = "700 52px Inter"; g.fillText(money(saldo), 66, 322);
  g.fillStyle = "rgba(255,255,255,.2)"; g.beginPath(); g.arc(505, 258, 18, 0, 7); g.fill();
  g.globalAlpha = 0.9; drawNu(g, 66, 405, 36); g.globalAlpha = 1;
  g.fillStyle = "#fff"; g.font = "500 24px Inter"; g.fillText("nubank", 140, 424); g.fillText("›", 500, 424);
  [0, 1, 2, 3].forEach((i) => { g.fillStyle = i === 0 ? NU.ink : "#c9c3d1"; g.beginPath(); g.arc(270 + i * 20, 505, 5, 0, 7); g.fill(); });
  [["Pix", 0], ["Pagar", 1], ["Transferir", 0]].forEach(([lab, on], i) => {
    const cx = 130 + i * 170, cy = 610;
    g.fillStyle = on ? NU.roxo : "#ebe8ef"; g.beginPath(); g.arc(cx, cy, 58, 0, 7); g.fill();
    g.fillStyle = on ? "#fff" : NU.ink; g.font = "600 38px Inter"; g.textAlign = "center"; g.fillText(i === 0 ? "◆" : i === 1 ? "▤" : "⇄", cx, cy + 2);
    g.fillStyle = NU.ink; g.font = "600 28px Inter"; g.fillText(lab, cx, cy + 96);
  });
  g.textAlign = "left"; g.fillStyle = NU.ink; g.font = "700 38px Inter"; g.fillText("Acesso rápido", 50, 800); g.fillText("→", 520, 800);
  g.fillStyle = "#fff"; rr(g, 40, 850, 250, 230, 26); g.fill(); g.strokeStyle = "#e3dfe8"; g.lineWidth = 2; g.stroke();
  g.fillStyle = "#32bcad"; g.font = "700 34px Inter"; g.fillText("pix", 70, 905);
  g.fillStyle = NU.ink; g.font = "500 26px Inter"; g.fillText("Transferir", 70, 990); g.fillText("com Pix", 70, 1026);
  g.fillStyle = "#e9dcff"; rr(g, 310, 850, 250, 230, 26); g.fill();
  g.fillStyle = NU.ink; for (let i = 0; i < 26; i++) g.fillRect(340 + i * 7.4, 890, i % 3 === 0 ? 5 : 2.5, 70);
  g.font = "500 26px Inter"; g.fillText("Pagar boleto", 340, 1010);
  g.fillStyle = "#fff"; g.fillRect(0, 1120, w, h - 1120); g.fillStyle = "#ece9f0"; g.fillRect(0, 1120, w, 2);
  ["Início", "nu", "Buscar", "Pix", "Perfil"].forEach((lab, i) => {
    const cx = 64 + i * 118, col = i === 0 ? NU.roxo : "#6c6578";
    if (lab === "nu") drawNu(g, cx - 25, 1148, 28, col);
    else { g.fillStyle = col; g.strokeStyle = col; g.lineWidth = 3; g.beginPath(); g.arc(cx, 1162, 14, 0, 7); i === 0 ? g.fill() : g.stroke(); }
    g.fillStyle = col; g.font = "500 21px Inter"; g.textAlign = "center"; g.fillText(lab, cx, 1210);
  });
  g.textAlign = "left";
  g.fillStyle = "rgba(0,0,0,.85)"; rr(g, 200, h - 30, 200, 9, 5); g.fill();
}

// ------------------------------------------------------------------ objetos 3D
export const plastic = (color = "#7a1fd6") =>
  new THREE.MeshPhysicalMaterial({ color, roughness: 0.26, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.08, sheen: 0.6, sheenColor: new THREE.Color("#e2c6ff"), sheenRoughness: 0.4 });

// Caixinha roxa: corpo arredondado, tampa com dobradiça atrás e fenda de moeda, logo na frente
export function makeBox({ W = 2.4, H = 1.5, D = 1.7 } = {}) {
  const grp = new THREE.Group(), r = 0.32, bev = 0.12;
  const mat = plastic();
  const body = new THREE.Mesh(new THREE.ExtrudeGeometry(rrShape(W - 2 * bev, D - 2 * bev, r - 0.05), { depth: H - 2 * bev, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 10, curveSegments: 40 }), mat);
  body.geometry.rotateX(-Math.PI / 2); body.geometry.translate(0, bev, 0);
  body.castShadow = true; grp.add(body);
  const hinge = new THREE.Group(); hinge.position.set(0, H + 0.004, -D / 2); grp.add(hinge);
  const lidH = 0.26, lb = 0.08;
  const lid = new THREE.Mesh(new THREE.ExtrudeGeometry(rrShape(W + 0.04 - 2 * lb, D + 0.04 - 2 * lb, r - 0.02), { depth: lidH - 2 * lb, bevelEnabled: true, bevelThickness: lb, bevelSize: lb, bevelSegments: 8, curveSegments: 40 }), plastic("#8a2be2"));
  lid.geometry.rotateX(-Math.PI / 2); lid.geometry.translate(0, lb, D / 2);
  lid.castShadow = true; hinge.add(lid);
  const slot = new THREE.Mesh(new THREE.ShapeGeometry(rrShape(0.95, 0.14, 0.07), 16), new THREE.MeshPhysicalMaterial({ color: "#1a0533", roughness: 0.6 }));
  slot.rotation.x = -Math.PI / 2; slot.position.set(0, lidH + 0.002, D / 2); hinge.add(slot);
  if (IMG.nu) {
    const c = document.createElement("canvas"); c.width = 512; c.height = 288; drawNu(c.getContext("2d"), 0, 0, 286);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const logo = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 0.534), new THREE.MeshPhysicalMaterial({ map: t, transparent: true, roughness: 0.3, clearcoat: 1, emissive: "#ffffff", emissiveIntensity: 0.25, emissiveMap: t }));
    logo.position.set(0, H * 0.5, D / 2 + 0.003); grp.add(logo);
  }
  return { group: grp, hinge, mat };
}

// Escudo roxo com check branco (protegendo)
export function makeShield() {
  const s = new THREE.Shape();
  s.moveTo(0, 1.05); s.bezierCurveTo(0.35, 0.86, 0.62, 0.82, 0.86, 0.84); s.lineTo(0.86, 0.1);
  s.bezierCurveTo(0.86, -0.55, 0.38, -0.92, 0, -1.1); s.bezierCurveTo(-0.38, -0.92, -0.86, -0.55, -0.86, 0.1);
  s.lineTo(-0.86, 0.84); s.bezierCurveTo(-0.62, 0.82, -0.35, 0.86, 0, 1.05);
  const grp = new THREE.Group();
  const sh = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 0.22, bevelEnabled: true, bevelThickness: 0.1, bevelSize: 0.08, bevelSegments: 10, curveSegments: 40 }), plastic());
  sh.geometry.translate(0, 0, -0.11); sh.castShadow = true; grp.add(sh);
  const ck = new THREE.Shape(); ck.moveTo(-0.42, 0.02); ck.lineTo(-0.27, 0.17); ck.lineTo(-0.1, 0.0); ck.lineTo(0.33, 0.43); ck.lineTo(0.48, 0.28); ck.lineTo(-0.1, -0.3); ck.closePath();
  const c = new THREE.Mesh(new THREE.ExtrudeGeometry(ck, { depth: 0.08, bevelEnabled: true, bevelThickness: 0.04, bevelSize: 0.03, bevelSegments: 5 }), new THREE.MeshPhysicalMaterial({ color: "#ffffff", roughness: 0.25, clearcoat: 1 }));
  c.position.set(0, 0, 0.22); grp.add(c);
  return grp;
}

// Moeda leve (pilhas): cilindro serrilhado de faces lisas, geometria compartilhada
let liteGeo = null;
const liteMat = () => new THREE.MeshPhysicalMaterial({ color: "#7a2bd3", metalness: 1, roughness: 0.32, clearcoat: 0.6 });
export function makeCoinLite(R = 0.42, T = 0.1, mat = null) {
  if (!liteGeo) {
    liteGeo = new THREE.CylinderGeometry(1, 1, 1, 160, 1, false);
    const p = liteGeo.attributes.position;
    for (let k = 0; k < p.count; k++) {
      const x = p.getX(k), z = p.getZ(k);
      if (Math.hypot(x, z) > 0.99) { const s2 = 1 + 0.012 * Math.cos(Math.atan2(z, x) * 80); p.setX(k, x * s2); p.setZ(k, z * s2); }
    }
    liteGeo.computeVertexNormals();
  }
  const m = new THREE.Mesh(liteGeo, mat || liteMat());
  m.scale.set(R, T, R); m.castShadow = true;
  return m;
}
