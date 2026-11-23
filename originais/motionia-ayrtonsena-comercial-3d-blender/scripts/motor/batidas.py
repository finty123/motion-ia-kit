# Grade de batidas da trilha (sem librosa): envelope de onset por fluxo espectral,
# BPM por autocorrelacao, fase das batidas, forca de cada batida, PAUSAS (onde a musica cai e volta forte)
# e o trecho mais forte com o tamanho do video.
# Uso: python batidas.py <musica.mp3> [batidas do video, padrao 44]  -> beats.json
import json, subprocess, sys
from pathlib import Path
import numpy as np

AQUI = Path(__file__).resolve().parent
SR, HOP, NFFT = 22050, 512, 2048

wav = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(wav, dtype=np.float32)
dur = len(x) / SR

# espectrograma -> fluxo espectral (so aumentos), separado em graves (kick) e geral
quadros = 1 + (len(x) - NFFT) // HOP
janela = np.hanning(NFFT).astype(np.float32)
idx = np.arange(NFFT)[None, :] + HOP * np.arange(quadros)[:, None]
S = np.abs(np.fft.rfft(x[idx] * janela, axis=1))
S = np.log1p(100 * S)
freqs = np.fft.rfftfreq(NFFT, 1 / SR)
fluxo = np.maximum(0, np.diff(S, axis=0))
onset = fluxo.sum(axis=1)
grave = fluxo[:, freqs[:-0 or None][:fluxo.shape[1]] < 150].sum(axis=1)
fps_env = SR / HOP


def normaliza(v):
    v = v - np.convolve(v, np.ones(16) / 16, mode="same")
    v = np.maximum(v, 0)
    return v / (v.max() + 1e-9)


onset, grave = normaliza(onset), normaliza(grave)

# BPM: autocorrelacao do envelope entre 80 e 180 BPM, preferindo a faixa 90-140
ac = np.correlate(onset, onset, mode="full")[len(onset) - 1:]
lags = np.arange(len(ac))
bpms = 60 * fps_env / np.maximum(lags, 1)
faixa = (bpms > 80) & (bpms < 180)
peso = np.exp(-0.5 * (np.log2(bpms / 120) / 0.6) ** 2)
melhor = lags[faixa][np.argmax((ac * peso)[faixa])]
# refina com parabola
a, b, c = ac[melhor - 1], ac[melhor], ac[melhor + 1]
lag_fino = melhor + 0.5 * (a - c) / (a - 2 * b + c)
bpm = 60 * fps_env / lag_fino
periodo = 60 / bpm

# fase: desloca uma grade e escolhe a que soma mais onset (com peso extra no grave)
env = onset + 1.5 * grave
t_env = (np.arange(len(env)) + 1) * HOP / SR
fases = np.linspace(0, periodo, 200, endpoint=False)
def soma(f):
    tb = np.arange(f, dur, periodo)
    return np.interp(tb, t_env, env).sum()
fase = fases[np.argmax([soma(f) for f in fases])]
batidas = np.arange(fase, dur - 0.05, periodo)

# forca de cada batida (energia RMS em volta) e tempo forte: o compasso comeca onde o grave e mais forte
rms = np.sqrt(np.convolve(x ** 2, np.ones(HOP) / HOP, mode="same"))[::HOP]
t_rms = np.arange(len(rms)) * HOP / SR
forca = np.interp(batidas, t_rms, rms)
g_b = np.interp(batidas, t_env, grave)
offset = int(np.argmax([g_b[k::4].sum() for k in range(4)]))
batidas = batidas[offset:]
forca, g_b = forca[offset:], g_b[offset:]

# trecho do tamanho do video com mais energia e com um aumento forte no comeco (gancho)
NB = int(sys.argv[2]) if len(sys.argv) > 2 else 44
melhor_ini, melhor_nota = 0, -1
for ini in range(0, max(1, len(batidas) - NB), 4):
    bloco = forca[ini:ini + NB]
    nota = bloco.mean() + 0.6 * bloco[:8].mean() - 0.4 * bloco.std()
    if nota > melhor_nota:
        melhor_ini, melhor_nota = ini, nota

# pausas: a energia cai bem abaixo do que vinha (break/respiro) e volta forte em ate 4 batidas.
# E nelas que entram os momentos grandes (a camera entrando no furo cai na pausa, o corredor na volta).
fn = forca / (forca.max() + 1e-9)
pausas, k = [], 8
while k < len(fn) - 4:
    antes = np.median(fn[k - 8:k])
    if antes > 0.25 and fn[k] < 0.5 * antes:
        volta = next((j for j in range(k + 1, min(len(fn), k + 5)) if fn[j] > 0.85 * antes), None)
        if volta:
            pausas.append({"batida": int(k), "tempo": round(float(batidas[k]), 3),
                           "volta_batida": int(volta), "volta_tempo": round(float(batidas[volta]), 3),
                           "queda": round(float(1 - fn[k] / antes), 2)})
            k = volta + 4
            continue
    k += 1

saida = {
    "musica": Path(sys.argv[1]).name, "duracao": round(dur, 3), "bpm": round(bpm, 2), "periodo": round(periodo, 4),
    "batidas": [round(float(t), 4) for t in batidas],
    "forca": [round(float(v), 4) for v in forca / forca.max()],
    "grave": [round(float(v), 4) for v in g_b],
    "trecho_sugerido": {"batida_inicial": melhor_ini, "inicio_s": round(float(batidas[melhor_ini]), 3),
                        "fim_s": round(float(batidas[min(len(batidas) - 1, melhor_ini + NB)]), 3)},
    "pausas": pausas,
}
(AQUI / "beats.json").write_text(json.dumps(saida, indent=1), encoding="utf-8")
print(f"duracao {dur:.1f}s  BPM {bpm:.2f}  periodo {periodo:.3f}s  batidas {len(batidas)}")
print("trecho sugerido:", saida["trecho_sugerido"])
print("pausas (cai e volta forte):", [(p_["tempo"], p_["volta_tempo"]) for p_ in pausas] or "nenhuma clara")

# energia por compasso, pra eu escolher o trecho olhando
comp = [forca[i:i + 4].mean() for i in range(0, len(forca) - 4, 4)]
for i in range(0, len(comp), 8):
    linha = " ".join(f"{v / max(comp):.2f}" for v in comp[i:i + 8])
    print(f"compasso {i + 1:3d} ({batidas[i * 4]:6.1f}s): {linha}")
