"""Letra cantada -> words_raw.json [[inicio, fim, "palavra"], ...] (faster-whisper, tempo por palavra).
Uso: python transcrever_letra.py musica.m4a saida/words_raw.json [--modelo large-v3] [--lingua en] [--fix "errado=certo"]
Música cantada engana o Whisper: use large-v3 (o medium errou palavras e tempos no Training Season).
Os tempos ainda podem vir até ~0,6 s fora; o analisar_musica.py prende cada palavra no ataque da voz."""
import sys as _s; _s.stdout.reconfigure(encoding='utf-8', errors='replace')  # acentos certos no console do Windows
import os, json, subprocess, argparse
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('out'); ap.add_argument('--modelo', default='large-v3')
ap.add_argument('--lingua', default=None, help='en, pt, es... (vazio = detecta)'); ap.add_argument('--fix', default=''); ap.add_argument('--prompt', default='')
A = ap.parse_args()
cache = os.path.join(os.path.dirname(os.path.abspath(A.out)), '_cache'); os.makedirs(cache, exist_ok=True)
tmp = os.path.join(cache, '_letra.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A.audio, '-ar', '16000', '-ac', '1', tmp], check=True)
import soundfile as sf
from faster_whisper import WhisperModel
audio = sf.read(tmp, dtype='float32')[0]   # passa o array: o av.open do faster-whisper quebra com m4a em algumas versões
m = WhisperModel(A.modelo, device='cpu', compute_type='int8')
segs, info = m.transcribe(audio, language=A.lingua, word_timestamps=True, vad_filter=False, beam_size=5, initial_prompt=A.prompt or None)
fix = dict(p.split('=', 1) for p in A.fix.split(',') if '=' in p)
W = []
for s in segs:
    for w in s.words:
        t = w.word.strip(); W.append([round(w.start, 3), round(w.end, 3), fix.get(t, t)])
json.dump(W, open(A.out, 'w', encoding='utf-8'), ensure_ascii=False)
print('língua:', info.language)
print(' '.join(f'{i}:{t}@{a:.2f}' for i, (a, b, t) in enumerate(W)))
