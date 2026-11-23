"""Render no PC do Ayrton sem travar tudo: 4 workers, processo (e filhos Chrome/ffmpeg) em prioridade
abaixo do normal, depois normaliza o áudio pra -14 LUFS / pico -1,5 dBTP sem recodificar o vídeo.

Uso (na pasta do projeto): python render_leve.py "D:\\...\\Motions\\Nome do video.mp4"
Só rode depois que ele aprovar a prévia completa.
"""
import json, os, re, subprocess, sys

saida = sys.argv[1]
cmd = f'npx hyperframes render --workers 4 --quality looks -o "{saida}"'
if os.name == "nt":  # filhos herdam a prioridade BelowNormal
    subprocess.run(f'start "" /belownormal /b /wait cmd /c "{cmd}"', shell=True, check=True)
else:
    subprocess.run("nice -n 10 " + cmd, shell=True, check=True)

def medir(arq):
    r = subprocess.run(["ffmpeg", "-i", arq, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))

m = medir(saida)
tmp = saida + ".tmp.mp4"
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", saida, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "256k",
                "-ar", "48000", "-movflags", "+faststart", tmp], check=True)
os.replace(tmp, saida)
r = subprocess.run(["ffmpeg", "-i", saida, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
resumo = r.stderr[r.stderr.rfind("Summary"):]
print("pronto:", saida); print("\n".join(l for l in resumo.splitlines() if "I:" in l or "Peak:" in l))
