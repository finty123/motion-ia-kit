# Catálogo de estilos

Cada estilo diz quando combina, paleta de partida, fontes, os recursos do motor/kit e as transições. Ajuste a paleta aos materiais que a pessoa mandar (capa do álbum manda na paleta).

Comum a todos (é o que dá cara de After Effects):
- câmera 3D sempre em movimento (`setCam3` com órbita, dolly e rolagem leve por cena);
- lente meio fisheye (`RITMO.fisheye` 0,10–0,20);
- motion blur (2 subquadros no render) e desfoque no que passa perto da câmera;
- grão (já vem no motor), retícula opcional (`RITMO.halftone`);
- glow só na palavra forte da cena, com flash no impacto.

---

## 1. Tipografia 3D cinética ("Training Season" / "Tu é doido")
**Quando:** pop com atitude, batida marcada, letra com palavras de impacto. É o estilo aprovado do Training Season.
**Paleta:** vermelho bem escuro `#7A0820`, branco `#FFFFFF`, preto, glow `#ff2d55`, vermelho de texto `#e8173f`. Variações: roxo escuro + verde-limão (Motion com IA), azul petróleo + laranja.
**Fontes:** Anton (palavra gigante 3D), Space Mono (detalhes técnicos: loading, régua), Inter 700 (assinatura).
**Recursos:** W3 com extrusão, palavra em tela cheia uma de cada vez, letra repetida (I subindo), buraco vermelho, espelho infinito, vidro estilhaçando, laço, mira REC, balões de chat, contagem 3-2-1, carimbo (stamp3), loading bar.
**Transições:** mergulho na letra até a tela ficar da cor dela, branco escurecendo sugado pelo buraco, wipe de cor, corte seco na batida principal.
**Exemplo:** `examples/training-season/scenes.js`.

## 2. Mundo da capa + neon ("See You Again")
**Quando:** R&B, rap melódico, indie, nostalgia, música com capa forte. O cenário É o universo do álbum.
**Paleta:** gradiente laranja `#ff8a1f` → vermelho `#e2321f`, creme `#fff3c4`, neon amarelo `#ffe08a`, verde da vegetação. Tire as cores da capa quando houver.
**Fontes (papel fixo):**
- assinatura fina com neon (write-on) pras palavras suaves ("Can I", "If I Would See You"); hoje temos Segoe Script, Gabriola e Little Moment (pack); a mais fiel seria uma assinatura monoline fina (ex.: Mrs Saint Delafield, do Google Fonts, grátis), e só deve ser baixada com o ok do Ayrton;
- script mais grosso com glow pra palavra final (Pacifico);
- serifada bold em etiquetas (albra ou Chamberi Display, do pack), empilhadas e ligadas por uma linha curva à mão;
- sans condensada grande e cinética (Bahnschrift) pras frases rápidas.
**Recursos:** `writeOn`, `pill` com sombra leve, `starburst` atrás da pessoa batendo com a palavra neon, `propsField` com os objetos do álbum (abelhas, flores), `lensPass` (objeto cruzando a lente pra cortar a cena), `letterTrail` pra sílaba esticada (Foreverrrr), `RITMO.vazamento` (luz quente), formato quadrado dentro do vertical (`compor_quadrado.py`).
**Transições:** objeto passando na lente, clarão estourado (`clarao`), blur whip.

## 3. Colagem retrô / riso ("Juno")
**Quando:** pop leve, romântico, divertido, letra com duplo sentido. Visual de papel impresso.
**Paleta:** creme `#fff4d6`, rosa `#e8607a`, rosa claro `#f6d9d4`, marrom `#8a5a44`, amarelo manteiga `#fff3b0`. Tudo levemente lavado (retícula 0,10–0,18).
**Fontes:** Chamberi Display Bold (serifada retrô macia, quase igual à do Juno), Misky (serifada condensada em caixa alta, pro "FALL IN"), Relationship of mélodrame (itálico elegante pras palavras de apoio), Playfair Display.
**Recursos:** `pill` com sombra longa diagonal e texto que troca dentro ("make me" → "wanna make you"), `scramble` (letras embaralhando dentro da pílula), `circleText` (o "ooooh" girando), `gridFloor` (chão de grade em perspectiva), `propsField` com emoji/objetos (beijos, corações, emoji 🤨), composição que se monta palavra por palavra com tamanhos diferentes e uma palavra girando 90°, parede de tijolos com o @ no final.
**Transições:** íris de coração (`iris(..., 'coracao')`), círculo crescendo, zoom atravessando, blur whip.

## 4. Objetos 3D na batida ("Bolinha glow")
**Quando:** eletrônica, trap, música instrumental ou com pouca letra. O ritmo vira objeto.
**Paleta:** fundo escuro da marca + um destaque neon. Pouca cor.
**Fontes:** uma só (Anton ou Bebas), pouco texto.
**Recursos:** partitura primeiro (regra dele: só existe objeto onde tem batida), `box3`, `ring` nas batidas, câmera copiando o ângulo da referência, bokeh.
**Transições:** corte seco no drop, flash curto, câmera atravessando.

## 5. Glitch digital / Y2K
**Quando:** hyperpop, funk, letra sobre internet, celular, mensagem, "overload".
**Paleta:** preto, branco, um ácido (verde `#c6ff34` ou magenta `#ff2bd6`), azul de tela `#2b5cff`.
**Fontes:** Space Mono, Bungee, Anton.
**Recursos:** aberração cromática forte nas cues (`ch`), `scramble`, balões de chat se multiplicando, janelas de software (`plane`), barra de loading, troca de fontes rápida (receita da tuedoido).
**Transições:** glitch de tela cheia, tape-stop visual, corte seco.

## 6. Editorial preto e branco
**Quando:** balada, voz em primeiro plano, letra séria ou poética.
**Paleta:** off-white `#f2f0ee`, preto, um vermelho de detalhe.
**Fontes:** Playfair Display / Chamberi Display (serifada grande), Relationship of mélodrame (itálico), Inter fino de apoio.
**Recursos:** palavra gigante serifada, muito respiro na tela, `writeOn` discreto sem neon, linha fina desenhando, câmera lenta mas sem parar.
**Transições:** fade por máscara, wipe lento, corte na respiração da voz.

---

## Composição do quadrado dentro do vertical
Construa e renderize em `--size 1080x1080`; no fim rode `compor_quadrado.py quadrado.mp4 vertical.mp4`. Ele faz o fundo com a mesma cena ampliada, borrada, escurecida e com retícula.
