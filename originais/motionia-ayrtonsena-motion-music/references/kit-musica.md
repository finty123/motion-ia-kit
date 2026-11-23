# kit_musica.js — API

Carregado pelo `build.py` depois do motor (`engine.js`, `engine2.js`, `helpers.js`, `kit.js`). Tudo é função pura do tempo `t`. Exemplo de cada um em `examples/demo-kit/scenes.js`.

## Utilidades
- `scr(fn)`: desenha em coordenada de tela (sem câmera), `fn(ctx)`.
- `rowGap(ws, sz, gap, font)`: X centrais de uma linha centrada com espaço fixo (o espaço do Anton é estreito).
- `fitSize(s, wmax, hmax, font)`: tamanho de fonte pra caber em `wmax`, limitado a `hmax`.
- `beatNear(t)`, `beatsBetween(a, b)`.
- `clarao(t, forca)`: clarão estourado + blur (transição de luz entre blocos).
- `scramble(s, t, t0, dur, seed)`: texto com letras embaralhando até resolver.

## Pós-efeitos globais (defina no topo do scenes.js)
```js
RITMO.fisheye = 0.16;            // lente olho de peixe (0,10–0,20). Pode ser função: t => t < 9 ? 0.12 : 0.2
RITMO.halftone = 0.12;           // retícula por cima (colagem/riso)
RITMO.vazamento = 0.6;           // luz quente andando (filme)
```
`POSTFX` é a lista de passes; dá pra empurrar um passe próprio: `POSTFX.push(t => { ... desenha em X ... })`.

## Texto
- `writeOn(ctx, t, s, t0, dur, o)`: script se escrevendo da esquerda pra direita, com ponta de caneta brilhando e glow neon. `o`: `x, y, z, rx, ry, rz, s, size, font ('Pacifico'), col, glowCol, glow (0.9), out, outD`.
- `pill(ctx, t, o)`: etiqueta arredondada com sombra longa diagonal; o texto troca dentro (desliza) nos tempos de `textos`. `o`: `id` (único por pílula), `textos: [[t, 'texto'], ...]`, `x, y, z, rx, ry, rz, size, font, wt, bg, fg, sombra (true), sombraLen, sombraCol, sombraAlpha (0.32), scramble (seg), out, padX, padY, raio`.
- `circleText(ctx, t, s, t0, o)`: letras em volta de um círculo girando, nascendo uma a uma. `o`: `x, y, z, r, size, font, col, spin (rad/s, negativo = anti-horário), stagger, a0, glow, glowCol`.
- `trailHead(t, times, path)` + `letterTrail(ctx, t, ch, times, path, o)`: sílaba esticada. `path(i) -> {x, y, z, rz}`. Ordem na cena: `h = trailHead(...)`, `setCam3` seguindo `h`, fundo, `letterTrail(...)`.

## Transições
- `iris(ctx, t, t0, dur, cor, forma, cx, cy)`: forma (`'circulo'`, `'coracao'`, `'estrela'`) cresce e cobre a tela com a cor da PRÓXIMA cena. Comece a próxima cena com esse fundo.
- `lensPass(ctx, t, t0, dur, desenho, o)`: objeto gigante e desfocado cruzando a lente; o corte vai em `t0 + dur/2`. `desenho` = emoji (string) ou `function(c, x, y, s)`. **Chame igual nas duas cenas** (a que sai e a que entra) pra atravessar o corte. `o`: `dir (1/-1), dy, s, blur`.

## Cenário
- `starburst(ctx, t, t0, o)`: explosão de quadrinho que bate com a palavra. `o`: `x, y, z (200 = atrás do texto), r, pontas, col, giro, glow (0.25), out`. Use cor que contraste com o texto da frente.
- `gridFloor(ctx, t, o)`: chão de grade em perspectiva rolando. `o`: `y, step, n, col, lw, vel`.
- `propsField(ctx, t, t0, desenho, o)`: objetos do universo da música espalhados em profundidade, os mais perto desfocados. `desenho` = emoji ou imagem. `o`: `n, seed, area, vel, tam, espalha, desfoque`.

## Peças do Training Season (aprovadas)
- `loadingBar(ctx, t, marcos, o)`: "LOADING 000%"; `marcos = [[t, fração], ...]`; some depois do último. `o`: `fim, w, y, col, label`.
- `redHole(ctx, t, t0, t1, o)`: buraco negro VERMELHO (miolo escuro, borda vermelha, disco girando) crescendo e fechando em `t1`. `o`: `r0, r1, cor, meio, borda`.
- `assinatura(ctx, t, t0, txt, o)`: pequena, branca, glow, centralizada, **em coordenada de tela** (não gira com a câmera), sem fade out. `txt` é obrigatório e vem do @ que a pessoa informou (ex.: `'by @fulano'`); sem `txt` não desenha nada. `o`: `size (46), col, font ('Inter'), wt, y, glow, fadeIn`.

## Armadilhas conhecidas
- Em cena com câmera girando muito, o que tem que ficar parado vai em `scr()`; `plane()` gira junto com a câmera.
- `lensPass` desenhado só numa cena some no corte. Chame nas duas.
- Desenhar antes do `setCam3` usa a câmera da cena anterior.
