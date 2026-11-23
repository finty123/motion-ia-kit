# API do motor (scripts/engine/)

O `build.py` junta, nesta ordem: `engine.js` (base 2D, pós-efeitos), `engine2.js` (3D), `helpers.js` (janela de software, código, ventoinhas, texto de prompt) e `kit.js` (cenas reutilizáveis e runtime). Depois entra o `scenes.js` do projeto. Tudo é função pura do tempo `t`, sem estado entre quadros, e o aleatório tem semente fixa (`mulberry32`).

## Índice
1. Estrutura obrigatória do scenes.js
2. Tempo, sincronia e cues
3. Câmera 3D e coordenadas
4. Texto 3D: W3, L3, text3D
5. Planos, caixas, carimbos
6. Fundo, glow, blur, anel
7. Kit pronto: chat, vídeo genérico, logo, linhas centradas, swipe
8. Utilitários

## 1. Estrutura obrigatória do scenes.js

```js
const END = 83.5;                       // duração total (fala + CTA segurando + logo)
function S1f(ctx, t) { setCam3({...}); bgv(ctx, K, V, 0.4); W3(ctx, t, 'PALAVRA', w(0) - 0.07, {...}); }
cue(w(0), 'hit_small', 0.6, { sh: 0.2 });
// ...
scene(0, S1f);
scene(w(4), S2f);                       // cada cena começa num índice de palavra
scene(END - 3.5, LOGOf);
```

- Cada cena é `function(ctx, t)` e desenha a tela inteira, fundo incluso.
- `finalizeScenes()` roda sozinho no build: ordena as cenas e põe blur nas trocas.
- Cores prontas: `K` preto, `WH` branco, `V` principal, `L` destaque, `DV` principal muito escura (fundo com glow), `SIDE` (lateral da extrusão). Para trocar a paleta, use `build.py --paleta "principal=#hex,destaque=#hex"`.
- Para forçar a divisão do logo: `const LOGO_SPLIT = 750;`.

## 2. Tempo, sincronia e cues

- `w(i)` dá o início da palavra i. `WD[i]` é `[início, fim, "palavra"]`, vindo do words.json cortado.
- Comece animações de impacto em `w(i) - 0.07`. Para elementos citados ("esse X aqui"), comece em `w(i) - 0.35`.
- `cue(t, sfx, v, { sh, fl, ch, bl })`:
  - Agenda um som e efeitos de tela.
  - `sh` é o tremor + soco de zoom, `fl` o flash branco, `ch` a aberração cromática, `bl` o blur gaussiano. Todos vão de 0 a 1,2.
  - O `mix.py` lê essas cues para sintetizar o som. A lista de sons está em `audio.md`.
- `cue(t, 'muffle', duração)`: janela de som "embaixo d'água" (buraco negro, tela preta).
- `cue(t, 'blurcue', 0, { bl: 0.6 })`: só blur, sem som.
- `beatPulse(t)`: vale 0 a 1, e pulsa nas batidas da música (`BEATS`). Use para glow e escala no CTA.
- Molas e curvas:
  - `sp(t, t0, zeta=0.62, w=15)`: mola de 0 a 1 com overshoot.
  - `P(t, a, b)`: progresso linear com clamp.
  - Easings `eo3`, `ei3`, `eio`, `eiExp`, `eoExp` e o auxiliar `lerp`.

## 3. Câmera 3D e coordenadas

- **Mundo.** A origem é o centro da tela, `y` positivo para baixo e `z` positivo para longe. No plano z=0, 1 unidade = 1 px.
- `setCam3({ x, y, z, rx, ry, rz })`:
  - Câmera da cena, chamada no começo de cada cena.
  - `z` positivo aproxima (dolly-in).
  - `ry` faz a órbita lateral, `rx` a inclinação e `rz` a rolagem.
- **Padrão vivo:** `ry: 0.3*Math.sin((t-t0)*0.9)`, `z: lerp(-150, 250, P(t, t0, tFim))`, `rz: 0.03*Math.sin(t*1.4)`.
- `P3(ponto, pose)` devolve `[xTela, yTela, z, escala]`. Útil para desenhar linhas 2D presas a objetos 3D (risco no preço, X no carimbo).

## 4. Texto 3D

`W3(ctx, t, texto, t0, o)` é a peça principal: a palavra entra com mola, giro e impacto.

| Parâmetro | Padrão | Uso |
|---|---|---|
| `x, y, z` | 0 | posição final no mundo |
| `rx, ry, rz` | 0 | rotação final |
| `size` | 200 | px da fonte |
| `font`, `wt` | 'Anton', '' | outras: `'"Playfair Display"'`, `'"Bebas Neue"'`, `'Pacifico'`, `'"Space Mono"'`, `'Bungee'`, `'"Abril Fatface"'`, `'"Permanent Marker"'`, `'Inter'` |
| `face`, `side` | WH, SIDE | cor da frente e da extrusão |
| `depth` | size*0.16 | profundidade da extrusão |
| `from` | `{z:-900, rz:0.25}` | de onde vem (somado à pose final). Ex.: `{z:2400, ry:-1.8}` vem do fundo girando; `{z:-1100, rz:0.5}` vem da câmera; `{y:-500, rx:-1.6}` cai de cima |
| `zeta`, `w` | 0.52, 15 | mola: zeta menor = mais rebote |
| `glow` | 0.25 | brilho base (0 = sem). `glowCol` muda a cor |
| `flash` | 0.9 | brilho extra no impacto, que decai em ~0,3 s |
| `out`, `outD`, `outZ` | — , 0.22, 1100 | saída: voa para a câmera e some a partir de `out` |
| `drift` | 0 | balanço contínuo depois de entrar (0,08 a 0,18) |
| `glint` | — | 0 a 1: reflexo de luz passando na face |
| `N` | 2 | subdivisão da face (3 para letras grandes que giram muito) |

Mais funções de texto:

- `L3(ctx, t, texto, t0, { x, y, size=48, col, font='Inter', wt='800', out })`: linha de apoio plana, que entra em 3D sem extrusão.
- `text3D(ctx, texto, pose, op)`: desenha sem animação. Use em contadores e em posições interpoladas à mão.
- `text3Dglow(ctx, texto, pose, op, quantidade)`: glow do texto desenhado com `text3D`.
- `rowX(['E','TU','PODE'], size)`: devolve os X centrais de cada palavra para montar uma linha CENTRADA.

## 5. Planos, caixas, carimbos

- `plane(ctx, textura, pose, N=4, w, h, lz=0, alpha=1)`:
  - Qualquer canvas ou imagem vira um plano 3D com perspectiva real.
  - Use N=6 a 8 para janelas e cards grandes, N=10 a 16 para planos enormes (parede de texto).
  - `pose` aceita `parent` (pose do pai) para hierarquia.
  - As células atrás da câmera são descartadas sozinhas.
- `box3(ctx, [w,h,d], pose, (iFace, luz) => ({ fill, stroke, lw, draw(c, w, h) }))`:
  - Caixa 3D com faces ordenadas e iluminação. As faces são 0 frente, 1 trás, 2 esquerda, 3 direita, 4 topo, 5 base.
  - `draw` pinta conteúdo dentro da face (ventoinhas, telas).
- `stamp3(ctx, t, t0, chave, texto, size, { x, y, z, rz, bg=L, fc=K, out })`: carimbo (caixa colorida com texto) que slam em 3D com espessura e glow. Exemplos: DIFÍCIL, GENÉRICO, BLACK, PERA AÍ.
- `pcFace3(t, emissivo)`: faces de PC gamer, para usar com `box3([260,560,580], ...)`.
- `aeWindow(ctx, x, y, w, h, t)`: janela genérica de timeline com keyframes. Desenhe num canvas `mk(1500,800)` e use como textura.
- `CODE`, `codeLine(ctx, linha, x, y, size)`: código colorido para editor.

## 6. Fundo, glow, blur, anel

- **Fundo.**
  - `bgv(ctx, base, glowCol=V, alfa=0.45, gx, gy)`: fundo chapado + glow radial. Use `bgv(ctx, DV, V, 0.55)` para o roxo escuro com glow.
  - `bg(ctx, cor)`: fundo chapado, sem glow.
  - `swipeBG(ctx, t, [[t0, cor], [t1, cor], ...])`: troca de cor com wipe diagonal. Devolve o índice do segmento atual, útil para escolher o conteúdo.
- **Glow e blur.**
  - `glow(ctx, g => { desenho em g }, quantidade, blur=7)`: brilho aditivo. Dentro, desenhe com as mesmas funções (`plane(g, ...)`) e a câmera já vem aplicada. Para desenho 2D em coordenada de tela, use `g.setTransform(.25,0,0,.25,0,0)`.
  - `blurDraw(ctx, fn, px, alfa)`: desenha uma camada com desfoque gaussiano (profundidade de campo).
  - `bokeh(ctx, t, quantidade)`: partículas desfocadas de fundo.
- **Anel e partículas.**
  - `ring(ctx, t, t0, cor, velocidade=2200, largura=36, duração=0.8, x, y)`: anel de choque no impacto.
  - `STARS`: estrelas para cenas de espaço.

## 7. Kit pronto

- `chatTex(t, título, msg, digitaIni, digitaFim, envia, pontosIni, pontosFim, resposta)`:
  - Devolve um canvas 900x760 de chat digitando, enviando e respondendo.
  - Use com `plane(ctx, chatTex(...), pose, 6, 900, 760)`.
- `badTex(t, w=960, h=540)`: o "vídeo genérico ruim" proposital (gradiente arco-íris, serifa, estrelas). É o único lugar onde esse visual é permitido.
- `badVideo(ctx, x, y, w, h, t, raio, simples)`: a versão 2D, para grades.
- `logo3(ctx, t, pose, partes, glintP, glow)`:
  - Logo com extrusão real. `partes = [['M', {x, y, z, rx, ry, rz, al}], ['I', {...}]]`: 'M' é a parte 1 e 'I' a parte 2.
  - `glintP` (0 a 1) é o reflexo passando.
  - Para logo inteiro, passe as duas partes com a mesma pose.
- `phone(ctx, x, y, w, h)`, `heart`, `eyeIcon`, `stampTex`: peças de interface.
- **No exemplo** (`examples/motion-ia/scenes.js`, para copiar):
  - `editorTex`: editor digitando e apagando.
  - `postTex`: post publicando, com visualizações subindo.
  - `ctaPhoneTex`: comentário → notificação → DM → link → toque.
  - `gridTexs`: grade de vídeos multiplicando.
  - `partSetup`/`shardPos2`: explosão que reconstrói texto.
  - `QFONTS`: troca de fontes.
  - `VORT`: vórtice de sucção.
  - `S1`/`s1layout`: palavra alongada com câmera seguindo.
  - `FREEZE2`: congelar a cena anterior como plano 3D.
  - `wallTex`: parede de prompt rolando como piso.

## 8. Utilitários

- **Canvas e desenho 2D:**
  - `mk(w,h)` devolve `{c, x}` (canvas + contexto).
  - `TX(texto, size, cor, fonte, peso)`: textura de texto em cache.
  - `T(ctx, texto, x, y, size, cor, { f, w, a, al, sc, r, stroke })`: texto 2D direto.
  - `rr(ctx, x, y, w, h, raio)`: retângulo arredondado.
- **Cor:** `mix(a, b, t)` e `rgba(hex, a)`.
- **Matemática:** `clamp` e `mulberry32(seed)`.
- **Medida de texto:** `tw(texto, size, fonte)`.
