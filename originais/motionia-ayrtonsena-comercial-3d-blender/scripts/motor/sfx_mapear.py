# Procura na pasta de efeitos sonoros da pessoa um arquivo pra cada tipo que o comercial usa e grava em
# projeto.json ("sfx"). Escolhe pelo nome do arquivo e descarta o que nao combina (vidro, pop, blip, laser...).
# Uso: python sfx_mapear.py "<pasta de SFX>"    -> mostra o que escolheu (confira e ajuste se quiser)
import json, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PROIBIDO = ["glass", "vidro", "pop", "blip", "bip", "beep", "laser", "cartoon", "bubble", "bolha", "kid",
            "infantil", "game", "coin", "moeda", "arcade", "8bit", "8-bit", "boing", "squeak", "fart", "notif"]
TIPOS = {   # tipo: (palavras que contam ponto, quantos arquivos guardar)
    "whoosh_grave": (["sub", "large", "deep", "low", "grave", "heavy", "big"], 1),
    "whoosh": (["whoosh", "woosh", "swoosh", "swish", "swipe", "transition"], 4),
    "whoosh_corredor": (["riser", "pass", "fly", "woosh", "whoosh"], 1),
    "boom": (["boom", "bang", "impact", "hit", "explosion", "thud", "cinematic"], 2),
    "clique": (["shutter", "camera", "obturador", "click", "clique"], 1),
    "spot": (["lamp", "light switch", "switch", "spotlight", "lampada", "interruptor"], 1),
    "soco": (["punch", "soco", "kick", "thump", "body hit"], 1),
    "lamina": (["knife", "sword", "blade", "lamina", "faca", "snickt", "metal"], 1),
}
EXT = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aif", ".aiff"}

pasta = Path(sys.argv[1])
arqs = [p for p in pasta.rglob("*") if p.suffix.lower() in EXT]
if not arqs:
    sys.exit(f"nenhum audio em {pasta}")


def nota(p, tipo):
    palavras = TIPOS[tipo][0]
    nome = str(p.relative_to(pasta)).lower()
    if any(x in nome for x in PROIBIDO):
        return -1
    if tipo == "whoosh_grave" and not any(w in nome for w in ("whoosh", "woosh", "swoosh")):
        return 0   # o grave da queda tem que ser um whoosh
    return sum(2 for w in palavras if w in p.stem.lower()) + sum(1 for w in palavras if w in nome)


escolha, usados = {}, set()
for tipo, (palavras, qtd) in TIPOS.items():
    cand = sorted(((nota(p, tipo), str(p)) for p in arqs if str(p) not in usados), reverse=True)
    cand = [c for n, c in cand if n > 0][:qtd]
    usados.update(cand)
    escolha[tipo] = [str(Path(c).relative_to(pasta)).replace("\\", "/") for c in cand]

cfg_p = AQUI / "projeto.json"
cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
cfg["sfx"] = {"pasta": str(pasta), "arquivos": escolha}
cfg_p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
for tipo, lst in escolha.items():
    print(f"{tipo:16s} {', '.join(lst) if lst else '(nada na pasta: vai o sintetico)'}")
