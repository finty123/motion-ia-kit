"""Remonta a narração a partir do áudio bruto: mesmos trechos (takes), só muda ONDE cada um começa.
Nunca corta palavra: os cortes têm que cair em silêncio (confira com silencedetect antes).

Uso: python remontar_narracao.py bruto.wav takes.json saida.wav --total 46.2
takes.json: [{"de": 0.36, "ate": 4.15, "em": 0.06}, ...]   (segundos do bruto, segundo do vídeo)
Dica: uma fala com pausas pode virar 2-3 trechos (cortados nas pausas) pra cada palavra-chave cair numa batida.
"""
import argparse, json, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("bruto"); ap.add_argument("takes"); ap.add_argument("saida")
ap.add_argument("--total", type=float, required=True)
a = ap.parse_args()
T = json.load(open(a.takes, encoding="utf8"))
cmd = ["ffmpeg", "-v", "error", "-y"]
filtros, nomes = [], []
for i, t in enumerate(T):
    cmd += ["-ss", str(t["de"]), "-to", str(t["ate"]), "-i", a.bruto]
    ms = int(round(t["em"] * 1000)); dur = t["ate"] - t["de"]
    filtros.append(f"[{i}:a]aformat=channel_layouts=mono,afade=t=in:d=0.01,afade=t=out:st={dur - 0.012:.3f}:d=0.012,adelay={ms}|{ms}[a{i}]")
    nomes.append(f"[a{i}]")
filtros.append("".join(nomes) + f"amix=inputs={len(T)}:normalize=0:duration=longest,apad=whole_dur={a.total},atrim=0:{a.total}")
cmd += ["-filter_complex", ";".join(filtros), "-ar", "48000", a.saida]
subprocess.run(cmd, check=True)
print("ok:", a.saida)
