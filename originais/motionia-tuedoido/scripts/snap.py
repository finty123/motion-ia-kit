"""Renderiza quadros soltos e monta a FOLHA DE CONTATO pra conferir antes do render completo.
Uso: python3 snap.py proj/index.html proj/folha.jpg 0.5,1.3,2.6,...   (ou --cada 2.0)
Também salva proj/cues.json (todas as cues de som/impacto) e imprime END e erros do JS."""
import sys, base64, json, os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
html, out, arg = sys.argv[1], sys.argv[2], sys.argv[3]
with sync_playwright() as p:
    b = p.chromium.launch(args=['--disable-gpu']); W, H = 1920, 1080
    pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + os.path.abspath(html)); pg.wait_for_function('window.READY||window.ERR', timeout=90000)
    if pg.evaluate('window.ERR'): print('ERRO:', pg.evaluate('window.ERR')); sys.exit(1)
    end = pg.evaluate('typeof END!=="undefined"?END:0'); json.dump(pg.evaluate('CUES'), open(os.path.join(os.path.dirname(os.path.abspath(html)), 'cues.json'), 'w'))
    ts = [i * float(arg.split('=')[1] if '=' in arg else sys.argv[4]) for i in range(int(end / float(sys.argv[4])) + 1)] if arg == '--cada' else [float(x) for x in arg.split(',')]
    ims = []
    for t in ts:
        d = pg.evaluate(f"(()=>{{frame({t},0);return document.getElementById('c').toDataURL('image/jpeg',0.8)}})()")
        open('/tmp/_s.jpg', 'wb').write(base64.b64decode(d.split(',')[1])); ims.append((t, Image.open('/tmp/_s.jpg').convert('RGB').resize((480, 270))))
    b.close()
cols = 4; sh = Image.new('RGB', (cols * 480, ((len(ims) + cols - 1) // cols) * 294), '#222'); dr = ImageDraw.Draw(sh)
for i, (t, im) in enumerate(ims): x, y = (i % cols) * 480, (i // cols) * 294; sh.paste(im, (x, y + 24)); dr.text((x + 6, y + 6), f'{t:.2f}s', fill='white')
sh.save(out, quality=85); print('folha', out, '| END', end, '| erros JS:', errs[:5])
