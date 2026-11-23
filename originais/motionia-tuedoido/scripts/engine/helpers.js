const SMEARS = [];
const AER = mulberry32(21);
const AE_ROWS = ['Texto 01', 'Texto 02', 'Forma 3D', 'Câmera', 'Luz Principal', 'Partículas', 'Ajuste', 'Glow', 'Fundo'].map((n, i) => ({ n, c: [V, L, WH, '#888'][i % 4], keys: Array.from({ length: 4 + Math.floor(AER() * 5) }, () => AER()) }));
function aeWindow(ctx, x, y, w, h, t) {
  ctx.save();
  rr(ctx, x, y, w, h, 18); ctx.fillStyle = '#121212'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#2b2b2b'; ctx.stroke();
  ctx.save(); rr(ctx, x, y, w, h, 18); ctx.clip();
  ctx.fillStyle = '#1b1b1b'; ctx.fillRect(x, y, w, 48);
  ['#444', '#444', '#444'].forEach((c, i) => { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x + 28 + i * 24, y + 24, 7, 0, 7); ctx.fill(); });
  T(ctx, 'Composição 1  •  Linha do tempo', x + 120, y + 25, 19, '#9a9a9a', { f: 'Inter', w: 500, a: 'left' });
  const lp = 330, top = y + 48, rh = 44, ty = top + 46;
  ctx.fillStyle = '#161616'; ctx.fillRect(x, top, lp, h - 48);
  // ruler
  ctx.fillStyle = '#1e1e1e'; ctx.fillRect(x + lp, top, w - lp, 46);
  for (let i = 0; i <= 20; i++) { const xx = x + lp + 20 + i * (w - lp - 40) / 20; ctx.fillStyle = '#555'; ctx.fillRect(xx, top + (i % 2 ? 32 : 22), 2, i % 2 ? 12 : 22); if (i % 4 === 0) T(ctx, `0:${String(i / 2).padStart(2, '0')}`, xx + 6, top + 16, 15, '#777', { f: 'Inter', a: 'left' }); }
  AE_ROWS.forEach((r, i) => {
    const yy = ty + i * rh;
    ctx.fillStyle = i % 2 ? '#141414' : '#171717'; ctx.fillRect(x, yy, w, rh);
    ctx.fillStyle = r.c; ctx.fillRect(x + 18, yy + 13, 18, 18);
    T(ctx, r.n, x + 50, yy + rh / 2, 19, '#cfcfcf', { f: 'Inter', w: 500, a: 'left' });
    const bx = x + lp + 20 + r.keys[0] * 120, bw = (w - lp - 60) * (0.5 + r.keys[1] * 0.45);
    ctx.fillStyle = rgba(r.c === '#888' ? '#7F3AED' : r.c, 0.22); ctx.fillRect(bx, yy + 8, bw, rh - 16);
    r.keys.forEach((k, j) => { const kx = bx + k * bw; ctx.save(); ctx.translate(kx, yy + rh / 2); ctx.rotate(Math.PI / 4); ctx.fillStyle = j % 2 ? L : WH; ctx.fillRect(-6, -6, 12, 12); ctx.restore(); });
  });
  // graph editor
  const gy = ty + AE_ROWS.length * rh + 10, gh = y + h - gy - 14;
  ctx.fillStyle = '#0e0e0e'; ctx.fillRect(x + lp, gy, w - lp, gh);
  ctx.lineWidth = 4;
  [[V, 0.2], [L, 0.65]].forEach(([c, o]) => { ctx.strokeStyle = c; ctx.beginPath(); for (let i = 0; i <= 60; i++) { const px = x + lp + 20 + i / 60 * (w - lp - 40); const v = 0.5 + 0.38 * Math.sin(i / 60 * 6.28 * 1.2 + o * 6 + t * 0.5) * Math.exp(-i / 90); const py = gy + gh * (1 - v); i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); } ctx.stroke(); });
  // playhead
  const phx = x + lp + 20 + ((t * 0.18) % 1) * (w - lp - 40);
  ctx.fillStyle = L; ctx.fillRect(phx - 1.5, top, 3, h - 48); ctx.beginPath(); ctx.moveTo(phx - 10, top); ctx.lineTo(phx + 10, top); ctx.lineTo(phx, top + 14); ctx.fill();
  ctx.restore(); ctx.restore();
}
const CODE = ['import { cena } from "./motion"', 'const camera = criarCamera({ fov: 35 })', 'function animar(t) {', '  const k = mola(t, 0.62, 15)', '  texto.escala = lerp(1.6, 1, k)', '  brilho.intensidade = pulso(t)', '}', 'for (const p of particulas) {', '  p.x += p.vx * dt', '  p.y += p.vy * dt', '}', 'export function render(t) {', '  limpar(ctx)', '  desenharFundo(ctx, "#7F3AED")', '  desenharLogo(ctx, t)', '  aplicarGlow(ctx, "#C6FF34")', '  desfoqueDeMovimento(4)', '}', 'window.seek = render', 'gravar({ fps: 60, crf: 16 })', 'mixar(narracao, efeitos, musica)', '// pronto'];
function codeLine(ctx, s, x, y, sz) {
  ctx.save(); ctx.font = `${sz}px "DejaVu Sans Mono", monospace`; ctx.textBaseline = 'middle';
  const parts = s.split(/(\s+|[(){}.,"=])/); let cx = x;
  const kw = new Set(['import', 'from', 'const', 'function', 'for', 'of', 'export', 'return']);
  for (const p of parts) { if (!p) continue; let c = '#d6d6d6'; if (kw.has(p)) c = '#a77bff'; else if (/^\d/.test(p)) c = L; else if (p.startsWith('//')) c = '#666'; else if (/[(){}.,"=]/.test(p)) c = '#888'; ctx.fillStyle = c; ctx.fillText(p, cx, y); cx += ctx.measureText(p).width; }
  ctx.restore();
}
function fans(c, w, h, t, em) {
  for (let k = 0; k < 3; k++) {
    const cx = w * 0.62, cy = h * (0.2 + k * 0.24), r = Math.min(w, h) * 0.17;
    c.strokeStyle = k === 1 ? L : V; c.lineWidth = r * 0.16; c.beginPath(); c.arc(cx, cy, r, 0, 7); c.stroke();
    if (!em) { c.fillStyle = '#222'; for (let b = 0; b < 7; b++) { const a = b / 7 * 6.283 + t * 9; c.save(); c.translate(cx, cy); c.rotate(a); c.beginPath(); c.ellipse(r * 0.45, 0, r * 0.42, r * 0.14, 0.4, 0, 7); c.fill(); c.restore(); } }
  }
  c.fillStyle = em ? L : '#333'; c.fillRect(w * 0.08, h * 0.86, w * 0.84, h * 0.035);
  if (!em) { c.fillStyle = '#111'; c.fillRect(w * 0.06, h * 0.78, w * 0.88, h * 0.07); }
}
const WALL = `<entradas> Produto: curso Motion com IA. Usa só os materiais em anexo.|Narração: relógio mestre do vídeo. Música: trilha em anexo, a partir de t=0.|Logo: vetoriza com potrace, extrude em 3D e anima em 3D.|Paleta: preto #000000, violeta #7F3AED, lime #C6FF34, branco.|Referência: extrai um quadro a cada 0,5 s e escreve o guia de estilo.|Formato: 1920x1080 (16:9). </entradas>|<direcao> Showreel de motion designer, câmera 3D viva o tempo todo.|A troca de fundo é a transição: wipes, máscaras, mergulho em letras.|Glow em lime e violeta só nos elementos de impacto.|Câmera: dolly-in, orbit, crash zoom, tremor de 4 a 6 quadros.|Tipografia cinética gigante + linha pequena de apoio.|Proibido: sons infantis, gradiente arco-íris, fade em tudo, tempo morto. </direcao>|<estrutura> words.json com faster-whisper, word_timestamps=True.|A palavra entra 2 a 3 quadros antes do início no áudio.|Marcos da música em beats.json: 12,0 s · 48,0 s · 49,5 s · 73,0 s.|1. 0,00–2,95 olhos + TU É DOIDO, mergulho no último O.|2. 2,96–4,40 palavras descendo em cascata.|3. 4,84–5,80 congelamento, RGB split, PERA AÍ.|4. 6,16–10,06 janela tipo After cortada por lâmina.|5. 10,64–14,44 sucção + impacto CLAUDE em 3D.|6. 15,10–17,18 código apagado, 0 LINHAS.|7. 17,46–19,22 PC gamer 3D no espaço.|8. 22,04–26,36 quadrado vira cubo, voa e explode.|9. 30,28–34,64 pedido genérico, resultado genérico.|10. 51,92–55,34 o número 2 em 3D. </estrutura>|<construcao> 1. Um HTML, um canvas, window.seek(t). Sem timers.|2. Molas de forma fechada; ruído só com seed (mulberry32).|3. cues.json: imagem e som leem o mesmo arquivo.|4. Bloom, profundidade de campo, aberração cromática, grão.|5. Narração > efeitos > música; ducking de −10 a −12 dB.|6. Master −14 LUFS, true peak −1 dBTP.|7. Render 60 fps, 4 subquadros, H.264 yuv420p, CRF 16. </construcao>|<pegadinhas> Nunca usa will-change no que a câmera aproxima.|Margem de segurança de 96 px nas laterais.|O miolo do O tem a cor exata do próximo fundo.|Texto 3D de frente no quadro de leitura.|Bloom não pode estourar texto branco pequeno. </pegadinhas>|<comeco> Mostra a tabela de estados antes de escrever código.|Folha de contato, notas de 1 a 10, corrige os 3 piores.|Repete até tudo ficar 8+. </comeco>`.split('|');
