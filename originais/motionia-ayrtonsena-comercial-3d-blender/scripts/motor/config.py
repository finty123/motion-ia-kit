# Configuracao do projeto (sem bpy: serve pro Blender e pros scripts de fora).
# Le projeto.json (o que foi decidido no briefing) e beats.json (a musica) e calcula a linha do tempo.
import json, math
from pathlib import Path
from linha_do_tempo import gerar, n_batidas

AQUI = Path(__file__).resolve().parent
PROJETO = AQUI.parent            # <projeto>/motor/ -> <projeto>/
RENDER = PROJETO / "render"
RESULTADOS = PROJETO / "resultados"
FPS = 30


def _ler(nome):
    p = AQUI / nome
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


CFG = _ler("projeto.json")
BEATS = _ler("beats.json")
MUSICA = CFG.get("musica", {})
BPM = float(MUSICA.get("bpm") or BEATS.get("bpm") or 120)
QB = 60 / BPM * FPS              # quadros por batida


def F(b):
    """quadro (float) da batida b (b1 = quadro 0)"""
    return (b - 1) * QB


SABORES = CFG.get("sabores") or [{"nome": "sabor", "modelo": "sabor"}]
N_SABORES = len(SABORES)
TL = CFG.get("linha_do_tempo") or gerar(N_SABORES)
N_BATIDAS = n_batidas(TL)
TOTAL = int(round(N_BATIDAS * QB))
MARCA = CFG.get("marca", "Marca")


def hex_rgb(h, linear=False):
    """'#ff0f6b' -> (1.0, 0.06, 0.42). As cores de luz do Blender usam o valor direto (foi assim que o
    comercial aprovado foi ajustado); linear=True converte de sRGB pra cor de material."""
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    if linear:
        c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return tuple(c)


COR_SABOR = [hex_rgb(s.get("cor", "#ff2e93")) for s in SABORES]

# tamanho da lata: a cena e montada com a altura fixa (~4,9 unidades) e o diametro escala.
# A lata fina de 350 ml (146 x 58 mm) e a referencia (raio 1).
LATA = CFG.get("lata", {})
_alt, _diam = float(LATA.get("altura_mm", 146)), float(LATA.get("diametro_mm", 58))
RAIO = (_diam / _alt) / (58 / 146)
FOCO_ROTULO = float(LATA.get("foco_rotulo", 0.46))   # altura (0 = pe do rotulo, 1 = topo) do ponto que a camera encara


def ordem_trocas():
    """indice do rotulo em cada troca: comeca no sabor 1 (que sobe na revelacao), passa por todos e volta pro 1"""
    n = N_SABORES
    return [(k + 1) % n for k in range(len(TL["trocas"]))]
