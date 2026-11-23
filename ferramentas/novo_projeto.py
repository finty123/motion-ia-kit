"""Cria um projeto independente para Codex e Claude Code."""
import argparse
import json
import shutil
import tempfile
from pathlib import Path

from adaptar import KIT, gerar


def criar(destino):
    destino = destino.expanduser().resolve()
    if destino.exists():
        raise ValueError("Escolha um nome de pasta que ainda não exista.")
    if destino.is_relative_to(KIT):
        raise ValueError("Escolha um local fora do kit para os arquivos do vídeo.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="motion-kit-", dir=destino.parent) as temp:
        projeto = Path(temp) / "projeto"
        projeto.mkdir()
        pastas = ["01-marca", "02-produto", "03-referencias", "04-producao", "05-exportacoes"]
        for nome in pastas:
            (projeto / nome).mkdir()
        for nome in ("AGENTS.md", "CLAUDE.md", "BRIEFING.md"):
            shutil.copyfile(KIT / "modelo-projeto" / nome, projeto / nome)
        local = projeto / ".agents" / "skills"
        gerar({"pasta_projetos": str(destino), "pasta_resultados": str(destino / pastas[-1]),
               "pasta_sfx": "", "assinatura": "", "sfx_txt": "`assets/sfx-kit/`"},
              local, incluir_aprendizados=False)
        shutil.copytree(local, projeto / ".claude" / "skills")
        (projeto / ".claude" / "launch.json").write_text(
            json.dumps({"version": "0.0.1", "configurations": []}, indent=2), encoding="utf-8")
        projeto.rename(destino)
    print(f"Projeto criado em {destino}. Abra essa pasta no seu assistente.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pasta", type=Path, help="Nova pasta fora do kit")
    try:
        criar(parser.parse_args().pasta)
    except (OSError, ValueError) as erro:
        parser.exit(1, f"Não foi possível criar o projeto: {erro}\n")
