"""Analisa e recorta a música do clipe (trecho, cortes de compasso) e gera beats.json no tempo do vídeo.
1) Análise:  python3 musica.py analisar trilha.mp3
   -> BPM, batidas e MARCOS (onde a energia sobe/cai). Use pra alinhar: batida entrando na palavra de impacto, queda no preço etc.
2) Edição:   python3 musica.py editar trilha.mp3 saida_dir --offset 0.96 [--cortar 59.65:65.85]
   --offset: pula X s do começo da música (adianta tudo)
   --cortar: remove um trecho (tempo ORIGINAL; use múltiplos de compasso = 4 batidas) com crossfade de 30 ms
   -> saida_dir/musica-editada.wav e saida_dir/beats.json (batidas já no tempo do vídeo)"""
import sys as _s; _s.stdout.reconfigure(encoding='utf-8', errors='replace')  # acentos certos no console do Windows
import os, sys, json, argparse, subprocess, numpy as np, soundfile as sf, librosa
ap = argparse.ArgumentParser(); ap.add_argument('modo', choices=['analisar', 'editar']); ap.add_argument('musica'); ap.add_argument('out', nargs='?')
ap.add_argument('--offset', type=float, default=0.0); ap.add_argument('--cortar', default=''); ap.add_argument('--ate', type=float, default=0.0, help='termina a música neste tempo ORIGINAL (s) — use pra pegar só o trecho')
A = ap.parse_args()
CACHE = os.path.join(os.path.abspath(A.out) if A.out else os.path.dirname(os.path.abspath(A.musica)), '_cache'); os.makedirs(CACHE, exist_ok=True)
if A.out: os.makedirs(A.out, exist_ok=True)
_tmp = os.path.join(CACHE, '_ana.wav'); subprocess.run(['ffmpeg','-y','-v','error','-i',A.musica,'-ac','1','-ar','22050',_tmp], check=True)  # librosa não lê m4a/mp4 no Windows
y, sr = librosa.load(_tmp, sr=22050)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time'); beats = np.array(beats)
if A.modo == 'analisar':
    print('BPM ~', float(np.atleast_1d(tempo)[0]), '| batida a cada', round(float(np.median(np.diff(beats))), 3), 's | duração', round(len(y) / sr, 1), 's')
    rms = librosa.feature.rms(y=y)[0]; tt = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
    sec = [float(rms[(tt >= s) & (tt < s + 1)].mean()) for s in range(int(len(y) / sr))]
    print('energia por segundo:', ' '.join(f'{i}:{v:.2f}' for i, v in enumerate(sec)))
    for i in range(2, len(sec)):
        base = np.mean(sec[max(0, i - 3):i])
        if sec[i] > base * 1.4 and sec[i] > 0.15: print(f'  SOBE em ~{i}s ({base:.2f} -> {sec[i]:.2f})')
        if sec[i] < base * 0.5 and base > 0.15: print(f'  CAI  em ~{i}s ({base:.2f} -> {sec[i]:.2f})')
    sys.exit()
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A.musica, '-ar', '48000', '-ac', '2', os.path.join(CACHE, '_m.wav')], check=True)
m, SR = sf.read(os.path.join(CACHE, '_m.wav')); o = int(A.offset * SR)
if A.cortar:
    a, b = [float(v) for v in A.cortar.split(':')]; ia, ib, xf = int(a * SR), int(b * SR), int(0.03 * SR)
    P1, P2 = m[o:ia].copy(), m[ib:].copy(); fo = np.linspace(1, 0, xf)[:, None]; P1[-xf:] = P1[-xf:] * fo + P2[:xf] * (1 - fo); m2 = np.concatenate([P1, P2[xf:]]); L = b - a
else: m2 = m[o:]; a = b = 1e9; L = 0
nb = [round(float(x - A.offset if x < a else x - A.offset - L), 3) for x in beats if (x < a or x >= b) and x - A.offset >= 0]
if A.ate:
    fim = A.ate - A.offset - (L if A.ate >= b else 0); m2 = m2[:int(fim * SR)]; nb = [x for x in nb if x < fim]
sf.write(f'{A.out}/musica-editada.wav', m2, SR); json.dump(nb, open(f'{A.out}/beats.json', 'w'))
print('ok', round(len(m2) / SR, 1), 's de música; batidas:', len(nb))
