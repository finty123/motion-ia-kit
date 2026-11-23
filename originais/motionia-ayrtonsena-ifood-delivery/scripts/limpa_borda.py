# Remove sobras (sombra/papel) pouco saturadas ligadas ao lado de fora do recorte.
import sys, numpy as np
from PIL import Image, ImageFilter
src, out, smax, vmin, vmax = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:6])
yfrac = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
im = Image.open(src).convert('RGBA'); a = np.asarray(im).astype(np.float32)/255
rgb, al = a[..., :3], a[..., 3]
mx, mn = rgb.max(2), rgb.min(2); sat = (mx-mn)/np.maximum(mx, 1e-6)
cand = (sat < smax) & (mx >= vmin) & (mx <= vmax) & (al > 0)
cand[:int(yfrac*cand.shape[0])] = False   # só abaixo dessa altura
fora = al < 0.05
reg = fora.copy()
def dil(m):
    d = m.copy()
    d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
    return d
for _ in range(2000):
    novo = dil(reg) & (cand | fora)
    if (novo == reg).all(): break
    reg = novo
tirar = reg & ~fora
print(src, 'pixels removidos:', int(tirar.sum()))
alpha = np.where(reg, 0, al*255).astype(np.uint8)
A = Image.fromarray(alpha, 'L').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
o = im.copy(); o.putalpha(A)
bb = A.point(lambda v: 255 if v > 8 else 0).getbbox(); o.crop(bb).save(out)
