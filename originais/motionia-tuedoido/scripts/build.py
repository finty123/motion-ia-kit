"""Monta o index.html único (fontes e logo embutidos) a partir do scenes.js do projeto.
Uso: python3 build.py --scenes proj/scenes.js --words proj/words.json --beats proj/beats.json --logo proj/logo_alpha.png --out proj/index.html"""
import base64, json, argparse, os
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(H)
ap = argparse.ArgumentParser(); ap.add_argument('--scenes', required=True); ap.add_argument('--words', required=True); ap.add_argument('--beats', required=True); ap.add_argument('--logo', default=''); ap.add_argument('--out', required=True); ap.add_argument('--size', default='1920x1080')
ap.add_argument('--paleta', default='', help='principal=#7F3AED,destaque=#C6FF34  (as cores escuras derivam da principal)')
A = ap.parse_args()
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
fonts = [('Anton', 'Anton.ttf', ''), ('Inter', 'Inter.ttf', 'font-weight:100 900;'), ('Playfair Display', 'Playfair.ttf', 'font-weight:400 900;'), ('Bebas Neue', 'Bebas.ttf', ''), ('Pacifico', 'Pacifico.ttf', ''), ('Space Mono', 'SpaceMono.ttf', ''), ('Bungee', 'Bungee.ttf', ''), ('Abril Fatface', 'Abril.ttf', ''), ('Permanent Marker', 'Marker.ttf', '')]
ff = ''.join(f"@font-face{{font-family:'{n}';src:url(data:font/ttf;base64,{b64(os.path.join(ROOT, 'assets/fonts', f))}) format('truetype');{x}}}\n" for n, f, x in fonts)
Wd, Hd = [int(v) for v in A.size.split('x')]
eng = ''.join(open(os.path.join(H, 'engine', f)).read() + '\n' for f in ['engine.js', 'engine2.js', 'helpers.js', 'kit.js'])
eng = eng.replace('const W = 1920, H = 1080;', f'const W = {Wd}, H = {Hd};')
scn = open(A.scenes).read()
if A.paleta:
    import re
    pal = dict(p.split('=') for p in A.paleta.split(','))
    def dk(h, k): h = h.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4)); return '#%02x%02x%02x' % (int(r * (1 - k)), int(g * (1 - k)), int(b * (1 - k)))
    Vn, Ln = pal.get('principal', '#7F3AED'), pal.get('destaque', '#C6FF34')
    mp = {'#7F3AED': Vn, '#C6FF34': Ln, '#1a0636': dk(Vn, .85), '#2a0d55': dk(Vn, .72), '#3d1680': dk(Vn, .55), '#3a1580': dk(Vn, .55), '#12062b': dk(Vn, .88), '#5a7a10': dk(Ln, .55), '#4d6610': dk(Ln, .6)}
    rgbL = ','.join(str(int(Ln.lstrip('#')[i:i + 2], 16)) for i in (0, 2, 4))
    def sub(t):
        for a, b in mp.items(): t = re.sub(re.escape(a), b, t, flags=re.I)
        return t.replace('rgba(198,255,52', 'rgba(' + rgbL)
    eng, scn = sub(eng), sub(scn)
logo = f"LOGO_IMG=new Image(); LOGO_IMG.src='data:image/png;base64,{b64(A.logo)}'; await LOGO_IMG.decode();" if A.logo else ''
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{ff}html,body{{margin:0;background:#000}}canvas{{display:block}}</style></head><body><canvas id="c"></canvas>
<script>const WD={json.dumps(json.load(open(A.words)), ensure_ascii=False)};const BEATS={json.dumps(json.load(open(A.beats)))};let LOGO_IMG=null;</script>
<script>{eng}</script>
<script>{scn}</script>
<script>(async()=>{{ const fams=['Anton','Inter','Playfair Display','Bebas Neue','Pacifico','Space Mono','Bungee','Abril Fatface','Permanent Marker'];
 await Promise.all(fams.flatMap(f=>[400,500,600,700,800].map(w=>document.fonts.load(w+' 40px "'+f+'"')))); await document.fonts.ready; {logo}
 finalizeScenes(); window.READY=true; }})().catch(e=>{{window.ERR=String(e.stack||e)}});</script></body></html>"""
open(A.out, 'w').write(html); print('ok', A.out, len(html) // 1024, 'KB')
