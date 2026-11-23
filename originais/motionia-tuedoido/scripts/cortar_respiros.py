"""Corta os respiros (silêncios) da narração e remapeia os tempos das palavras.
Uso: python3 cortar_respiros.py narracao.mp3 words.json saida_dir [--gap 0.15] [--keep "48:0.75,209:0.95"]
--gap : quanto silêncio sobra entre frases (padrão 0.15 s)
--keep: depois da palavra de índice N, deixa X s de pausa (respiro intencional: preço, CTA, momento de impacto)
Gera saida_dir/narracao-cortada.wav e saida_dir/words.json"""
import sys, json, argparse, subprocess, numpy as np, soundfile as sf
ap = argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('words'); ap.add_argument('out'); ap.add_argument('--gap', type=float, default=0.15); ap.add_argument('--keep', default=''); ap.add_argument('--thr', type=float, default=0.02); ap.add_argument('--min', type=float, default=0.28)
A = ap.parse_args()
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A.audio, '-ar', '48000', '-ac', '1', '/tmp/_n.wav'], check=True)
y, sr = sf.read('/tmp/_n.wav'); W = json.load(open(A.words))
keep = {int(k): float(v) for k, v in (p.split(':') for p in A.keep.split(',') if ':' in p)}
fr = int(0.01 * sr); env = np.sqrt(np.convolve(y ** 2, np.ones(fr) / fr, 'same'))[::fr]
runs, s = [], None
for i, q in enumerate(env < A.thr):
    if q and s is None: s = i
    if not q and s is not None:
        if (i - s) / 100 >= A.min: runs.append((s / 100, i / 100))
        s = None
ops = []  # (pos, remove_len) or insert silence
for a, b in runs:
    if a < 0.05: continue
    if any(a + 0.04 < w[0] < b - 0.04 for w in W): continue
    prev = max([i for i, w in enumerate(W) if w[0] < a] or [-1])
    want = keep.get(prev, A.gap); have = b - a
    if have > want: ops.append(('cut', a + want * 0.55, b - want * 0.45))
    elif want > have: ops.append(('ins', b - 0.02, want - have))
ops.sort(key=lambda o: o[1])
out, prev, T, tmap = [], 0.0, 0.0, []
f = int(0.008 * sr)
def push(a, b):
    global T
    seg = y[int(a * sr):int(b * sr)].copy()
    if len(seg) > 2 * f: seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    tmap.append((a, b, T)); out.append(seg); T += len(seg) / sr
for o in ops:
    if o[0] == 'cut': push(prev, o[1]); prev = o[2]
    else: push(prev, o[1]); prev = o[1]; out.append(np.zeros(int(o[2] * sr))); T += o[2]
push(prev, len(y) / sr)
def m(t):
    for a, b, T0 in tmap:
        if a - 1e-6 <= t <= b + 1e-6: return T0 + (t - a)
    for a, b, T0 in tmap:
        if t < a: return T0
    return tmap[-1][2] + tmap[-1][1] - tmap[-1][0]
W2 = [[round(m(a), 3), round(m(b), 3), t] for a, b, t in W]
sf.write(f'{A.out}/narracao-cortada.wav', np.concatenate(out), sr); json.dump(W2, open(f'{A.out}/words.json', 'w'), ensure_ascii=False)
print('duração', round(T, 2), 's (antes', round(len(y) / sr, 2), ')')
print(' '.join(f'{i}:{t}@{a}' for i, (a, b, t) in enumerate(W2)))
