# Guia da referência — "POV o iFood não me contratou" (After Effects, 21,5 s, 720×1280, 30 fps)

Fontes do estudo: 86 quadros a cada 0,25 s (`docs/ref-quadros/`, folhas em `docs/ref-folhas/`, folha N = 4 s a partir de (N−1)×4 s), tiras a 10–15 fps dos trechos-chave e os 9 prints de `ANEXOS/02-frames-da-referencia`.
A referência foi filmada do monitor: cor e nitidez reais são melhores do que aparecem. Medidas abaixo em % da tela do vídeo (vertical) e já convertidas pra 1920×1080.

## 1. Linha do tempo da referência

| Tempo | Cena | Duração |
|---|---|---|
| 0,0–1,2 | "Tá com fome?" letreiro vermelho à mão em fundo creme | 1,2 s |
| 1,2–3,6 | Vermelho; estrela facetada vermelho-escuro gira atrás; logo iFood se monta letra a letra com faíscas | 2,4 s |
| 3,6–5,0 | Splash sai pra esquerda (wipe 0,15 s) → lista branca; ícones entram em cascata | 1,4 s |
| 5,0–6,8 | Lista rola rápido pra cima com aberração cromática (RGB split) | 1,8 s |
| 6,8–8,0 | Tela vira celular inclinado na mão lilás; "NA PALMA DA SUA MÃO!" palavra por palavra | 1,2 s |
| 8,0–11,5 | Comidas: Pizza → Sushi → Hambúrguer → Salada, troca diagonal | ~0,85 s por comida |
| 11,5–12,7 | RAPIDINHO lilás esticado + motoboy | 1,2 s |
| 12,7–15,2 | Mapa visto de cima, moto, câmera seguindo, pin | 2,5 s |
| 15,2–16,7 | "Seu pedido foi entregue" + estrelas (NÃO usar) | — |
| 16,7–17,7 | "FOI TRANQUILO!" letreiro à mão no vermelho | 1,0 s |
| 17,7–21,5 | Logo se monta de novo e fica | 3,8 s |

Ritmo: nenhuma cena para mais de ~0,6 s sem algo mexendo. Média de 1,3 s por ideia. Nunca tem fade pro preto: toda troca é por movimento (wipe, whip, zoom, troca diagonal, morph).

## 2. Tipografia

| Uso | Família parecida (temos) | Peso | Caixa | Tamanho relativo | Em 1920×1080 |
|---|---|---|---|---|---|
| Nome da comida ("Pizza", "Ham/bur/guer") | Montserrat | 800 ExtraBold | Inicial maiúscula | cap ≈ 9% da altura, palavra ≈ 85% da largura da tela vertical | 230–280 px, entreletra −2%, entrelinha 0,82 |
| Bordão "NA PALMA DA SUA MÃO!" | Montserrat | 900 Black Itálico | MAIÚSCULA | ≈ 7% da altura | 150–180 px, entrelinha 0,9 |
| RAPIDINHO | League Gothic (condensada) | — | MAIÚSCULA | letra esticada vertical (scaleY 2,0–2,4) | 260 px × scaleY 2,2 |
| Preço na pílula "R$ 44,00" | Montserrat | 500 | — | ≈ 2,2% da altura | 46–52 px, cinza #6B6B6B |
| UI do app (nomes, tags) | Montserrat / Inter (o app usa Sul Sans; a mais parecida aqui é Montserrat) | 600–700 nome, 400 resto | — | — | sempre ≥ 26 px depois do zoom |

Sílabas: palavra longa quebra em sílabas empilhadas, alinhadas à esquerda ("Ham / bur / guer", "Sa / lada"). Palavra curta fica numa linha só.
Cor do texto grande: branco puro #FFFFFF no vermelho; lilás no fundo creme.

## 3. Cores medidas

- Vermelho de fundo: #EA1D2C (no monitor puxa pra #E8102A). Faceta atrás do logo: #C8101F a #B00E1C.
- Creme/branco de tela: #F7F4EC (fundo do RAPIDINHO e mapa); tela do app #FFFFFF.
- Lilás da mão e do RAPIDINHO: #B89BFF, contorno/linhas da mão #8E6CF0, sombra do RAPIDINHO #9C7FF0.
- Mapa: quarteirões #FBF6E6 (creme bem claro), ruas #E6E2EE (lilás acinzentado), sem bordas.
- Pílula de preço: branca #FFFFFF, sombra 0 8px 20px rgba(0,0,0,.18); botão do carrinho círculo #EA1D2C com carrinho branco.
- Selos (carrinho, %): "flor" branca recortada (círculo com borda ondulada) com ícone vermelho.

## 4. Como cada coisa entra e sai (velocidade e easing)

Regra geral da referência:
- Entrada: rápida e com mola. 6–9 quadros (0,2–0,3 s), `back.out(1.6)` ou `expo.out`. Escala 0,6→1,04→1.
- Saída: 4–6 quadros (0,13–0,2 s), `power3.in`, sempre com motion blur na direção do movimento.
- Durante o "parado": câmera derivando 2–4% (escala 1→1,05 ou deslocamento lento), `none`/`sine.inOut`.
- Stagger de elementos em lista/sílabas: 0,06–0,10 s.

### Logo (1,2–3,6 s)
Corte pro vermelho; estrela facetada de ~16 pontas, 1,4× a largura da tela, gira 8°/s. Letras do "ifood" entram uma a uma (i, f, o, o, d) a cada 0,12 s com escala 0→1,15→1 e 3–4 riscos brancos curtos (faíscas) saindo em volta; o sorriso-seta desenha por último (0,3 s). Logo final ≈ 30% da largura.

### Lista de restaurantes (3,6–6,8 s)
- Wipe horizontal: o vermelho sai pra esquerda em 0,15 s revelando branco.
- 1º card entra pela direita (ícone quadrado vermelho arredondado, raio 22%) e para no lugar com overshoot; os seguintes caem em cascata pra baixo a cada 0,1 s. Ícone ≈ 13% da largura; nome em negrito, 2 linhas cinza, tag colorida (roxa/verde) embaixo.
- Topo: abas "Restaurantes / Mercado / Farmácia" com ícones redondos, aparecem por último.
- Rolagem: acelera de 0 a ~3 telas/s em 0,4 s (`power2.in`) com RGB split (canais deslocados 6–12 px) e faixas arco-íris; termina num whip pra próxima cena.

### Na palma da sua mão (6,8–8,0 s)
- A lista em tela cheia encolhe pra 55% da largura e gira −25° (0,3 s, `power3.out`): vira a tela de um celular branco (cantos 12%, borda lilás clara).
- A mão lilás sobe de baixo (+40% → 0, 0,3 s, `back.out`) e "pega" o celular; leve balanço de 3° depois.
- Fundo vermelho com 2–3 anéis concêntricos (traço lilás/branco 30% opacidade) pulsando do centro do celular a cada ~0,6 s.
- Palavras: NA → PALMA → DA → SUA → MÃO!, uma a cada 0,12 s, entrando com escala 1,3→1 (batida), no topo da tela, alinhadas à esquerda.
- Selos "flor" com carrinho (canto sup. esq.) e % (canto inf. dir.) estalam com rotação −20°→0, 0,25 s.

### Comidas — câmera 3D (8,0–11,5 s)
- O "mundo" das comidas é um plano inclinado em perspectiva (rotateY ≈ −12°, rotateX ≈ 6°) que a câmera atravessa na DIAGONAL: cada comida está à direita-abaixo da anterior.
- Troca: tudo desliza pra cima-esquerda (≈ 1 tela na diagonal) em 0,27 s (8 quadros), `power3.inOut`, com motion blur direcional; a comida que sai continua visível no canto superior esquerdo por alguns quadros (parallax: comida anda mais que a palavra).
- Entrada da comida: vem da profundidade (escala 0,6→1,04→1, rotação 15°→0) com blur que limpa em 4 quadros.
- Palavra: entra 2 quadros depois da comida, por sílaba, de baixo pra cima (y +40 px → 0, 0,2 s, `expo.out`), stagger 0,07 s. Fica atrás da comida em profundidade (a comida passa por cima de parte da palavra).
- Pílula de preço: entra 4–6 quadros depois, deslizando da direita, sobreposta à base da comida (canto inf. direito).
- Parado: câmera empurra devagar (escala 1→1,04) e a comida gira 3–5°.
- Foto real recortada com sombra suave embaixo, comida ≈ 55–60% da largura da tela vertical.

### RAPIDINHO (11,5–12,7 s)
- Fundo creme #F7F4EC com 3–5 linhas cinza horizontais finas correndo pra esquerda (velocidade).
- Letras surgem da esquerda pra direita, uma a cada 0,04 s, crescendo pra cima (scaleY 0→2,4→2,1, origem embaixo, `back.out`). Bloco final ocupa ≈ 80% da largura.
- Motoboy (ilustração flat: moto vermelha, baú vermelho, roupa vermelho/pêssego, capacete vermelho) entra pela esquerda em 0,2 s e fica na frente do texto; trepida (2 px, ~8 Hz), rodas giram.
- Saída: tudo dá whip pra direita com blur horizontal (0,2 s); sobra um ponto vermelho que cai no mapa.

### Mapa (12,7–15,2 s)
- Visto de cima, sem perspectiva. Grade de quarteirões creme arredondados (raio ≈ 15% do lado) separados por ruas lilás-acinzentadas.
- Começa com zoom 2,5× na moto (ícone vermelho visto de cima, ≈ 4% da largura) e abre pra 1× em 0,6 s (`power2.out`).
- A moto anda pela rua (vertical, depois curva) a velocidade constante; a câmera segue com atraso de ~0,15 s (a moto fica sempre perto do centro).
- O pin preto de localização cai de cima com quique (0,25 s) ao lado de onde a moto vai parar.

### "FOI TRANQUILO!" e logo final (16,7–21,5 s)
Letreiro à mão branco no vermelho que se escreve em 0,4 s e sai por máscara; o logo se monta igual à abertura e fica com a estrela facetada girando atrás.

## 5. O que muda pro nosso (16:9, nossa história)
- Tudo centralizado, mas a composição ocupa as duas laterais: palavra gigante atravessando o quadro + objeto na frente; câmera 3D atravessando; elementos de profundidade (comida que sai, selos, anéis) nas laterais.
- UI do app sempre 1,6–2× do tamanho real, nunca celular pequeno no meio de tela vazia.
- Sem "Tá com fome?", sem "FOI TRANQUILO!", sem tela de pedido entregue com estrelas, sem POV.
