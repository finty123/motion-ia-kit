# Regras do Ayrton (aprendidas no Motion iFood – Fome de madrugada, 27–28/10/2026)

Cada regra veio de uma reprovação ou de um ajuste. O porquê está junto pra você aplicar o espírito, não só a letra.

## Visual
- **Chapado e colorido, nada de glow.** A 1ª versão do começo tinha fundo escuro e números com brilho vermelho; ele reprovou: "o design que eu te passei não tem glow". Use cores sólidas da paleta, sem sombra, sem brilho, sem gradiente.
- **Nada listrado.** A estrela facetada (raios) atrás do logo foi reprovada duas vezes. Logo sobre cor chapada.
- **Troca de cor a cada cena**, sempre com as cores da marca. No iFood: creme → vermelho → vinho → mostarda → branco (app) → vermelho → creme… A troca é uma onda (círculo de `clip-path` crescendo de onde a ação acontece) ou um corte seco na batida.
- **Leve e engraçadinho:** números que pulam como gelatina no ronco da barriga, traços de "susto" estalando (as linhas do motoboy do carrossel iFood), texto que entorta de raiva, letras que esticam ("DOOOOIDO").
- **16:9 composto, não vazio:** palavra gigante atravessando o quadro com o objeto na frente (celular entre "quase" e "tudo."), elementos nos dois lados, câmera atravessando. Nunca um celular pequeno no meio com as laterais vazias.
- **Tipografia:** Montserrat 900 (Black) grande, caixa baixa nas frases, itálico caixa alta nos bordões ("NA PALMA DA SUA MÃO!"), League Gothic esticada (scaleY ~2) pro "RAPIDINHO". Fonte pequena e fraca foi motivo de reprovação.

## Ilustração e assets
- **Proibido ilustração feita com retângulo e círculo** (mão, moto, sacola, cozinha). Ficou "tosco" na 1ª versão. Ou é foto real recortada, ou SVG desenhado com paths no estilo flat da marca (planos chapados, sem contorno, facetas de 2–3 tons), ou modelo 3D. Mostre uma folha com as ilustrações antes de animar.
- Ele prefere menos ilustração e mais coisa real: cortou a mão e a campainha desenhadas, trocou a sacola desenhada pela **foto real da sacola**, e o "dim-dom" virou só tipografia.
- **Recortes:** o recorte automático estragou a pizza. Confira cada recorte em fundo da cor da marca; sombra cinza e papel aparecem.
- **Logo:** sempre o SVG oficial. Nunca redesenhe.
- **UI do app:** recriada em vetor igual às telas reais (home com a foto saindo de cima de um bloco colorido, chips, banners, cards de loja, app do entregador). Nada de UI genérica. Nomes de restaurante inventados, nunca marcas reais.
- **Celular 3D realista** (iphone.glb do registry, com a tela desenhada em canvas): ele gostou. Corpo grafite e sem o logo da Apple.

## Movimento
- **Tudo na batida da música.** "Uma coisa que eu senti muito falta foi fazer as coisas na batida da música." Cortes, trocas de cor, palavras, pops, cliques, chegadas e o logo caem em batidas ou meias batidas. A entrada forte da música coincide com o momento-chave da marca (o logo aparecendo).
- **Tudo junto, nada "blocado".** O celular subindo, depois girando, depois aproximando foi reprovado: tem que subir, girar e aproximar ao mesmo tempo.
- **Ritmo rápido.** A 1ª abertura (relógio 1:47 com estrondos antes da fala) ficou lenta. Comece direto na fala, com texto acompanhando e câmera 3D voando entre as palavras.
- **Fluido como a referência:** um elemento vira o outro (a pizza salta da categoria e vira a cena das comidas, o botão "Fazer pedido" sobe e vira a tela, o "tudo" de "tudo fechado." desliza pra "quase tudo."). Sem slideshow de cenas soltas.
- **Fala reativa vira texto na tela:** "Tá de brincadeira comigo, né?" e "beleza." apareceram escritos a pedido dele. Toda fala importante tem um texto acompanhando.
- **Comidas:** palavra gigante branca em sílabas, colada na foto (o "Açaí" longe do pote foi corrigido), pílula de preço com carrinho e troca diagonal com desfoque. Cada comida entra na palavra falada.

## Som
- **Voz > efeitos > música.** Música ~0,12 debaixo da fala e ~0,25–0,35 sem fala.
- **Voz clara:** a voz de WhatsApp soou abafada; tratar com `scripts/voz_clara.py`.
- **Muito som de UI** (clique, pop, interface) em todo toque, card, chip, botão e palavra que estala, alternando 2–3 arquivos. Cinemático (boom) só no gancho e no logo final.
- **Sem riser.** "Esse riser aí não combinou."
- Nada de som de desenho animado ou de meme. Ronco de barriga de verdade: ele mandou um (tummy song); o "Deep Growl" da pasta é rugido, não serve.
- Mix final em −14 LUFS e pico −1 dBTP.

## Final
- O logo se monta letra por letra (i, f, o, o, d e o sorriso girando por último) e o "o" da direita dá uma piscadinha (as bolinhas do "oo" são olhos).
- Depois, **troca de take**: fundo branco e **@ayrtonsena.stg** preto no meio, subindo letra por letra e pulando de leve na batida, com "comercial não oficial" pequeno embaixo. Segura ~2,5 s.

## Processo
- Nada de exportar antes de ele aprovar a prévia completa.
- No render, no máximo 4 workers e prioridade baixa: o PC dele (i5-12400F, 16 GB, GTX 1050 Ti, C: quase cheio) trava.
- Mostre tabela → começo no nível final → resto; quando ele disser "gera até o fim", faça tudo de uma vez.
