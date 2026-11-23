# Coisas do computador: achar o Blender, nunca abrir dois Blenders juntos, rodar em prioridade baixa
# (o PC continua usavel) e tocar o alarme. Funciona no Windows, Mac e Linux.
import glob, os, platform, shutil, subprocess, sys, time
from pathlib import Path

SO = platform.system()


def encontrar_blender(cfg=None):
    """caminho do blender: o de projeto.json ("blender"), o do PATH ou o mais novo nas pastas padrao"""
    if cfg and cfg.get("blender") and Path(cfg["blender"]).exists():
        return cfg["blender"]
    no_path = shutil.which("blender")
    if no_path:
        return no_path
    if SO == "Windows":
        cands = glob.glob(r"C:\Program Files\Blender Foundation\Blender *\blender.exe")
        cands += glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Programs\Blender Foundation\Blender *\blender.exe"))
        cands += glob.glob(r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe")
    elif SO == "Darwin":
        cands = glob.glob("/Applications/Blender*.app/Contents/MacOS/Blender")
    else:
        cands = glob.glob("/opt/blender*/blender") + glob.glob(os.path.expanduser("~/blender*/blender"))

    def versao(c):
        import re
        m = re.search(r"(\d+)\.(\d+)", c)
        return (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return max(cands, key=versao) if cands else None


def blender_rodando():
    """tem algum Blender aberto? (dois juntos estouram a RAM e tudo fica ~5x mais lento)"""
    try:
        import psutil
        return any((p.info["name"] or "").lower().startswith("blender") for p in psutil.process_iter(["name"]))
    except ImportError:
        pass
    try:
        if SO == "Windows":   # tasklist/WMI podem estar quebrados; o PowerShell resolve
            out = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process blender -ErrorAction SilentlyContinue).Count"],
                                 capture_output=True, text=True).stdout.strip()
            return out not in ("", "0")
        return subprocess.run(["pgrep", "-i", "blender"], capture_output=True).returncode == 0
    except Exception:
        return False


def esperar_blender():
    avisou = False
    while blender_rodando():
        if not avisou:
            print("esperando o outro Blender terminar (nunca dois juntos)...", flush=True)
            avisou = True
        time.sleep(30)


def rodar_baixo(cmd, log=None, env=None):
    """roda um comando em prioridade baixa e espera; devolve o codigo de saida"""
    kw = {}
    if SO == "Windows":
        kw["creationflags"] = 0x00004000          # BELOW_NORMAL_PRIORITY_CLASS
    else:
        kw["preexec_fn"] = lambda: os.nice(10)
    saida = open(log, "w", encoding="utf-8", errors="replace") if log else None
    try:
        return subprocess.run(cmd, stdout=saida or None, stderr=subprocess.STDOUT if saida else None,
                              env=env, **kw).returncode
    finally:
        if saida:
            saida.close()


def alarme(vezes=6):
    """avisa que o FINAL ficou pronto (rascunho e previa nao tocam)"""
    for _ in range(vezes):
        try:
            if SO == "Windows":
                import winsound
                for f in (880, 1175, 1568):
                    winsound.Beep(f, 180)
            elif SO == "Darwin":
                subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
            else:
                sys.stdout.write("\a"); sys.stdout.flush()
        except Exception:
            sys.stdout.write("\a"); sys.stdout.flush()
        time.sleep(0.6)
