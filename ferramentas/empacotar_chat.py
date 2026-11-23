"""Gera chat/<skill>.zip pra subir no Claude.ai (Configurações > Capacidades > Skills > Enviar skill).

Uso: python ferramentas/empacotar_chat.py
Cada zip tem a pasta da skill na raiz (<skill>/SKILL.md ...), com barras "/" — o formato que o Claude.ai aceita.
(O Compress-Archive do PowerShell 5 grava "\\" nos caminhos e o upload pode falhar; por isso é em Python.)
"""
import zipfile
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
SRC, OUT = KIT / "originais", KIT / "chat"

# skills que só fazem sentido no Claude Code (precisam de HyperFrames local ou Blender)
SO_CODE = {
    "motion-ia-ayrton-nubank-app-style": "precisa do HyperFrames rodando no PC (prévia e render)",
    "motionia-ayrtonsena-comercial-3d-blender": "precisa do Blender instalado no PC",
}


def main():
    OUT.mkdir(exist_ok=True)
    for sk in sorted(p for p in SRC.iterdir() if (p / "SKILL.md").exists()):
        z = OUT / f"{sk.name}.zip"
        with zipfile.ZipFile(z.with_suffix(".tmp"), "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(sk.rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts and f.name != ".kit-manifest.json":
                    caminho = f"{sk.name}/{f.relative_to(sk).as_posix()}"
                    if f == sk / "SKILL.md":
                        nota_chat = ("No chat, use os arquivos anexados e pergunte qual assinatura usar. "
                                     "Os caminhos locais e o perfil do autor são referências do curso. ")
                        if sk.name in SO_CODE:
                            nota_chat += "A produção deste estilo é feita no Claude Code."
                        if sk.name == "motionia-ayrtonsena-ifood-delivery":
                            nota_chat += "Entregue o pacote de pré-produção para continuar no Claude Code."
                        zf.writestr(caminho, f.read_text(encoding="utf-8").rstrip() + "\n\n## Uso no chat\n\n" + nota_chat + "\n")
                    else:
                        zf.write(f, caminho)
        z.with_suffix(".tmp").replace(z)
        nota = f"  (só Claude Code: {SO_CODE[sk.name]})" if sk.name in SO_CODE else ""
        print(f"ok {z.name}  {z.stat().st_size / 1e6:.1f} MB{nota}")


if __name__ == "__main__":
    main()
