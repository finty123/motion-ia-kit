import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(np.float32)/255
mx, mn = a.max(2), a.min(2); sat = (mx-mn)/np.maximum(mx,1e-6)
cand = (sat < 0.16).astype(np.uint8)*255          # fundo cinza = pouca saturação
m = Image.fromarray(cand, 'L').copy()
h, w = cand.shape
for p in [(0,0),(w-1,0),(0,h-1),(w-1,h-1),(w//2,0),(w//2,h-1),(0,h//2),(w-1,h//2)]:
    if m.getpixel(p) == 255: ImageDraw.floodfill(m, p, 128)
bg = (np.asarray(m) == 128)
alpha = Image.fromarray(((~bg)*255).astype(np.uint8), 'L')
alpha = alpha.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(5))   # fecha buracos e come 1 px de borda
alpha = alpha.filter(ImageFilter.GaussianBlur(0.8))
rgba = im.copy(); rgba.putalpha(alpha)
bb = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
rgba.crop((max(bb[0]-6,0), max(bb[1]-6,0), min(bb[2]+6,w), min(bb[3]+6,h))).save(out)
print('bbox', bb)
