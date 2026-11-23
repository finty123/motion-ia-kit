# Roda o render. Um Blender por vez, em prioridade baixa, retomando de onde parou (quadros prontos sao pulados).
# Uso:
#   python rodar.py <plano> <rascunho|previa|final> [quadros,de,teste]   um plano (com quadros vai pra render/testes)
#   python rodar.py tudo <rascunho|previa|final>    camadas + 5 planos + mixagem + video (so o final toca alarme)
#   python rodar.py rapido                          com pressa: termina a helice em previa, amplia, video final
#   python rodar.py medir <plano> <qualidade>       renderiza 3 quadros e diz quanto o plano todo vai levar
#   python rodar.py refazer <plano> <qualidade>     apaga os quadros desse plano e renderiza de novo (depois de um ajuste)
#   python rodar.py pecas                           monta pecas/pecas.blend com os modelos baixados (projeto.json -> pecas)
# Planos: queda, detalhes, revela, giros, helice (a helice e o pesado).
import os, subprocess, sys, time
from pathlib import Path
import config as C
import sistema as S

PLANOS = ["queda", "detalhes", "revela", "giros", "helice"]
LOGS = C.PROJETO / "logs"
LOGS.mkdir(exist_ok=True)
BLENDER = S.encontrar_blender(C.CFG)


def py(script, *args):
    r = subprocess.run([sys.executable, str(C.AQUI / script), *args])
    if r.returncode:
        sys.exit(f"{script} falhou (codigo {r.returncode})")


def quadros_prontos(plano, qualidade):
    return len(list((C.RENDER / qualidade / plano).glob("f_*.png")))


def plano(nome, qualidade, teste=None):
    if not BLENDER:
        sys.exit("Blender nao encontrado: instale o 4.2 ou mais novo, ou ponha o caminho em projeto.json (\"blender\")")
    S.esperar_blender()
    env = dict(os.environ)
    env.setdefault("AMOSTRAS_FINAL", "24")
    cmd = [BLENDER, "-b", "-P", str(C.AQUI / "comercial.py"), "--", nome, qualidade] + ([teste] if teste else [])
    antes, t0 = quadros_prontos(nome, qualidade), time.time()
    print(f"== {nome} {qualidade}" + (f" quadros {teste}" if teste else ""), flush=True)
    cod = S.rodar_baixo(cmd, LOGS / f"{nome}-{qualidade}.txt", env)
    feitos = (len(teste.split(",")) if teste else quadros_prontos(nome, qualidade) - antes)
    dt = time.time() - t0
    print(f"   {feitos} quadros em {dt / 60:.1f} min" + (f" ({dt / feitos:.1f} s/quadro)" if feitos else ""), flush=True)
    log = (LOGS / f"{nome}-{qualidade}.txt").read_text(encoding="utf-8", errors="replace")
    if cod or "Traceback" in log:
        print(log[-2500:])
        sys.exit(f"o plano {nome} deu erro: veja logs/{nome}-{qualidade}.txt")


def intervalo(nome):
    """quadros que o plano renderiza (pra estimar o tempo)"""
    tl, F = C.TL, C.F
    return {"queda": (0, F(tl["revela"])), "detalhes": (F(tl["revela"]), F(tl["revela"] + 4)),
            "revela": (F(tl["revela"]), F(tl["trocas"][0]) - 8), "giros": (F(tl["trocas"][0]) - 8, F(tl["cruz"])),
            "helice": (F(tl["cruz"]), F(tl["logo"]))}[nome]


def medir(nome, qualidade):
    a, b = intervalo(nome)
    q = [int(a + (b - a) * k) for k in (0.25, 0.55, 0.85)]
    t0 = time.time()
    plano(nome, qualidade, ",".join(map(str, q)))
    por = (time.time() - t0) / 3      # inclui montar a cena (mais pessimista, e melhor assim)
    total = (b - a) * por
    print(f"ESTIMATIVA {nome} {qualidade}: ~{por:.0f} s/quadro x {int(b - a)} quadros = ~{total / 60:.0f} min")


def tudo(qualidade):
    t0 = time.time()
    py("camadas.py", qualidade)
    for p in PLANOS:
        plano(p, qualidade)
    py("mixar.py")
    py("compor.py", qualidade)
    print(f"PRONTO {qualidade} em {(time.time() - t0) / 60:.0f} min")
    if qualidade == "final":
        S.alarme()


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit("uso: python rodar.py <plano> <rascunho|previa|final> [quadros] | tudo <qualidade> | rapido | medir <plano> <qualidade>")
    if a[0] == "tudo":
        tudo(a[1])
    elif a[0] == "rapido":      # os planos leves em 1080p; so a helice (o pesado) em previa ampliada
        for p in PLANOS[:-1]:
            plano(p, "final")
        plano("helice", "previa")
        py("ampliar.py")
        py("camadas.py", "final")
        py("mixar.py")
        py("compor.py", "final")
        S.alarme()
    elif a[0] == "refazer":    # o motor pula quadros que ja existem: depois de mudar a cena, eles precisam sair
        for f in (C.RENDER / a[2] / a[1]).glob("f_*.png"):
            f.unlink()
        plano(a[1], a[2])
    elif a[0] == "pecas":
        S.esperar_blender()
        cod = S.rodar_baixo([BLENDER, "-b", "-P", str(C.AQUI / "preparar_pecas.py")], LOGS / "pecas.txt")
        print((LOGS / "pecas.txt").read_text(encoding="utf-8", errors="replace")[-1500:])
        sys.exit(cod)
    elif a[0] == "medir":
        medir(a[1], a[2])
    else:
        plano(a[0], a[1], a[2] if len(a) > 2 else None)
