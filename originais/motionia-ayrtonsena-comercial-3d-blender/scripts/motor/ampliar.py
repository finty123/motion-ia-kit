# Versao com pressa: tapa os quadros da helice que nao chegaram a sair em 1080p com os da previa (960x540)
# ampliados. Vao pra render/final/helice_rapido; o compor.py so usa onde falta o quadro de verdade.
# Uso: python ampliar.py
from PIL import Image
import config as C

prev, final = C.RENDER / "previa" / "helice", C.RENDER / "final" / "helice"
saida = C.RENDER / "final" / "helice_rapido"
saida.mkdir(parents=True, exist_ok=True)
n = 0
for p in sorted(prev.glob("f_*.png")):
    if (final / p.name).exists() or (saida / p.name).exists():
        continue
    Image.open(p).resize((1920, 1080), Image.LANCZOS).save(saida / p.name)
    n += 1
print("ampliados:", n)
