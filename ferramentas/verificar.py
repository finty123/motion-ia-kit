"""Confere se o PC está pronto pras skills do curso Motion IA. Não instala nada.

Uso: python ferramentas/verificar.py
"""
import hashlib, importlib, json, os, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KIT = Path(__file__).resolve().parent.parent
SKILLS_DIR = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "skills"
OK, NO, OPC = "  [ok]  ", "  [FALTA]", "  [opcional]"
faltas = 0


def linha(ok, nome, info="", opcional=False):
    global faltas
    if not ok and not opcional:
        faltas += 1
    print(f"{OK if ok else (OPC if opcional else NO)} {nome}{'  -  ' + info if info else ''}")


def cmd(*a, timeout=60):
    try:
        exe = shutil.which(a[0])
        if not exe:
            return None
        r = subprocess.run([exe, *a[1:]], capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
        if r.returncode:
            return None
        return (r.stdout or r.stderr).strip().splitlines()[0] if (r.stdout or r.stderr).strip() else ""
    except Exception:
        return None


def blender():
    for base in (Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Blender Foundation",):
        if base.exists():
            exes = sorted(base.glob("Blender */blender.exe"))
            if exes:
                return exes[-1]
    w = shutil.which("blender")
    return Path(w) if w else None


print("\n== Programas")
v = sys.version_info
linha(v >= (3, 10), "Python", f"{v.major}.{v.minor}.{v.micro}")
nv = cmd("node", "-v")
linha(bool(nv) and int(nv.lstrip("v").split(".")[0]) >= 22, "Node.js 22+", nv or "não encontrado")
fv = cmd("ffmpeg", "-version")
linha(bool(fv), "FFmpeg", (fv or "não encontrado")[:60])
linha(bool(cmd("ffprobe", "-version")), "FFprobe")
b = blender()
linha(bool(b), "Blender 4.2+ (só pra skill do comercial 3D de lata)", str(b) if b else "não instalado", opcional=True)

print("\n== Bibliotecas Python")
for mod, pip in [("faster_whisper", "faster-whisper"), ("librosa", "librosa"), ("soundfile", "soundfile"), ("scipy", "scipy"),
                 ("PIL", "pillow"), ("playwright", "playwright"), ("numpy", "numpy"), ("cv2", "opencv-python"),
                 ("psutil", "psutil"), ("pyloudnorm", "pyloudnorm")]:
    try:
        importlib.import_module(mod); linha(True, pip)
    except Exception:
        linha(False, pip, f"python -m pip install {pip}")
try:  # abre e fecha o navegador de verdade (a pasta existir não basta: cada versão do Playwright pede o seu)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        p.chromium.launch().close()
    linha(True, "Chromium do Playwright")
except Exception:
    linha(False, "Chromium do Playwright", "python -m playwright install chromium")

print("\n== HyperFrames (cache do npx)")
cache = Path(os.environ.get("LOCALAPPDATA", "")) / "npm-cache" / "_npx"
achadas = set()
if cache.exists():
    for pj in cache.glob("*/node_modules/hyperframes/package.json"):
        try:
            achadas.add(json.loads(pj.read_text(encoding="utf-8"))["version"])
        except Exception:
            pass
for ver in ("0.8.190", "0.8.210", "0.9.5"):
    linha(ver in achadas, f"hyperframes@{ver}", "" if ver in achadas else "ainda não baixado (baixa sozinho no primeiro uso)", opcional=ver not in achadas)

print("\n== Skills instaladas em", SKILLS_DIR)
src = KIT / "skills"
for original in sorted((KIT / "originais").glob("*/SKILL.md")):
    nome = original.parent.name
    dst = SKILLS_DIR / nome
    manifesto = src / nome / ".kit-manifest.json"
    if not manifesto.is_file():
        linha(False, nome, "gere e instale as skills com INSTALAR.cmd")
        continue
    arquivos = json.loads(manifesto.read_text(encoding="utf-8"))
    presentes = sum((dst / rel).is_file() and hashlib.sha256((dst / rel).read_bytes()).hexdigest() == sha
                    for rel, sha in arquivos.items())
    linha(presentes == len(arquivos) and (dst / manifesto.name).is_file(), nome,
          f"{presentes}/{len(arquivos)} arquivos conferidos por conteúdo")

print("\n== Pastas do config.json")
cfg = KIT / "config.json"
if cfg.exists():
    c = json.loads(cfg.read_text(encoding="utf-8"))
    for k in ("pasta_projetos", "pasta_resultados"):
        linha(Path(c[k]).exists(), k, c[k])
    lj = Path(c["pasta_projetos"]) / ".claude" / "launch.json"
    linha(lj.exists(), "launch.json da prévia", str(lj))
    print(f"   assinatura: {c.get('assinatura') or '(vazia: a skill pergunta em cada vídeo)'}")
else:
    linha(False, "config.json", "rode o INSTALAR.cmd")

print("\nTudo pronto!" if faltas == 0 else f"\nFaltam {faltas} itens obrigatórios (veja [FALTA] acima).")
sys.exit(0 if faltas == 0 else 1)
