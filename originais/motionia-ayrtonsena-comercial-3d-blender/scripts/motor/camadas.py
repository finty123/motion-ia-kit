# Renderiza as camadas 2D (camadas.html) quadro a quadro com o Chrome sem janela.
# Uso: python camadas.py <previa|final> [quadros separados por virgula]
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import config as C

AQUI, RENDER = C.AQUI, C.RENDER
qualidade = sys.argv[1]
W, H = {"final": (1920, 1080), "previa": (960, 540)}.get(qualidade, (640, 360))
total = C.TOTAL
# o html le a configuracao daqui (sabores, palavras, fontes, textos do final, linha do tempo)
cfg = dict(C.CFG, bpm=C.BPM, linha_do_tempo=C.TL, sabores=C.SABORES)
(AQUI / "cfg.js").write_text("window.CFG = " + json.dumps(cfg, ensure_ascii=False) + ";\n", encoding="utf-8")
quadros = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else range(total)
saida = RENDER / qualidade
for camada in ("tras", "frente"):
    (saida / camada).mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    try:
        nav = p.chromium.launch(channel="chrome")     # Chrome instalado
    except Exception:
        nav = p.chromium.launch()                     # Chromium do Playwright (playwright install chromium)
    pg = nav.new_page(viewport={"width": W, "height": H})
    pg.goto((AQUI / "camadas.html").as_uri() + f"?w={W}&h={H}")
    pg.wait_for_function("window.pronto !== undefined", timeout=30000)
    pg.evaluate("Promise.race([window.pronto, new Promise(r => setTimeout(r, 20000))])")   # fonte que nao carrega nao trava
    pg.wait_for_timeout(300)
    canvas = pg.locator("#c")
    for f in quadros:
        for camada in ("tras", "frente"):
            pg.evaluate(f"window.seek({f}, '{camada}')")
            canvas.screenshot(path=str(saida / camada / f"f_{f:04d}.png"), omit_background=(camada == "frente"))
    nav.close()
print(f"camadas {qualidade}: {len(quadros)} quadros")
