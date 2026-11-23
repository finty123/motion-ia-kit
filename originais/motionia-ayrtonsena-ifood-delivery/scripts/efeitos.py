"""Gera as tags <audio> dos efeitos com o GOLPE de cada arquivo caindo 1 quadro depois da imagem.

Uso: python efeitos.py deixas.json [--pasta assets/audio/sfx] [--trilha-inicial 30]
deixas.json: [{"id": "co-clique", "arquivo": "click-button.mp3", "t": 24.45, "vol": 0.85},
              {"id": "vx-ronco", "arquivo": "ronco.mp3", "t": 3.25, "vol": 1, "dur": 0.95, "media_start": 17.2}, ...]
  t = segundo do vídeo em que a IMAGEM acontece (clique, pop, palavra, pouso, troca).
O golpe de cada arquivo é medido uma vez com `npx hyperframes audio <arq> --json` (onset pra impactos, pico pro resto)
e guardado em golpes.json na pasta dos efeitos. Cole a saída dentro do #root do index.html.
"""
import argparse, json, os, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("deixas"); ap.add_argument("--pasta", default="assets/audio/sfx"); ap.add_argument("--trilha-inicial", type=int, default=30)
a = ap.parse_args()
Q = 1 / 30
cache_p = os.path.join(a.pasta, "golpes.json")
cache = json.load(open(cache_p, encoding="utf8")) if os.path.exists(cache_p) else {}
IMPACTO = ("boom", "pop-up.wav", "popup-1", "correct", "iphone", "trailer", "interface.wav", "ronco")

def golpe(arq):
    if arq in cache: return cache[arq]
    r = subprocess.run(f'npx hyperframes audio "{os.path.join(a.pasta, arq)}" --json', shell=True, capture_output=True, text=True)
    it = json.loads(r.stdout)["items"][0]; m = it.get("moments", {}); dur = it.get("duration", 1)
    g = m.get("onset", 0) if any(k in arq for k in IMPACTO) else m.get("peak", m.get("onset", 0))
    cache[arq] = {"golpe": round(g or 0, 3), "dur": round(dur, 3)}
    json.dump(cache, open(cache_p, "w", encoding="utf8"), indent=1)
    return cache[arq]

def f(x): return ("%.3f" % x).rstrip("0").rstrip(".")
for k, e in enumerate(json.load(open(a.deixas, encoding="utf8"))):
    g = golpe(e["arquivo"])
    ms = e.get("media_start")
    ini = max(0, e["t"] + Q - (0.025 if ms is not None else g["golpe"]))
    dur = min(e.get("dur", 0.9), g["dur"] - (ms or 0)) if ms is None else e.get("dur", 0.9)
    extra = (f' data-media-start="{f(ms)}" data-fade-out="0.08"' if ms is not None else "") + (f' data-fade-out="{e["fade_out"]}"' if "fade_out" in e else "")
    print(f'      <audio id="sfx-{e["id"]}" class="clip" src="{a.pasta}/{e["arquivo"]}" data-start="{f(ini)}" data-duration="{f(dur)}"{extra} '
          f'data-track-index="{a.trilha_inicial + k}" data-volume="{e.get("vol", 0.5)}"></audio>')
