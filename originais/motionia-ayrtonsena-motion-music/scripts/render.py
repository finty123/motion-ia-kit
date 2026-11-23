"""Render completo, em blocos RETOMÁVEIS (se a sessão cair, roda de novo que ele continua de onde parou).
Uso (em segundo plano!):  setsid nohup python3 render.py proj/index.html proj/video_mudo.mp4 > proj/render.log 2>&1 < /dev/null &
30 fps com motion blur real (2 subquadros). Acompanhe com: tail -1 proj/render.log"""
import sys as _s; _s.stdout.reconfigure(encoding='utf-8', errors='replace')  # acentos certos no console do Windows
import sys, os, base64, subprocess, time, glob
from playwright.sync_api import sync_playwright
html, out = sys.argv[1], sys.argv[2]; FPS = 30; CH = 150
d = os.path.join(os.path.dirname(os.path.abspath(out)), '_blocos'); os.makedirs(d, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--disable-gpu']); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto(__import__('pathlib').Path(html).resolve().as_uri()); pg.wait_for_function('window.READY', timeout=90000)
    END = pg.evaluate('END'); N = int(END * FPS); t0 = time.time()
    for c0 in range(0, N, CH):
        seg = os.path.join(d, f'{c0:06d}.mp4')
        if os.path.exists(seg): continue
        ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', seg + '.tmp.mp4'], stdin=subprocess.PIPE)
        for i in range(c0, min(N, c0 + CH)):
            data = pg.evaluate(f"(()=>{{frame({i / FPS},{1 / (2 * FPS)});return document.getElementById('c').toDataURL('image/jpeg',0.93)}})()")
            ff.stdin.write(base64.b64decode(data[23:]))
        ff.stdin.close(); ff.wait(); os.rename(seg + '.tmp.mp4', seg)
        print(min(N, c0 + CH), '/', N, 'quadros', round(time.time() - t0), 's', flush=True)
    b.close()
lst = os.path.join(d, 'lista.txt'); open(lst, 'w').write(''.join(f"file '{f}'\n" for f in sorted(glob.glob(os.path.join(d, '[0-9]*.mp4')))))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], check=True); print('PRONTO', out, flush=True)
