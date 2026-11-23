# Receitas de cena (arquivos do modelo em `assets/modelo/compositions/`)

Os tempos abaixo são do Motion Nubank (narração no 0, 35,5 s). Ao fazer outra marca, copie a cena que serve, troque texto e tempos pelos do `words.json` e mantenha a mecânica.

| Cena (arquivo) | Início–fim | O que faz | Técnica que importa |
|---|---|---|---|
| `abertura.html` | 0–0,74 | "Você" gigante no quadro 0, fundo roxo; a frase continua no mesmo tamanho com a câmera acompanhando ("Você correu") | mede as letras (`offsetLeft`) e anda o `x` da linha até o centro da próxima palavra; blur yoyo no meio do pan |
| `mao.html` | 0,74–5,95 | corte seco → mão recortada com "mês inteiro" atrás, zoom out acelerado, ícones de vidro; pan pra esquerda até o celular 3D; frase + notificações à direita; moedas caem | recorte PNG por cima do texto; tela da foto trocada via `matrix3d`; pan com parallax/arrasto (texto fica pra trás com `skewX`, mão inclina, ícones da frente correm mais); celular 3D chega atrasado e assenta com mola; cards entram com `back.out` |
| `corrida.html` | 5,85–12,5 | "Agora" + moeda rolando; no "correr!" a câmera 3D segue a moeda até "Abre o [logo]"; caixinha 3D sobe, pílula de vidro digita, tampa abre, moeda pula dentro, tampa fecha, brilha, rendimentos sobem; câmera mergulha na caixinha | **câmera compartilhada DOM + three.js**: `#co-world` recebe `translate(-camX·201,5·s, camY·201,5·s) scale(s)` com `s = 10/camZ` (201,5 px por unidade em z=0 com fov 30 e câmera em z=10); câmera three em `(camX, camY, camZ)` sem rotação. Canvas por BAIXO do DOM pra pílula e chips ficarem na frente da caixinha |
| `lista.html` | 12,5–17,65 | lista com bolinha no item ativo + card de vidro trocando (Pix, cartão 3D em CSS, caixinha, gráfico); card vira toggle "No automático" e ícones 3D giram em volta | ícones em elipse em pé (rx 4,7, ry 2,45 unidades, câmera z 12), peças de frente pra câmera, escala 0,74; o módulo three registra `window.__hf.buildReady` e a timeline clássica chama `window.__liRing(t)`; saída mergulha no toggle |
| `diaenoite.html` | 17,7–23,15 | celular em pé cortado embaixo, câmera começa colada na tela e recua; "De dia / De noite / No fim de semana" no topo, luz e fundo mudam; cena encolhe em card e o seletor de iPhone gira (rendendo / guardando / protegendo) com objeto 3D por palavra | tela do celular redesenhada só quando muda (`lastKey`); relógio da timeline adicionado POR ÚLTIMO (o seletor já atualizado quando desenha); luz de brilho atrás do celular, nunca na frente (vira bolinha no vidro) |
| `rende.html` | 23,15–25,95 | odômetro R$ 12.476,80 → 12.480,00 com barras roxas subindo e notificação "rendeu hoje" | contas em centavos inteiros; uma casa só rola no último centavo antes da virada (`pos = base + clamp(tot % q − (q − 1))`); máscara de fade nas colunas |
| `vida.html` | 25,95–30,6 | nuvem de chips de vidro em profundidade + "Então, enquanto você cuida da sua vida," palavra por palavra; implode e vem "o roxinho [moeda 3D] cuida do seu dinheiro." | chips em CSS 3D (`transform-style: preserve-3d`), câmera derivando; palavras entram em gradiente e assentam em tinta |
| `final.html` | 30,5–35,5 | íris roxa do centro, logo "nu" se desenha em dois traços com brilho; logo sai e entra "by @ayrtonsena.stg" parado até o fim | SVG com `<mask>` de dois paths (`pathLength=1`, `stroke-dashoffset` 1→0) sobre o PNG do logo; brilho = retângulo com gradiente mascarado pelo logo |

## Transições que ele aprovou
- Corte seco no fim de uma frase + zoom out acelerado no plano seguinte.
- Pan lateral de câmera com parallax e arrasto (nunca bloco rígido).
- Mergulho (zoom in + blur) numa peça e a próxima cena abrindo colada nela (toggle → tela do celular).
- Cena encolhendo em card (`scale 0.5`, `borderRadius`) e o assunto seguinte ao lado.
- Íris de cor da marca saindo do centro pro final.

## Liquid Glass (CSS em `index.html`)
`.glass`: fundo branco translúcido em gradiente, `backdrop-filter: blur(22px) saturate(190%) brightness(1.05)`, sombras internas de luz e borda com reflexo (pseudo-elemento com máscara `xor`). Variações `.glass.lilas` e `.glass.roxo`. Funciona em cima do canvas 3D (o vidro desfoca as moedas atrás).
