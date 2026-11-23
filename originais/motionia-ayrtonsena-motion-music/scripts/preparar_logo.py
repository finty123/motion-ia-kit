"""Logo (PNG/JPG, fundo escuro, claro ou transparente) -> PNG recortado com transparência pronto pro motor 3D.
Uso: python3 preparar_logo.py logo.png saida/logo_alpha.png [--branco]
Se o logo for escuro (some no fundo escuro), ele vira branco automaticamente."""
import sys, numpy as np
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]; force_white = '--branco' in sys.argv
im = Image.open(src).convert('RGBA'); a = np.array(im).astype(float)
rgb, al = a[..., :3], a[..., 3]
if al.min() > 250:  # sem transparência: decide pelo fundo (cantos)
    cs = np.concatenate([rgb[:10, :10].reshape(-1, 3), rgb[-10:, -10:].reshape(-1, 3), rgb[:10, -10:].reshape(-1, 3), rgb[-10:, :10].reshape(-1, 3)])
    bgc = cs.mean(0); dist = np.sqrt(((rgb - bgc) ** 2).sum(-1)); al = np.clip((dist - 30) / 120, 0, 1) * 255
lum = (rgb[..., 0] * .299 + rgb[..., 1] * .587 + rgb[..., 2] * .114) / 255
mask = al > 40
if force_white or (mask.any() and lum[mask].mean() < 0.35): rgb[:] = 255
ys, xs = np.where(al > 25); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
out = np.dstack([rgb, al]).astype(np.uint8)[max(0, y0 - 4):y1 + 5, max(0, x0 - 4):x1 + 5]
Image.fromarray(out).save(dst); print('logo ok', dst, out.shape[1], 'x', out.shape[0])
