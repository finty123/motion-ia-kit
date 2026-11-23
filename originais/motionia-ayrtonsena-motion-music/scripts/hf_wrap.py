"""Coloca o clipe (index.html do build.py) dentro de um projeto HyperFrames pra PRÉVIA e RENDER.
Uso: python hf_wrap.py proj/index.html proj/hf --audio proj/mix.wav [--fps 30]
Depois:  cd proj/hf && npx --yes hyperframes@0.9.5 check
         npx --yes hyperframes@0.9.5 preview --port 3031      (abre no navegador dele e espera o ok)
         npx --yes hyperframes@0.9.5 render --workers 4 -o ../video.mp4   (só depois da aprovação)

Por que: o Ayrton aprova tudo na prévia do HyperFrames antes do render (regra dele). O motor desenha num
canvas; aqui ele vira uma composição que desenha o quadro a cada 'hf-seek'. Na prévia roda sem subquadro
(leve); no render (Chrome automatizado) usa 2 subquadros = motion blur real."""
import sys as _s; _s.stdout.reconfigure(encoding='utf-8', errors='replace')  # acentos certos no console do Windows
import os, re, sys, json, shutil, argparse
ap = argparse.ArgumentParser(); ap.add_argument('html'); ap.add_argument('out'); ap.add_argument('--audio', default=''); ap.add_argument('--fps', type=int, default=30)
A = ap.parse_args()
src = open(A.html, encoding='utf-8').read()
style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
scripts = re.findall(r'<script>(.*?)</script>', src, re.S)
data, eng, scn, init = scripts[0], scripts[1], scripts[2], scripts[3]
W, H = [int(v) for v in re.search(r'const W = (\d+), H = (\d+);', eng).groups()]
END = float(re.search(r'const END\s*=\s*([\d.]+)', scn).group(1))
fams = re.search(r'const fams=(\[.*?\]);', init).group(1)
logo = re.search(r'(LOGO_IMG=new Image\(\);.*?await LOGO_IMG\.decode\(\);)', init, re.S)
logo = logo.group(1).replace('await LOGO_IMG.decode();', 'await new Promise(r => { LOGO_IMG.onload = r; if (LOGO_IMG.complete) r(); });') if logo else ''  # decode() trava em aba escondida
os.makedirs(os.path.join(A.out, 'compositions'), exist_ok=True); os.makedirs(os.path.join(A.out, 'assets', 'audio'), exist_ok=True)
res = 'landscape' if W > H else ('portrait' if H > W else 'square')
style = style.replace('html,body{margin:0;background:#000}canvas{display:block}', '')
comp = f"""<template>
  <style>{style}
    #root {{ position: absolute; inset: 0; background: #000; }}
    #c {{ position: absolute; inset: 0; width: 100%; height: 100%; display: block; }}
  </style>
  <div id="root" data-composition-id="clipe" data-width="{W}" data-height="{H}" data-layout-allow-overlap data-layout-allow-overflow>
    <canvas id="c" width="{W}" height="{H}"></canvas>
  </div>
  <script>
// tudo num script só: o HyperFrames roda cada <script> da composição num escopo próprio,
// então motor, cenas e init precisam dividir o mesmo bloco pra se enxergarem
{data}
{eng}
{scn}
const __FPS = {A.fps}, __SUB = navigator.webdriver ? 1 / (2 * __FPS) : 0;
const __pronto = (async () => {{
  const fams = {fams};
  await Promise.all(fams.flatMap(f => [400, 500, 600, 700, 800].map(w => document.fonts.load(w + ' 40px "' + f + '"'))));
  await document.fonts.ready; {logo}
  finalizeScenes(); window.READY = true; return true;
}})();
let __ok = false; __pronto.then(() => {{ __ok = true; window.frame(0, 0); }});
window.__hf = window.__hf || {{}}; window.__hf.buildReady = window.__hf.buildReady || {{}}; window.__hf.buildReady["clipe"] = __pronto;
window.addEventListener("hf-seek", e => {{
  const t = Math.min(e.detail.time, {END} - 1e-3);
  if (__ok) window.frame(t, __SUB); else e.detail.waitUntil(__pronto.then(() => window.frame(t, __SUB)));
}});
const __tl = gsap.timeline({{ paused: true }}); __tl.to({{}}, {{ duration: {END} }}, 0);
window.__timelines["clipe"] = __tl;
  </script>
</template>
"""
open(os.path.join(A.out, 'compositions', 'clipe.html'), 'w', encoding='utf-8').write(comp)
aud = ''
if A.audio:
    shutil.copy(A.audio, os.path.join(A.out, 'assets', 'audio', 'trilha.wav'))
    aud = f'<audio id="trilha" class="clip" src="assets/audio/trilha.wav" data-start="0" data-duration="{END}" data-track-index="2"></audio>'
idx = f"""<!doctype html>
<html lang="pt-BR" data-resolution="{res}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Motion Music</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }} #root {{ position: relative; width: 100%; height: 100%; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-fps="{A.fps}" data-width="{W}" data-height="{H}">
      <div id="clipe" data-composition-id="clipe" data-composition-src="compositions/clipe.html" data-start="0" data-duration="{END}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>
      {aud}
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
"""
open(os.path.join(A.out, 'index.html'), 'w', encoding='utf-8').write(idx)
json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json", "paths": {"blocks": "compositions", "assets": "assets"}, "media": {"autoProxy": True}, "authoringSkill": "hyperframes"}, open(os.path.join(A.out, 'hyperframes.json'), 'w'), indent=2)
json.dump({"name": "clipe", "private": True, "type": "module", "scripts": {"dev": "npx --yes hyperframes@0.9.5 preview", "check": "npx --yes hyperframes@0.9.5 check", "render": "npx --yes hyperframes@0.9.5 render"}}, open(os.path.join(A.out, 'package.json'), 'w'), indent=2)
print(f'ok {A.out} | {W}x{H} {res} | {END}s | {A.fps} fps | áudio: {"sim" if aud else "não"}')
