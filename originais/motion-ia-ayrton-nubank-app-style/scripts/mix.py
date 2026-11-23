"""Mixa o áudio do comercial num arquivo só: narração na frente, música abaixada com sidechain da voz
e SFX de UI presos às ações da tela. Uma trilha única evita o mixer do HyperFrames abaixando tudo.

Uso:
  python mix.py PROJETO --duracao 35.5 --musica-offset 3.88 [--cues PROJETO/cues.json]
                [--sfx "D:\\Backup\\Videos\\Edição de video\\SFX\\Ui"] [--sobe-musica 30.5]

Lê PROJETO/assets/narracao.(mp3|wav) e PROJETO/assets/musica.(mp3|wav); grava PROJETO/assets/mix.wav (-14 LUFS, -1 dBTP).
cues.json: {"cues": [{"t": 2.16, "arquivo": "Pop-up (1).wav", "ganho_db": -4, "max_s": 1.6}, ...]}
Precisa de numpy, soundfile e ffmpeg no PATH."""
import argparse, json, subprocess, sys
from pathlib import Path
import numpy as np
import soundfile as sf

SR = 48000
SFX_PADRAO = r"D:\Backup\Videos\Edição de video\SFX\Ui"


def load(path, start=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start), "-i", str(path)]
    if dur: cmd += ["-t", str(dur)]
    cmd += ["-f", "f32le", "-ac", "2", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()


def db(x): return 10 ** (x / 20)


def achar(pasta, nome):
    for ext in (".mp3", ".wav", ".m4a"):
        p = pasta / f"{nome}{ext}"
        if p.exists(): return p
    sys.exit(f"faltou {pasta / nome}.mp3|wav")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("projeto"); ap.add_argument("--duracao", type=float, required=True)
    ap.add_argument("--musica-offset", type=float, default=0.0, help="segundo da faixa que toca no 0 do vídeo")
    ap.add_argument("--cues"); ap.add_argument("--sfx", default=SFX_PADRAO)
    ap.add_argument("--musica-db", type=float, default=-17, help="nível da música sob a voz")
    ap.add_argument("--sobe-musica", type=float, default=None, help="a partir daqui a música sobe 6 dB (depois da última fala)")
    a = ap.parse_args()
    root, n = Path(a.projeto), int(a.duracao * SR)
    narr = np.zeros((n, 2), np.float32); v = load(achar(root / "assets", "narracao")); narr[: min(n, len(v))] = v[:n]
    mus = np.zeros((n, 2), np.float32); m = load(achar(root / "assets", "musica"), a.musica_offset, a.duracao); mus[: len(m)] = m[:n]
    sfx = np.zeros((n, 2), np.float32)
    cues = json.load(open(a.cues or root / "cues.json", encoding="utf-8"))["cues"]
    for c in cues:
        x = load(Path(a.sfx) / c["arquivo"], 0, c.get("max_s"))
        if c.get("max_s"):
            k = min(len(x), int(0.12 * SR)); x[-k:] *= np.linspace(1, 0, k)[:, None]
        x *= db(-6) / max(1e-6, np.abs(x).max()) * db(c.get("ganho_db", -8))
        i = int(c["t"] * SR); j = min(n, i + len(x))
        if j > i: sfx[i:j] += x[: j - i]
    # sidechain: a música abaixa onde tem voz
    env = np.abs(narr).max(1); win = int(0.25 * SR)
    env = np.convolve(env, np.ones(win) / win, "same")
    duck = 1 - 0.55 * np.clip(env / (env.max() * 0.25 + 1e-9), 0, 1)
    t = np.arange(n) / SR
    base = np.full(n, db(a.musica_db))
    if a.sobe_musica is not None: base = np.where(t < a.sobe_musica, db(a.musica_db), db(a.musica_db + 6))
    base *= np.clip(t / 0.6, 0, 1) * np.clip((a.duracao - t) / 1.6, 0, 1)
    mix = narr + mus * (base * duck)[:, None] + sfx
    raw = root / "assets" / "mix-raw.wav"; sf.write(raw, mix, SR, subtype="FLOAT")
    out = root / "assets" / "mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1:LRA=11", "-ar", str(SR), "-c:a", "pcm_s16le", str(out)], check=True)
    raw.unlink(missing_ok=True)
    print("ok", out)


if __name__ == "__main__":
    main()
