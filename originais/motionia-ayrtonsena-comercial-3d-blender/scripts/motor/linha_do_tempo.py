# Linha do tempo do comercial, em batidas da musica (batida 1 = quadro 0).
# O arco e o do comercial aprovado (Dane-se v3); so muda o numero de sabores e o encaixe na musica.
# Uso: python linha_do_tempo.py            -> calcula, sugere o corte da musica e grava em projeto.json
#      python linha_do_tempo.py --mostrar  -> so imprime a tabela (pra mostrar e aprovar)
import json, math, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def gerar(n_sabores):
    """Arco aprovado: queda com gota -> olho -> 4 closes secos -> lata sobe -> uma troca de sabor por sabor
    (a primeira com mais tempo, depois acelerando) -> cata-vento com rastro -> furo -> corredor neon ->
    fileira acendendo uma lata por batida -> logo com stroke -> so o @."""
    n = max(1, n_sabores)
    passos = [2, 2, 1.5]
    trocas, t = [], 10.0
    for k in range(n):
        trocas.append(t)
        t += passos[k] if k < len(passos) else 1.5
    cruz = float(math.ceil(trocas[-1] + 1.5))   # batida inteira: o corte da musica nao pode cair no contratempo
    furo = cruz + 8                      # o furo cai na pausa da musica (ver sugerir_corte)
    fileira = furo + 4.5
    n_fileira = max(3, n)
    acende = [fileira + 0.5 + k for k in range(n_fileira)]
    logo = acende[-1] + 2
    return {
        "queda_lenta": 3, "olho": 5, "detalhes": 7, "revela": 9,
        "trocas": trocas, "cruz": cruz, "rastro": cruz + 1, "mergulho": furo - 2, "furo": furo,
        "fim_corredor": furo + 2.3, "fileira": fileira, "acende": acende,
        "logo": logo, "arroba": logo + 4.5, "fim": logo + 8.6,
    }


def n_batidas(tl):
    return int(math.ceil(tl["fim"]))


def sugerir_corte(beats, inicio_s, furo):
    """Procura uma pausa da musica (queda forte de energia seguida de volta) depois do inicio do trecho.
    Devolve (corte, texto): corte = [batida do video onde emenda, batida do trecho que entra ali] ou None.
    Assim a pausa cai no furo e a volta forte cai no corredor, como no comercial aprovado."""
    bt = beats.get("batidas", [])
    pausas = beats.get("pausas", [])
    if not bt:
        return None, "sem beats.json: rode batidas.py antes"
    s0 = min(range(len(bt)), key=lambda i: abs(bt[i] - inicio_s))
    for p in pausas:
        # batida do trecho que entra no furo: a anterior a pausa (a camera atravessa o furo e a musica cai
        # logo em seguida, como no comercial aprovado)
        b_trecho = p["batida"] - s0
        if b_trecho == round(furo):
            return None, f"a pausa ({p['tempo']:.1f}s) ja cai no furo sem cortar nada"
        if b_trecho > furo:
            return [furo, b_trecho], (f"pausa em {p['tempo']:.1f}s da musica: pulando da batida {furo:g} "
                                      f"pra {b_trecho} do trecho, ela cai no furo e a volta forte no corredor")
    return None, "nenhuma pausa clara depois do inicio: o furo fica sem corte na musica (ou escolha outro trecho)"


def tabela(tl, sabores):
    nomes = [s.get("nome", f"sabor {i + 1}") for i, s in enumerate(sabores)] or ["sabor 1"]
    seq = [nomes[(k + 1) % len(nomes)] for k in range(len(tl["trocas"]))]
    linhas = [
        ("1-" + f"{tl['detalhes']:g}", "queda", f"camera cai junto com uma gota ate quase encostar na tampa; na batida {tl['olho']:g} desce rapido e encara o foco do rotulo"),
        (f"{tl['detalhes']:g}-{tl['revela']:g}", "detalhes", "4 closes de meia batida em corte seco (tampa, logo, lateral, pescoco)"),
        (f"{tl['revela']:g}-{tl['trocas'][0]:g}", "revela", f"a lata sobe de baixo ja girando ({nomes[0]})"),
    ]
    for b, nome in zip(tl["trocas"], seq):
        linhas.append((f"{b:g}", "giros", f"giro rapido troca pra {nome}: fundo, palavra atras e pecas explodindo"))
    linhas += [
        (f"{tl['cruz']:g}", "helice", "as latas abrem em cata-vento (fundo fixo, giro liso)"),
        (f"{tl['rastro']:g}-{tl['mergulho']:g}", "helice", "rastro de copias nitidas abre o leque"),
        (f"{tl['mergulho']:g}-{tl['furo']:g}", "helice", "camera mergulha; o furo do meio abre"),
        (f"{tl['furo']:g}-{tl['fim_corredor']:g}", "helice", "atravessa o furo (pausa da musica) e entra no corredor de aneis neon"),
        (f"{tl['fim_corredor']:g}-{tl['fileira']:g}", "helice", "sai na fileira de latas em silhueta, chao espelhado"),
        (f"{tl['acende'][0]:g}-{tl['acende'][-1]:g}", "helice", "uma lata acende por batida, camera desliza e freia na ultima"),
        (f"{tl['logo']:g}-{tl['arroba']:g}", "canvas", "logo se desenha em stroke, preenche; linha do produto e aviso"),
        (f"{tl['arroba']:g}-{tl['fim']:g}", "canvas", "so a assinatura (@), bastante tempo, fecha no preto"),
    ]
    out = ["| Batidas | Plano | O que acontece |", "|---|---|---|"]
    out += [f"| {a} | {b} | {c} |" for a, b, c in linhas]
    return "\n".join(out)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    cfg_p = AQUI / "projeto.json"
    cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
    beats_p = AQUI / "beats.json"
    beats = json.loads(beats_p.read_text(encoding="utf-8")) if beats_p.exists() else {}
    sabores = cfg.get("sabores", [])
    if not sabores or any(s.get("modelo", "").startswith("nome-do-arquivo") for s in sabores):
        sys.exit("projeto.json ainda e o modelo: preencha marca, sabores e musica.inicio antes (references/projeto-json.md)")
    tl = cfg.get("linha_do_tempo") or gerar(len(sabores))
    mudou = len(tl.get("trocas", [])) != max(1, len(sabores))   # numero de sabores mudou: a linha antiga nao serve
    if "--mostrar" not in sys.argv:
        if "--refazer" in sys.argv or mudou or not cfg.get("linha_do_tempo"):
            tl = gerar(len(sabores))
        mus = cfg.setdefault("musica", {})
        if "corte" not in mus or "--refazer" in sys.argv or mudou:
            corte, txt = sugerir_corte(beats, float(mus.get("inicio", 0)), tl["furo"])
            mus["corte"] = corte
            print("musica:", txt)
        cfg["linha_do_tempo"] = tl
        cfg_p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    bpm = float(cfg.get("musica", {}).get("bpm") or beats.get("bpm") or 120)
    nb = n_batidas(tl)
    print(f"{len(sabores)} sabores, {nb} batidas a {bpm:.2f} BPM = {nb * 60 / bpm:.1f} s\n")
    print(tabela(tl, sabores))
