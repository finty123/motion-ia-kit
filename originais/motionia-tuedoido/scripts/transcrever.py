"""Narração -> words.json [[inicio, fim, "palavra"], ...] com tempo por palavra (faster-whisper).
Uso: python3 transcrever.py narracao.mp3 saida/words.json [--modelo small|medium] [--fix "caldo=Claude,pronto=prompt"]
Instala se faltar: pip install faster-whisper soundfile --break-system-packages"""
import sys, json, subprocess, argparse
ap = argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('out'); ap.add_argument('--modelo', default='small'); ap.add_argument('--fix', default=''); ap.add_argument('--prompt', default='')
A = ap.parse_args()
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A.audio, '-ar', '16000', '-ac', '1', '/tmp/_tr.wav'], check=True)
import soundfile as sf
from faster_whisper import WhisperModel
m = WhisperModel(A.modelo, device='cpu', compute_type='int8')
segs, _ = m.transcribe(sf.read('/tmp/_tr.wav', dtype='float32')[0], language='pt', word_timestamps=True, initial_prompt=A.prompt or None)
fix = dict(p.split('=', 1) for p in A.fix.split(',') if '=' in p)
W = []
for s in segs:
    for w in s.words:
        t = w.word.strip(); W.append([round(w.start, 3), round(w.end, 3), fix.get(t, t)])
json.dump(W, open(A.out, 'w'), ensure_ascii=False)
print(' '.join(f'{i}:{t}@{a}' for i, (a, b, t) in enumerate(W)))
