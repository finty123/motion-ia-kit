# Kit 3D (three.js 0.181.2) — `compositions/kit3d.js` e `kit3d-extra.js`

Tudo é desenhado a partir do tempo (`render(t)` puro), dentro do `onUpdate` de um tween "relógio" da timeline GSAP da cena. Nada de `requestAnimationFrame`.

## kit3d.js
- `ready()` — carrega fontes (Outfit, Inter) e o logo `assets/nu-branco.png` em `IMG.nu`. Sempre `await ready()` antes de criar moeda/caixinha/telas.
- `makeStage(canvas, {fov=30, w, h, shadow, exposure})` → `{renderer, scene, camera, key, fill, ground, render}`. Ambiente de estúdio próprio (domo + softboxes) via PMREM = reflexo realista; ACES; sombra suave num `ShadowMaterial` (ligue com `ground.visible = true`).
- `makeCoin({R, T, color, glyph})` — moeda com relevo de verdade: face em grade polar deslocada por mapa de altura (borda alta, cifrão em relevo), borda serrilhada, metal roxo com verniz. Pesada (~80k vértices): até ~10 por cena.
- `makePhone({frame, backColor})` → `{group, canvas, ctx, texture, update}`. iPhone com moldura de titânio, vidro preto, camada de reflexo aditiva, câmeras atrás e botões. A tela é um canvas 600×1278: desenhe e chame `update()`.
- Telas prontas: `drawHome(g)`, `drawCaixinha(g, {valor, prog})`, `drawLock(g, {hora, data, k (0 dia → 1 noite), notif})`, `drawAuto(g, {on})`.
- Utilitários: `seg(t,a,b)`, `ease.outExpo/outQuart/inOut/inCubic/spring`, `lerp`, `money(v)`, `NU` (cores).

## kit3d-extra.js
- `drawNu(g, x, y, h, cor)` — logo do PNG em qualquer cor (canvas).
- `drawHome2(g, {saldo})` — tela inicial no estilo da foto da mão (header roxo com logo, card da conta, Pix/Pagar/Transferir, acesso rápido, abas).
- `plastic(cor)` — plástico brilhante (clearcoat + sheen) do 3D da marca.
- `makeBox({W,H,D})` → `{group, hinge, mat}` — caixinha com tampa (abre com `hinge.rotation.x = -1.9`), fenda e logo na frente; origem na base.
- `makeShield()` — escudo com check.
- `makeCoinLite(R, T)` — moeda leve pra pilhas (geometria compartilhada).

## Pegadinhas que já custaram tempo
- Cada cena 3D precisa da linha `import "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";` no próprio arquivo, senão o `check` acusa `missing_three_script`.
- Script `type="module"`: registre `window.__timelines[id]` no FIM, depois do `await ready()`.
- Cena com timeline clássica + módulo 3D separado: o módulo cria `window.__hf.buildReady["chave"]` antes e resolve no fim; a timeline chama a função do módulo se existir.
- O tween "relógio" vem depois dos tweens que alimentam o desenho (ex.: seletor), pra que o quadro use os valores já atualizados.
- Canvas por cima ou por baixo do DOM decide quem tampa quem (pílula atrás da tampa da caixinha = canvas por baixo).
- O Studio do HyperFrames grava `data-hf-id="..."` nas tags: edições por script devem usar regex tolerante a esses atributos.
- Luz pontual na frente do celular aparece como bolinha no vidro: deixe atrás (z negativo).
- Metal com rugosidade baixa sob luz fraca estoura em riscos brancos: rugosidade ≥ 0,3.
