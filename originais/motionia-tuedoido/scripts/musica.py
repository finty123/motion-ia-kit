"""Analisa e edita a trilha para casar com a narração.
1) Análise:  python3 musica.py analisar trilha.mp3
   -> BPM, batidas e MARCOS (onde a energia sobe/cai). Use pra alinhar: batida entrando na palavra de impacto, queda no preço etc.
2) Edição:   python3 musica.py editar trilha.mp3 saida_dir --offset 0.96 [--cortar 59.65:65.85]
   --offset: pula X s do começo da música (adianta tudo)
   --cortar: remove um trecho (tempo ORIGINAL; use múltiplos de compasso = 4 batidas) com crossfade de 30 ms
   -> saida_dir/musica-editada.wav e saida_dir/beats.json (batidas já no tempo do vídeo)"""
import sys, json, argparse, subprocess, numpy as np, soundfile as sf, librosa
ap = argparse.ArgumentParser(); ap.add_argument('modo', choices=['analisar', 'editar']); ap.add_argument('musica'); ap.add_argument('out', nargs='?')
ap.add_argument('--offset', type=float, default=0.0); ap.add_argument('--cortar', default='')
A = ap.parse_args()
y, sr = librosa.load(A.musica, sr=22050)
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
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A.musica, '-ar', '48000', '-ac', '2', '/tmp/_m.wav'], check=True)
m, SR = sf.read('/tmp/_m.wav'); o = int(A.offset * SR)
if A.cortar:
    a, b = [float(v) for v in A.cortar.split(':')]; ia, ib, xf = int(a * SR), int(b * SR), int(0.03 * SR)
    P1, P2 = m[o:ia].copy(), m[ib:].copy(); fo = np.linspace(1, 0, xf)[:, None]; P1[-xf:] = P1[-xf:] * fo + P2[:xf] * (1 - fo); m2 = np.concatenate([P1, P2[xf:]]); L = b - a
else: m2 = m[o:]; a = b = 1e9; L = 0
nb = [round(float(x - A.offset if x < a else x - A.offset - L), 3) for x in beats if (x < a or x >= b) and x - A.offset >= 0]
sf.write(f'{A.out}/musica-editada.wav', m2, SR); json.dump(nb, open(f'{A.out}/beats.json', 'w'))
print('ok', round(len(m2) / SR, 1), 's de música; batidas:', len(nb))
