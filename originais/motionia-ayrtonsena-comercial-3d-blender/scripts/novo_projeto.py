# Cria a pasta do projeto com o motor copiado e um projeto.json de partida.
# Uso: python novo_projeto.py "<pasta do projeto>" "<Marca>"
#      (se a pasta ja tem motor/, so atualiza os scripts e NAO mexe no projeto.json nem nos renders)
import json, shutil, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
pasta, marca = Path(sys.argv[1]), (sys.argv[2] if len(sys.argv) > 2 else "Marca")
motor = pasta / "motor"
for sub in ("musica", "rotulos", "modelos", "pecas", "render", "resultados", "logs", "referencias", "motor/assets"):
    (pasta / sub).mkdir(parents=True, exist_ok=True)
for arq in (SKILL / "scripts" / "motor").iterdir():
    if arq.is_file() and not arq.name.startswith("_"):
        shutil.copy2(arq, motor / arq.name)
cfg_p = motor / "projeto.json"
if not cfg_p.exists():
    modelo = json.loads((SKILL / "assets" / "projeto-modelo.json").read_text(encoding="utf-8"))
    modelo["marca"] = marca
    cfg_p.write_text(json.dumps(modelo, indent=2, ensure_ascii=False), encoding="utf-8")
    print("projeto.json criado (preencha com o briefing)")
else:
    print("projeto.json ja existia: mantido")
print("pronto:", pasta)
