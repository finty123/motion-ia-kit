"""Gera skills/ (versão adaptada a este PC) a partir de originais/ (como vieram do curso) + config.json.

Uso:  python ferramentas/adaptar.py            (lê config.json; se não existir, usa config.exemplo.json)

O que muda (e só isso):
  1. Pastas e assinatura do autor do curso -> as pastas e a assinatura do config.json.
  2. Scripts que só rodavam no Linux do chat (/tmp, file://) -> funcionam no Windows.
  3. No fim de cada SKILL.md entra a seção "Configuração deste computador".
Os originais nunca são alterados. Rode de novo sempre que mudar o config.json.
"""
import hashlib, json, re, shutil, sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
ORIG, OUT = KIT / "originais", KIT / "skills"
TEXTO = {".md", ".py", ".js", ".json", ".html", ".sh", ".txt", ".css"}


def carregar_config():
    for nome in ("config.json", "config.exemplo.json"):
        p = KIT / nome
        if p.exists():
            c = json.loads(p.read_text(encoding="utf-8"))
            break
    else:
        sys.exit("config.json não encontrado")
    c.setdefault("assinatura", "")
    if not c.get("pasta_projetos"):
        c["pasta_projetos"] = str(Path.home() / "Videos" / "Motion-Projetos")
    if not c.get("pasta_resultados"):
        c["pasta_resultados"] = str(Path(c["pasta_projetos"]) / "resultados")
    for k in ("pasta_projetos", "pasta_resultados"):
        c[k] = str(Path(c[k]))
    # SFX: pasta própria do usuário, se configurada; senão o pacote do kit que vai dentro de cada skill
    c["pasta_sfx"] = str(Path(c["pasta_sfx"])) if c.get("pasta_sfx") else ""
    c["sfx_txt"] = f"`{c['pasta_sfx']}`" if c["pasta_sfx"] else "`assets/sfx-kit/` (dentro da pasta desta skill)"
    return c


# skills que usam efeitos de interface: recebem uma cópia do pacote sfx/ do kit em assets/sfx-kit/
SFX_SKILLS = ("motion-ia-ayrton-nubank-app-style", "motionia-ayrtonsena-ifood-delivery", "motionia-ayrtonsena-comercial-3d-blender")


# ---------------------------------------------------------------- trocas pontuais
def trocas(c):
    proj, res, sfx = c["pasta_projetos"], c["pasta_resultados"], c["sfx_txt"]
    a = c["assinatura"].strip().lstrip("@")
    sig = f"@{a}" if a else "@<perfil do usuário>"
    sig_codigo = f"by @{a}" if a else "by @SEU_PERFIL"
    return {
        # ---- Nubank App Style
        "motion-ia-ayrton-nubank-app-style/SKILL.md": [
            ("Guia o Ayrton do briefing", "Guia o usuário do briefing"),
            ("final com logo e 'by @ayrtonsena.stg', música + SFX de UI da pasta dele",
             f"final com logo e assinatura 'by {sig}', música + SFX de UI do kit"),
            ("Use SEMPRE que o Ayrton pedir", "Use SEMPRE que o usuário pedir"),
            (r"C:\Users\Ayrton\Downloads\motion-<marca>", proj + r"\motion-<marca>"),
            (r"registra a prévia no `Downloads\.claude\launch.json`",
             r"registra a prévia no `.claude\launch.json` da pasta de projetos (" + proj + r"\.claude\launch.json)"),
            (r"(padrão: `D:\Backup\Videos\#clientes\Ayrton Sena\Motions\`)", f"(padrão: `{res}\\`)"),
        ],
        "motion-ia-ayrton-nubank-app-style/scripts/novo_projeto.py": [
            (r"C:\\Users\\Ayrton\\Downloads\\motion-<marca>", proj.replace("\\", "\\\\") + r"\\motion-<marca>"),
        ],
        "motion-ia-ayrton-nubank-app-style/references/briefing-e-roteiro.md": [
            ("O Ayrton quer só ativar a skill", "O usuário quer só ativar a skill"),
            ('Logo + "by @ayrtonsena.stg" (Recomendado)', f'Logo + "by {sig}" (Recomendado)'),
        ],
        "motion-ia-ayrton-nubank-app-style/references/cenas.md": [
            ('entra "by @ayrtonsena.stg"', f'entra "by {sig}"'),
        ],
        "motion-ia-ayrton-nubank-app-style/references/regras-do-ayrton.md": [
            ('**"by @ayrtonsena.stg"**', f'**"by {sig}"**'),
            (r"`D:\Backup\Videos\#clientes\Ayrton Sena\Motions\Motion <Marca>.mp4`", f"`{res}\\Motion <Marca>.mp4`"),
        ],
        "motion-ia-ayrton-nubank-app-style/references/audio.md": [
            (r"`D:\Backup\Videos\Edição de video\SFX\Ui`", f"{sfx} (pacote de SFX do kit; veja `manifest.json` lá dentro)"),
        ],
        "motion-ia-ayrton-nubank-app-style/assets/modelo/compositions/final.html": [
            ('"by @ayrtonsena.stg"', json.dumps(sig_codigo)),
        ],
        # ---- iFood Delivery
        "motionia-ayrtonsena-ifood-delivery/SKILL.md": [
            (r"- **Efeitos sonoros:** do Ayrton, em `D:\Backup\Videos\#clientes\SFX-20261024T181631Z-1-001\SFX` (veja `references/audio-e-batida.md`).",
             f"- **Efeitos sonoros:** o pacote de SFX do kit, em {sfx} (veja `references/audio-e-batida.md` e a tabela de equivalência no fim deste arquivo)."),
            (r"Os trabalhos do Ayrton vão em `D:\Backup\Videos\#clientes\Ayrton Sena\Motions`.", f"Os vídeos prontos vão em `{res}`."),
        ],
        "motionia-ayrtonsena-ifood-delivery/references/audio-e-batida.md": [
            ("## Efeitos (pasta do Ayrton)", "## Efeitos (pasta original do autor; neste PC use o pacote do kit, tabela no fim do SKILL.md)"),
        ],
        "motionia-ayrtonsena-ifood-delivery/references/briefing-e-copy.md": [
            ("(a pasta do Ayrton serve)", "(o pacote de SFX do kit serve)"),
        ],
        "motionia-ayrtonsena-ifood-delivery/references/regras-do-ayrton.md": [
            ("**@ayrtonsena.stg** preto no meio", f"**{sig}** preto no meio"),
        ],
        # ---- Comercial 3D (Blender): a seção "Se for o Ayrton" sai inteira (vira a seção do kit)
        "motionia-ayrtonsena-comercial-3d-blender/SKILL.md": [
            (re.compile(r"\n## Se for o Ayrton \(@ayrtonsena\.stg\)\n.*\Z", re.S), "\n"),
        ],
        # ---- Motion Music
        "motionia-ayrtonsena-motion-music/SKILL.md": [
            ("Projeto: no Code, `Downloads/<nome>-motion/`", f"Projeto: no Code, `{proj}\\<nome>-motion\\`"),
        ],
        "motionia-ayrtonsena-motion-music/references/fontes.md": [
            ("**Pack do Ayrton** (só no PC dele):", "**Pack do autor do curso** (não existe neste PC; use `assets/fonts` da skill ou Google Fonts):"),
        ],
    }


# ---------------------------------------------------------------- Linux -> Windows
CAB_UTF8 = ("import builtins as _bi; _op = _bi.open  # kit: no Windows, arquivo de texto sem encoding vira UTF-8\n"
            "def _open_utf8(f, mode='r', *a, **k):\n"
            "    if 'b' not in mode and 'encoding' not in k and len(a) < 2: k['encoding'] = 'utf-8'\n"
            "    return _op(f, mode, *a, **k)\n"
            "_bi.open = _open_utf8\n")


def windows_py(txt, utf8=False):
    """Scripts escritos pro chat (Linux): /tmp, file:// e open() sem encoding quebram no Windows."""
    mudou = utf8
    if re.search(r"""['"]/tmp/""", txt):
        txt = re.sub(r"""(['"])/tmp/""", r"_TMP + \1", txt)
        mudou = True
    if "'file://' + os.path.abspath(" in txt:
        txt = re.sub(r"'file://' \+ os\.path\.abspath\(([^()]+)\)", r"__import__('pathlib').Path(\1).resolve().as_uri()", txt)
        mudou = True
    if mudou:
        cab = ("import sys as _s, tempfile as _tf; _s.stdout.reconfigure(encoding='utf-8', errors='replace')  # kit: Windows\n"
               "_TMP = _tf.gettempdir().replace('\\\\', '/') + '/'\n" + (CAB_UTF8 if utf8 else ""))
        # depois da docstring do topo, se houver
        m = re.match(r'(\s*""".*?"""\s*\n)', txt, re.S)
        txt = (m.group(1) + cab + txt[m.end():]) if m else cab + txt
    return txt


# ---------------------------------------------------------------- seção do kit
TABELA_SFX = """| Pedido na skill (pasta do autor) | Use do pacote do kit |
|---|---|
| clique / toque / Ui click / Click digital | `click.mp3`, `click-soft.mp3`, `key-press.mp3` |
| pop-up / card / pílula / Correct | `pop.mp3`, `ping.mp3`, `notification.mp3` |
| interface / chip ativa | `click-soft.mp3`, `sparkle.mp3` |
| whoosh / swoosh / troca de cena | `whoosh.mp3`, `whoosh-short.mp3`, `whoosh-cinematic.mp3` |
| notificação / sucesso / Iphone | `notification.mp3`, `chime.mp3` |
| impacto / Sub Boom / Trailer Boom | `impact-bass-1.mp3`, `impact-bass-2.mp3` |
| digitação | `typing.mp3`, `key-press.mp3` |
| glitch | `glitch-1.mp3`, `glitch-2.mp3`, `glitch-3.mp3` |
| riser | `riser.mp3` (só onde a skill permitir) |
| erro | `error.mp3` |

O `manifest.json` da pasta descreve cada arquivo (duração e uso). Se o usuário tiver uma pasta própria de efeitos, prefira a dele."""


def secao_kit(nome, c):
    proj, res, sfx = c["pasta_projetos"], c["pasta_resultados"], c["sfx_txt"]
    a = c["assinatura"].strip().lstrip("@")
    sig = (f"`@{a}` (configurada no kit). Use só quando o estilo pedir assinatura e confirme no briefing."
           if a else "não configurada: pergunte no briefing qual @ ou nome usar. Sem resposta, o vídeo sai sem assinatura.")
    s = f"""

---

## Configuração deste computador (kit Motion IA)

> Seção acrescentada pelo instalador do kit. Ela vale mais que qualquer pasta ou assinatura citada acima.

- **Quem usa:** o dono deste computador, não o autor do curso. Quando o texto acima diz que "o Ayrton aprovou/reprovou/pediu", isso é o histórico do estilo e continua valendo como regra. Quando fala em pastas, perfil, assinatura ou arquivos "dele", use o que está aqui.
- **Pasta de projetos:** `{proj}` (crie uma subpasta por vídeo; nunca trabalhe solto na raiz).
- **Pasta dos vídeos prontos:** `{res}`.
- **Efeitos sonoros (SFX):** {sfx if (nome in SFX_SKILLS or c["pasta_sfx"]) else "os que a própria skill indicar (dela mesma ou sintetizados em código)"}.
- **Assinatura no final:** {sig} Nunca use `@ayrtonsena.stg` (é do autor do curso).
- **Ferramentas já instaladas pelo kit:** Python com faster-whisper, librosa, soundfile, scipy, pillow, playwright (+ Chromium), opencv e psutil; FFmpeg; Node.js e HyperFrames (com o navegador de render).
- **Windows:** use `python` (não `python3`) e `python -m pip`. O faster-whisper roda em `device="cpu"`, `compute_type="int8"`.
- **Processos longos (render, transcrição):** no Claude Code rode em segundo plano (Bash com `run_in_background`), mandando a saída para um `.log` na pasta do projeto, em vez de `setsid nohup`. Não fique consultando o log em loop: espere o aviso de término.
- **Nunca** apague nem sobrescreva arquivos fora da pasta do projeto atual. Antes de sobrescrever um vídeo pronto, salve a versão anterior com outro nome.
"""
    if nome == "motionia-tuedoido":
        s += f"""
### Rodando esta skill no Claude Code (Windows)

Esta skill foi escrita para o chat do Claude.ai. No Claude Code troque:

| No texto da skill | Neste computador |
|---|---|
| `/mnt/user-data/uploads` (anexos) | os arquivos que o usuário arrastou ou indicou na conversa; copie-os para `{proj}\\<projeto>\\entrada\\` |
| `/home/claude/<projeto>/` | `{proj}\\<projeto>\\` |
| `pip install ... --break-system-packages` | não precisa (o kit já instalou); se faltar algo, `python -m pip install <pacote>` |
| `python3` | `python` |
| `setsid nohup python3 $S/render.py ... &` | Bash com `run_in_background: true`: `python "$S/render.py" "$P/index.html" "$P/video_mudo.mp4" > "$P/render.log" 2>&1` |
| `sleep 290; tail -1 render.log` | espere o aviso de término do processo em segundo plano |
| `/mnt/user-data/outputs/<nome>.mp4` | `{res}\\<nome>.mp4` |
| abrir imagem com `view` | ferramenta Read (lê a imagem) |
| `present_files` | diga o caminho completo do arquivo final |

Os scripts desta pasta já foram ajustados pelo kit para Windows (pasta temporária e endereço `file://`).
"""
    if nome in ("motionia-ayrtonsena-ifood-delivery", "motion-ia-ayrton-nubank-app-style", "motionia-ayrtonsena-comercial-3d-blender"):
        s += f"""
### Equivalência de efeitos sonoros

A skill cita arquivos da pasta pessoal do autor, que não existem aqui. Use os equivalentes do pacote do kit em {sfx}:

{TABELA_SFX}
"""
    if nome in ("motion-ia-ayrton-nubank-app-style", "motionia-ayrtonsena-comercial-3d-blender"):
        s += f"""
### Prévia no navegador do Claude

A prévia usa o `.claude\\launch.json` da pasta onde o Claude Code foi aberto. Abra o Claude Code na pasta de projetos (`{proj}`); o kit já criou esse arquivo lá.
"""
    if nome == "motionia-ayrtonsena-comercial-3d-blender":
        s += """
### Blender

Precisa do Blender 4.2 ou mais novo. Rode `python <skill>/scripts/verificar.py` antes de começar: ele diz o que falta sem instalar nada. Peças, mapas de condensação e logo do projeto original do autor não existem aqui; use os de `assets/exemplo-danese/` como referência e gere os do projeto novo.
"""
    return s


# ---------------------------------------------------------------- main
def aplicar(arq, pares):
    txt = arq.read_text(encoding="utf-8")
    for velho, novo in pares:
        if isinstance(velho, re.Pattern):
            txt2 = velho.sub(novo, txt)
        else:
            txt2 = txt.replace(velho, novo)
        if txt2 == txt:
            print(f"  AVISO: trecho não encontrado em {arq.relative_to(OUT)}: {str(velho)[:70]}")
        txt = txt2
    arq.write_text(txt, encoding="utf-8")


def main():
    c = carregar_config()
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ORIG, OUT, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for nome in SFX_SKILLS:
        shutil.copytree(KIT / "sfx", OUT / nome / "assets" / "sfx-kit")
    for rel, pares in trocas(c).items():
        aplicar(OUT / rel, pares)
    n = 0
    for py in OUT.rglob("*.py"):
        t = py.read_text(encoding="utf-8")
        # a tuedoido foi escrita pro chat (Linux): lê/grava texto sem encoding -> força UTF-8
        t2 = windows_py(t, utf8=("motionia-tuedoido" in py.parts and "open(" in t and "encoding=" not in t))
        if t2 != t:
            py.write_text(t2, encoding="utf-8"); n += 1
    for sk in sorted(p for p in OUT.iterdir() if (p / "SKILL.md").exists()):
        f = sk / "SKILL.md"
        f.write_text(f.read_text(encoding="utf-8").rstrip() + "\n" + secao_kit(sk.name, c), encoding="utf-8")
        ajustes = KIT / "aprendizados" / sk.name
        if ajustes.is_dir():
            shutil.copytree(ajustes, sk, dirs_exist_ok=True)
        print(f"ok {sk.name}")
    # impressão digital de cada arquivo: o trazer_aprendizados.py usa pra saber o que a skill aprendeu depois de instalada
    for sk in sorted(p for p in OUT.iterdir() if (p / "SKILL.md").exists()):
        man = {f.relative_to(sk).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
               for f in sorted(sk.rglob("*")) if f.is_file() and f.name != ".kit-manifest.json"}
        (sk / ".kit-manifest.json").write_text(json.dumps(man, indent=0), encoding="utf-8")
    print(f"scripts ajustados para Windows: {n}")
    print(f"pronto: {OUT}")


if __name__ == "__main__":
    main()
