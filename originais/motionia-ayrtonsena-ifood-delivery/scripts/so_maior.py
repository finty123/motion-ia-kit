# Mantém só a peça ligada ao centro da imagem (tira farelos soltos).
import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA'); a = np.asarray(im).copy()
m = a[..., 3] > 20; h, w = m.shape
reg = np.zeros_like(m); ys, xs = np.nonzero(m); i = np.argmin((ys-h/2)**2 + (xs-w/2)**2); reg[ys[i], xs[i]] = True
while True:
    d = reg.copy(); d[1:] |= reg[:-1]; d[:-1] |= reg[1:]; d[:, 1:] |= reg[:, :-1]; d[:, :-1] |= reg[:, 1:]
    d &= m
    if (d == reg).all(): break
    reg = d
# preserva a borda suave: zera só o que está longe da peça principal
near = reg.copy()
for _ in range(3):
    n = near.copy(); n[1:] |= near[:-1]; n[:-1] |= near[1:]; n[:, 1:] |= near[:, :-1]; n[:, :-1] |= near[:, 1:]; near = n
a[..., 3] = np.where(near, a[..., 3], 0)
o = Image.fromarray(a, 'RGBA'); o.crop(o.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()).save(out)
print('ok', out)
