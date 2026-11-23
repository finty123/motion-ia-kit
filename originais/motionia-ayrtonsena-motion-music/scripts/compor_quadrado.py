"""Quadrado dentro do vertical (estilo See You Again): o clipe 1:1 no meio e a MESMA cena ampliada, borrada,
escurecida e com retícula em cima e embaixo. Mantém o áudio.
Uso: python compor_quadrado.py quadrado.mp4 saida_vertical.mp4 [--escuro 0.45] [--blur 18]"""
import sys as _s; _s.stdout.reconfigure(encoding='utf-8', errors='replace')  # acentos certos no console do Windows
import os, argparse, subprocess
from PIL import Image, ImageDraw
ap = argparse.ArgumentParser(); ap.add_argument('entrada'); ap.add_argument('saida')
ap.add_argument('--escuro', type=float, default=0.45, help='0 = sem escurecer, 1 = preto'); ap.add_argument('--blur', type=int, default=18)
A = ap.parse_args()
W, H = 1080, 1920
cache = os.path.join(os.path.dirname(os.path.abspath(A.saida)), '_cache'); os.makedirs(cache, exist_ok=True)
dots = os.path.join(cache, '_reticula.png')
im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
for y in range(0, H, 10):
    for x in range((y // 10 % 2) * 5, W, 10): d.ellipse([x - 2.6, y - 2.6, x + 2.6, y + 2.6], fill=(0, 0, 0, 120))
im.save(dots)
fc = (f"[0:v]scale={W}:{W}[sq];[0:v]scale={H}:{H},crop={W}:{H},boxblur={A.blur}:2,"
      f"eq=brightness={-A.escuro * 0.5:.2f}:saturation=1.1[bg];[bg][1:v]overlay=0:0[bgd];"
      f"[bgd][sq]overlay=0:{(H - W) // 2},format=yuv420p[v]")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A.entrada, '-i', dots, '-filter_complex', fc, '-map', '[v]', '-map', '0:a?',
                '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-c:a', 'copy', '-movflags', '+faststart', A.saida], check=True)
print('ok', A.saida)
