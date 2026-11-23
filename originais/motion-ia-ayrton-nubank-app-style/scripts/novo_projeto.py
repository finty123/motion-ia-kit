"""Cria um projeto novo a partir do modelo do Motion Nubank e registra a prévia no launch.json de Downloads.
Uso: python novo_projeto.py C:\\Users\\Ayrton\\Downloads\\motion-<marca> [--porta 3040]
Copia index.html, compositions/ (cenas + kit3d.js + kit3d-extra.js), assets/nu-branco.png, cues.json e scripts/mix.py.
As cenas copiadas são do Nubank: use como ponto de partida e reescreva textos, tempos e marca."""
import argparse, json, shutil
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("destino"); ap.add_argument("--porta", type=int, default=3040)
    a = ap.parse_args()
    dst = Path(a.destino)
    if dst.exists() and any(dst.iterdir()):
        raise SystemExit(f"{dst} já existe e não está vazia")
    shutil.copytree(SKILL / "assets" / "modelo", dst, dirs_exist_ok=True)
    (dst / "scripts").mkdir(exist_ok=True)
    shutil.copy(SKILL / "scripts" / "mix.py", dst / "scripts" / "mix.py")
    pkg = json.loads((dst / "package.json").read_text(encoding="utf-8")); pkg["name"] = dst.name
    (dst / "package.json").write_text(json.dumps(pkg, indent=2), encoding="utf-8")
    launch = dst.parent / ".claude" / "launch.json"
    if launch.exists():
        d = json.loads(launch.read_text(encoding="utf-8"))
        d["configurations"] = [c for c in d["configurations"] if c["name"] != dst.name]
        d["configurations"].append({"name": dst.name, "runtimeExecutable": "npx", "runtimeArgs": ["hyperframes", "preview", dst.name, "--port", str(a.porta), "--no-open"], "port": a.porta})
        launch.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
        print("prévia registrada:", dst.name, "porta", a.porta)
    print("ok", dst)


if __name__ == "__main__":
    main()
