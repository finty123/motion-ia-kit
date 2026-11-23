# Áudio: narração, música e SFX de UI

## Narração
Ele grava ou gera no ElevenLabs (voz "Ana Alice - Friendly & Clear" no Nubank). Copie pra `assets/narracao.mp3`. Começa no 0 do vídeo.

## Música
Da pasta dele: `D:\Backup\Music\mÚSICAS DE FUNDO\` (subpastas Animado, Inspiracional, LO-Fi\Calmo, LO-Fi\Animado, "chegando lá", "funny moment"). Se ele não mandar, escolha pelo clima e meça BPM e onde a batida entra (librosa). No Nubank: "Motion" (Danijel Zambo, pasta "chegando lá", 104 BPM), batida em 9,98 s da faixa → `--musica-offset 3.88` pra cair no "Agora" (6,1 s). Copie pra `assets/musica.mp3`.

## SFX (só desta pasta, e bastante)
`D:\Backup\Videos\Edição de video\SFX\Ui`

| Ação na tela | Arquivo |
|---|---|
| Notificação aparecendo | `Pop-up (1..5).wav`, `Pop up 2.wav` |
| Digitando | `Type iphone.mp3` (é baixo: ganho −2) |
| Item de lista ativando | `Click  (1..4).wav` (dois espaços no nome) + `Interface2.wav` cortado em 1 s |
| Toggle / botão | `Ui click.wav`, `Select.wav`, `Click digital.mp3` |
| Passagem / pan / mergulho | `UI - Digital Whoosh.wav` |
| Abertura de cena / painel | `Ui open.wav`, `UI open(1).wav`, `Modern Interface Activate.mp3` |
| Moeda / brilho / logo | `Little Shine 05.wav`, `Magic Shine.wav`, `Pure Gold Shining.wav` |
| Confirmação (caixinha fechou, escudo) | `Correct  (1..3).wav`, `Ui confirm.wav` |
| Contador | `Counting.wav` (corte no tempo do odômetro) |
| Câmera seguindo algo | `Spacey zing.wav` (corte em 1,6 s) |
| Camada de "tecnologia" | `Hologram 1/2.mp3` (baixo, cortado) |

Lista completa do Nubank (57 efeitos com tempos e ganhos) em `assets/modelo/cues.json`.

## Mix
```
python scripts/mix.py PROJETO --duracao 35.5 --musica-offset 3.88 --sobe-musica 30.5
```
Gera `assets/mix.wav`: narração 0 dB, música −17 dB com sidechain (abaixa ~55% sob a voz), sobe 6 dB depois da última fala, fade de 1,6 s no fim, −14 LUFS. No `index.html` entra um único `<audio id="mix">`. Mudou o tempo de alguma ação? Mexa no `cues.json` e rode de novo.
