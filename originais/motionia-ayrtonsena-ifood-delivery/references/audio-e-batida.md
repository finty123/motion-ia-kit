# Áudio e batida

## Batida (o que ele mais sentiu falta)
1. Marque a trilha: `<audio id="musica" data-timeline-role="music" …>`.
2. `npx hyperframes beats --json` → `beats/<trilha>.json` (BPM e cada batida com força).
3. Decida o momento-chave da marca (ex.: o logo acendendo no celular aos 8,15 s) e rode
   `python scripts/batida.py beats/<trilha>.json --momento 8.15` → dá o `data-media-start` que faz a entrada forte cair ali, mais a lista de batidas no tempo do vídeo.
4. A música começa no 0 do vídeo (a parte calma da trilha fica por baixo da abertura).
5. Posicione nas batidas (ou meias batidas): trocas de cor, cortes, palavras que estalam, cliques do cursor, pousos, logo, @. As falas também podem andar: mova o INÍCIO de cada take (nunca corte palavra) pra palavra-chave cair na batida (`scripts/remontar_narracao.py`). Uma fala com pausas pode ser dividida nas pausas.
6. Anote as batidas no comentário do topo de cada cena (`// batidas: 16,28 · 16,84 · 18,46`).

## Voz
- Voz > efeitos > música.
- Áudio de WhatsApp vem abafado: `python scripts/voz_clara.py narracao.wav narracao-clara.wav` (meta: presença 2–6 kHz uns 6–9 dB abaixo dos médios).
- Se tiver vários takes, use o que ele indicar e não troque take.

## Música
`data-automation` de volume: 0,12–0,16 debaixo da fala, 0,25–0,35 sem fala, 0,35 no final e fade nos últimos ~0,6 s. Sem riser.

## Efeitos (pasta do Ayrton)
`D:\Backup\Videos\#clientes\SFX-20261024T181631Z-1-001\SFX` (os nomes têm 2 espaços: `Click  (1).wav`).
| Uso | Arquivos |
| --- | --- |
| clique / toque / palavra que estala | Ui\Click  (1)…(5).wav, Ui\Click digital.mp3, Ui\Ui click.wav, Computer\Click Button.mp3 |
| card / pílula / tag / pop | Ui\Pop up.wav, Ui\Pop up 2.wav, Ui\Pop-up (1)…(5).wav, Ui\Correct  (2).wav |
| interface / chip ativa / rolagem | Ui\Interface.wav, Ui\Interface2.wav, Ui\Modern Interface Activate.mp3 |
| troca de cena / passada | Wooshes\Fast Swoosh 3.wav, Fast Swoosh 7.wav, Whoosh 03.wav, Woosh Standard.mp3 |
| notificação / sucesso | Diversos\Iphone.mp3, Diversos\Success Notification .wav (+ o som oficial da marca, se tiver) |
| impacto (só gancho e logo) | Hits - impacts\Sub Boom.mp3, Boom 3.mp3, Trailer Boom.mp3 |
| ronco de barriga | o tummy song que ele mandou (Downloads\kuzu420-tummy-song-465787.mp3), trechos 17,2 / 2,57 / 7,72 / 12,0 s |
Proibido: pasta SFX Memes, som de desenho animado, "Deep Growl" como ronco, riser.

Muito som de UI: todo toque, card, chip, palavra e pouso tem som, alternando 2–3 arquivos (nunca o mesmo em sequência). Gere as tags com `scripts/efeitos.py deixas.json`: ele mede o golpe de cada arquivo e põe o som 1 quadro depois da imagem.

## Fechamento
`python scripts/render_leve.py "<saída>.mp4"` → −14 LUFS, pico ≤ −1 dBTP. Diga que foi medido, não ouvido.
