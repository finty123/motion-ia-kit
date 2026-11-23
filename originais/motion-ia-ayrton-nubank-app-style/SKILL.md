---
name: motion-ia-ayrton-nubank-app-style
description: "Motion IA @ayrton.stg — Nubank App Style. Guia o Ayrton do briefing (faz as perguntas) e do roteiro com texto pro ElevenLabs até o MP4: comerciais horizontais estilo SaaS/app (referência Holo + Liquid Glass + 3D realista three.js) em HyperFrames, no padrão aprovado do Motion Nubank: abertura gigante, mão segurando o celular com palavra atrás, câmera 3D seguindo objetos, celular/moedas/caixinha 3D, cards de vidro, ícones girando como showreel, final com logo e 'by @ayrtonsena.stg', música + SFX de UI da pasta dele. Use SEMPRE que o Ayrton pedir 'vídeo estilo SaaS', 'comercial de app', 'motion estilo Nubank', 'igual o do Nubank', 'comercial de fã/não oficial' de marca (banco, fintech, app, SaaS), 'Nubank App Style', ou mandar uma referência tipo comercial de startup/app pedindo pra adaptar pra uma marca, mesmo sem citar a skill. Não usar pra Reels falados dele (edicao-videos-ayrton-reels), motion narrado em fundo escuro com tipografia 3D (motionia-tuedoido) nem clientes com skill própria."
---

# Motion IA @ayrton.stg — Nubank App Style

Comercial horizontal (1920×1080, 60 fps, ~35 s) de app/marca no estilo dos lançamentos de SaaS: fundo claro com respiro, vidro Liquid Glass, 3D realista e câmera sempre em movimento, com narração, música e SFX de UI. O modelo completo aprovado (Motion Nubank) está em `assets/modelo/`; partir dele é muito mais rápido e seguro do que começar do zero.

Antes de construir, leia **`references/regras-do-ayrton.md`**: são as correções que ele fez, rodada por rodada. Elas explicam o que ele aprova (movimento com arrasto e assentamento, abertura grande, celular à esquerda, fundo branco no plano da mão, assinatura no final) e evitam repetir os mesmos ajustes.

## Fluxo

Ele quer só ativar a skill e ser guiado. Mesmo que a mensagem seja só "/motion-ia-ayrton-nubank-app-style" ou "faz um motion estilo Nubank", conduza você a conversa: briefing → roteiro aprovado → materiais → produção. As perguntas, o formato do roteiro e o texto pro ElevenLabs estão em **`references/briefing-e-roteiro.md`**. Leia ao ativar a skill.

### 1. Briefing (a primeira resposta é sempre esta)
Numa mensagem só:
- **Perguntas clicáveis** (ferramenta de opções): objetivo, tom, duração e final.
- **Perguntas abertas** curtas no texto: marca e o que do app mostrar, ideia/gancho, referência, materiais que ele já tem.

Não pergunte o que ele já disse. Se não responder algo, assuma o recomendado e avise no fim.

### 2. Referência (se ele mandar)
Analise antes do roteiro: objetivo, atos com tempos, visual e a tabela com o nome dos efeitos (`references/analise-referencia.md`).

### 3. Roteiro (espera aprovação)
Escreva sempre, com ou sem referência: estrutura de 7 atos, a contagem de palavras batendo com a duração escolhida e uma tabela com fala, o que aparece na tela e a receita de cena (`references/cenas.md`). Entregue também o **texto pronto pro ElevenLabs** num bloco de código e a duração estimada. Nada de produção antes do "aprovado": mudar a fala depois de gravada obriga a regravar.

### 4. Materiais
Com o roteiro aprovado, peça só o que falta:
- Narração gravada ou gerada no ElevenLabs. Obrigatória: é ela que marca o tempo do vídeo.
- Logo da marca em PNG (o fundo sai com `scripts/logo_alpha.py`).
- Foto de mão segurando o celular, se o roteiro usar o plano da mão.
- Telas ou cores da marca.
- Música: se não vier, escolha na pasta dele (`references/audio.md`) e diga qual foi.

O formato é horizontal, a menos que ele peça outro.

### 5. Projeto
```
python scripts/novo_projeto.py C:\Users\Ayrton\Downloads\motion-<marca> --porta 3040
python scripts/transcrever.py <narracao> C:\Users\Ayrton\Downloads\motion-<marca>\words.json --prompt "<marca>, <termos>"
```
`novo_projeto.py` copia o modelo (index, cenas, kit 3D, cues, mix.py) e registra a prévia no `Downloads\.claude\launch.json`. Os scripts Python usam numpy, soundfile, faster-whisper, librosa e pillow; se faltar, crie uma venv no scratchpad (no Windows o Whisper precisa de `device="cpu"` e áudio passado como array).

### 6. Mapa de cenas
Uma cena por frase da narração, com início no tempo da palavra (`words.json`, narração no 0). Use `references/cenas.md` pra escolher a receita de cada frase (abertura, mão, corrida com câmera, lista + toggle + showreel, dia/noite + seletor, odômetro, nuvem de chips, final). Hosts podem se sobrepor alguns décimos pra a transição acontecer; dê `z-index` crescente nos hosts.

### 7. Construir
- Edite as cenas copiadas: textos, tempos, cores, telas do app (`drawHome2`, `drawCaixinha`…), objetos 3D (`references/kit3d.md`).
- Marca diferente do Nubank: troque `--roxo`/`--grad` no `index.html`, o PNG do logo, as cores em `NU` e `plastic()`.
- Foto da mão: recorte com `npx hyperframes remove-background foto.jpg -o assets/mao-recorte.png` e troque a tela da foto com `python scripts/tela_na_foto.py foto.jpg` (cole o `matrix3d` no `#ma-scr`). A medição automática é um ponto de partida: abra a imagem de prova que ele salva e, se o contorno não bater na borda da tela, rode de novo com `--cantos "x,y x,y x,y x,y"` (ordem: sup. esq., sup. dir., inf. dir., inf. esq.). No Nubank os cantos certos eram `570,301 807,301 879,733 502,733`.
- Em toda passagem: parallax, arrasto e assentamento. É a correção que ele mais repetiu.

### 8. Conferir
```
npx hyperframes check --json          (0 erros; avisos de leitura rápida são normais nesse ritmo)
npx hyperframes snapshot --at <16–24 tempos> --json   (abra as folhas e olhe)
```
Na folha, procure texto atrás de objeto sem querer, celular encobrindo a frase, pilha de moedas cortada no rodapé e cena vazia no meio da transição. Corrija e tire nova folha.

### 9. Áudio
Monte/ajuste `cues.json` (SFX da pasta UI em cada ação: pop-up, digitação, clique, whoosh, brilho) e rode:
```
python scripts/mix.py <projeto> --duracao <s> --musica-offset <s> --sobe-musica <fim da fala>
```
O `index.html` usa só `<audio id="mix" src="assets/mix.wav">`.

### 10. Prévia e aprovação
Abra a prévia (`preview_start` com o nome do projeto) e mande o link `http://localhost:<porta>/#project/<pasta>`. Resuma o que tem em cada trecho e o que você assumiu. Renderize só depois do "aprovado".

### 11. Render e entrega
```
npx hyperframes render -o "renders/Motion <Marca>.mp4" -q delivery   (em segundo plano; ~2–3 min pra 35 s)
```
Confira com uma folha (`ffmpeg -vf "fps=1/2,scale=320:-1,tile=6x3"`) e o volume (ebur128 ≈ −14/−15 LUFS). Copie pra pasta que ele indicar (padrão: `D:\Backup\Videos\#clientes\Ayrton Sena\Motions\`).

## Recursos
- `references/briefing-e-roteiro.md`: perguntas do briefing, como escrever o roteiro, tabela de palavras × duração e o texto pro ElevenLabs. Leia ao ativar.
- `references/regras-do-ayrton.md`: o que ele aprova e o que já pediu pra mudar. Leia sempre.
- `references/cenas.md`: receitas de cada cena do modelo, com a técnica de cada uma.
- `references/kit3d.md`: API do kit 3D e pegadinhas.
- `references/audio.md`: música, SFX de UI por ação e mixagem.
- `references/analise-referencia.md`: como analisar referência, estrutura de 7 atos e glossário de efeitos.
- `assets/modelo/`: projeto HyperFrames completo do Motion Nubank (sem mídia com direito autoral: narração, música e foto vêm do projeto novo).
- `scripts/`: `novo_projeto.py`, `transcrever.py`, `tela_na_foto.py`, `logo_alpha.py`, `mix.py`.
