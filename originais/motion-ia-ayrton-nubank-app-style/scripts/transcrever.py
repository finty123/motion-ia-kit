"""Transcreve a narração com tempo por palavra (faster-whisper, CPU) e grava words.json.
Uso: python transcrever.py narracao.mp3 PROJETO/words.json [--prompt "Nubank, Pix, caixinha"]
Imprime índice:palavra@tempo pra montar o mapa de cenas. Confira nomes próprios: o Whisper erra marca.
Obs.: no Windows passe o áudio como array (soundfile) e device=cpu; o decode do PyAV e o CUDA falham aqui."""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("saida"); ap.add_argument("--prompt", default=""); ap.add_argument("--modelo", default="small")
    a = ap.parse_args()
    import soundfile as sf
    from faster_whisper import WhisperModel
    tmp = Path(tempfile.gettempdir()) / "narr16.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.audio, "-ac", "1", "-ar", "16000", str(tmp)], check=True)
    audio, _ = sf.read(tmp, dtype="float32")
    model = WhisperModel(a.modelo, device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio, language="pt", word_timestamps=True, initial_prompt=a.prompt or None)
    words = []
    for s in segs:
        print(f"{s.start:6.2f} {s.end:6.2f} {s.text}")
        for w in s.words:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
    Path(a.saida).write_text(json.dumps(words, ensure_ascii=False, indent=0), encoding="utf-8")
    print(" ".join(f"{i}:{x['w']}@{x['s']}" for i, x in enumerate(words)))


if __name__ == "__main__":
    sys.exit(main())
