"""Traz de volta pro kit o que as skills instaladas aprenderam (regras novas, erros e lições, scripts novos).

Uso: python ferramentas/trazer_aprendizados.py        (o instalador roda isso sozinho antes de reinstalar)

As skills gravam correções nelas mesmas, em C:\\Users\\<você>\\.claude\\skills\\<skill>\\ (ex.: references/regras.md).
Na instalação, cada skill recebe um `.kit-manifest.json` com a impressão digital (sha256) de cada arquivo.
Este script compara a skill instalada com esse manifesto e copia pra aprendizados/:
  - arquivos que mudaram depois da instalação;
  - arquivos novos.
O SKILL.md não é copiado automaticamente (ele tem a seção do kit no fim): se mudou, o script avisa e salva
uma cópia ao lado (revisoes/<skill>/SKILL.md.instalado-<data>) pra você revisar.
"""
import hashlib, json, os, shutil, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KIT = Path(__file__).resolve().parent.parent
ORIG = KIT / "originais"
INSTALADO = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "skills"
MANIFESTO = ".kit-manifest.json"
IGNORA = {"__pycache__", "sfx-kit", "_blocos"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    total = 0
    for o in sorted(p for p in ORIG.iterdir() if (p / "SKILL.md").exists()):
        inst = INSTALADO / o.name
        man = inst / MANIFESTO
        if not man.exists():
            continue  # não instalada, ou instalada fora do kit: não mexe
        m = json.loads(man.read_text(encoding="utf-8"))
        for f in sorted(inst.rglob("*")):
            if not f.is_file() or f.name == MANIFESTO or IGNORA & set(f.parts) or f.suffix == ".pyc":
                continue
            rel = f.relative_to(inst).as_posix()
            if m.get(rel) == sha(f):
                continue
            if rel == "SKILL.md":
                dst = KIT / "revisoes" / o.name / f"SKILL.md.instalado-{time.strftime('%Y%m%d-%H%M')}"
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                print(f"  revise: {o.name}/SKILL.md mudou na skill instalada (cópia em {dst.relative_to(KIT)})")
            else:
                dst = KIT / "aprendizados" / o.name / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                print(f"  {'novo' if rel not in m else 'atualizado'}: {o.name}/{rel}")
            total += 1
    print(f"aprendizados trazidos pro kit: {total}" if total else "nenhum aprendizado novo nas skills instaladas")


if __name__ == "__main__":
    main()
