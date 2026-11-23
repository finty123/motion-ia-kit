"""Transcreve as aulas com áudio e retoma pares TXT/JSON já concluídos.

Uso: python estudo/transcrever_aulas.py "pasta dos MP4" "pasta das transcrições"
O primeiro uso do modelo small precisa de internet se ele não estiver no cache.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def pronto(txt, dados):
    if not txt.is_file() or not dados.is_file() or not txt.stat().st_size:
        return False
    try:
        partes = json.loads(dados.read_text(encoding="utf-8"))
        return bool(partes) and all(
            isinstance(p, dict) and {"s", "e", "t"} <= p.keys() for p in partes
        )
    except (ValueError, OSError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("videos", type=Path)
    parser.add_argument("saida", type=Path)
    parser.add_argument("--modelo", default="small")
    args = parser.parse_args()
    videos = sorted(args.videos.rglob("*.mp4"))
    if not videos:
        parser.error("A pasta selecionada não contém aulas MP4.")
    if len({p.stem.casefold() for p in videos}) != len(videos):
        parser.error("Há vídeos com nomes repetidos. Selecione apenas a pasta das aulas.")
    args.saida.mkdir(parents=True, exist_ok=True)
    modelo = None
    falhas = []
    for video in videos:
        txt = args.saida / (video.stem + ".txt")
        dados = args.saida / (video.stem + ".json")
        if pronto(txt, dados):
            print("Já transcrita:", video.name)
            continue
        try:
            faixa = subprocess.check_output([
                "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                "stream=index", "-of", "csv=p=0", str(video),
            ]).strip()
            if not faixa:
                print("Sem faixa de áudio:", video.name)
                continue
            import numpy as np
            from faster_whisper import WhisperModel
            if modelo is None:
                modelo = WhisperModel(args.modelo, device="cpu", compute_type="int8")
            pcm = subprocess.check_output([
                "ffmpeg", "-nostdin", "-v", "error", "-i", str(video), "-map", "0:a:0",
                "-ac", "1", "-ar", "16000", "-f", "f32le", "pipe:1",
            ])
            segmentos, _ = modelo.transcribe(np.frombuffer(pcm, dtype="<f4"), language="pt",
                                             beam_size=2, vad_filter=True)
            partes = [{"s": round(s.start, 2), "e": round(s.end, 2), "t": s.text.strip()}
                      for s in segmentos if s.text.strip()]
            if not partes:
                print("Áudio sem fala detectada:", video.name)
                continue
            linhas = []
            for parte in partes:
                minuto, segundo = divmod(int(parte["s"]), 60)
                linhas.append(f"[{minuto:02}:{segundo:02}] {parte['t']}")
            for arquivo, conteudo in ((txt, "\n".join(linhas) + "\n"),
                                      (dados, json.dumps(partes, ensure_ascii=False))):
                temporario = arquivo.with_suffix(arquivo.suffix + ".tmp")
                temporario.write_text(conteudo, encoding="utf-8")
                temporario.replace(arquivo)
            print("Concluída:", video.name, flush=True)
        except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
            falhas.append(video.name)
            print(f"Falhou {video.name}: {exc}", file=sys.stderr)
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
