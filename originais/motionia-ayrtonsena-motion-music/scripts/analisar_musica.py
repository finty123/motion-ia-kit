"""Raio-x da música pro motion music: BPM, batidas, BATIDAS FORTES (onde o grave volta/entra), RESPIROS
(onde a música esvazia), ataques da voz e a letra presa no ataque. Gera analise.json + partitura.png.
Uso: python analisar_musica.py musica.wav saida_dir [--words words_raw.json] [--ini 0] [--fim 0]

Por que existe: no Training Season o Whisper marcou o HOLD em 10,2 s, mas a batida que o ouvido sente
(o bumbo voltando) era 9,47 s. Quem manda é o que se OUVE: impacto principal = batida forte medida aqui."""
import sys as _s; _s.stdout.reconfigure(encoding='utf-8', errors='replace')  # acentos certos no console do Windows
import os, sys, json, argparse, subprocess
import numpy as np, librosa
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('out')
ap.add_argument('--words', default=''); ap.add_argument('--ini', type=float, default=0); ap.add_argument('--fim', type=float, default=0)
A = ap.parse_args(); os.makedirs(A.out, exist_ok=True)
os.makedirs(os.path.join(A.out, '_cache'), exist_ok=True); tmp = os.path.join(A.out, '_cache', '_raiox.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A.audio, '-ac', '1', '-ar', '22050', tmp], check=True)
y, sr = librosa.load(tmp, sr=22050)
if A.fim: y = y[:int(A.fim * sr)]
DUR = len(y) / sr
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time'); beats = [float(b) for b in beats]
bpm = float(np.atleast_1d(tempo)[0])

HOP = 256; S = np.abs(librosa.stft(y, hop_length=HOP)); f = librosa.fft_frequencies(sr=sr)
ft = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr, hop_length=HOP)
low, tot = S[f < 150].sum(0), S.sum(0)
step = 0.05; grid = np.arange(0, DUR, step)
def bins(x): return np.array([x[(ft >= g) & (ft < g + step)].mean() if np.any((ft >= g) & (ft < g + step)) else 0 for g in grid])
L, T = bins(low) / (low.mean() + 1e-9), bins(tot) / (tot.mean() + 1e-9)

# batidas fortes: grave salta bem acima do que vinha antes (volta do bumbo, drop, impacto)
hits = []
for i in range(6, len(grid)):
    prev = L[max(0, i - 8):i].mean()
    if L[i] > 1.8 and L[i] > prev * 2.2 and (not hits or grid[i] - hits[-1]['t'] > 0.35):
        fz = float(L[i] / (prev + 1e-6)); hits.append({'t': round(float(grid[i]), 2), 'forca': round(fz, 1), 'principal': fz >= 5})
if hits: max(hits, key=lambda h: h['forca'])['maior'] = True
# respiros: trecho de >= 0.8 s com energia bem abaixo da mediana
med = np.median(T); resp = []; a = None
for i, v in enumerate(T):
    if v < med * 0.55 and a is None: a = grid[i]
    if (v >= med * 0.55 or i == len(T) - 1) and a is not None:
        if grid[i] - a >= 0.8: resp.append([round(float(a), 2), round(float(grid[i]), 2)])
        a = None
# ataques da voz (banda média do harmônico)
yh = librosa.effects.harmonic(y, margin=4)
Sh = np.abs(librosa.stft(yh, hop_length=128)); fh = librosa.fft_frequencies(sr=sr)
e = np.log1p(Sh[(fh > 250) & (fh < 4000)]).sum(0); th = librosa.frames_to_time(np.arange(len(e)), sr=sr, hop_length=128)
d = np.maximum(0, np.diff(e, prepend=e[0])); d = np.convolve(d, np.ones(3) / 3, 'same'); thr = np.percentile(d, 85)
voz = [round(float(th[i]), 2) for i in range(1, len(d) - 1) if d[i] > thr and d[i] >= d[i - 1] and d[i] >= d[i + 1]]

words = []
if A.words and os.path.exists(A.words):
    # prende cada palavra no ataque da voz mais próximo, EM ORDEM e sem duas palavras no mesmo ataque
    raw = [x for x in json.load(open(A.words, encoding='utf-8')) if not (A.fim and x[0] > A.fim)]
    en = (e - e.min()) / (e.max() - e.min() + 1e-9); thrE = np.percentile(en, 40)
    last = -1.0
    for k, (a0, b0, w) in enumerate(raw):
        cands = [v for v in voz if abs(v - a0) <= 0.25 and v > last + 0.04]
        snap = min(cands, key=lambda v: abs(v - a0)) if cands else max(a0, last + 0.05)
        last = snap
        # sílaba segurada: a voz continua soando até bem depois do início (nota longa, "I" esticado, "ooooh")
        prox = raw[k + 1][0] if k + 1 < len(raw) else DUR
        i0 = np.searchsorted(th, snap + 0.15); fimv = snap; baixo = 0
        for j in range(i0, len(th)):
            if th[j] >= prox - 0.05: fimv = th[j]; break
            baixo = baixo + 1 if en[j] < thrE else 0
            if baixo * (th[1] - th[0]) >= 0.15: fimv = th[j]; break
            fimv = th[j]
        words.append({'w': w, 'whisper': a0, 't': round(float(snap), 2), 'fim': b0, 'fim_voz': round(float(fimv), 2), 'segura': bool(fimv - snap >= 1.0)})
an = {'bpm': round(bpm, 2), 'batida_s': round(60 / bpm, 3), 'dur': round(DUR, 2), 'beats': [round(b, 3) for b in beats],
      'batidas_fortes': hits, 'respiros': resp, 'ataques_voz': voz, 'palavras': words}
json.dump(an, open(os.path.join(A.out, 'analise.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- partitura.png: uma linha a cada 8 s ----------
ROW, PX, HR = 8.0, 260, 230   # 8 s por linha, 260 px por segundo
nrows = int(np.ceil(DUR / ROW)); img = Image.new('RGB', (int(ROW * PX) + 80, nrows * HR + 60), '#111')
dr = ImageDraw.Draw(img)
try: fnt = ImageFont.truetype('arial.ttf', 15); fb = ImageFont.truetype('arialbd.ttf', 17)
except Exception: fnt = fb = ImageFont.load_default()
dr.text((10, 12), f'BPM {bpm:.1f} | batida {60 / bpm:.3f}s | vermelho = batida forte (grossa = principal) | azul = respiro | cinza = energia | rosa = grave | amarelo = sílaba segurada | linha clara = a cada 4 batidas (contadas do início, não é o tempo 1 real)', fill='#ddd', font=fb)
for r in range(nrows):
    y0 = 50 + r * HR; t0 = r * ROW
    X = lambda t: 60 + (t - t0) * PX
    for a0, b0 in resp:
        if b0 > t0 and a0 < t0 + ROW: dr.rectangle([X(max(a0, t0)), y0, X(min(b0, t0 + ROW)), y0 + 150], fill='#13304a')
    for i, g in enumerate(grid):
        if t0 <= g < t0 + ROW:
            dr.line([X(g), y0 + 150, X(g), y0 + 150 - min(140, T[i] * 45)], fill='#555', width=12)
            dr.line([X(g), y0 + 150, X(g), y0 + 150 - min(140, L[i] * 25)], fill='#c2185b', width=5)
    for k, b in enumerate(beats):
        if t0 <= b < t0 + ROW: dr.line([X(b), y0, X(b), y0 + 150], fill='#888' if k % 4 else '#eee', width=1)
    for v in voz:
        if t0 <= v < t0 + ROW: dr.line([X(v), y0 + 152, X(v), y0 + 162], fill='#7fd', width=2)
    for h in hits:
        if t0 <= h['t'] < t0 + ROW:
            dr.line([X(h['t']), y0 - 4, X(h['t']), y0 + 156], fill='#ff2d55' if h['principal'] else '#a33', width=6 if h['principal'] else 2); dr.text((X(h['t']) + 4, y0 - 2), f"{h['t']:.2f}" + (' MAIOR' if h.get('maior') else ''), fill='#ff2d55', font=fb)
    for k, wd in enumerate(words):
        if wd['segura'] and wd['fim_voz'] > t0 and wd['t'] < t0 + ROW: dr.rectangle([X(max(wd['t'], t0)), y0 + 163, X(min(wd['fim_voz'], t0 + ROW)), y0 + 166], fill='#ffd23f')
        if t0 <= wd['t'] < t0 + ROW: dr.text((X(wd['t']), y0 + 168 + (k % 3) * 17), f"{wd['w']} {wd['t']:.2f}" + (' (segura)' if wd['segura'] else ''), fill='#ffd23f' if wd['segura'] else '#fff', font=fnt)
    for s in range(int(t0), int(t0 + ROW) + 1): dr.text((X(s) - 6, y0 + 140), str(s), fill='#aaa', font=fnt)
img.save(os.path.join(A.out, 'partitura.png'))
print(f'BPM {bpm:.1f} | dur {DUR:.2f}s')
print('BATIDAS PRINCIPAIS (impacto grande aqui):', ' '.join(f"{h['t']}(x{h['forca']})" for h in hits if h['principal']))
print('batidas fortes menores:', ' '.join(f"{h['t']}" for h in hits if not h['principal']))
print('respiros:', resp)
print('palavras (presas no ataque da voz, em ordem):', ' '.join(f"{w['w']}@{w['t']}" + (f"~{w['fim_voz']}" if w['segura'] else '') for w in words))
print('maior batida:', [h['t'] for h in hits if h.get('maior')], '| sílabas seguradas:', [(w['w'], w['t'], w['fim_voz']) for w in words if w['segura']])
print('->', os.path.join(A.out, 'analise.json'), '+ partitura.png')
