# Estrutura aprovada — comercial Dane-se (v3, 31/10/2026)

103,36 BPM, 30 fps, **44 batidas ≈ 25,6 s**. Uma batida = QB = 60/BPM·30 ≈ 17,4 quadros. Quadro da batida b: F(b) = (b−1)·QB.
Essa versão nasceu da edição porca dele por cima da v2 (23 s). Ele aprovou o rascunho dizendo "tá ótimo!! parece até a versão final".

| Batidas | Plano (Blender) | O que acontece | Som |
|---|---|---|---|
| 1–7 | `queda` | Fundo escuro, contraluz rosa. Câmera de cima: uma gota (refração real) cai na tampa e a câmera despenca junto, freando a milímetros. Depois desce colada no pescoço e para de frente pro **olho** do rótulo na batida 5–7, como se encarasse quem assiste. Sem texto. | whoosh grave na queda (1,25); whoosh no mergulho (5) |
| 7–9 | `detalhes` | **4 closes de meia batida em corte seco** (tampa com gotas, lacre, lateral, fundo). Renderizados com 1 batida cada; o `compor.py` usa só meia. | clique de câmera em 7 / 7,5 / 8 / 8,5 |
| 9–10 | `revela` | A lata **sobe de baixo** (ease-out com leve overshoot) já girando 1 volta e para na posição fixa. Ele pediu: "tem que aparecer e depois já virar e explodir". | whoosh (9,3) |
| 10 / 12 / 14 / 15,5 | `giros` | Na mesma posição, giro rápido; no borrão troca o sabor (limão → manga → água → melancia), troca o fundo e a **palavra gigante atrás** (CORAGEM, ATITUDE, REAL, DANE-SE) e as frutas **explodem** e flutuam em câmera lenta. As trocas aceleram (2, 2, 1,5 batida). Sem zoom. | whoosh + boom em cada troca |
| 17 | `helice` | As 4 latas abrem em **cruz/cata-vento**, tampas no centro. **Fundo rosa fixo** e giro liso e contínuo: nada de parar ou trocar de cor a cada batida. | whoosh grave + boom |
| 18–23 | `helice` | Rastro: 6 cópias nítidas de cada lata repetem o giro com atraso e abrem um leque (cata-vento cheio). | whooshes 19, 21 |
| 23–25 | `helice` | Câmera mergulha pro centro; o furo do meio abre como uma íris (o raio das cópias cresce) e dá pra ver o corredor lá dentro. | whoosh invertido terminando em 25 |
| 25–26 | `helice` | Atravessa o furo, o rosa vira escuro. Cai na **pausa da música** (corte na trilha). | — |
| 26–27,3 | `helice` | **Corredor de anéis neon** em contorno de lata, alternando as cores dos sabores. A volta forte da música entra em 27. | woosh8 (26,8) |
| 27,3–29,5 | `helice` | Sai do corredor: **fileira de latas em silhueta** num chão espelhado escuro, contraluz larga atrás. Leve pan (0,35 rad) pra lata nunca andar pra trás na tela. | — |
| 30–33 | `helice` | Uma lata **acende por batida** (spot suave, sem piscar). A câmera desliza de lado, constante, e **freia centralizada na última lata**, nunca em espaço vazio. | estalo de lâmpada + soco em cada uma |
| 35–39 | canvas | Fundo preto. **Logo desenhado com stroke** (trim path por letra, brilho rosa), depois preenche de baixo pra cima, e o traço some. "ENERGY DRINK · ZERO AÇÚCAR" e "COMERCIAL NÃO OFICIAL" (legível, ≥2 s). | boom (35) + lâmina (35,1) |
| 39,5–43,6 | canvas | Só **@AYRTONSENA.STG**, bem mais tempo; fecha no preto. | whoosh (39,5) |

**Música:** `CORTE_MUSICA = (25, 45)`. As batidas 1–24 do vídeo são as batidas 1–24 do trecho; da 25 em diante, pula pra 45 da trilha. Assim a pausa da música (45–46) cai no furo e a volta forte cai no corredor. Emenda com crossfade de 12 ms.

**Para outra marca:** mantenha o arco (gancho de macro → closes secos → lata entra e troca sabores → cata-vento → mergulho → corredor → fileira acendendo → logo em stroke → @). Ajuste o número de sabores, as palavras (reais da marca) e os tempos à música nova, sempre caindo na batida. Os momentos grandes vão nas mudanças da música: a pausa e a volta forte.

O prompt original da v1 (estrutura de 64 batidas a 120 BPM, direção e construção) está em `prompt-original-danese.md`. Ele mostra a intenção, mas a v3 acima é o que foi aprovado.
