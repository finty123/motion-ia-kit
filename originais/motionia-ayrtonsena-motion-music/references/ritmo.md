# Ritmo: ler a música e casar com a imagem

## O que o raio-x entrega (`analisar_musica.py`)
- `bpm`, `batida_s`, `beats`: a grade de batidas (librosa). Às vezes sai em dobro ou na metade (152 ou 76): conte no ouvido pela partitura.
- `batidas_fortes`: onde o grave salta. `principal: true` (força ≥ 5) = volta do bumbo, drop, impacto. É onde vai o **maior impacto da cena**.
- `respiros`: trechos de ≥ 0,8 s em que a música esvazia. Pedem tensão (vórtice, buraco negro, câmera girando), nunca tela parada.
- `ataques_voz`: ataques da banda da voz (o harmônico). Cada palavra do Whisper é presa no ataque mais próximo (±0,25 s), em ordem e sem duas palavras dividirem o mesmo ataque.
- `palavras[].segura` + `fim_voz`: nota segurada (a voz continua soando ≥ 1 s). No Training Season pegou o "I" de 1,97 a 5,51 s. É a candidata a letra repetida / objeto crescendo.
- `batidas_fortes[].maior`: a batida mais forte do trecho (13,15 s no Training Season).
- `partitura.png`: uma linha a cada 8 s, com cinza = energia, rosa = grave, linha vermelha grossa = batida principal ("MAIOR" na mais forte), azul = respiro, tracinho verde = ataque da voz, faixa amarela = sílaba segurada e a letra embaixo. As linhas claras a cada 4 batidas são contadas do início do trecho, não são o tempo 1 real do compasso.

## Regras de sincronia (o que funcionou e o que ele corrigiu)
1. **A palavra entra na sílaba cantada, não no bumbo.** Nos dois edits de referência a troca de imagem cai a 30–130 ms do ataque da voz. Comece a animação em `w(i) - 0.07`, porque a mola leva esse tempo pra "bater".
2. **O impacto principal vai na batida que se OUVE.** No Training Season o Whisper marcou o HOLD em 10,2 s, mas o bumbo voltava em 9,47 s. O Ayrton disse que estava atrasado até a palavra ir pro 9,47. Quando a palavra forte cai até ~0,8 s de uma batida principal, use a batida (a do HOLD estava a 0,69 s).
3. **Cena nova a cada frase cantada** (1,5–2 s, 3 a 4 batidas). O cenário inteiro troca no começo da frase; dentro dela, as palavras entram uma a uma.
4. **Sílaba esticada = letra repetida.** O "I" de 3 s virou um I subindo sem parar; "Foreverrrr" vira fila de "r"; "ooooh" vira círculo de "o". A câmera acompanha a ponta.
5. **Movimento contínuo.** Não faça o objeto crescer ou empurrar em degraus a cada batida (o Ayrton chamou de "paradinhas"). Velocidade constante e a batida entra como brilho, pulso de glow ou anel, sem frear o movimento.
6. **Respiro da música = tensão visual** que termina exatamente no próximo impacto (o buraco negro fechando e o HOLD explodindo).
7. **Quando o bumbo some antes do refrão/drop** (ex.: 23,8–25,1 s no Training Season), use contagem, cronômetro ou riser visual que termina na volta do bumbo.
8. **Nada parado por mais de ~0,5 s**: depois de entrar, a palavra gira devagar, desliza ou pulsa até a próxima.

## Como preencher o words.json do projeto
Só os marcadores que o `scenes.js` usa: `[[início, fim, "PALAVRA"], ...]`. Os tempos vêm de `analise.json > palavras[].t`, corrigidos pela regra 2. Exemplo aprovado: `examples/training-season/words.json`.

## Conferência antes do render
- Snap em cada batida principal e em cada palavra-chave (`snap.py`).
- Se a prévia do HyperFrames estiver aberta, toque o trecho e veja se o impacto "bate" com o grave.
