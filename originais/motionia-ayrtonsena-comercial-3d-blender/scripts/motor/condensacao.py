# Gera o mapa de condensacao da lata (roda fora do Blender, uma vez so):
#   assets/condensacao_normal.png  -> normal map (espaco tangente) das gotas e escorridos
#   assets/condensacao_mascara.png -> R = cobertura de agua, G = nevoa, B = altura da gota
# Mapeamento: u = angulo (0..1, emenda sem costura), v = z do corpo / 5.
# Uso: python condensacao.py
import math
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

AQUI = Path(__file__).resolve().parent
W, H = 6144, 4864
LARG, ALT = math.tau, 5.0               # tamanho fisico da faixa (unidades da cena)
PX = W / LARG                           # pixels por unidade
Z_MIN, Z_MAX = 0.32, 4.86               # onde pode ter gota (fora do fundo e da tampa)
rng = np.random.default_rng(7)

altura = np.zeros((H, W), np.float32)   # linha 0 = z 0 (v pra cima); inverte ao salvar
limpa = np.zeros((H, W), np.float32)    # 1 = onde a agua escorreu/juntou e levou a nevoa


def carimbo(cx, cz, r, aspecto=1.0, ang=0.0, peso_baixo=0.0, alvo=altura, perfil="calota", forca=1.0):
    """Gota eliptica (calota esferica) em u/z fisicos, com emenda horizontal."""
    rx, rz = r * aspecto, r / aspecto
    ext = max(rx, rz) * 1.25
    x0, x1 = int((cx - ext) * PX) - 1, int((cx + ext) * PX) + 2
    y0, y1 = max(0, int((cz - ext) * PX) - 1), min(H, int((cz + ext) * PX) + 2)
    if y1 <= y0:
        return
    xs = (np.arange(x0, x1) + 0.5) / PX - cx
    ys = (np.arange(y0, y1) + 0.5) / PX - cz
    gx, gy = np.meshgrid(xs, ys)
    c, s = math.cos(ang), math.sin(ang)
    lx, ly = c * gx + s * gy, -s * gx + c * gy
    # gravidade: a parte de baixo da gota fica mais gorda
    ly = np.where(ly < 0, ly / (1 + peso_baixo), ly)
    d2 = (lx / rx) ** 2 + (ly / rz) ** 2
    if perfil == "calota":
        h = np.sqrt(np.clip(1 - d2, 0, 1)) * r * 0.42 * forca
    else:                                # filme fino (rastro)
        h = np.clip(1 - d2, 0, 1) ** 0.6 * r * 0.18 * forca
    cols = np.arange(x0, x1) % W
    reg = alvo[y0:y1][:, cols]
    alvo[y0:y1, cols] = np.maximum(reg, h)


def grupo(circulos, peso_baixo=0.3):
    """Varias calotas fundidas numa gota so, lisa (soma dos campos, sem vinco)."""
    ext = max(r for _, _, r in circulos) * 1.3
    us = [c[0] for c in circulos]; zs = [c[1] for c in circulos]
    x0, x1 = int((min(us) - ext) * PX) - 1, int((max(us) + ext) * PX) + 2
    y0, y1 = max(0, int((min(zs) - ext) * PX) - 1), min(H, int((max(zs) + ext) * PX) + 2)
    if y1 <= y0:
        return
    gx, gy = np.meshgrid((np.arange(x0, x1) + 0.5) / PX, (np.arange(y0, y1) + 0.5) / PX)
    vol = np.zeros_like(gx)
    for cx, cz, r in circulos:      # soma dos quadrados das calotas: une liso, sem plato
        ly = gy - cz
        ly = np.where(ly < 0, ly / (1 + peso_baixo), ly)
        vol += r ** 2 * np.clip(1 - ((gx - cx) ** 2 + ly ** 2) / r ** 2, 0, None)
    h = np.sqrt(vol) * 0.42
    cols = np.arange(x0, x1) % W
    altura[y0:y1, cols] = np.maximum(altura[y0:y1][:, cols], h)


def ruido_baixo(escala, semente):
    r = np.random.default_rng(semente).random((max(2, int(H / escala)), max(2, int(W / escala)))).astype(np.float32)
    r = ndimage.zoom(r, (H / r.shape[0], W / r.shape[1]), order=3, mode="grid-wrap")[:H, :W]
    return (r - r.min()) / (r.max() - r.min() + 1e-6)


# nevoa e densidade variam em manchas (lata real nunca e uniforme)
manchas = ruido_baixo(380, 1) * 0.6 + ruido_baixo(120, 2) * 0.4


def sorteia(n, z_min=Z_MIN, z_max=Z_MAX, por_mancha=True):
    pts = []
    while len(pts) < n:
        u, z = rng.uniform(0, LARG), rng.uniform(z_min, z_max)
        if por_mancha and rng.random() > manchas[int(z * PX) % H, int(u * PX) % W] ** 1.4 + 0.15:
            continue
        pts.append((u, z))
    return pts


# 1) escorridos: descem tortos, deixam um filme fino com contas e uma gota grande na ponta
for _ in range(26):
    u, z = rng.uniform(0, LARG), rng.uniform(2.0, Z_MAX - 0.1)
    comp = rng.uniform(0.5, 2.6)
    larg = rng.uniform(0.016, 0.03)
    passos = int(comp * PX / 3)
    deriva = 0.0
    for i in range(passos):
        z -= comp / passos
        if z < Z_MIN:
            break
        deriva = float(np.clip(deriva * 0.97 + rng.normal(0, 0.00012), -0.0007, 0.0007))
        u += deriva
        carimbo(u, z, larg, 1.0, perfil="filme")
        carimbo(u, z, larg * 1.9, 1.0, alvo=limpa, perfil="filme", forca=40)
        if rng.random() < 0.012:            # contas que ficaram no caminho
            carimbo(u, z, larg * rng.uniform(1.0, 1.5), 1.05, peso_baixo=0.3)
    carimbo(u, z, larg * rng.uniform(1.9, 2.6), 0.92, peso_baixo=0.55)
    carimbo(u, z, larg * 4.0, 1.0, alvo=limpa, perfil="filme", forca=40)

# 2) gotas grandes, algumas fundidas (2-3 calotas juntas viram uma gota irregular)
for u, z in sorteia(170):
    r = rng.uniform(0.032, 0.07)
    extras = int(rng.integers(0, 3))
    if extras == 0:
        carimbo(u, z, r, rng.uniform(0.85, 1.0), rng.uniform(-0.3, 0.3), peso_baixo=rng.uniform(0.1, 0.5))
    else:
        grupo([(u, z, r)] + [(u + rng.normal(0, r * 0.75), z + rng.normal(0, r * 0.6), r * rng.uniform(0.55, 0.85))
                             for _ in range(extras)], peso_baixo=rng.uniform(0.2, 0.5))
    carimbo(u, z, r * 2.2, 1.0, alvo=limpa, perfil="filme", forca=30)

# escorrido e gota grande levam as gotinhas em volta (pula, nao corta pedaco)
limpa = np.clip(limpa / (limpa.max() * 0.05 + 1e-6), 0, 1)
limpa = ndimage.gaussian_filter(limpa, 3, mode=("nearest", "wrap"))
livre = lambda u, z: limpa[int(z * PX) % H, int(u * PX) % W] < 0.35

# 3) gotas medias
for u, z in [p_ for p_ in sorteia(4600) if livre(*p_)]:
    r = rng.uniform(0.012, 0.03)
    carimbo(u, z, r, rng.uniform(0.85, 1.12), rng.uniform(-0.5, 0.5), peso_baixo=rng.uniform(0, 0.3))

# 4) gotinhas (densas nas manchas)
for u, z in [p_ for p_ in sorteia(80000) if livre(*p_)]:
    carimbo(u, z, rng.uniform(0.0035, 0.011), rng.uniform(0.85, 1.15))

altura = ndimage.gaussian_filter(altura, 0.8, mode=("nearest", "wrap"))
agua = np.clip(altura / 0.0012, 0, 1)                       # cobertura (borda macia)
nevoa = np.clip(manchas * 1.25 - 0.15, 0, 1) * (1 - limpa) * (1 - agua)
zz = (np.arange(H) + 0.5) / PX
fora = (zz < Z_MIN - 0.05) | (zz > Z_MAX + 0.04)
nevoa[fora] = 0

# normal map em espaco tangente (x = ao redor, y = pra cima)
dx = (np.roll(altura, -1, 1) - np.roll(altura, 1, 1)) * PX / 2
dy = np.zeros_like(altura)
dy[1:-1] = (altura[2:] - altura[:-2]) * PX / 2
nrm = np.stack([-dx, -dy, np.ones_like(altura)], -1)
nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
img_n = ((nrm * 0.5 + 0.5) * 255 + 0.5).astype(np.uint8)
hn = np.clip(altura / (altura.max() * 0.6), 0, 1)
img_m = (np.stack([agua, nevoa, hn], -1) * 255 + 0.5).astype(np.uint8)

saida = AQUI / "assets"
Image.fromarray(img_n[::-1]).save(saida / "condensacao_normal.png", optimize=False)
Image.fromarray(img_m[::-1]).save(saida / "condensacao_mascara.png", optimize=False)
print("condensacao pronta:", W, "x", H, "| cobertura de agua", round(float(agua.mean()), 3), "| nevoa", round(float(nevoa.mean()), 3))
