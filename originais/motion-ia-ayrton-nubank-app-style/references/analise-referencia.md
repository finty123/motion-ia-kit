# Analisar a referência e escrever o roteiro

## Quando ele manda um vídeo de referência
1. Quadros: 1 por segundo numa folha (`ffmpeg -vf "fps=1,scale=420:-1,drawtext=...,tile=3x5"`), depois folhas densas (6 fps) só nas transições.
2. Voz: transcreva (`scripts/transcrever.py`; o áudio de referência pode ser inglês, tire o `language="pt"` se for o caso). Sem voz = comercial guiado pela música.
3. Ritmo: BPM e curva de energia com librosa (a batida que entra é o marco pra palavra forte).
4. Entregue: objetivo, roteiro em atos com tempos, visual (paleta, fonte, elementos) e a **tabela de efeitos com nome em inglês** (ele pede "o nome dos efeitos" pra buscar e reusar).

## Estrutura que funciona (7 atos, ~35–45 s)
1. **Identidade** (0–7 s): fala de quem assiste ("Você correu o mês inteiro…").
2. **Problema / virada** (7–10 s): "Agora é a vez do seu dinheiro correr!"
3. **Revelação** (10–15 s): a marca aparece + a primeira ação no app ("Abre o Nubank, crie uma caixinha").
4. **Funções** (15–20 s): lista com item ativo + card de interface trocando.
5. **Sempre ligado** (20–26 s): "no automático", "de dia, de noite, no fim de semana".
6. **Resultado** (26–31 s): número grande subindo, frase de alívio ("enquanto você cuida da sua vida…").
7. **Marca / CTA** (31–35 s): logo e assinatura.

Cada palavra-chave falada aparece na tela no mesmo instante, com uma ideia nova a cada 2–3 s.

## Glossário de efeitos (comercial da Holo, a referência original)
| Efeito | O que é |
|---|---|
| 3D Text Rotate-in + Gradient Fill | palavra entra girando em 3D com gradiente dentro da letra |
| Fluted / Ribbed Glass + Mesh Gradient | faixas verticais de vidro distorcendo uma mancha de gradiente (ele NÃO quis isso no Nubank) |
| Per-character Blur Reveal | letras saem do desfoque uma a uma |
| Shape Morph (blob → pílula) | mancha de gradiente vira cápsula com texto |
| Pixel Dissolve / Dither Reveal | pontinhos viram mosaico e resolvem na imagem |
| Floating 3D Glass Icons + Hand Phone | celular na mão com ícones de vidro 3D em volta e texto grande atrás |
| Image Burst / Implode | cards explodem do centro e se recolhem |
| 3D Card Cloud (Z-space parallax) | fotos e pílulas flutuando em profundidade |
| Glass Lens Refraction | esfera de vidro passa distorcendo a palavra |
| Match Cut → 3D Globe with Pins | a esfera vira globo com etiquetas orbitando |
| Gradient Wipe → Logo Reveal | gradiente passa nas letras e corta pro logo |
| Typewriter + Cursor + Pull-back | barra digitando e câmera recuando |
| 3D Character Fly-by + Smoke Trail | mascote 3D voando com rastro |
| Active List Highlight + UI Card Carousel + Glow Aura | lista com bolinha no item ativo e card com brilho na borda |
| Card → Blob → Toggle Morph | card vira mancha e vira toggle de iOS ligando |
| Masonry Wall Reveal | mural de criativos em volta da palavra |
| Screen Zoom-out Reveal | a tela recua e vira um monitor/celular numa cena 3D |
| Day-to-Night Lighting | a cena 3D muda de luz do dia pra noite |
| Scale-down to Card | a cena encolhe virando card |
| iOS Picker Wheel / Slot Roll | lista em cilindro com item ativo |
| Bento Grid Build | fotos se encaixam numa grade |
| 3D Fly-through | câmera atravessa um campo de cards |
| Gradient-to-Black Settle + Inline Icons | palavras em gradiente assentam em preto com ícones entre elas |
| Odometer Counter + Bar Chart Grow | número rolando dígito a dígito com barras subindo |
| Character Fade-in (URL) | endereço surge letra a letra |

Base: easing suave (expo / in-out), motion blur nos movimentos, fundo claro com respiro.
