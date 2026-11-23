"""Tira o fundo chapado de um logo (ex.: "nu" branco no roxo) e devolve o logo BRANCO com transparência,
recortado e ampliado 4x com borda nítida (dá pra usar grande no final e como máscara CSS em qualquer cor).
Uso: python logo_alpha.py logo.png PROJETO/assets/logo-branco.png [--escala 4]"""
import argparse
import numpy as np
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada"); ap.add_argument("saida"); ap.add_argument("--escala", type=int, default=4)
    a = ap.parse_args()
    im = np.asarray(Image.open(a.entrada).convert("RGB")).astype(float)
    bg = im[5, 5]
    alpha = np.clip(np.linalg.norm(im - bg, axis=2) / np.linalg.norm(np.array([255, 255, 255]) - bg), 0, 1)
    ys, xs = np.where(alpha > 0.5); pad = 6
    alpha = alpha[ys.min() - pad: ys.max() + pad + 1, xs.min() - pad: xs.max() + pad + 1]
    A = Image.fromarray((alpha * 255).astype(np.uint8))
    A = np.asarray(A.resize((A.width * a.escala, A.height * a.escala), Image.LANCZOS)).astype(float) / 255
    x = np.clip((A - 0.32) / 0.36, 0, 1); x = x * x * (3 - 2 * x)
    out = np.zeros(A.shape + (4,), np.uint8); out[..., :3] = 255; out[..., 3] = (x * 255).round()
    Image.fromarray(out).save(a.saida)
    print("ok", a.saida, out.shape[1], "x", out.shape[0])


if __name__ == "__main__":
    main()
