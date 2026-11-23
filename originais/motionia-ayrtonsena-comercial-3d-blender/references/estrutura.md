# Estrutura (o arco aprovado)

O comercial Dane-se foi aprovado com "tá ótimo!! parece até a versão final". A estrutura dele é o ponto de partida de todo projeto: o `linha_do_tempo.py` recalcula as batidas pro número de sabores e acha onde encaixar a pausa da música. Mude o arco só se a pessoa pedir algo que ele não tem.

## O arco, cena a cena

| # | Plano | O que acontece | Por que funciona |
|---|---|---|---|
| 1 | `queda` | Fundo escuro com contraluz na cor do sabor 1. A câmera está lá em cima, centralizada, e cai junto com uma gota até um close forte da tampa, a gota quase encostando. Na batida, desce rápido e para encarando o foco do rótulo (olho, logo). Sem texto. | Gancho de movimento nos 2 primeiros segundos. |
| 2 | `detalhes` | 4 closes de meia batida em corte seco: tampa com gotas, logo, lateral, pescoço. | Mostra qualidade (o realismo vende) num ritmo que prende. |
| 3 | `revela` | A lata sobe de baixo já girando, com um leve overshoot, e para inclinada. | "Aparecer e já virar e explodir". |
| 4 | `giros` | No mesmo lugar, giro rápido; no borrão troca o rótulo, o fundo vira a cor do sabor, a palavra gigante entra atrás e as peças explodem e flutuam em câmera lenta. Uma troca por sabor, acelerando (2, 2, 1,5 batida...). Sem zoom. | Mostra todos os sabores sem repetir. |
| 5 | `helice` | As latas abrem em cata-vento, separadas, com fundo fixo e giro liso. | O "truque" das referências caras. |
| 6 | `helice` | Rastro: cópias nítidas repetem o giro com atraso e abrem o leque. | — |
| 7 | `helice` | A câmera mergulha; o furo do meio abre como íris. | Prepara a virada. |
| 8 | `helice` | Atravessa o furo, a cor vira escuro, e a música cai na pausa logo depois. | O momento grande na mudança da música. |
| 9 | `helice` | Corredor de anéis neon em contorno de lata, alternando as cores dos sabores. A volta forte da música entra aqui. | — |
| 10 | `helice` | Sai na fileira de latas em silhueta, chão espelhado, contraluz larga atrás. | — |
| 11 | `helice` | Uma lata acende por batida (spot suave). A câmera desliza de lado e freia centralizada na última. | Fecha mostrando a linha toda. |
| 12 | canvas | Fundo preto. Logo desenhado em stroke, preenche de baixo pra cima; linha do produto e "COMERCIAL NÃO OFICIAL" (legível, ≥2 s). | — |
| 13 | canvas | Só a assinatura (@), uns 4 s, e fecha no preto. | — |

Os planos 5 a 11 são **uma câmera contínua, sem corte**. É o plano mais pesado de renderizar.

## Como as batidas são calculadas (linha_do_tempo.py)
- Abertura fixa: queda 1–7 (olho na 5), detalhes 7–9, revela 9.
- Trocas a partir da batida 10, uma por sabor, com passos de 2, 2 e depois 1,5. A sequência começa no sabor 1 (que sobe na revelação), passa pelos outros e termina de volta no 1.
- O cata-vento entra numa **batida inteira**, logo depois da última troca. O furo vem 8 batidas depois, o corredor ocupa 2,3 batidas, a fileira acende a partir de +5 (uma lata por batida, no mínimo 3 latas) e o logo entra 2 batidas depois da última lata.
- Duração: 4 sabores = 44 batidas (~25 s a 103 BPM). Cada sabor a mais ou a menos muda ~1,5 a 2 batidas.

## Encaixe na música
O `batidas.py` acha o BPM, as batidas e as **pausas** da música (onde a energia cai e volta forte). O `linha_do_tempo.py` escolhe um corte na trilha pra que a câmera atravesse o furo bem antes da pausa e o corredor pegue a volta forte, exatamente como no aprovado (no Dane-se, `corte = [25, 45]`). Se não houver pausa depois do trecho escolhido, ele avisa: escolha outro `inicio` ou siga sem corte.

**Trecho:** o `batidas.py` sugere o trecho mais forte com o tamanho do vídeo (`trecho_sugerido`). Confirme com a pessoa. Ela pode querer começar num ponto específico (o drop, o refrão).

## Quando adaptar
- **1 sabor:** a revelação mostra a lata e um giro com explosão; o cata-vento e a fileira repetem a mesma lata. Avise que fica menos variado.
- **Sem peças:** o sabor troca no giro sem explosão. Funciona, mas perde impacto. Sugira ao menos gotas ou gelo.
- **Mais de 6 sabores:** o vídeo passa de 30 s. Sugira mostrar 4–5 nas trocas e todos só na fileira (editando `trocas` no `projeto.json`).
- **Vertical (9:16):** o motor é 16:9. Um 9:16 bom pede reenquadrar as câmeras (planos `queda`, `giros` e principalmente a fileira lateral). Isso é trabalho extra em `comercial.py`: avise antes.
- **Edição porca:** se a pessoa cortar o rascunho do jeito dela, descubra os pulos casando cada trecho do vídeo dela com o rascunho (quadro a quadro, em cinza) e o áudio dela com a música. Ajuste `linha_do_tempo` e `musica.corte` no `projeto.json` pra bater com ela.

Pra editar à mão, mude `linha_do_tempo` no `projeto.json` (todas as cenas leem de lá) e rode `python linha_do_tempo.py --mostrar` pra conferir a tabela. Só use `--refazer` se quiser voltar ao padrão.
