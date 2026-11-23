# Exemplo aprovado: Training Season (Dua Lipa), 16:9, 31 s — v3 de 21/10/2026

Trecho de 27,5 s (123 BPM) + vácuo + assinatura. Música original do Ayrton: `Downloads\videoplayback.m4a`.
Vídeo final: `D:\Backup\Videos\#clientes\Ayrton Sena\Motions\Training Season - motion 16x9 v3.mp4`.

- `scenes.js`: as 10 cenas (A abertura carregando + I subindo, B branco sugado pelo buraco vermelho, C HOLD/ME/CLOSE + espelho infinito DEEPER, D RODEO, E TAKE CONTROL, F VULNERABLE em vidro, G CONVERSATION OVERLOAD, H TRAINING SEASON'S + 3-2-1, I OVER + vácuo, J assinatura).
- `words.json`: marcadores das palavras-chave com os tempos corrigidos pela batida (HOLD 9,47 = volta do bumbo).
- `beats.json`: batidas do trecho.

Montar de novo:
```bash
S=<pasta da skill>; E=$S/examples/training-season
python $S/scripts/build.py --scenes $E/scenes.js --words $E/words.json --beats $E/beats.json --out proj/index.html --paleta "principal=#7A0820,destaque=#FFFFFF"
python $S/scripts/mix_musica.py --music musica.wav --end 31.0 --vacuo 26.2:27.42 --closeup $S/assets/sfx/closeup.wav --out proj/mix.wav
python $S/scripts/hf_wrap.py proj/index.html proj/hf --audio proj/mix.wav
```

Mapa (tempo → cena):
| Tempo | Ouve-se | Cena |
|---|---|---|
| 0–1,95 | "You should know" | LOADING + uma palavra por vez em tela cheia |
| 1,95–5,46 | "I" esticado | I subindo contínuo, câmera colada no topo, mergulho até a tela ficar branca |
| 5,46–9,40 | respiro da música | branco escurecendo, sugado pelo buraco negro vermelho |
| 9,47 | volta do bumbo | HOLD gigante (estouro de linhas, anéis, flash) → HOLD ME CLOSE com arcos de abraço |
| 11,2 | "deeper" | espelho infinito contínuo |
| 13,21 / 14,19 | batida forte / "rodeo" | fundo vermelho, letras pulando nas batidas, laço girando |
| 16,22 | "take control" | fundo branco, mira REC travando |
| 17,3–21,2 | groove | WHEN I'M → VULNERABLE treme → estilhaça em vidro → volta vermelho |
| 21,29 | "conversation overload" | balões de chat se multiplicando + carimbo |
| 23,22 | "training season's" | fundo branco → contagem 3-2-1 no cronômetro (bumbo some) |
| 25,19 | volta do bumbo | OVER, maior impacto |
| 26,2–27,42 | fim | buraco negro suga OVER e a música (close-up) |
| 27,87–31 | silêncio | by @ayrtonsena.stg parado com glow |
