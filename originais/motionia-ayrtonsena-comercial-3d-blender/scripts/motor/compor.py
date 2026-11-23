# Compoe o video: fundo/palavras (canvas) -> lata 3D (Blender, com alfa) -> textos/cartao (canvas),
# brilho leve nas luzes fortes, e o audio. Gera a folha de contato (1 quadro por batida).
# Uso: python compor.py <rascunho|previa|final> [--so-com-musica]
import math, os, shutil, subprocess, sys
import config as C

PROJ, q = C.PROJETO, sys.argv[1]
R = C.RENDER / q
QB, TOTAL, N_BATIDAS, TL = C.QB, C.TOTAL, C.N_BATIDAS, C.TL
W, H = {"final": (1920, 1080), "previa": (960, 540)}.get(q, (640, 360))
PLANOS = ["revela", "giros", "helice", "helice_rapido"]   # helice_rapido: quadros da previa ampliados (ampliar.py), so onde falta o 1080p
F = C.F
DET, REV = TL["detalhes"], TL["revela"]


def origem(f):
    """quadro renderizado que entra no quadro f do video. A abertura usa o plano "queda" ate os detalhes;
    nos detalhes entram os 4 closes (renderizados de 1 batida cada, a partir da revelacao) com meia batida cada."""
    if f < F(DET):
        return R / "queda" / f"f_{f:04d}.png"
    if f < F(REV):
        k = min(3, int((f - F(DET)) // (QB / 2)))
        src = math.ceil(F(REV + k)) + (f - math.ceil(F(DET) + k * QB / 2))
        return R / "detalhes" / f"f_{src:04d}.png"
    return next((R / p / f"f_{f:04d}.png" for p in PLANOS if (R / p / f"f_{f:04d}.png").exists()), None)


def ligar(origem_, destino):
    try:
        os.link(origem_, destino)          # sem copiar (mesmo disco)
    except OSError:
        shutil.copy2(origem_, destino)


# junta os quadros 3D numa sequencia unica
uni = R / "lata3d"
uni.mkdir(parents=True, exist_ok=True)
vazio = R / "vazio.png"
if not vazio.exists():
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black@0.0:s={W}x{H},format=rgba",
                    "-frames:v", "1", str(vazio)], check=True)
faltando = []
for f in range(TOTAL):
    destino = uni / f"f_{f:04d}.png"
    if destino.exists():
        destino.unlink()
    origem_ = origem(f)
    origem_ = origem_ if origem_ and origem_.exists() else None
    if origem_ is None:
        if f < F(TL["logo"]):               # do logo pra frente e so 2D
            faltando.append(f)
        origem_ = vazio
    ligar(origem_, destino)
if faltando:
    print(f"AVISO: quadros 3D faltando ({len(faltando)}):", faltando[:20], "..." if len(faltando) > 20 else "")

nome = f"{C.MARCA} comercial 3D" + ("" if q == "final" else f" ({q})")
destino_mp4 = PROJ if q == "final" else C.RESULTADOS
destino_mp4.mkdir(exist_ok=True)
# brilho so nas partes bem claras; tem que ser em RGB (em YUV o blend screen deixa tudo magenta)
brilho = ("format=gbrp,split[a][b];[b]lutrgb=r='if(gt(val,205),val,0)':g='if(gt(val,205),val,0)':b='if(gt(val,205),val,0)',"
          f"gblur=sigma={12 if q == 'final' else 6}[g];[a][g]blend=all_mode=screen:all_opacity=0.45")
filtro = (f"[0:v][1:v]overlay=format=auto[x];[x][2:v]overlay=format=auto,{brilho},format=yuv420p[v]")
versoes = [("com musica", "audio_com_musica.wav"), ("sem musica", "audio_so_efeitos.wav")]
if "--so-com-musica" in sys.argv:
    versoes = versoes[:1]
for sufixo, audio in versoes:
    saida = destino_mp4 / f"{nome} ({sufixo}).mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", str(R / "tras" / "f_%04d.png"),
                    "-framerate", "30", "-i", str(uni / "f_%04d.png"), "-framerate", "30", "-i", str(R / "frente" / "f_%04d.png"),
                    "-i", str(C.RENDER / audio), "-filter_complex", filtro, "-map", "[v]", "-map", "3:a",
                    "-frames:v", str(TOTAL), "-c:v", "libx264", "-preset", "slow", "-crf", "16" if q == "final" else "20",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", str(saida)], check=True)
    print("video:", saida)

# folha de contato: um quadro por batida (meio da batida) - confira ela inteira antes de mostrar
mp4 = destino_mp4 / f"{nome} (com musica).mp4"
sel = "+".join(f"eq(n\\,{int((k + 0.5) * QB)})" for k in range(N_BATIDAS))
folha = C.RESULTADOS / f"folha-de-contato-{q}.png"
folha.parent.mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"select='{sel}',scale=320:-1,tile=8x{-(-N_BATIDAS // 8)}",
                "-frames:v", "1", str(folha)], check=True)
print("folha:", folha)
