# Mixagem: efeitos cinematograficos nas batidas + trecho da musica, normalizado em -14 LUFS.
# Gera render/audio_com_musica.wav e render/audio_so_efeitos.wav.
# Os efeitos vem de projeto.json ("sfx": pasta + arquivo de cada tipo, preenchido pelo sfx_mapear.py);
# o tipo que faltar sai do sfx_sintetico.py (assets/sfx/<tipo>.wav).
# Uso: python mixar.py
import shutil, subprocess
from pathlib import Path
import numpy as np
import config as C

SR = 48000
P = 60 / C.BPM
TL = C.TL
DUR = C.N_BATIDAS * P + 0.05
B = lambda n: (n - 1) * P
SFX_PROJ = C.AQUI / "assets" / "sfx"
MUS = C.MUSICA
TIPOS = ["whoosh_grave", "whoosh", "whoosh_corredor", "boom", "clique", "spot", "soco", "lamina"]

# (batida, tipo, ganho dB, alinhamento: "inicio" | "pico" | "fim", invertido, variacao)
CUES = [(1.25, "whoosh_grave", -6, "pico", False, 0),            # camera despenca junto com a gota
        (TL["olho"], "whoosh", -7, "pico", False, 3)]            # mergulho ate o foco do rotulo
for k in range(4):                                               # closes em corte seco
    CUES.append((TL["detalhes"] + k / 2, "clique", -10, "inicio", False, 0))
CUES.append((TL["revela"] + 0.3, "whoosh", -8, "pico", False, 2))   # lata sobe
for b in TL["trocas"]:                                           # trocas com explosao
    CUES += [(b, "whoosh", -8, "pico", False, 3), (b, "boom", -7, "inicio", False, 0)]
CUES += [(TL["cruz"], "whoosh_grave", -5, "pico", False, 0), (TL["cruz"], "boom", -5, "inicio", False, 0)]
CUES += [(TL["rastro"] + 1, "whoosh", -15, "pico", False, 0), (TL["rastro"] + 3, "whoosh", -13.2, "pico", False, 1)]
CUES += [(TL["furo"], "whoosh", -7, "fim", True, 2),             # entra no furo (pausa da musica)
         (TL["furo"] + 1.8, "whoosh_corredor", -6, "pico", False, 0)]
for b in TL["acende"]:                                           # spot acendendo cada lata
    CUES += [(b, "spot", -3, "inicio", False, 0), (b, "soco", -15, "inicio", False, 0)]
CUES += [(TL["logo"], "boom", -9, "inicio", False, 0), (TL["logo"] + 0.1, "lamina", -13, "inicio", False, 0),
         (TL["arroba"], "whoosh", -14, "pico", False, 2)]


def ler(caminho, ini=None, dur=None):
    cmd = ["ffmpeg", "-v", "error"]
    if ini is not None:
        cmd += ["-ss", str(ini)]
    if dur is not None:
        cmd += ["-t", str(dur)]
    cmd += ["-i", str(caminho), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)
    return x.reshape(-1, 2).copy()


def salvar(x, caminho):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=11", "-ar", str(SR), str(caminho)],
                   input=x.astype(np.float32).tobytes(), check=True)


def sons_do_tipo(tipo):
    """lista de sons de um tipo: os escolhidos na pasta do usuario (copiados pro projeto) ou o sintetico"""
    sfx = C.CFG.get("sfx", {})
    pasta = Path(sfx.get("pasta", "")) if sfx.get("pasta") else None
    escolhidos = sfx.get("arquivos", {}).get(tipo) or []
    escolhidos = [escolhidos] if isinstance(escolhidos, (str, dict)) else escolhidos
    SFX_PROJ.mkdir(parents=True, exist_ok=True)
    sons = []
    for item in escolhidos:
        rel, ini, dur = (item, None, None) if isinstance(item, str) else (item["arquivo"], item.get("ini"), item.get("dur"))
        destino = SFX_PROJ / Path(rel).name
        if not destino.exists() and pasta and (pasta / rel).exists():
            shutil.copy2(pasta / rel, destino)   # tudo que o projeto usa fica na pasta dele
        if destino.exists():
            sons.append(ler(destino, ini, dur))
    if not sons:
        sint = SFX_PROJ / f"{tipo}.wav"
        if not sint.exists():
            subprocess.run(["python", str(C.AQUI / "sfx_sintetico.py")], check=True)
        sons.append(ler(sint))
    return sons


sons = {t: sons_do_tipo(t) for t in TIPOS}
n = int(DUR * SR)
efeitos = np.zeros((n, 2), dtype=np.float32)
for batida, tipo, db, alinha, inv, var in CUES:
    s = sons[tipo][var % len(sons[tipo])]
    s = s[::-1] if inv else s
    env = np.convolve(np.abs(s).mean(axis=1), np.ones(480) / 480, mode="same")
    ref = {"inicio": 0, "pico": int(env.argmax()), "fim": len(s)}[alinha]
    i0 = int(B(batida) * SR) - ref
    a, z = max(0, i0), min(n, i0 + len(s))
    if z > a:
        efeitos[a:z] += s[a - i0:z - i0] * (10 ** (db / 20))

mix = efeitos.copy()
arq = MUS.get("arquivo")
if arq:
    caminho = Path(arq) if Path(arq).is_absolute() else C.PROJETO / arq
    ini = float(MUS.get("inicio", 0))
    corte = MUS.get("corte")
    if corte:      # pula um trecho: a pausa da musica cai no furo e a volta forte no corredor
        a_, z_ = corte
        parte1 = ler(caminho, ini, B(a_))
        parte2 = ler(caminho, ini + B(z_), DUR - B(a_) + 0.1)
        xf = int(0.012 * SR)                       # emenda com crossfade curtinho, sem clique
        rampa = np.linspace(0, 1, xf)[:, None]
        musica = np.concatenate([parte1[:-xf], parte1[-xf:] * (1 - rampa) + parte2[:xf] * rampa, parte2[xf:]])
    else:
        musica = ler(caminho, ini, DUR)
    musica = musica[:n]
    musica = np.pad(musica, ((0, n - len(musica)), (0, 0)))
    fade = int(0.3 * SR)
    musica[-fade:] *= np.linspace(1, 0, fade)[:, None]
    mix = efeitos + musica * (10 ** (float(MUS.get("volume_db", -5)) / 20))   # musica abaixo dos efeitos

C.RENDER.mkdir(parents=True, exist_ok=True)
salvar(mix, C.RENDER / "audio_com_musica.wav")
salvar(efeitos, C.RENDER / "audio_so_efeitos.wav")
print("audio pronto:", round(DUR, 2), "s,", len(CUES), "efeitos", "(sem musica)" if not arq else "")
