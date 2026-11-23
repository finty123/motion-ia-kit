---
name: motionia-ayrtonsena-ifood-delivery
description: "MotionIA @ayrtonsena.stg — iFood Delivery Style. Faz o briefing (referência, estilo, cores/ID, narração, comidas, final), escreve a copy e o roteiro com tabela de cenas e gera o comercial de app de delivery ou de comida no padrão aprovado do ‘Motion iFood – Fome de madrugada’: cores chapadas trocando a cada cena, tipografia gigante e engraçadinha acompanhando a fala, celular 3D, logo letra a letra, app recriado, comidas reais em câmera 3D com preço, sacola, entregador, RAPIDINHO, mapa e @ no final, tudo na batida da música. No Claude Code gera o MP4 em HyperFrames; no chat sem HyperFrames entrega copy, roteiro, texto pro ElevenLabs e prompt de produção. Use SEMPRE que pedirem motion ou comercial de iFood, Rappi, Zé Delivery, app de delivery, restaurante, pizzaria, hamburgueria, açaí, ‘estilo iFood’, ‘igual o Fome de madrugada’ ou mandarem narração e fotos de comida pedindo um motion, mesmo sem citar a skill. Não usar pra fintech/SaaS sem comida (motion-ia-ayrton-nubank-app-style) nem Reels falados dele."
---

# MotionIA @ayrtonsena.stg — iFood Delivery Style

Comercial horizontal (1920×1080, 30 fps, 40–50 s) de app de delivery ou de comida, com a voz da pessoa (reações reais) e o texto da marca na tela. O padrão é o **Motion iFood – Fome de madrugada**, aprovado pelo Ayrton em 28/10/2026. O projeto completo dele está em `assets/modelo/` (13 cenas em HyperFrames) e partir dele é muito mais rápido do que começar do zero.

O estilo, em uma frase: **chapado, colorido e engraçadinho, tudo acontecendo junto e na batida da música**. Antes de criar qualquer coisa, leia `references/regras-do-ayrton.md`. São as correções dele rodada por rodada (o que ele reprovou e por quê), e ignorar isso significa refazer o vídeo.

## Primeiro: em que modo você está

- **Claude Code com HyperFrames** (dá pra rodar `npx hyperframes`): você conduz o briefing, escreve a copy e depois **produz o vídeo inteiro**, até o MP4. Siga o fluxo completo abaixo e, na produção, use a skill `/hyperframes` junto.
- **Chat sem HyperFrames** (claude.ai, app, sem terminal): você conduz o briefing, escreve a copy e entrega o pacote de pré-produção pronto pra gravar e produzir. Leia `references/modo-chat.md`, que tem o formato da entrega.

Em dúvida, pergunte numa linha se a pessoa quer só o roteiro/copy ou o vídeo pronto.

## Fluxo

A pessoa quer ativar a skill e ser guiada. Mesmo que a mensagem seja só "faz um motion estilo iFood", conduza você a conversa: briefing → copy e tabela aprovadas → materiais → produção em blocos → render. Não junte etapas: cada aprovação evita refazer o que vem depois.

### 1. Briefing (a primeira resposta é sempre esta)
Numa mensagem só (detalhes e opções em `references/briefing-e-copy.md`):
- **Perguntas de opção** (ferramenta de perguntas clicáveis, quando houver): objetivo (fã/portfólio, anúncio, lançamento), tom (engraçado, emocional, direto), duração (30 / 45 / 60 s), formato (16:9 / 9:16), narração (voz própria gravada, ElevenLabs, sem voz).
- **Perguntas abertas** curtas: marca e produto, ideia ou situação (a "dor"), referência em vídeo, ID da marca (logo em SVG, cores, fonte), comidas/produtos e fotos, o que mostrar do app, final e @.

Não pergunte o que já foi dito. Se a pessoa não responder algo, assuma o recomendado e avise no fim.

### 2. Referência (se vier)
Extraia um quadro a cada 0,25 s e escreva o guia com números: tipografia, cores, como cada coisa entra e sai, velocidade, easing, câmera. Use `assets/modelo/docs/guia-da-referencia.md` como molde. A referência dá a **gramática e o acabamento**; a história é sempre a da pessoa.

### 3. Copy e roteiro (esperam aprovação)
- A voz é a reação humana ("Vixe Maria, que fome!") e o texto da marca vai na tela. Use a estrutura de 10 batidas (problema → virada → app → produto → pedido → entrega → payoff → marca → assinatura) de `references/briefing-e-copy.md`.
- Entregue: a copy da tela, a fala de cada trecho, o **texto pronto pro ElevenLabs** (se for gerado) e a **tabela de cenas**: momento · tempo · fala · o que aparece · como entra e sai · de onde vem cada asset · som de cada ação. Use o molde de `assets/modelo/docs/tabela-cenas.md` e as receitas de `references/cenas.md`.
- Liste toda ilustração com a fonte dela. Ilustração nunca é feita de retângulo e círculo: ou é foto real recortada, ou SVG desenhado no estilo flat da marca, ou modelo 3D. Se não houver fonte boa, pergunte.
- Pare e espere o "aprovado". Mudar a fala depois de gravada obriga a regravar.

### 4. Materiais
Peça só o que falta:
- **Narração:** é ela que marca o tempo. Se vier um bruto com vários takes, monte com `scripts/remontar_narracao.py`.
- **Logo oficial em SVG:** nunca redesenhe. Separe por letra pra animar (veja "logo letra a letra" em `references/cenas.md`).
- **Fotos das comidas:** confira cada recorte num fundo da cor da marca. Sombra cinza e papel ficam visíveis; limpe com `scripts/limpa_borda.py` e `scripts/so_maior.py`, e foto em fundo liso com `scripts/recortar_fundo_liso.py`.
- **Telas reais do app**, pra recriar em vetor igual.
- **Música:** a da marca, se a pessoa tiver.
- **Efeitos sonoros:** do Ayrton, em `D:\Backup\Videos\#clientes\SFX-20261024T181631Z-1-001\SFX` (veja `references/audio-e-batida.md`).

### 5. Produção (Claude Code + HyperFrames)
1. `npx hyperframes init <pasta> --example blank --non-interactive --resolution landscape`, depois copie `assets/modelo/compositions/` e `assets/modelo/assets/` pra ela e troque marca, cores, textos e fotos. Não mexa fora da pasta do projeto.
2. **Batida primeiro:** marque a trilha com `data-timeline-role="music"`, rode `npx hyperframes beats --json` e depois `python scripts/batida.py beats/<trilha>.json --momento <segundo do logo>`. Use a grade de batidas pra posicionar fala, cortes, trocas de cor, pops e chegadas (`references/audio-e-batida.md`).
3. **Faça o começo no nível final e mostre:** quadros com `npx hyperframes snapshot`, lado a lado com a referência, e a prévia aberta. Só depois do ok faça o resto. Quando a pessoa pedir "faz até o fim", faça tudo e mostre a prévia completa.
4. **Som:** voz mais clara com `scripts/voz_clara.py`, efeitos alinhados pelo golpe de cada arquivo com `scripts/efeitos.py` (o `scripts/gera_index_exemplo.py` mostra um index completo) e a música com `data-automation`: ~0,12 debaixo da fala e ~0,25–0,35 sem fala.
5. `npx hyperframes check` sem erros, snapshot de cada cena e prévia aberta (`npx hyperframes preview --background`). **Não exporte antes da aprovação da prévia completa.**
6. **Render:** `python scripts/render_leve.py "<pasta de saída>\<Nome>.mp4"` (4 workers, prioridade baixa, normaliza pra −14 LUFS e pico −1,5 dBTP). Os trabalhos do Ayrton vão em `D:\Backup\Videos\#clientes\Ayrton Sena\Motions`. Depois confira um mosaico de quadros do MP4.

### 6. Entrega
Diga onde ficou o arquivo, a duração, o volume medido e que o som foi medido, não ouvido.
