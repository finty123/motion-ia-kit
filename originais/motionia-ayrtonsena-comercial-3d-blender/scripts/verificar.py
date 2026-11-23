# Confere se o computador tem tudo pra fazer o comercial 3D e diz o que falta, sem instalar nada.
# Uso: python verificar.py
import importlib, platform, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "motor"))
import sistema as S

ok, faltas, avisos = [], [], []


def tem_modulo(nome, pip=None):
    try:
        importlib.import_module(nome)
        ok.append(f"python: {nome}")
    except ImportError:
        faltas.append(f"python: {nome}  ->  pip install {pip or nome}")


print(f"Sistema: {platform.system()} {platform.release()} | Python {platform.python_version()}")
if sys.version_info < (3, 9):
    faltas.append("Python 3.9 ou mais novo")
for m, pipn in (("numpy", None), ("PIL", "pillow"), ("cv2", "opencv-python"), ("scipy", None),
                ("playwright", None), ("psutil", None)):
    tem_modulo(m, pipn)
for prog in ("ffmpeg", "ffprobe"):
    (ok if shutil.which(prog) else faltas).append(prog if shutil.which(prog) else f"{prog} (instale o FFmpeg e coloque no PATH)")

b = S.encontrar_blender()
if b:
    import re
    m = re.search(r"Blender[ /\\-]*(\d+)\.(\d+)", b)    # pela pasta (nao abre o Blender, que pode estar renderizando)
    v = f"Blender {m.group(1)}.{m.group(2)}" if m else None
    if not v and not S.blender_rodando():
        try:
            v = subprocess.run([b, "-b", "--version"], capture_output=True, text=True, timeout=60).stdout.splitlines()[0]
        except Exception:
            v = None
    v = v or "versao desconhecida"
    ok.append(f"Blender: {v} ({b})")
    m = re.search(r"Blender (\d+)\.(\d+)", v)
    if m and (int(m.group(1)), int(m.group(2))) < (4, 2):
        faltas.append("Blender 4.2 ou mais novo (o motor usa o Eevee novo)")
else:
    faltas.append("Blender 4.2+ (blender.org, gratis). Se ja tem, ponha o caminho em projeto.json -> \"blender\"")

try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        try:
            p.chromium.launch(channel="chrome").close(); ok.append("navegador: Chrome")
        except Exception:
            p.chromium.launch().close(); ok.append("navegador: Chromium do Playwright")
except Exception:
    faltas.append("navegador pro Playwright  ->  python -m playwright install chromium")

try:
    import psutil
    ram = psutil.virtual_memory().total / 2 ** 30
    nucleos = psutil.cpu_count(logical=False)
    ok.append(f"RAM {ram:.0f} GB, {nucleos} nucleos")
    if ram < 12:
        avisos.append("menos de 12 GB de RAM: a helice (cena pesada) pode travar; feche tudo durante o render")
except ImportError:
    pass
livre = shutil.disk_usage(Path.cwd()).free / 2 ** 30
(ok if livre > 15 else avisos).append(f"disco livre aqui: {livre:.0f} GB" + ("" if livre > 15 else " (o projeto inteiro usa ~10-15 GB de quadros)"))

print("\nTEM:")
for x in ok:
    print("  ok ", x)
if avisos:
    print("\nATENCAO:")
    for x in avisos:
        print("  !  ", x)
print("\nFALTA:" if faltas else "\nNada faltando.")
for x in faltas:
    print("  x  ", x)
sys.exit(1 if faltas else 0)
