import os, numpy as np, soundfile as sf, json, subprocess, argparse, sys
from scipy import signal
ap = argparse.ArgumentParser(description='Sintetiza os SFX cinematográficos a partir das cues e mixa narração > SFX > música, com ducking e master -14 LUFS.')
ap.add_argument('--music'); ap.add_argument('--cues', default=''); ap.add_argument('--end', type=float, required=True)
ap.add_argument('--out', required=True); ap.add_argument('--music-db', type=float, default=-13, help='música relativa à narração (dB RMS)'); ap.add_argument('--sfx-db', type=float, default=-9)
ap.add_argument('--vacuo', default='', help='INI:FIM (s): a música é SUGADA até FIM e corta seco'); ap.add_argument('--closeup', default='', help='wav do close-up (bate no FIM do vácuo)'); ap.add_argument('--closeup-peak', type=float, default=0.347); ap.add_argument('--com-sfx', action='store_true', help='mistura também os SFX sintetizados das cues'); ap.add_argument('--music-lift', default='', help='INI:FIM em s para subir a música +5 dB depois que a narração acaba')
A = ap.parse_args()
SR = 48000; DUR = A.end; N = int(SR * DUR)
rng = np.random.default_rng(42)

def env(n, a, d, curve=4):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) * curve / max(d, 1e-3))
    return e
def bp_sweep(x, f0, f1, q=1.2):
    out = np.zeros_like(x); blk = 480; zi = None
    for i in range(0, len(x), blk):
        f = f0 * (f1 / f0) ** (i / max(1, len(x)))
        f = np.clip(f, 30, SR / 2.2)
        b, a = signal.iirpeak(f, q, fs=SR)
        if zi is None: zi = signal.lfilter_zi(b, a) * 0
        out[i:i + blk], zi = signal.lfilter(b, a, x[i:i + blk], zi=zi)
    return out
def lp(x, f, o=4): b, a = signal.butter(o, f, 'low', fs=SR); return signal.lfilter(b, a, x)
def hp(x, f, o=4): b, a = signal.butter(o, f, 'high', fs=SR); return signal.lfilter(b, a, x)
def norm(x, p=1.0): m = np.max(np.abs(x)) + 1e-9; return x / m * p
def st(x, pan0=0, pan1=None):
    pan1 = pan0 if pan1 is None else pan1; p = np.linspace(pan0, pan1, len(x))
    l = np.cos((p + 1) * np.pi / 4); r = np.sin((p + 1) * np.pi / 4); return np.stack([x * l, x * r], 1)
IR = None
def reverb(x, dur=2.2, mix=0.35):
    global IR
    n = int(dur * SR)
    if IR is None or len(IR[0]) != n:
        t = np.arange(n) / SR; IR = [lp(rng.standard_normal(n), 6000) * np.exp(-t * 6.9 / dur) for _ in range(2)]
    if x.ndim == 1: x = st(x)
    wet = np.stack([np.pad(signal.fftconvolve(x[:, c], IR[c]), (0, 1))[:len(x) + n] for c in range(2)], 1)
    dry = np.pad(x, ((0, n), (0, 0)))
    return dry * (1 - mix) + norm(wet, np.max(np.abs(x))) * mix

def whoosh(d=0.7, f0=300, f1=3000, pan=(-0.8, 0.8)):
    n = int(d * SR); x = rng.standard_normal(n); x = bp_sweep(x, f0, f1, 1.0)
    t = np.linspace(0, 1, n); e = np.sin(np.pi * t ** 0.7) ** 2
    return st(norm(x * e), *pan)
def sub(f0=70, f1=28, d=1.1):
    n = int(d * SR); t = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-t * 5); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(2.2 * np.sin(ph) * np.exp(-t * 3.2)) * 0.9
def transient(d=0.02, f=3000):
    n = int(d * SR); return hp(rng.standard_normal(n), f, 2) * np.exp(-np.arange(n) / SR * 180)
def boom(): x = sub(75, 30, 1.4); x[:960] += transient(0.02, 1500) * 0.6; return reverb(norm(x), 1.8, 0.25)
def braam():
    n = int(2.6 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in [55, 82.5, 110]:
        for dt in [-0.08, -0.03, 0.03, 0.08]: x += signal.sawtooth(2 * np.pi * f * (1 + dt / 12) * t)
    cut = 180 + 2200 * np.exp(-t * 2.2) * np.minimum(1, t / 0.06)
    y = np.zeros(n); blk = 480
    for i in range(0, n, blk):
        b, a = signal.butter(2, cut[i], 'low', fs=SR); y[i:i + blk] = signal.lfilter(b, a, x[i:i + blk])
    y = np.tanh(norm(y) * 3) * np.exp(-t * 1.1) * np.minimum(1, t / 0.015)
    s = sub(65, 32, 2.0); y[:len(s)] += s * 0.9
    return reverb(norm(y), 2.6, 0.3)
def riser(d=1.3):
    n = int(d * SR); t = np.linspace(0, 1, n); x = hp(rng.standard_normal(n), 800) * t ** 2
    f = 180 * (6 ** t); x += 0.4 * signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * t ** 3
    x = bp_sweep(x, 400, 7000, 0.7) * t ** 1.5
    return st(norm(x), -0.3, 0.3)
def reverse_tail(d=1.3):
    n = int(d * SR); t = np.arange(n) / SR; x = lp(rng.standard_normal(n), 5000) * np.exp(-t * 4)
    x = x[::-1]; return st(norm(x))
def tick(f=1800):
    n = int(0.06 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 160) * 0.6 + np.sin(2 * np.pi * 140 * t) * np.exp(-t * 60) * 0.6
    tr = transient(0.005, 4000); x[:len(tr)] += tr * 0.5; return st(norm(x))
def key():
    f = 1200 + rng.random() * 1400; n = int(0.05 * SR); t = np.arange(n) / SR
    x = transient(0.008, 2500) * 0.7; x = np.pad(x, (0, n - len(x))); x += np.sin(2 * np.pi * 220 * t) * np.exp(-t * 90) * 0.5 + np.sin(2 * np.pi * f * t) * np.exp(-t * 250) * 0.3
    return st(norm(x), (rng.random() - .5) * 0.6)
def click(): x = tick(2600)[:, 0] * 0.7; tr = transient(0.006, 5000); x[:len(tr)] += tr; return st(norm(x))
def hit(level='med'):
    f0, f1, d = {'small': (120, 60, 0.35), 'med': (95, 45, 0.6), 'big': (80, 32, 1.2), 'dry': (110, 55, 0.3), 'dry_low': (70, 38, 0.8), 'soft': (90, 50, 0.5)}[level]
    x = sub(f0, f1, d); x[:960] += transient(0.02, 1200) * (0.9 if level != 'soft' else 0.3)
    return reverb(norm(x), 1.2 if level in ('dry', 'dry_low') else 1.8, 0.12 if 'dry' in level else 0.28)
def slash():
    n = int(0.5 * SR); t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 3000) * np.exp(-t * 18)
    for f in [2350, 3720, 5130, 6900]: x += 0.25 * np.sin(2 * np.pi * f * t) * np.exp(-t * 7)
    return reverb(st(norm(x), -0.5, 0.5), 1.4, 0.25)
def glitch():
    n = int(0.35 * SR); t = np.arange(n) / SR; x = signal.square(2 * np.pi * 180 * t) * 0.4 + rng.standard_normal(n) * 0.5
    x = np.round(x * 6) / 6; gate = (np.floor(t * 38) % 2 == 0); x = x * gate * np.exp(-t * 4)
    return st(norm(lp(x, 6000)) * 0.8, 0.3, -0.3)
def tapestop():
    n = int(0.55 * SR); t = np.arange(n) / SR; f = 220 * (1 - t / 0.55) ** 2 + 20
    ph = 2 * np.pi * np.cumsum(f) / SR; x = signal.sawtooth(ph) + 0.6 * signal.sawtooth(ph * 1.5)
    return st(norm(lp(x, 1800) * (1 - t / 0.55)))
def explosion():
    n = int(2.6 * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    cut = 200 + 5000 * np.exp(-t * 2.5); y = np.zeros(n); blk = 480
    for i in range(0, n, blk):
        b, a = signal.butter(2, cut[i], 'low', fs=SR); y[i:i + blk] = signal.lfilter(b, a, x[i:i + blk])
    y = y * np.exp(-t * 1.6); s = sub(70, 25, 2.0); y = norm(y) * 0.8; y[:len(s)] += s
    cr = (rng.random(n) < 0.0009) * rng.standard_normal(n) * np.exp(-t * 3); y += hp(cr, 2000) * 0.5
    return reverb(norm(np.tanh(y * 1.5)), 2.8, 0.3)
def notif():
    n = int(0.7 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f, d0 in [(392, 0), (587.3, 0.09)]:
        m = t >= d0; tt = t[m] - d0; x[m] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7) * np.minimum(1, tt / 0.01) + 0.3 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 12)
    return reverb(st(norm(x)), 1.3, 0.3)
def shimmer():
    n = int(2.2 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in [2093, 2637, 3136, 4186]: x += np.sin(2 * np.pi * f * t + rng.random() * 6) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t + rng.random() * 6))
    return reverb(st(norm(x * np.exp(-t * 1.8) * np.minimum(1, t / 0.05))), 2.0, 0.4)
def hum():
    n = int(1.1 * SR); t = np.arange(n) / SR; x = lp(signal.square(2 * np.pi * 100 * t), 500) * np.minimum(1, t / 0.05) * np.exp(-t * 1.5)
    return st(norm(x))
def drone():
    n = int(2.5 * SR); t = np.arange(n) / SR; x = np.sin(2 * np.pi * 41 * t) + 0.6 * np.sin(2 * np.pi * 61.5 * t) + 0.3 * lp(rng.standard_normal(n), 300)
    return reverb(st(norm(x * np.sin(np.pi * t / 2.5) ** 2)), 2.0, 0.3)
def servo():
    n = int(0.6 * SR); t = np.arange(n) / SR; f = 260 + 500 * t / 0.6; x = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 30 * t)))
    return st(norm(lp(x, 2500) * np.sin(np.pi * t / 0.6)))
def dive(): w = whoosh(0.8, 200, 5000, (0, 0)); r = riser(0.75); n = max(len(w), len(r)); out = np.zeros((n, 2)); out[:len(w)] += w; out[:len(r)] += r * 0.6; return norm(out)
def suck():
    r = reverse_tail(1.3); rs = riser(1.3); out = r * 0.7 + rs[:len(r)] * 0.6; return norm(out)

def blackhole():
    n = int(1.4 * SR); t = np.arange(n) / SR; f = 90 * np.exp(-t * 1.6) + 18
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + 0.5 * np.sin(2 * np.pi * 7 * t)) + 0.6 * lp(rng.standard_normal(n), 400)
    x = lp(x, 900) * np.minimum(1, t / 0.15) * np.exp(-np.maximum(0, t - 0.9) * 4)
    w2 = whoosh(1.2, 2500, 120, (0.6, -0.6)); out = st(norm(np.tanh(x * 1.5))); out[:len(w2)] += w2 * 0.5
    return reverb(norm(out), 2.2, 0.35)
SFX = {'blackhole': blackhole,
    'whoosh': lambda: whoosh(0.6, 350, 3500), 'whoosh_long': lambda: whoosh(1.4, 200, 2500), 'whoosh_small': lambda: whoosh(0.35, 600, 4500),
    'whoosh_fast': lambda: whoosh(0.3, 500, 6000, (-1, 1)), 'whoosh_fall': lambda: whoosh(0.8, 2500, 250, (0.4, -0.4)), 'whoosh_up': lambda: whoosh(0.6, 300, 6000, (0, 0.6)),
    'whoosh_soft': lambda: whoosh(1.2, 250, 1500, (-0.4, 0.4)) * 0.7, 'rev_whoosh': lambda: reverse_tail(0.6),
    'tick': tick, 'key': key, 'click': click, 'click_heavy': lambda: hit('small'),
    'boom': boom, 'braam': braam, 'dive': dive, 'suck': suck, 'riser_short': lambda: riser(1.0), 'riser_long': lambda: riser(7.6),
    'hit_small': lambda: hit('small'), 'hit_med': lambda: hit('med'), 'hit_big': lambda: hit('big'), 'hit_dry': lambda: hit('dry'), 'hit_dry_low': lambda: hit('dry_low'), 'hit_soft': lambda: hit('soft'),
    'thump': lambda: hit('soft'), 'impact': lambda: hit('big'), 'impact_huge': lambda: norm(hit('big') + boom()[:len(hit('big'))] * 0.6) if False else hit('big'),
    'subhit': lambda: hit('med'), 'slash': slash, 'glitch': glitch, 'tapestop': tapestop, 'explosion': explosion, 'notif': notif, 'shimmer': shimmer, 'hum': hum, 'drone': drone, 'servo': servo,
}

# ---- versão MÚSICA PRINCIPAL (motion music) ----
# Padrão aprovado (Training Season, 21/10/2026): só a música + o close-up no buraco negro do final.
# SFX sintetizados das cues só entram com --com-sfx (aí ficam --sfx-db abaixo da música).
TMP = os.path.join(os.path.dirname(os.path.abspath(A.out)), '_cache'); os.makedirs(TMP, exist_ok=True)  # temporários no projeto (regra dele)
cues = json.load(open(A.cues)) if A.cues and os.path.exists(A.cues) else []
mp = os.path.join(TMP, '_mus.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A.music, '-ar', '48000', '-ac', '2', mp], check=True)
mus, _ = sf.read(mp); mus = np.pad(mus, ((0, max(0, N - len(mus))), (0, 0)))[:N]
def rmsdb(x): x = x[np.abs(x) > 1e-4]; return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12) if len(x) else -120
ref = rmsdb(mus)
v1 = None
if A.vacuo:
    # VÁCUO: a música é SUGADA (nunca desacelera): reverb invertido crescendo, estéreo fechando no centro,
    # faixa estreitando, volume subindo e corte seco no buraco negro (onde bate o close-up)
    v0, v1 = [float(v) for v in A.vacuo.split(':')]
    i0, i1 = int(v0 * SR), int(v1 * SR); L = i1 - i0; u = (np.arange(L) / L)[:, None]
    seg = mus[i0:i1].copy()
    wet = reverb(seg[::-1].copy(), 1.6, 1.0)[:L][::-1]; wet = wet / (np.max(np.abs(wet)) + 1e-9) * np.max(np.abs(seg))
    m0 = seg * (1 - u ** 1.4) + wet * (u ** 1.4) * 1.25
    mid, side = (m0[:, 0] + m0[:, 1]) / 2, (m0[:, 0] - m0[:, 1]) / 2; side *= (1 - u[:, 0]) ** 1.5
    m0 = np.stack([mid + side, mid - side], 1)
    uu = u[:, 0]; hpc = 20 * (700 / 20) ** (uu ** 1.5); lpc = 18000 * (1400 / 18000) ** (uu ** 1.3)
    out = np.zeros_like(m0); blk = 480; zh = np.zeros((2, 2)); zl = np.zeros((2, 2))
    for k in range(0, L, blk):
        bh, ah = signal.butter(2, hpc[k], 'high', fs=SR); bl, al = signal.butter(2, lpc[k], 'low', fs=SR)
        y, zh = signal.lfilter(bh, ah, m0[k:k + blk], axis=0, zi=zh); out[k:k + blk], zl = signal.lfilter(bl, al, y, axis=0, zi=zl)
    out *= (1 + 2.2 * u ** 1.5); fo = int(0.03 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    mus[i0:i1] = out; mus[i1:] = 0
mix = mus.copy()
if A.closeup:
    cu, csr = sf.read(A.closeup); cu = cu if cu.ndim == 2 else np.stack([cu, cu], 1)
    if csr != SR: cu = signal.resample(cu, int(len(cu) * SR / csr))
    at = (v1 if v1 is not None else DUR - 1.0) - A.closeup_peak
    ci = max(0, int(at * SR)); seg = cu[:max(0, N - ci)]; fx = np.zeros_like(mus); fx[ci:ci + len(seg)] = seg
    mix += fx * 10 ** ((ref - rmsdb(cu)) / 20)
if A.com_sfx and cues:
    bus = np.zeros((N + SR * 4, 2)); cache = {}
    for c in cues:
        s = c.get('sfx')
        if not s or s not in SFX: continue
        x = SFX[s]() if s in ('key', 'whoosh', 'whoosh_small', 'tick') else cache.setdefault(s, SFX[s]())
        if x.ndim == 1: x = st(x)
        x = norm(x) * c['v']; i = int(c['t'] * SR)
        if i < 0: x = x[-i:]; i = 0
        if i >= len(bus): continue
        bus[i:i + len(x)] += x[:len(bus) - i]
    bus = bus[:N]
    if np.any(bus): mix += bus * 10 ** ((ref + A.sfx_db - rmsdb(bus)) / 20)
pre = os.path.join(TMP, '_pre.wav'); sf.write(pre, mix / (np.max(np.abs(mix)) + 1e-9) * 0.9, SR)
def lufs(p):
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', p, '-af', 'loudnorm=I=-14:TP=-1:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(o.split('"input_i" : "')[1].split('"')[0])
gain = -14 - lufs(pre)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', pre, '-af', f'volume={gain:.2f}dB,alimiter=limit=0.891:attack=5:release=60:level=disabled', '-ar', '48000', A.out], check=True)
print('mix ok', A.out, 'LUFS', round(lufs(A.out), 2))
