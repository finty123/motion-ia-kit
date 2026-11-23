"""Grade de batidas no tempo do VÍDEO.

Uso:
  npx hyperframes beats --json            (no projeto, com data-timeline-role="music" no <audio> da trilha)
  python batida.py beats/<trilha>.json --momento 8.15
      --momento: segundo do vídeo onde a ENTRADA FORTE da música tem que cair (ex.: o logo aparecendo).
      --drop:    (opcional) segundo da TRILHA da entrada forte. Sem isso, pega a 1ª batida com força >= 0.8.
Saída: o data-media-start da trilha e a lista de batidas no tempo do vídeo (cole nos comentários das cenas).
"""
import argparse, json

ap = argparse.ArgumentParser()
ap.add_argument("beats_json")
ap.add_argument("--momento", type=float, required=True)
ap.add_argument("--drop", type=float)
ap.add_argument("--ate", type=float, default=90)
a = ap.parse_args()

d = json.load(open(a.beats_json, encoding="utf8"))
b = [(x["time"], x.get("strength", 0)) for x in d["beats"]]
drop = a.drop if a.drop is not None else next((t for t, s in b if s >= 0.8), b[0][0])
ms = round(drop - a.momento, 3)
if ms < 0:
    raise SystemExit(f"A entrada forte ({drop:.2f}s da trilha) vem antes do momento pedido: escolha um --momento <= {drop:.2f}")
grade = [round(t - ms, 2) for t, s in b if t >= ms and t - ms <= a.ate]
periodo = round((b[-1][0] - b[0][0]) / max(1, len(b) - 1), 3)
print(f"entrada forte da trilha: {drop:.3f}s  ->  data-media-start=\"{ms}\"  (cai em {a.momento}s do vídeo)")
print(f"batida a cada ~{periodo}s ({round(60 / periodo, 1)} BPM)")
print("batidas no vídeo:", grade)
