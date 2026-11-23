# Fabrica de latas: pra cada rotulo em <projeto>/rotulos/ que ainda nao tem modelo, amplia o rotulo
# (se for pequeno), monta a lata no Blender (prioridade baixa) e salva <projeto>/modelos/<nome>/
# com rotulo_2x.png (o que o comercial usa), lata.blend e previa.jpg (frente, giro, tampa) pra aprovar.
# Uso: python latas.py            -> so os rotulos novos
#      python latas.py "nome"     -> refaz esse (nome do arquivo sem extensao)
import os, subprocess, sys
import config as C
import sistema as S

ROTULOS, MODELOS = C.PROJETO / "rotulos", C.PROJETO / "modelos"
BLENDER = S.encontrar_blender(C.CFG)
if not BLENDER:
    sys.exit("Blender nao encontrado: instale o 4.2 ou mais novo, ou ponha o caminho em projeto.json (\"blender\")")
cor_de = {s.get("modelo", s.get("nome")): s.get("cor", "#ff0f6b") for s in C.SABORES}

so = sys.argv[1] if len(sys.argv) > 1 else None
rotulos = sorted(p for p in ROTULOS.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"))
for rot in rotulos:
    pasta = MODELOS / rot.stem
    if so and rot.stem != so:
        continue
    if not so and (pasta / "previa.jpg").exists():
        continue
    pasta.mkdir(parents=True, exist_ok=True)
    print(f"== {rot.stem}", flush=True)
    largura = int(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width",
                                  "-of", "csv=p=0", str(rot)], capture_output=True, text=True).stdout.split()[0])
    ampliado = pasta / "rotulo_2x.png"
    escala = "scale=iw*2:ih*2:flags=lanczos,unsharp=5:5:0.6" if largura < 2000 else "null"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(rot), "-vf", escala, str(ampliado)], check=True)
    S.esperar_blender()
    env = dict(os.environ, RAIO_LATA=str(C.RAIO), COR_LATA=cor_de.get(rot.stem, "#ff0f6b"))
    cod = S.rodar_baixo([BLENDER, "-b", "-P", str(C.AQUI / "fazer_lata.py"), "--", str(ampliado), str(pasta), "previa"],
                        pasta / "log.txt", env)
    if cod:
        sys.exit(f"deu erro na lata {rot.stem}: veja {pasta / 'log.txt'}")
    entradas = [str(pasta / f"previa_{n}.png") for n in ("frente", "giro", "tampa")]
    filtro = "".join(f"[{i}]scale=540:-1[v{i}];" for i in range(3)) + "[v0][v1][v2]hstack=3"
    args = ["ffmpeg", "-v", "error", "-y"]
    for e in entradas:
        args += ["-i", e]
    subprocess.run(args + ["-filter_complex", filtro, "-q:v", "2", str(pasta / "previa.jpg")], check=True)
    print(f"   ok -> {pasta / 'previa.jpg'}", flush=True)
nomes = {p.stem for p in rotulos}
faltam = [m for m in cor_de if m not in nomes]
if faltam:
    print("AVISO: sabores do projeto.json sem rotulo em rotulos/:", faltam)
