# Áudio: narração, efeitos, música, mix

## Narração
- `transcrever.py` gera o tempo por palavra. Confira os nomes que o Whisper erra e corrija com `--fix "errado=certo"`. Se precisar mais precisão, use `--modelo medium`, que é mais lento.
- `cortar_respiros.py` corta os silêncios e deixa `--gap 0.15` s entre frases. Com `--keep "IDX:SEG"` você define pausas intencionais depois da palavra IDX: preço, CTA, buraco negro, nome do produto. O script imprime a nova lista índice:palavra@tempo; use ESSES índices no scenes.js.

## Música
- `musica.py analisar` mostra BPM, energia por segundo e os pontos onde a energia SOBE ou CAI.
- **Alvos de alinhamento:**
  - a primeira SUBIDA forte cai na palavra de maior impacto da primeira metade (nome do produto);
  - uma QUEDA cai no preço antigo, o que faz o silêncio valorizar o número;
  - uma nova subida perto do CTA.
- `musica.py editar --offset X` pula o começo da música. `--cortar A:B` (tempo original) remove trechos em múltiplos de 4 batidas. Gera `musica-editada.wav` e `beats.json` já no tempo do vídeo.
- Exemplo real: offset 0,96 s e corte de 2 compassos (6,2 s). A batida entrou no "Claude" e a música caiu no "R$297".

## Efeitos (nomes aceitos em `cue(t, nome, volume, {...})`)
| Nome | Quando usar |
|---|---|
| `whoosh`, `whoosh_small`, `whoosh_fast`, `whoosh_long`, `whoosh_soft`, `whoosh_up`, `whoosh_fall`, `rev_whoosh` | trocas de cena, entradas, saídas, sobe/cai |
| `tick`, `key`, `click`, `click_heavy` | palavras de apoio, digitação, interface, troca de fonte, contagem |
| `hit_small`, `hit_med`, `hit_big`, `hit_dry`, `hit_dry_low`, `hit_soft`, `thump`, `subhit` | impactos de palavra (`hit_dry_low` no preço antigo) |
| `impact`, `impact_huge`, `boom` | palavra-chave forte, números, preço novo |
| `braam` | revelação principal (nome do produto) |
| `explosion` | explosões |
| `slash` | lâmina, risco, X |
| `glitch`, `tapestop` | congelar, erro, "pera aí" |
| `riser_short`, `riser_long`, `suck`, `dive` | antecipação (`suck`/`riser` TERMINAM no impacto: comece ~1,3 s antes), mergulho |
| `drone`, `hum` | espaço, vídeo ruim |
| `shimmer` | reflexo de luz, logo |
| `notif` | notificação (grave, nunca "plim") |
| `blackhole` | buraco negro (use junto com `cue(t,'muffle',duração)`) |
| `muffle` | não é som: abafa tudo (embaixo d'água) por `v` segundos |
| `blurcue` | não é som: só blur de tela (`bl`) |

Volumes típicos: 0,3 a 0,45 para ticks e teclas, 0,5 a 0,7 para whoosh e hits, 0,8 a 1,0 para impactos principais. MUITOS efeitos: toda troca de cena tem whoosh e toda palavra-chave tem hit/impact. Nada infantil.

## Mix (`mix.py`)
- Narração na frente. A música fica ~13 dB abaixo (`--music-db`) e os efeitos ~9 dB abaixo (`--sfx-db`), com ducking automático (música −11 dB, efeitos −5 dB sob a voz).
- `--music-lift FIM_DA_FALA:FIM_DA_FALA+2`: a música sobe +5 dB quando a voz acaba (CTA e logo).
- O master sai em −14 LUFS com limitador a −1 dB. Fade da música no último 1,5 s.
