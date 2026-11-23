# Referências de movimento

As tiras em `assets/referencias/` (8 quadros de cada) e os vídeos curtos em `assets/referencias/videos/` mostram cada vídeo usado no comercial Dane-se. São comerciais de outras marcas, tirados do Pinterest: servem só pra mostrar e estudar o movimento. Nunca copie logo, lata, cor ou composição deles, e não coloque essas imagens no vídeo nem em material publicado.

## Catálogo (o que cada uma ensina e onde entra na estrutura)

| Tira | O que acontece | Onde entra |
|---|---|---|
| `lit-energy-macro-plano-unico` | Plano único: macro na tampa com gotas, desce colado na lateral, ingredientes explodem com raios de luz. | Abertura e closes |
| `ape-brau-camera-escorrega-no-corpo` | Close na tampa e a câmera escorrega pelo corpo com desfoque bem raso, foco passeando nas gotas. | Closes de detalhe |
| `lucky-f-troca-de-sabor-com-cor-de-fundo` | Cada sabor com a sua cor de fundo; perto dos 14 s, o sabor troca com a lata parada no mesmo lugar. | Trocas de sabor |
| `olipop-explosao-de-ingredientes` | Giro rápido e os ingredientes explodem em volta, depois flutuam em câmera lenta. | Explosão nas trocas |
| `cycle-4-latas-cata-vento` | 4 latas em cruz, tampas no centro, **separadas**, girando como hélice. | Cata-vento |
| `gloria-rastro-em-leque` | Cópias nítidas da lata abrem em leque e formam uma flor. | Rastro |
| `bloom-pop-silhueta-tunel-fileira` | Silhueta contra luz, túnel neon, fileira de sabores em chão espelhado. | Corredor e fileira |
| `kenetik-lata-fatiando` | Estúdio claro, lata se divide em 3 fatias e junta; fruta passa na frente como transição. | Ideia extra (não usada) |
| `grape-soda-abre-em-pedacos` | Lata abre em pedaços mostrando o líquido e as uvas dentro. | Ideia extra (não usada) |
| `coca-quica-e-gira` | Lata quica e gira em estúdio escuro, closes no logo. | Ideia extra (não usada) |

O que se repete em todas: fundo na cor do sabor (sem cenário), lata quase sempre inclinada girando (reta só no final), macros com desfoque raso, um truque com várias latas e final com a fileira ou o logo no preto.

## Mostrar pra pessoa escolher (página de efeitos)
Gere a página e abra **no navegador de dentro do Claude** (o painel de navegador do app), nunca no navegador do sistema. Cada efeito aparece rodando em vídeo, com "Quero / Talvez / Não quero" e um campo de observação:
```bash
python <skill>/scripts/escolher_referencias.py "<projeto>/referencias" [videos de referencia dela...]
```
O painel não abre `file://`, então sirva a pasta pelo próprio `preview_start` (não pelo Bash). Crie ou complete o `.claude/launch.json` da pasta de trabalho com:
```json
{"version": "0.0.1", "configurations": [{"name": "efeitos", "runtimeExecutable": "python",
  "runtimeArgs": ["-m", "http.server", "8765", "--directory", "<projeto>/referencias"], "port": 8765}]}
```
Rode `preview_start` com `name: "efeitos"` e navegue até `http://localhost:8765/escolher-efeitos.html`. Se a porta estiver ocupada, troque nos dois lugares.
- **Ler as escolhas sem a pessoa precisar colar:** quando ela disser que terminou, leia direto da página com a ferramenta de JavaScript do navegador: `localStorage.getItem("escolhas-referencias")` (ou o texto pronto clicando em "Copiar escolhas"). Confirme com ela o resumo do que entendeu.
- Ao terminar, pare o servidor (`preview_stop`).
- Sem o painel de navegador (ex.: terminal puro), aí sim use `--abrir-fora` ou mande a imagem das tiras.
- As referências que ela mandou entram na mesma página, junto com as da skill.
- Ela também pode clicar em **Copiar escolhas** e colar no chat, ou em **Baixar arquivo** (`escolhas-referencias.json`).
- Com as escolhas na mão:
  - "Quero" nas partes do motor mantém a cena.
  - "Não quero" numa parte do motor: explique o que muda. Sem explosão = sabores sem peças. Sem cata-vento, corredor ou fileira = cortar a hélice, o que exige editar `comercial.py` e a linha do tempo, e muda o final.
  - "Quero" num Extra: avise que é cena nova (mais tempo e mais rodadas) antes de prometer.
  - As observações viram ajuste de tempo, cor ou movimento.
- Sem navegador (ou se ela pedir), mande a imagem das tiras:
```bash
cd assets/referencias && ffmpeg -y $(for f in *.jpg; do echo -i "$f"; done) -filter_complex "vstack=inputs=10" catalogo.jpg
```

## Quando a pessoa manda as referências dela
1. Salve em `<projeto>/referencias/`.
2. Pra cada vídeo, gere uma tira de 8 quadros e olhe todas:
   ```bash
   ffmpeg -i ref.mp4 -vf "fps=8/DURACAO,scale=240:-1,tile=8x1" -frames:v 1 tira.jpg
   ```
   Pra um momento específico ("lá pelos 14 s"), extraia um quadro a cada 0,25 s naquele trecho.
3. Escreva pra cada uma, em uma linha, o **movimento** (câmera, lata, transição, tempo). Ignore o conteúdo.
4. Diga em qual parte da estrutura cada movimento entra. Se algum não couber em nenhuma, proponha onde encaixar ou avise que exige construir um plano novo no Blender (mais tempo).
5. Se ela mandar um storyboard, use só a ordem, os tempos e a direção de cada cena. **Nunca o visual** (traço, fonte, papel, setas). O storyboard que a skill gera (`motor/storyboard.py`) já traz no topo a regra "isto é só rascunho de montagem".
