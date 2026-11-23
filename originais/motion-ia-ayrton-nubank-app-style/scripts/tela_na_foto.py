"""Troca a tela de um celular numa FOTO pela tela do app desenhada em canvas, na mesma perspectiva.
Mede a borda interna da tela (onde o vidro preto da moldura termina) e imprime o matrix3d do CSS que leva
um canvas de 600x1278 para os 4 cantos da tela no quadro 1920x1080 (foto em object-fit: cover).

Uso: python tela_na_foto.py foto.jpg [--x0 450 --x1 950 --y0 250 --y1 760] [--cantos "570,301 807,301 879,733 502,733"]
Sem --cantos, estima pelas bordas escuras na faixa x0..x1 / y0..y1 (ajuste a janela em volta do celular).
Confira o resultado num snapshot: se sobrar borda da tela original, mexa 2-5 px nos cantos."""
import argparse
import numpy as np
from PIL import Image


def medir(im, x0, x1, y0, y1):
    L, R = [], []
    for y in range(y0, y1, 6):
        row = im[y, x0:x1]; dark = row < 45; xs = np.where(dark)[0]
        if len(xs) < 4: continue
        i = xs[0]
        while i < len(row) and dark[i]: i += 1
        j = xs[-1]
        while j > 0 and dark[j]: j -= 1
        L.append((y, x0 + i)); R.append((y, x0 + j))
    def reta(pts):  # ajuste com rejeição de pontos fora (dedos, cantos arredondados)
        y = np.array([q[0] for q in pts], float); x = np.array([q[1] for q in pts], float)
        f = np.polyfit(y, x, 1)
        for _ in range(3):
            ok = np.abs(np.polyval(f, y) - x) < 4
            f = np.polyfit(y[ok], x[ok], 1)
        return f
    fl, fr = reta(L), reta(R)
    # topo e base: a primeira faixa preta vindo de cima e a primeira vindo de baixo (a moldura),
    # pra não confundir com coisas escuras dentro da tela (código de barras, ilha dinâmica)
    col = im[y0:y1, (x0 + x1) // 2] < 45
    i = int(np.argmax(col))
    while i < len(col) and col[i]: i += 1
    j = len(col) - 1 - int(np.argmax(col[::-1]))
    while j > 0 and col[j]: j -= 1
    top, bot = y0 + i, y0 + j
    return [(np.polyval(fl, top), top), (np.polyval(fr, top), top), (np.polyval(fr, bot), bot), (np.polyval(fl, bot), bot)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("foto"); ap.add_argument("--cantos"); ap.add_argument("--prova", default="tela_prova.jpg")
    for k, v in (("x0", 450), ("x1", 950), ("y0", 250), ("y1", 760)): ap.add_argument("--" + k, type=int, default=v)
    a = ap.parse_args()
    img = Image.open(a.foto); W, H = img.size
    if a.cantos: P = [tuple(map(float, c.split(","))) for c in a.cantos.split()]
    else: P = medir(np.asarray(img.convert("L")).astype(int), a.x0, a.x1, a.y0, a.y1)
    k = max(1920 / W, 1080 / H); ox, oy = (1920 - W * k) / 2, (1080 - H * k) / 2
    dst = [(float(x * k + ox), float(y * k + oy)) for x, y in P]
    w, h = 600, 1278; src = [(0, 0), (w, 0), (w, h), (0, h)]
    A, b = [], []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    s = np.linalg.solve(np.array(A), np.array(b)); Hm = np.append(s, 1).reshape(3, 3)
    m = [Hm[0, 0], Hm[1, 0], 0, Hm[2, 0], Hm[0, 1], Hm[1, 1], 0, Hm[2, 1], 0, 0, 1, 0, Hm[0, 2], Hm[1, 2], 0, Hm[2, 2]]
    # prova: desenha o quadrilátero em cima da foto pra conferir antes de usar
    from PIL import ImageDraw
    prova = img.convert("RGB"); d = ImageDraw.Draw(prova); d.polygon([tuple(map(float, q)) for q in P], outline=(255, 0, 80), width=3)
    prova.save(a.prova); print("prova:", a.prova, "(se o contorno não bater na borda da tela, rode de novo com --cantos)")
    print("cantos na foto:", [(round(x), round(y)) for x, y in P])
    print("cantos no quadro:", [(round(x, 1), round(y, 1)) for x, y in dst])
    print("transform: matrix3d(" + ",".join(f"{v:.8g}" for v in m) + "); transform-origin: 0 0;")


if __name__ == "__main__":
    main()
