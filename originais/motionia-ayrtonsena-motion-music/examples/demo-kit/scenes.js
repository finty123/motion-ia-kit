// DEMO do kit_musica.js — uma cena por efeito (serve de vitrine e de teste). Ritmo fictício de 120 BPM.
const END = 16;
RITMO.fisheye = 0.16; RITMO.halftone = 0.12; RITMO.vazamento = t => t < 8 ? 0.6 : 0;
const CREME = '#fff4d6', ROSA = '#e8607a', LAR = '#ff6a2b';
function D1(ctx, t) { // write-on neon + starburst + chuva de emoji
  setCam3({ ry: 0.2 * Math.sin(t * 0.9), z: 80 * t, rz: 0.03 * Math.sin(t * 1.3) });
  bgv(ctx, '#ff5a1f', '#ffd27a', 0.5, W / 2, H * 0.3);
  propsField(ctx, t, 0.1, '🐝', { n: 14, vel: 30, tam: 0.6 });
  starburst(ctx, t, 1.0, { r: 380, col: '#ffd23f', z: 300 });
  writeOn(ctx, t, 'Can I Get A Kiss', 0.3, 1.4, { size: 150, font: 'Pacifico', col: '#fff6d8', glowCol: '#ffe08a', glow: 1.1 });
}
function D2(ctx, t) { // pílulas com sombra longa e texto trocando + chão de grade
  setCam3({ ry: 0.25 * Math.sin((t - 2.5) * 1.1), rx: -0.12, z: 120 * (t - 2.5), rz: 0.04 * Math.sin(t) });
  bgv(ctx, '#f6d9d4', CREME, 0.4); gridFloor(ctx, t, { y: 330, col: rgba('#fff8d0', 0.7) });
  pill(ctx, t, { id: 'a', x: -220, y: -140, size: 120, font: '"Playfair Display"', wt: '900', bg: ROSA, fg: CREME, textos: [[2.7, 'you']] });
  pill(ctx, t, { id: 'b', x: 160, y: 20, size: 70, font: '"Playfair Display"', bg: CREME, fg: ROSA, textos: [[3.1, 'make me'], [3.7, 'wanna make you']] });
}
function D3(ctx, t) { // texto em círculo (ooooh) + íris de coração no fim
  setCam3({ rz: 0.3 * (t - 5), z: 60 * (t - 5) });
  bgv(ctx, ROSA, '#ff9fb2', 0.4);
  circleText(ctx, t, 'oooooooooooooooh', 5.1, { r: 360, size: 120, font: '"Playfair Display"', col: CREME, spin: 0.8 });
  circleText(ctx, t, 'oooooh!!', 5.4, { r: 170, size: 80, font: '"Playfair Display"', col: CREME, spin: -1.2 });
  iris(ctx, t, 7.3, 0.45, CREME, 'coracao');
}
function D4(ctx, t) { // letra repetida (Foreverrrr) com câmera seguindo + abelha passando na lente
  const times = []; for (let i = 0; i < 12; i++) times.push(8.2 + i * 0.12);
  const path = i => ({ x: -500 + i * 130, y: 60 - 120 * Math.sin(i * 0.25), rz: -0.15 + i * 0.03 });
  const h = trailHead(t, times, path);
  setCam3({ x: lerp(-500, h.x - 150, P(t, 8.0, 8.4)), y: h.y * 0.5, z: 100, ry: 0.2 * Math.sin(t * 1.4), rz: 0.05 * Math.sin(t * 2) });
  bgv(ctx, LAR, '#ffb36b', 0.4);
  W3(ctx, t, 'Fo', 8.0, { x: -760, y: 60, size: 260, side: '#a33', from: { z: -900, rz: 0.4 } });
  letterTrail(ctx, t, 'r', times, path, { size: 260, face: WH, side: '#a33', glow: 0.2 });
  lensPass(ctx, t, 10.0, 0.6, '🐝', { dir: 1 });   // atravessa o corte: chamada igual nas duas cenas
}
function D5(ctx, t) { // buraco vermelho + loading + assinatura
  setCam3({ rz: 0.4 * (t - 10.3), z: 100 * P(t, 10.3, 13) });
  bg(ctx, mix('#2a030b', '#000000', P(t, 10.3, 13)));
  loadingBar(ctx, t, [[10.4, 0.3], [11.0, 0.7], [11.6, 1]], {});
  lensPass(ctx, t, 10.0, 0.6, '🐝', { dir: 1 });
  redHole(ctx, t, 11.0, 13.0, {});
  assinatura(ctx, t, 13.4);
}
scene(0, D1); scene(2.5, D2); scene(5.0, D3); scene(8.0, D4); scene(10.3, D5);
clarao(2.5); cue(1.0, 'v', 0, { sh: 0.4, ch: 0.4 }); cue(7.75, 'v', 0, { sh: 0.3 }); clarao(10.3, 0.5);
