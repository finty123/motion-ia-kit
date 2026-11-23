# Storyboard de rascunho (lapis) a partir da estrutura do projeto: um quadro por cena, com tempo, desenho,
# cor / camera / tela / som, e no topo a REGRA de que e so rascunho de montagem (o visual dele nao vai pro video).
# Gera resultados/storyboard.html e resultados/storyboard.png.
# Uso: python storyboard.py                 -> monta as cenas do arco padrao com os dados do projeto.json
#      python storyboard.py --so-png        -> so refaz o PNG (depois de editar as cenas no html a mao)
#      Pra uma ideia fora do padrao, edite a lista "cenas" no html gerado e rode --so-png.
import json, sys
from pathlib import Path
import config as C

SAIDA = C.RESULTADOS
SAIDA.mkdir(exist_ok=True)
HTML, PNG = SAIDA / "storyboard.html", SAIDA / "storyboard.png"


def seg(b):
    return C.F(b) / C.FPS


def faixa(b0, b1):
    return f"{seg(b0):.1f}–{seg(b1):.1f} s · b{b0:g}–{b1:g}"


def bloco(b0, b1):
    """tempo da cena: texto pro quadro + batidas"""
    return {"t": faixa(b0, b1), "b0": b0, "b1": b1}


def montar_cenas():
    tl, sab = C.TL, C.SABORES
    nome0 = sab[0].get("nome", "sabor 1")
    cor = lambda s: (s.get("fundo") or ["#555555"])[0]
    cenas = [
        {"tipo": "queda", "nome": "Gota cai na tampa", **bloco(1, tl["olho"]), "cor": [C.CFG.get("fundo_abertura", ["#2a1020"])[0], sab[0].get("cor", "#ff2e93")],
         "cam": "lá em cima, centralizada, cai junto com a gota e freia num close forte da tampa", "tela": "nenhum texto: o movimento é o gancho",
         "som": "whoosh grave caindo"},
        {"tipo": "mergulho", "nome": "Mergulho no logo", **bloco(tl["olho"], tl["detalhes"]), "cor": [sab[0].get("cor", "#ff2e93")],
         "cam": f"na batida {tl['olho']:g} desce rápido pela frente e para encarando o logo/olho do rótulo", "tela": "só o rótulo", "som": "whoosh no mergulho"},
        {"tipo": "closes", "nome": "4 closes secos", **bloco(tl["detalhes"], tl["revela"]), "cor": [sab[0].get("cor", "#ff2e93")],
         "cam": "4 partes diferentes da lata, meia batida cada, corte seco", "tela": "nenhum texto", "som": "clique de câmera em cada corte"},
        {"tipo": "revela", "nome": f"Lata sobe ({nome0})", **bloco(tl["revela"], tl["trocas"][0]), "cor": [cor(sab[0])],
         "cam": "parada; a lata sobe de baixo já girando e para inclinada", "tela": "nenhum texto", "som": "whoosh subindo"},
    ]
    trocas = tl["trocas"]
    for k, b in enumerate(trocas):
        s = sab[(k + 1) % len(sab)]
        fim = trocas[k + 1] if k + 1 < len(trocas) else tl["cruz"]
        cenas.append({"tipo": "troca", "nome": f"Giro → {s.get('nome', 'sabor')}", **bloco(b, fim), "cor": [cor(s), s.get("cor", "#ff2e93")],
                      "fundo": cor(s), "palavra": s.get("palavra", ""), "peca": "gota" if s.get("respingo") else ("nenhuma" if not s.get("pecas") else "rodela"),
                      "cam": "mesmo lugar, sem zoom, afastando devagar" + ("; trocas acelerando" if k else ""),
                      "tela": (f"{s['palavra']} gigante ATRÁS da lata" if s.get("palavra") else "sem palavra"),
                      "som": "whoosh do giro + boom da explosão"})
    fc = C.CFG.get("fundo_cruz") or sab[0].get("cor", "#ff2e93")
    n_fil = len(tl["acende"])
    cenas += [
        {"tipo": "cruz", "nome": "Cata-vento", **bloco(tl["cruz"], tl["rastro"]), "cor": [fc], "fundo": fc,
         "cam": "de frente; as latas abrem em cruz, separadas, giro liso", "tela": "nenhum texto", "som": "whoosh grave + boom"},
        {"tipo": "rastro", "nome": "Rastro em leque", **bloco(tl["rastro"], tl["mergulho"]), "cor": [fc], "fundo": fc,
         "cam": "parada, leve push-in", "tela": "nenhum texto", "som": "whooshes suaves"},
        {"tipo": "furo", "nome": "Mergulho no furo", **bloco(tl["mergulho"], tl["furo"]), "cor": [fc, "#111111"], "fundo": fc,
         "cam": "mergulha pro centro; o furo abre como íris; a cor vira escuro", "tela": "nenhum texto", "som": "whoosh invertido (a música cai na pausa logo depois)"},
        {"tipo": "corredor", "nome": "Corredor neon", **bloco(tl["furo"], tl["fim_corredor"]), "cor": [s.get("cor", "#ff2e93") for s in sab],
         "cam": "atravessa os anéis em velocidade (uma câmera só, sem corte)", "tela": "nenhum texto", "som": "whoosh atravessando; volta forte da música"},
        {"tipo": "fileira", "nome": "Fileira em silhueta", **bloco(tl["fim_corredor"], tl["acende"][0]), "cor": ["#111111", sab[0].get("cor", "#ff2e93")],
         "n": n_fil, "cam": "sai do corredor e já desliza de lado", "tela": "nenhum texto", "som": "—"},
        {"tipo": "acende", "nome": "Uma lata acende por batida", **bloco(tl["acende"][0], tl["logo"]), "cor": ["#111111"],
         "n": n_fil, "b0": tl["acende"][0],
         "cam": "desliza de lado e freia centralizada na última lata", "tela": "nenhum texto", "som": "estalo de lâmpada + soco em cada uma"},
        {"tipo": "logo", "nome": "Logo em stroke", **bloco(tl["logo"], tl["arroba"]), "cor": ["#000000", C.CFG.get("cor_marca", "#ff2e93")],
         "marca": C.MARCA, "linha": C.CFG.get("final", {}).get("linha", ""), "aviso": C.CFG.get("final", {}).get("aviso", ""),
         "cam": "parada", "tela": "logo desenhado em traço, preenche; linha do produto + aviso", "som": "boom + lâmina"},
        {"tipo": "arroba", "nome": "Só o @", **bloco(tl["arroba"], tl["fim"]), "cor": ["#000000"], "arroba": C.CFG.get("assinatura", ""),
         "cam": "parada", "tela": "só a assinatura, uns 4 s, fecha no preto", "som": "whoosh suave"},
    ]
    return cenas


MOLDE = r"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Storyboard __MARCA__</title>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Patrick+Hand&display=swap" rel="stylesheet">
<style>
  :root { --papel:#f5f1e6; --lapis:#2b2b2b; --cinza:#8a857a; --aviso:#b3261e; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--papel); color:var(--lapis); font-family:"Patrick Hand","Comic Sans MS",cursive; }
  .folha { width:1600px; margin:0 auto; padding:36px 40px 48px; }
  h1 { font-family:"Caveat",cursive; font-size:54px; margin:0; line-height:1; }
  .sub { font-size:20px; color:var(--cinza); margin:6px 0 18px; }
  .regra { border:3px dashed var(--aviso); color:var(--aviso); padding:12px 18px; font-size:21px; line-height:1.35; margin-bottom:26px; border-radius:6px; }
  .regra b { font-family:"Caveat",cursive; font-size:30px; display:block; }
  .grade { display:grid; grid-template-columns:repeat(3,1fr); gap:26px 30px; }
  .quadro svg { width:100%; display:block; background:#fbf9f3; border:2.5px solid var(--lapis); border-radius:4px; filter:url(#tremido); }
  .cab { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px; gap:10px; }
  .cab .n { font-family:"Caveat",cursive; font-size:30px; font-weight:700; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .cab .t { font-size:18px; color:var(--cinza); white-space:nowrap; }
  .notas { font-size:17px; line-height:1.3; margin-top:8px; }
  .notas div { margin:2px 0; } .notas span { color:var(--cinza); }
  .cor { display:inline-block; width:14px; height:14px; border:1.5px solid var(--lapis); vertical-align:-2px; margin-right:3px; border-radius:3px; }
  .rodape { margin-top:26px; font-size:18px; color:var(--cinza); }
</style></head><body>
<svg width="0" height="0" style="position:absolute"><filter id="tremido"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="2.2"/></filter></svg>
<div class="folha">
  <h1>__MARCA__ · storyboard (rascunho)</h1>
  <div class="sub">__SUB__</div>
  <div class="regra"><b>REGRA: isto é só rascunho de montagem.</b>
    Este desenho mostra a ORDEM das cenas, o que entra em cada uma e para onde a câmera e as latas se movem. NÃO copie o visual dele: nem o traço de lápis, nem a fonte manuscrita, nem o papel, nem as setas, nem a composição exata. O design final segue as latas 3D reais e a direção aprovada. Os quadradinhos de cor são só anotação.</div>
  <div class="grade" id="grade"></div>
  <div class="rodape">Legenda: seta cheia = câmera · seta tracejada = lata ou peças · bN = batida N · letras vazadas = palavra ATRÁS da lata · lata escura = silhueta</div>
</div>
<script>
const cenas = __CENAS__;
const L = "#2b2b2b";
function lata(x, y, w, h, ang, rot = "", o = {}) {
  const r = w / 2, ey = w * 0.16, topo = y - h / 2, base = y + h / 2, pesc = h * 0.1, cheia = o.cheia || "#fbf9f3";
  let s = `<g transform="rotate(${ang} ${x} ${y})" fill="none" stroke="${L}" stroke-width="2.2" stroke-linecap="round">`;
  s += `<path d="M${x - r},${topo + pesc} L${x - r},${base - ey * 0.4} Q${x},${base + ey} ${x + r},${base - ey * 0.4} L${x + r},${topo + pesc} L${x + r * 0.84},${topo} L${x - r * 0.84},${topo} Z" fill="${cheia}" stroke="none"/>`;
  s += `<path d="M${x - r},${topo + pesc} L${x - r},${base - ey * 0.4} Q${x},${base + ey} ${x + r},${base - ey * 0.4} L${x + r},${topo + pesc}"/>`;
  s += `<path d="M${x - r},${topo + pesc} Q${x - r},${topo + pesc * 0.4} ${x - r * 0.84},${topo} M${x + r},${topo + pesc} Q${x + r},${topo + pesc * 0.4} ${x + r * 0.84},${topo}"/>`;
  s += `<ellipse cx="${x}" cy="${topo}" rx="${r * 0.84}" ry="${ey * 0.85}" fill="${cheia}"/><ellipse cx="${x + r * 0.1}" cy="${topo}" rx="${r * 0.28}" ry="${ey * 0.3}" stroke-width="1.6"/>`;
  if (!o.silhueta) s += `<line x1="${x + r * 0.55}" y1="${topo + pesc + 6}" x2="${x + r * 0.55}" y2="${base - 10}" stroke-width="1.3" stroke-dasharray="3 5"/>`;
  if (rot) s += `<text x="${x}" y="${y + 4}" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="${w * 0.3}" fill="${L}" stroke="none" transform="rotate(-90 ${x} ${y})">${rot}</text>`;
  if (o.gotas) for (let i = 0; i < 9; i++) s += `<circle cx="${x - r * 0.7 + (i * 37 % 100) / 100 * r * 1.4}" cy="${topo + pesc + 10 + (i * 53 % 100) / 100 * (h - pesc - 30)}" r="1.6" fill="${L}" stroke="none"/>`;
  return s + "</g>";
}
const seta = (d, tr = false) => `<path d="${d}" fill="none" stroke="${L}" stroke-width="2.4" stroke-linecap="round" ${tr ? 'stroke-dasharray="7 6"' : ""} marker-end="url(#ponta)"/>`;
const giro = (x, y, rx) => `<path d="M${x - rx},${y} A${rx},${rx * 0.32} 0 1 0 ${x + rx * 0.2},${y + rx * 0.31}" fill="none" stroke="${L}" stroke-width="2" marker-end="url(#ponta)"/>`;
const txt = (x, y, t, tam = 20, o = "") => `<text x="${x}" y="${y}" font-family="Caveat" font-size="${tam}" fill="${L}" ${o}>${t}</text>`;
const vazada = (x, y, t, tam) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="${tam}" fill="none" stroke="${L}" stroke-width="1.6" letter-spacing="4" textLength="${Math.min(440, t.length * tam * 0.55)}" lengthAdjust="spacingAndGlyphs">${t}</text>`;
const fundo = (c) => c ? `<rect x="0" y="0" width="480" height="270" fill="${c}" opacity="0.22"/>` : "";
const rodela = (x, y, r, a) => `<g transform="rotate(${a} ${x} ${y})" fill="#fbf9f3" stroke="${L}" stroke-width="1.6"><circle cx="${x}" cy="${y}" r="${r}"/><circle cx="${x}" cy="${y}" r="${r * 0.72}" fill="none"/>` +
  [0, 1, 2, 3, 4, 5].map(i => `<line x1="${x}" y1="${y}" x2="${x + Math.cos(i * Math.PI / 3) * r * 0.72}" y2="${y + Math.sin(i * Math.PI / 3) * r * 0.72}" stroke-width="1"/>`).join("") + `</g>`;
const gota = (x, y, r, a) => `<g transform="rotate(${a} ${x} ${y})" fill="#fbf9f3" stroke="${L}" stroke-width="1.6"><path d="M${x},${y - r * 1.3} Q${x + r},${y + r * 0.1} ${x},${y + r * 0.9} Q${x - r},${y + r * 0.1} ${x},${y - r * 1.3} Z"/></g>`;
function explosao(cx, cy, peca, qtd) {
  let s = "";
  for (let i = 0; i < qtd; i++) {
    const a = i / qtd * Math.PI * 2 + 0.3, d = 105 + (i * 37 % 60), x = cx + Math.cos(a) * d * 1.45, y = cy + Math.sin(a) * d * 0.82;
    s += `<path d="M${cx + Math.cos(a) * 55},${cy + Math.sin(a) * 40} L${x - Math.cos(a) * 18},${y - Math.sin(a) * 12}" stroke="${L}" stroke-width="1.1" stroke-dasharray="2 5"/>` + peca(x, y, 9 + (i * 13 % 7), i * 47);
  }
  return s;
}
const giroRapido = (x, y) => `<path d="M${x - 58},${y - 20} A58,18 0 1 0 ${x + 30},${y - 34}" fill="none" stroke="${L}" stroke-width="2.6" marker-end="url(#ponta)"/>`;
const cruz = (s = 1, d = 62) => lata(240, 135 - d * s, 40 * s, 96 * s, 0) + lata(240, 135 + d * s, 40 * s, 96 * s, 180) + lata(240 - d * s, 135, 40 * s, 96 * s, -90) + lata(240 + d * s, 135, 40 * s, 96 * s, 90);
const contorno = (cx, cy, w, h) => { const r = w / 2, c = w * 0.22; return `M${cx - r + c},${cy - h / 2} L${cx + r - c},${cy - h / 2} L${cx + r},${cy - h / 2 + c} L${cx + r},${cy + h / 2 - c} L${cx + r - c},${cy + h / 2} L${cx - r + c},${cy + h / 2} L${cx - r},${cy + h / 2 - c} L${cx - r},${cy - h / 2 + c} Z`; };
const defs = `<defs><marker id="ponta" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="${L}"/></marker></defs>`;

const DESENHO = {
  queda: c => fundo(c.cor[0]) + `<ellipse cx="250" cy="236" rx="220" ry="58" fill="#fbf9f3" stroke="${L}" stroke-width="2.4"/><ellipse cx="250" cy="236" rx="196" ry="48" fill="none" stroke="${L}" stroke-width="1.6"/>` +
    `<path d="M190,228 q60,-24 130,-4 q14,10 -6,18 q-70,16 -118,2 q-18,-6 -6,-16z" fill="none" stroke="${L}" stroke-width="2"/>` + gota(250, 150, 14, 180) +
    `<path d="M250,10 L250,118" stroke="${L}" stroke-width="3" stroke-dasharray="3 7" marker-end="url(#ponta)"/>` + txt(270, 60, "câmera cai junto", 22) + txt(270, 84, "com a gota", 22) + txt(270, 180, "freia: quase encosta", 19),
  mergulho: c => fundo(c.cor[0]) + `<rect x="110" y="0" width="260" height="270" fill="#fbf9f3" stroke="${L}" stroke-width="2.4"/>` +
    `<path d="M140,150 Q240,60 340,150 Q240,240 140,150 Z" fill="#fbf9f3" stroke="${L}" stroke-width="2.4"/><circle cx="240" cy="150" r="46" fill="none" stroke="${L}" stroke-width="2.2"/><circle cx="240" cy="150" r="20" fill="${L}"/>` +
    `<path d="M60,10 Q60,120 60,250" stroke="${L}" stroke-width="2.6" fill="none" marker-end="url(#ponta)"/>` + txt(380, 40, "encara", 22) + txt(380, 62, "o logo", 22) + txt(14, 262, "desce rápido na batida", 16),
  closes: c => [["tampa", 0, 0], ["logo", 240, 0], ["lateral", 0, 135], ["pescoço", 240, 135]].map(([n, x, y], i) =>
      `<rect x="${x}" y="${y}" width="240" height="135" fill="none" stroke="${L}" stroke-width="1.8"/>` + txt(x + 10, y + 26, `${i + 1}. ${n}`, 22) +
      (i === 0 ? `<ellipse cx="${x + 130}" cy="${y + 90}" rx="80" ry="26" fill="none" stroke="${L}" stroke-width="2"/>` :
       i === 1 ? `<circle cx="${x + 130}" cy="${y + 78}" r="30" fill="none" stroke="${L}" stroke-width="2"/>` :
       i === 2 ? `<path d="M${x + 90},${y + 40} L${x + 70},${y + 130} M${x + 190},${y + 40} L${x + 170},${y + 130}" stroke="${L}" stroke-width="2"/>` :
                 `<path d="M${x + 60},${y + 120} Q${x + 120},${y + 40} ${x + 200},${y + 120}" fill="none" stroke="${L}" stroke-width="2"/>`)).join("") + txt(120, 268, "corte seco, meia batida cada", 15),
  revela: c => fundo(c.cor[0]) + lata(240, 130, 70, 190, 18, "", { gotas: true }) + giro(240, 130, 60) + seta("M240,268 L240,236", true) + txt(290, 250, "sobe de baixo já girando", 18),
  troca: c => fundo(c.fundo) + (c.palavra ? vazada(240, 178, c.palavra, 92) : "") + (c.peca === "nenhuma" ? "" : explosao(240, 140, c.peca === "gota" ? gota : rodela, 11)) +
    lata(240, 140, 70, 190, -18, "", { gotas: true }) + giroRapido(240, 140) + txt(14, 28, "giro rápido: troca no borrão", 18) + (c.peca === "nenhuma" ? "" : txt(14, 262, "peças explodem e flutuam", 16)),
  cruz: c => fundo(c.fundo) + cruz() + giro(240, 135, 170) + txt(14, 30, "latas separadas", 18) + txt(330, 262, "giro liso, fundo fixo", 17),
  rastro: c => fundo(c.fundo) + [5, 4, 3, 2, 1].map(k => `<g transform="rotate(${-k * 9} 240 135)" opacity="${0.15 + (5 - k) * 0.12}">${cruz()}</g>`).join("") + cruz() + txt(14, 30, "cópias nítidas em leque", 18),
  furo: c => fundo(c.fundo) + `<g opacity="0.5">${cruz(1.15, 95)}</g><circle cx="240" cy="135" r="34" fill="#2b2b2b" opacity="0.85"/>` + seta("M420,250 L270,150") + txt(14, 30, "o furo do meio abre", 18) + txt(300, 262, "câmera entra no furo", 17),
  corredor: c => `<rect width="480" height="270" fill="#1d1a1c" opacity="0.15"/>` + [0, 1, 2, 3, 4, 5].map(i => { const k = 1 - i * 0.14; return `<path d="${contorno(240, 135, 300 * k * 0.62, 250 * k)}" fill="none" stroke="${c.cor[i % c.cor.length]}" stroke-width="${3.4 - i * 0.45}"/>`; }).join("") + seta("M240,262 L240,170") + txt(14, 30, "anéis neon, um atrás do outro", 17),
  fileira: c => fundo("#111") + `<path d="M0,200 L480,200" stroke="${L}" stroke-width="2"/>` + Array.from({ length: Math.min(c.n, 5) }, (_, i) => lata(60 + i * 90, 140, 50, 116, 0, "", { cheia: "#3b3438", silhueta: true })).join("") + txt(14, 30, "silhuetas, chão espelhado, luz atrás", 17),
  acende: c => fundo("#111") + `<path d="M0,200 L480,200" stroke="${L}" stroke-width="2"/>` + Array.from({ length: Math.min(c.n, 5) }, (_, i) => lata(60 + i * 90, 140, 50, 116, 0, "", i < Math.min(c.n, 5) - 1 ? {} : { cheia: "#3b3438", silhueta: true }) + txt(50 + i * 90, 236, "b" + (c.b0 + i), 20)).join("") + seta("M120,258 L380,258") + txt(14, 30, "uma acende por batida; freia na última", 17),
  logo: c => fundo("#111") + `<rect x="140" y="44" width="200" height="110" fill="none" stroke="${L}" stroke-width="2.4" stroke-dasharray="10 6"/>` + `<text x="240" y="112" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="40" fill="none" stroke="${L}" stroke-width="1.4" textLength="180" lengthAdjust="spacingAndGlyphs">${c.marca}</text>` +
    txt(240, 190, c.linha, 22, 'text-anchor="middle"') + txt(240, 226, c.aviso, 16, 'text-anchor="middle"') + txt(16, 30, "traço se desenha → preenche", 17),
  arroba: c => fundo("#111") + txt(240, 150, c.arroba || "@", 44, 'text-anchor="middle" font-weight="700"') + txt(150, 250, "fica uns 4 s → preto", 18),
};
document.getElementById("grade").innerHTML = cenas.map((c, i) => `
  <div class="quadro"><div class="cab"><span class="n">${i + 1}. ${c.nome}</span><span class="t">${c.t}</span></div>
  <svg viewBox="0 0 480 270">${defs}${(DESENHO[c.tipo] || (() => txt(20, 140, c.desenho || "(desenhar)", 24)))(c)}</svg>
  <div class="notas"><div><span>cor:</span> ${(c.cor || []).map(h => `<i class="cor" style="background:${h}"></i>`).join("")}</div>
  <div><span>câmera:</span> ${c.cam}</div><div><span>tela:</span> ${c.tela}</div><div><span>som:</span> ${c.som}</div></div></div>`).join("");
window.pronto = document.fonts.ready;
</script></body></html>
"""


def gerar_html():
    sub = (f"Comercial 3D{' não oficial' if C.CFG.get('nao_oficial', True) else ''} · 16:9 · {C.N_BATIDAS * 60 / C.BPM:.1f} s · "
           f"{C.BPM:.2f} BPM ({C.N_BATIDAS} batidas) · {C.N_SABORES} sabores · sem narração, só música + efeitos")
    html = (MOLDE.replace("__MARCA__", C.MARCA).replace("__SUB__", sub)
            .replace("__CENAS__", json.dumps(montar_cenas(), ensure_ascii=False, indent=1)))
    HTML.write_text(html, encoding="utf-8")


def gerar_png():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        try:
            nav = p.chromium.launch(channel="chrome")
        except Exception:
            nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": 1600, "height": 1200})
        pg.goto(HTML.as_uri())
        pg.evaluate("window.pronto")
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(PNG), full_page=True)
        nav.close()


if __name__ == "__main__":
    if "--so-png" not in sys.argv:
        gerar_html()
    gerar_png()
    print("storyboard:", HTML, "\npng:", PNG)
