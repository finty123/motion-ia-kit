"""Deixa a voz clara (áudio de WhatsApp / celular costuma vir abafado) e mostra o antes/depois por faixa.

Uso: python voz_clara.py narracao.wav narracao-clara.wav
Meta: presença (2-6 kHz) ~6-9 dB abaixo dos médios; antes disso a voz soa abafada.
Se o resultado ficar agudo/chiado, baixe os ganhos de 3200/5200 Hz e o highshelf em 2 dB.
"""
import re, subprocess, sys

CADEIA = ("highpass=f=85,equalizer=f=250:t=q:w=1.0:g=-4,equalizer=f=3200:t=q:w=0.9:g=7,"
          "equalizer=f=5200:t=q:w=1.2:g=5,highshelf=f=7000:g=5,aexciter=amount=1.2:drive=4:freq=3500:blend=0,"
          "acompressor=threshold=-22dB:ratio=3:attack=5:release=90:makeup=3,alimiter=limit=0.89:level=false")
FAIXAS = {"graves <300": "lowpass=f=300", "médios 300-2k": "highpass=f=300,lowpass=f=2000",
          "presença 2-6k": "highpass=f=2000,lowpass=f=6000", "brilho >6k": "highpass=f=6000"}

def bandas(arq):
    out = {}
    for nome, f in FAIXAS.items():
        r = subprocess.run(["ffmpeg", "-i", arq, "-af", f + ",volumedetect", "-f", "null", "-"], capture_output=True, text=True)
        m = re.search(r"mean_volume: ([-0-9.]+)", r.stderr); out[nome] = float(m.group(1)) if m else None
    return out

ent, sai = sys.argv[1], sys.argv[2]
antes = bandas(ent)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ent, "-af", CADEIA, "-ar", "48000", sai], check=True)
depois = bandas(sai)
for k in FAIXAS:
    print(f"{k:15s} antes {antes[k]:6.1f} dB   depois {depois[k]:6.1f} dB")
print("presença vs médios: antes", round(antes["presença 2-6k"] - antes["médios 300-2k"], 1), "dB / depois",
      round(depois["presença 2-6k"] - depois["médios 300-2k"], 1), "dB")
