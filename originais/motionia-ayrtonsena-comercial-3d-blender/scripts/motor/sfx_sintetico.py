# Efeitos sonoros sinteticos (plano B quando a pessoa nao tem pasta de SFX): so sons cinematograficos,
# nada de blip/pop/laser. Gera assets/sfx/<tipo>.wav pra cada tipo que ainda nao existe.
# Uso: python sfx_sintetico.py
import subprocess
from pathlib import Path
import numpy as np

AQUI = Path(__file__).resolve().parent
SR = 48000
OUT = AQUI / "assets" / "sfx"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(3)


def t(d):
    return np.arange(int(d * SR)) / SR


def passa_baixa(x, corte):
    """filtro simples de 1 polo, corte pode variar no tempo (array)"""
    corte = np.broadcast_to(corte, x.shape)
    y, acc = np.empty_like(x), 0.0
    a = np.exp(-2 * np.pi * corte / SR)
    for i in range(len(x)):
        acc = a[i] * acc + (1 - a[i]) * x[i]
        y[i] = acc
    return y


def whoosh(d=1.1, grave=False):
    tt = t(d)
    env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 2.2
    pico = 0.62
    env *= np.exp(-((tt / d - pico) ** 2) / 0.05)
    ruido = rng.standard_normal(len(tt))
    corte = (300 if grave else 900) + (2600 if grave else 6500) * np.exp(-((tt / d - pico) ** 2) / 0.02)
    x = passa_baixa(ruido, corte) * env
    if grave:
        x += 0.5 * np.sin(2 * np.pi * (55 - 20 * tt / d) * tt) * env
    return x


def boom(d=2.0):
    tt = t(d)
    sub = np.sin(2 * np.pi * (70 * np.exp(-tt * 3) + 32) * tt) * np.exp(-tt * 2.2)
    ruido = passa_baixa(rng.standard_normal(len(tt)), 900 * np.exp(-tt * 6) + 120) * np.exp(-tt * 5)
    ataque = np.minimum(1, tt / 0.004)
    return (sub + 0.6 * ruido) * ataque


def clique(d=0.25):
    tt = t(d)
    a = passa_baixa(rng.standard_normal(len(tt)), 5000) * np.exp(-tt * 90)
    b = np.roll(passa_baixa(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 70), int(0.06 * SR)) * 0.7
    return a + b


def spot(d=0.6):
    tt = t(d)
    estalo = passa_baixa(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 120)
    corpo = np.sin(2 * np.pi * 95 * tt) * np.exp(-tt * 9) * 0.5
    return estalo + corpo


def soco(d=0.6):
    tt = t(d)
    return (np.sin(2 * np.pi * (120 * np.exp(-tt * 18) + 45) * tt) * np.exp(-tt * 10)
            + 0.5 * passa_baixa(rng.standard_normal(len(tt)), 1500) * np.exp(-tt * 40))


def lamina(d=1.4):
    tt = t(d)
    tom = sum(np.sin(2 * np.pi * f * tt + rng.uniform(0, 6)) for f in (2300, 3410, 5120)) / 3
    raspa = passa_baixa(rng.standard_normal(len(tt)), 7000) * np.exp(-((tt - 0.05) ** 2) / 0.002)
    return tom * np.exp(-tt * 3.5) * np.minimum(1, tt / 0.01) * 0.6 + raspa * 0.5


TIPOS = {"whoosh_grave": lambda: whoosh(1.4, True), "whoosh": whoosh, "whoosh_corredor": lambda: whoosh(1.6),
         "boom": boom, "clique": clique, "spot": spot, "soco": soco, "lamina": lamina}
for nome, fn in TIPOS.items():
    p = OUT / f"{nome}.wav"
    if p.exists():
        continue
    x = fn()
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    est = np.stack([x, np.roll(x, 40)], axis=1).astype(np.float32)   # leve abertura estereo
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(p)],
                   input=est.tobytes(), check=True)
    print("gerado", p.name)
