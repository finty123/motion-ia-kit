# Prepara o logo pro cartao final: recorta, centraliza num quadrado 500x500 (assets/logo.png) e traca o
# contorno vetorial das letras (assets/logo_contornos.js) pra animacao de stroke estilo After Effects.
# Uso: python contorno_logo.py <logo.png|jpg|webp>
#      (PNG com fundo transparente e o melhor; com fundo liso ele tira o fundo pela cor do canto)
import json, sys
from pathlib import Path
import cv2
import numpy as np

AQUI = Path(__file__).resolve().parent
LADO, ESC = 500, 4
img = cv2.imdecode(np.fromfile(sys.argv[1], np.uint8), cv2.IMREAD_UNCHANGED)   # aceita caminho com acento (Windows)
if img is None:
    sys.exit("nao consegui abrir o logo: " + sys.argv[1])
if img.ndim == 2:
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
if img.shape[2] == 3:   # sem transparencia: o que for diferente da cor do canto vira logo
    canto = img[:4, :4].reshape(-1, 3).mean(axis=0)
    dif = np.abs(img.astype(np.float32) - canto).max(axis=2)
    alfa = np.clip((dif - 18) * 6, 0, 255).astype(np.uint8)
    img = np.dstack([img, alfa])
ys, xs = np.where(img[:, :, 3] > 20)
img = img[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
h, w = img.shape[:2]
k = (LADO * 0.94) / max(h, w)
img = cv2.resize(img, (max(1, int(w * k)), max(1, int(h * k))), interpolation=cv2.INTER_AREA)
quad = np.zeros((LADO, LADO, 4), np.uint8)
y0, x0 = (LADO - img.shape[0]) // 2, (LADO - img.shape[1]) // 2
quad[y0:y0 + img.shape[0], x0:x0 + img.shape[1]] = img
(AQUI / "assets").mkdir(exist_ok=True)
cv2.imencode(".png", quad)[1].tofile(str(AQUI / "assets" / "logo.png"))

alfa = cv2.resize(quad[:, :, 3], None, fx=ESC, fy=ESC, interpolation=cv2.INTER_CUBIC)
alfa = cv2.GaussianBlur(alfa, (0, 0), 2.2 * ESC)          # some a textura gasta, fica so a forma da letra
_, m = cv2.threshold(alfa, 90, 255, cv2.THRESH_BINARY)
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5 * ESC, 5 * ESC), np.uint8))
contornos, _ = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
saida = []
for c in contornos:
    if cv2.contourArea(c) < 60 * ESC * ESC:
        continue
    p = cv2.approxPolyDP(c, 0.6 * ESC, True)[:, 0, :] / ESC
    saida.append([[round(float(x), 1), round(float(y), 1)] for x, y in p])
# ordem de leitura: linha por linha (agrupa pelo centro vertical), da esquerda pra direita
centro = lambda p: (sum(y for _, y in p) / len(p))
saida.sort(key=centro)
linhas, atual = [], []
for p in saida:
    if atual and centro(p) - centro(atual[-1]) > 60:
        linhas.append(atual); atual = []
    atual.append(p)
if atual:
    linhas.append(atual)
saida = [p for ln in linhas for p in sorted(ln, key=lambda p: min(x for x, _ in p))]
(AQUI / "assets" / "logo_contornos.js").write_text("window.LOGO_CONTORNOS = " + json.dumps(saida) + ";\n", encoding="utf-8")
(AQUI.parent / "logs").mkdir(exist_ok=True)
prev = np.zeros((LADO, LADO, 3), np.uint8)
for i, p in enumerate(saida):
    cv2.polylines(prev, [np.array(p, np.int32)], True, (60 + 12 * i % 195, 255, 255 - 10 * i % 200), 1)
cv2.imencode(".png", prev)[1].tofile(str(AQUI.parent / "logs" / "logo_contornos.png"))
print(len(saida), "contornos,", sum(len(p) for p in saida), "pontos -> confira logs/logo_contornos.png")
