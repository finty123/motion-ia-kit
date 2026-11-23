# Áudio

## Padrão aprovado (Training Season, 21/10/2026)
**Só a música + um close-up no buraco negro do final.** Os tremores, flashes e blur das cues continuam no visual, mas sem som. O `mix_musica.py` ignora os SFX sintetizados das cues, a menos que se passe `--com-sfx`.

```bash
python S/mix_musica.py --music P/musica-editada.wav --end 31.0 --vacuo 26.2:27.42 --closeup S/assets/sfx/closeup.wav --out P/mix.wav
```

- `--vacuo INI:FIM`: a música é **sugada**, nunca desacelerada. É feita de reverb invertido crescendo, estéreo fechando no centro, faixa de frequência estreitando (grave e agudo somem) e volume subindo até um corte seco em FIM. O Ayrton reprovou a versão que desacelerava ("não pode ser como se estivesse parando a música").
- `--closeup arquivo.wav`: o pico (0,347 s dentro do `closeup.wav`) cai exatamente em FIM. Ajuste com `--closeup-peak` se trocar o arquivo.
- Sem `--vacuo`, o close-up cai 1 s antes do fim.
- Master em −14 LUFS e pico em −1 dBTP.

## Quando ele pedir efeitos sonoros
`--com-sfx --sfx-db -6` mistura os SFX das cues (nomes em `api-do-motor.md`). Só cinematográficos: hit, boom, whoosh, clique, glitch, close-up. Nada infantil (blip, pop, bip, laser, sininho). Samples dele: `D:\Backup\Videos\#clientes\SFX-20261024T181631Z-1-001\SFX` e `assets/sfx/` (closeup, sub, subwhoosh).

## Trecho da música
`musica.py editar musica.m4a P --offset INI --ate FIM` recorta o trecho (tempo original) e gera `beats.json` já no tempo do vídeo. `--cortar A:B` remove compassos do meio (múltiplos de 4 batidas).

## Duração do vídeo
`END` = fim do vácuo + 0,45 s (entrada da assinatura) + ~3 s de assinatura parada. No Training Season: música até 27,5 s, vácuo fechando em 27,42 s e END = 31 s.
