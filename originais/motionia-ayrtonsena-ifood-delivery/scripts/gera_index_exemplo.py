# Gera o index.html do v2 com as cenas, a voz, a música (na batida) e os efeitos alinhados pelo "golpe" de cada arquivo.
import sys
destino = sys.argv[1]
TOTAL = 46.2
Q = 1 / 30
# tempo (s) do golpe dentro de cada arquivo: o som entra 1 quadro depois da imagem
GOLPE = {
    "boom-3.mp3": .033, "sub-boom.mp3": .057, "click-1.wav": .047, "click-2.wav": .015, "click-3.wav": .108,
    "click-4.wav": .044, "click-5.wav": .055, "click-digital.mp3": .063, "ui-click.wav": .172, "interface.wav": .125,
    "interface-2.wav": .001, "interface-activate.mp3": .152, "pop-up.wav": .398, "pop-up-2.wav": .35, "popup-1.wav": .368,
    "popup-2.wav": .018, "popup-3.wav": .011, "popup-4.wav": .022, "popup-5.wav": .041, "correct-2.wav": .149,
    "swoosh-3.wav": .219, "swoosh-7.wav": .34, "whoosh-03.wav": .659, "woosh-standard.mp3": .993, "notificacao-ifood.wav": .351,
    "iphone.mp3": .859, "success.wav": .005, "click-button.mp3": .179, "trailer-boom.mp3": .304, "campainha-dimdom-corte.wav": .054,
}
DUR = {"click-button.mp3": .24, "click-1.wav": .8}
# (id, arquivo, momento da imagem, volume, duração, media-start do ronco)
SFX = [
    # abertura: "Vixe Maria, rapaz, que fome, viu?" + 2:47 + ronco
    ("vx-ronco1", "ronco-tummy.mp3", 0.0, .6, .8, 0.52), ("vx-vixe", "click-1.wav", .12, .45), ("vx-maria", "click-3.wav", .66, .4),
    ("vx-rapaz", "click-4.wav", 1.01, .4), ("vx-fome", "click-5.wav", 1.52, .4), ("vx-ronco2", "ronco-tummy.mp3", 1.82, .55, .55, 7.72),
    ("vx-viu", "click-2.wav", 2.3, .45), ("vx-onda", "swoosh-3.wav", 3.14, .5), ("vx-ronco3", "ronco-tummy.mp3", 3.25, 1.0, .95, 17.2),
    ("vx-boom", "sub-boom.mp3", 3.25, .55, 1.6), ("vx-queda", "swoosh-7.wav", 3.98, .5), ("vx-ronco4", "ronco-tummy.mp3", 3.85, .7, .9, 2.57),
    # tudo fechado / quase tudo / celular
    ("fe-letras", "ui-click.wav", 3.9, .45), ("fe-ponto", "click-2.wav", 4.34, .75), ("fe-raiva", "click-digital.mp3", 5.42, .55),
    ("fe-risco", "swoosh-3.wav", 4.95, .4), ("fe-ta", "click-1.wav", 4.86, .45), ("fe-brinc", "click-3.wav", 5.13, .45),
    ("fe-comigo", "click-4.wav", 5.74, .45), ("fe-ne", "pop-up-2.wav", 6.14, .45),
    ("ce-sobe", "woosh-standard.mp3", 7.0, .55, 2.0), ("ce-giro", "whoosh-03.wav", 6.95, .6), ("ce-para", "interface.wav", 7.62, .5),
    ("ce-ifood", "notificacao-ifood.wav", 8.15, 1.0), ("ce-l1", "popup-4.wav", 8.22, .35), ("ce-l2", "popup-5.wav", 8.36, .35),
    ("ce-mergulho", "swoosh-7.wav", 9.1, .6),
    # lista
    ("li-c1", "popup-2.wav", 9.32, .45), ("li-c2", "popup-3.wav", 9.44, .45), ("li-c3", "popup-4.wav", 9.56, .45), ("li-c4", "popup-5.wav", 9.68, .45),
    ("li-tags", "correct-2.wav", 10.33, .45, 1.4), ("li-t2", "click-4.wav", 10.47, .4), ("li-t3", "click-5.wav", 10.6, .4),
    ("li-rola", "interface-2.wav", 11.42, .45), ("li-whip", "swoosh-3.wav", 11.85, .55),
    # aberto agora / na palma
    ("pa-letras", "ui-click.wav", 11.95, .45), ("pa-pilula", "popup-2.wav", 12.5, .55), ("pa-onda", "swoosh-7.wav", 13.2, .55),
    ("pa-sobe", "woosh-standard.mp3", 13.45, .45, 2.0), ("pa-na", "click-1.wav", 13.06, .5), ("pa-da", "click-3.wav", 13.33, .5),
    ("pa-mao", "click-5.wav", 13.6, .5), ("pa-selo1", "pop-up-2.wav", 13.59, .5), ("pa-selo2", "popup-3.wav", 13.73, .45),
    ("pa-mergulho", "swoosh-3.wav", 15.05, .55),
    # home
    ("ho-f1", "popup-4.wav", 14.72, .4), ("ho-f2", "popup-5.wav", 14.88, .4), ("ho-f3", "popup-2.wav", 15.04, .4),
    ("ho-banner", "interface-2.wav", 14.97, .4), ("ho-chip", "click-2.wav", 16.28, .7), ("ho-chip-on", "interface-activate.mp3", 16.34, .5),
    ("ho-arrasta", "swoosh-7.wav", 16.99, .45), ("ho-clique", "click-button.mp3", 18.46, .85), ("ho-pulo", "popup-1.wav", 18.56, .55),
    ("ho-voa", "whoosh-03.wav", 19.0, .5),
    # comidas
    ("co-p1", "pop-up-2.wav", 19.75, .45), ("co-t1", "swoosh-3.wav", 20.02, .55), ("co-p2", "popup-3.wav", 20.26, .45),
    ("co-t2", "swoosh-7.wav", 21.69, .55), ("co-p3", "popup-4.wav", 21.92, .45), ("co-t3", "swoosh-3.wav", 23.33, .55),
    ("co-p4", "popup-5.wav", 23.56, .45), ("co-sacola", "interface.wav", 23.9, .45), ("co-clique", "click-button.mp3", 24.45, .85), ("co-beleza", "popup-3.wav", 24.4, .4),
    ("co-cresce", "woosh-standard.mp3", 24.75, .4, 1.8),
    # preparo e coleta
    ("pr-sacola", "pop-up.wav", 25.53, .55), ("pr-pilula", "popup-1.wav", 25.58, .45), ("pr-c1", "popup-2.wav", 26.09, .45),
    ("pr-c2", "popup-3.wav", 26.36, .45), ("pr-c3", "popup-4.wav", 26.63, .45), ("pr-c4", "popup-5.wav", 26.9, .45),
    ("pr-pronto", "correct-2.wav", 27.16, .45, 1.2), ("pr-whip", "swoosh-7.wav", 27.58, .5), ("pr-corrida", "iphone.mp3", 27.75, .45, 1.2),
    ("pr-toque", "click-5.wav", 28.24, .7), ("pr-coletado", "success.wav", 28.27, .45), ("pr-sai", "swoosh-3.wav", 28.65, .5),
    # RAPIDINHO
    ("ra-moto", "swoosh-7.wav", 28.95, .55), ("ra-l1", "click-3.wav", 28.85, .4), ("ra-l2", "click-1.wav", 29.03, .4),
    ("ra-l3", "click-4.wav", 29.21, .4), ("ra-sai", "swoosh-3.wav", 31.42, .55),
    ("ra-empina", "whoosh-03.wav", 29.95, .45), ("ra-pulo", "popup-4.wav", 30.43, .35), ("ra-empina2", "swoosh-3.wav", 31.03, .4),
    # mapa
    ("ma-zoom", "interface-2.wav", 31.5, .4), ("ma-card", "pop-up-2.wav", 32.05, .45), ("ma-pin", "popup-3.wav", 32.59, .45),
    ("ma-mergulho", "swoosh-7.wav", 33.95, .45),
    # dim-dom (o "dim" bate em 34,22)
    ("dd-campainha", "campainha-dimdom-corte.wav", 34.22 - Q, 1.0, 1.75),
    # doido
    ("do-tu", "click-1.wav", 35.3, .5), ("do-e", "click-2.wav", 35.5, .5), ("do-bate", "pop-up-2.wav", 35.83, .55),
    ("do-o1", "click-3.wav", 35.97, .45), ("do-o2", "click-4.wav", 36.15, .45), ("do-o3", "click-5.wav", 36.33, .45),
    ("do-vem", "woosh-standard.mp3", 37.7, .5, 1.5), ("do-pousa", "pop-up.wav", 37.97, .55),
    # final: sem riser; impacto só no logo
    ("fi-onda", "swoosh-3.wav", 39.45, .5), ("fi-palavras", "ui-click.wav", 39.66, .4), ("fi-l1", "popup-2.wav", 41.28, .35),
    ("fi-l2", "popup-3.wav", 41.415, .35), ("fi-l3", "popup-4.wav", 41.55, .35), ("fi-l4", "popup-5.wav", 41.685, .35),
    ("fi-boom", "trailer-boom.mp3", 41.28, .7, 2.6), ("fi-pisca", "click-4.wav", 42.93, .5),
    ("fi-take", "swoosh-7.wav", 43.44, .45), ("fi-arroba", "ui-click.wav", 43.5, .45), ("fi-pulo1", "click-4.wav", 43.97, .35), ("fi-pulo2", "click-5.wav", 45.09, .35),
]
CENAS = [("vixe", 0, 4.2), ("fechado", 3.8, 5.5), ("celular", 6.5, 2.85), ("lista", 9.2, 2.8), ("palma", 11.9, 3.3),
         ("home", 14.62, 4.73), ("comidas", 19.28, 5.8), ("preparo", 25.0, 3.85), ("rapidinho", 28.8, 2.8), ("mapa", 31.5, 2.7),
         ("dimdom", 34.12, 1.2), ("doido", 35.25, 4.05), ("final", 39.25, TOTAL - 39.25)]
# música: mais baixa embaixo da fala, mais alta onde não tem fala; a entrada forte (22,535 s da trilha) cai no logo (8,15)
PONTOS = [(0, .16), (3.1, .16), (3.25, .3), (4.7, .3), (4.85, .14), (6.55, .14), (6.7, .3), (9.1, .3), (9.25, .12), (12.0, .12),
          (12.15, .25), (14.5, .25), (14.65, .12), (25.2, .12), (25.35, .25), (28.6, .25), (28.75, .12), (31.55, .12), (31.7, .25),
          (35.15, .25), (35.3, .12), (39.25, .12), (39.45, .35), (45.6, .35), (TOTAL, 0)]

def f(x): return ("%.3f" % x).rstrip("0").rstrip(".")
hosts = "\n".join(
    f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{f(a)}" data-duration="{f(d)}" '
    f'data-track-index="{i + 1}" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index: {i + 1}"></div>'
    for i, (c, a, d) in enumerate(CENAS))
auto = '{"version":1,"lanes":[{"target":"volume","points":[' + ",".join('{"t":%s,"v":%s}' % (f(t), v) for t, v in PONTOS) + "]}]}"
efeitos = []
for k, e in enumerate(SFX):
    id_, arq, t, vol = e[0], e[1], e[2], e[3]
    dur = e[4] if len(e) > 4 else DUR.get(arq, 0.9)
    if arq == "ronco-tummy.mp3":
        ini, ms = t + Q - 0.025, e[5]
        extra = f' data-media-start="{f(ms)}" data-fade-out="0.08"'
    else:
        ini, extra = t + Q - GOLPE[arq], ""
        if arq in ("woosh-standard.mp3", "trailer-boom.mp3", "sub-boom.mp3", "correct-2.wav"): extra = ' data-fade-out="0.5"'
    ini = max(0, ini)
    efeitos.append(f'      <audio id="sfx-{id_}" class="clip" src="assets/audio/sfx/{arq}" data-start="{f(ini)}" data-duration="{f(dur)}"{extra} data-track-index="{30 + k}" data-volume="{vol}"></audio>')

html = f'''<!doctype html>
<html lang="pt-BR" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        margin: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #f8f1e7;
      }}
      #root {{
        width: 100%;
        height: 100%;
        position: relative;
        font-family: "Montserrat", sans-serif;
      }}
    </style>
  </head>
  <body>
    <!-- Fome de madrugada — comercial de fã, não oficial. 16:9, 30 fps, {f(TOTAL)} s. Tudo na batida da música (110,5 BPM). -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{f(TOTAL)}" data-width="1920" data-height="1080">
{hosts}

      <!-- voz: mesmos takes, inícios ajustados pra batida -->
      <audio id="voz" class="clip" src="assets/audio/voz/narracao-v4.wav" data-start="0" data-duration="{f(TOTAL)}" data-track-index="20" data-volume="1"></audio>
      <!-- música desde o começo: a parte calma embaixo do "Vixe", a entrada forte no logo do iFood -->
      <audio id="musica" data-timeline-role="music" class="clip" src="assets/audio/musica/musica-ifood.wav" data-start="0" data-duration="{f(TOTAL)}" data-media-start="14.385" data-track-index="21" data-volume="1"
        data-automation='{auto}'></audio>

      <!-- efeitos: muito UI, cinemático só no 2:47 e no logo -->
{chr(10).join(efeitos)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(destino, "w", encoding="utf8").write(html)
print("ok", len(SFX), "efeitos")
