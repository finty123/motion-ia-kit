---
name: prompt-motion-graphics
description: Monta, em português, o PROMPT pronto pra gerar um vídeo de motion graphics feito com código (HTML + canvas + window.seek, trilha e efeitos sonoros em código) pra rodar no chat do Claude ou no Claude Code. Use SEMPRE que o usuário pedir um prompt de motion graphics, prompt de vídeo animado, "prompt pra fazer um vídeo tipo showreel", "prompt de filme de produto", vídeo de interface animada, vídeo de logo animada, vinheta, comercial pra telão, vídeo de lançamento de produto/marca/cliente feito por código, ou colar referência de vídeo pedindo um prompt naquele estilo — mesmo que não diga "skill" nem "motion". A skill entrevista o que falta (produto, site ou materiais, formato, duração, música, história) e entrega o prompt no modelo de tags (entradas, direcao, estrutura, construcao, pegadinhas, comeco). NÃO gera o vídeo nem escreve o código, só o prompt. Não use pra roteiro de Reels falado (roteiro-reels-viral), prompts de Seedance com personagem (nr7-scene-director) nem carrossel.
---

# Prompt de Motion Graphics

Esta skill monta um prompt. Quem vai gerar o vídeo é outra sessão do Claude (normalmente o Claude Code), que recebe esse prompt e escreve o código da animação. Por isso o prompt precisa ser específico o bastante pra que o Claude que recebe não precise adivinhar nada: materiais reais, direção visual, estrutura no tempo da música, regras de construção e o ponto em que ele deve parar e pedir aprovação.

O modelo vem de prompts que funcionam bem em inglês (ver `references/modelo-original-en.md`). A skill reproduz essa mesma estrutura, escrita em português do Brasil.

## Fluxo

### 1. Entrevista (só o que falta)

Antes de perguntar, aproveite o que já está na conversa: se o usuário já disse o cliente, o site, o formato ou mandou imagens, não pergunte de novo. Pergunte o restante numa única rodada, curta, em tópicos numerados. Se a ferramenta de opções clicáveis estiver disponível, use pra perguntas fechadas (formato, música, estilo).

O que precisa estar definido:

1. **Produto ou marca + site.** Nome e URL.
   - **Com site:** o prompt manda o Claude visitar o site e pegar logo, cores, fontes, frase principal e capturas de tela reais (Playwright).
   - **Sem site:** avise o usuário, com clareza, que ele vai precisar anexar na hora de rodar o prompt: logo (PNG ou SVG), cores em hex, nome das fontes, a frase/slogan e as imagens ou capturas que vão aparecer. Sem isso o vídeo sai inventado.
2. **Onde o vídeo vai passar e pra quê.** Lançamento, anúncio, Reels, telão de loja em loop, apresentação pro cliente. Isso muda formato, ritmo e se o final precisa emendar no começo.
3. **Formato.** Padrão 1920x1080 (16:9). Pergunte sempre, porque pode ser 1080x1920 (9:16), 1080x1080 (1:1) ou 1080x1350 (4:5). Se for pra duas versões, a horizontal primeiro e a vertical a partir da mesma linha do tempo.
4. **Duração e ritmo.** Padrão 120 BPM, 8 compassos (16 s). Se pedir mais tempo, converta em compassos (tabela abaixo).
5. **Música.** Padrão: trilha original sintetizada em código, com sons de interface/efeitos sincronizados. Alternativa: o usuário anexa uma trilha livre de direitos perto do BPM, e a grade de batidas sai dela.
6. **A história.** De 8 a 12 estados/momentos, em ordem. Se o usuário não tiver, proponha você uma sequência (ver "Montando a estrutura") e peça aprovação junto com as outras respostas.
7. **Estilo.** Escolha a direção na seção "Direções" a partir do que ele descreveu; confirme só se estiver ambíguo.
8. **Onde o prompt vai rodar: no chat ou no Claude Code?** Isso muda a prévia (veja "Chat ou Claude Code" abaixo). Se a pessoa não disser e não der pra saber pela conversa, pergunte junto com o resto.
9. **Pasta e arquivo.** Nome da pasta nova do projeto (ex.: `gigante-barbearia/`) e o número/nome do arquivo final em `resultados/` (ex.: `resultados/08-gigante-marca.mp4`). Se ele não disser, sugira e siga.

Se faltar só um detalhe pequeno, assuma o padrão, escreva o prompt e diga no fim o que assumiu.

### 2. Escreva o prompt

Entregue o prompt inteiro num único bloco de código, pronto pra copiar, seguindo exatamente o molde abaixo. Tudo em português, exceto nomes técnicos (window.seek, numpy/librosa, H.264 etc.).

### 3. Depois do bloco

Em poucas linhas, fora do bloco:
- o que o usuário precisa anexar ao rodar (logo, fotos, trilha), se houver;
- o que você assumiu por padrão;
- a duração final que a estrutura dá;
- onde colar o prompt (chat ou Claude Code), que tem que bater com o bloco de prévia usado.

## Molde do prompt

```
<entradas>
Produto: [nome] ([url]). Usa como frase do produto [o título principal do site / a frase informada].
Pega o logo real, as cores da marca, as fontes e as capturas de interface do site com Playwright. Escolhe uma cor de destaque da marca.
[SEM SITE: Os materiais estão em anexo: logo, cores (hex), fontes, frase e imagens. Usa só esses materiais reais, nunca redesenha nem inventa.]
[IMAGENS EM ANEXO: lista o que recebeu e onde cada imagem vai antes de animar.]
Música: [sintetiza uma trilha original em código a X BPM / usa a trilha em anexo].
Formato: [1920x1080 (16:9)].
</entradas>

<direcao>
[Bloco da direção escolhida, adaptado ao produto. Termina com a linha "Proibido: ..."]
</direcao>

<estrutura>
[X] BPM, [N] compassos, alguma coisa acontece em toda batida.
[estado 1] → [estado 2] → ... → [estado final que volta ao primeiro]
</estrutura>

<construcao>
1. Um arquivo HTML, um canvas, window.seek(t). Sem transições de CSS, sem timers, sem estado carregado entre quadros. Ruído só com seed (mulberry32), nunca Math.random.
2. Molas de forma fechada. Um valor com vários alvos = a soma de uma mola por mudança.
3. O texto dentro de um contêiner que se transforma entra depois que a transformação começa e sai antes que ela termine.
4. Indicadores de aba: borda da frente e borda de trás em molas diferentes, pra esticar.
5. Grade de batidas tirada da trilha (numpy/librosa), salva em beats.json. Começa num tempo forte. Sons de interface nos picos medidos. Loudness -14 LUFS.
6. Render no Chrome sem janela a 60 fps, 4 subquadros por quadro, misturados pra dar desfoque de movimento. Encode H.264 yuv420p, CRF 16.
</construcao>

<pegadinhas>
Nunca usa will-change em nada que a câmera aproxima (o texto fica borrado).
O último quadro tem que ser igual ao primeiro, incluindo a posição e a velocidade do cursor.
[+ pegadinhas específicas do caso]
</pegadinhas>

<comeco>
Me mostra a lista de estados na grade de batidas, em tabela, antes de escrever código.
Quando eu aprovar, renderiza. Antes do render completo, me mostra uma folha de contato com um quadro por batida e dá nota de 1 a 10 pra: gancho nos 2 primeiros segundos, legibilidade, qualidade do movimento, variedade, fidelidade à marca e sincronia do som. Corrige os 3 piores pontos e repete até tudo ficar 8+.
Salva a folha de contato em resultados/[NN]-[nome]-folha-de-contato.png e me mostra a tabela de notas de cada rodada antes do vídeo final.
Salva o vídeo final em resultados/[NN]-[nome].mp4.
</comeco>

[BLOCO DE PRÉVIA: o do chat ou o do Claude Code, da seção "Chat ou Claude Code"]
Este é um projeto novo: trabalha só dentro de uma pasta nova chamada [pasta]/ e não apaga, não altera nem sobrescreve nada que já existe nas outras pastas nem em resultados/.
```

Ajustes no molde:
- Itens 3 e 4 de `<construcao>` só fazem sentido quando há interface com contêiner e abas. Num vídeo de marca/fotos, troque por regras equivalentes do caso (ex.: "O texto entra depois que a máscara da foto começa a abrir e sai antes que ela feche").
- A segunda pegadinha (último quadro = primeiro) é obrigatória quando o vídeo passa em loop. Se não houver cursor, tire a parte do cursor e mantenha a da posição e velocidade dos elementos.
- Se for gerar duas versões de formato, acrescente em `<comeco>`: "Faz 16:9 primeiro, depois 9:16 a partir da mesma linha do tempo."
- Quando houver dois ou mais vídeos da mesma marca, o primeiro prompt deve mandar salvar `[pasta]/docs/guia-de-estilo.md` (paleta em hex, fontes, transições, ritmo) e os seguintes devem mandar ler e seguir esse guia, na mesma pasta.

## Chat ou Claude Code

O prompt muda no fim conforme o lugar onde ele vai rodar. Troque o marcador `[BLOCO DE PRÉVIA]` do molde por um destes dois blocos, sem misturar.

**Se for rodar no chat do Claude** (inclusive no celular): o HyperFrames não roda no chat. A prévia é feita com quadros do próprio vídeo.

```
Não usa o HyperFrames nem nenhuma skill. Antes do render final, me mostra a prévia em quadros: tira quadros do próprio vídeo (um por estado da estrutura, depois que tudo entrou na tela), me manda as imagens aqui na conversa e espera eu aprovar. Se eu pedir ajuste, corrige e me manda os quadros de novo. Só gera o MP4 final depois do meu ok.
```

**Se for rodar no Claude Code** (no computador): usa o HyperFrames pra montar o vídeo e mostrar a prévia antes do render.

```
Monta o vídeo com o HyperFrames (npx hyperframes; precisa de Node.js 22+ e FFmpeg; se faltar algo, me avisa e me ajuda a instalar). Antes do render, abre a prévia com npx hyperframes preview, me passa o link pra eu ver no navegador e espera eu aprovar. Se eu pedir ajuste, corrige e atualiza a prévia. Só renderiza o MP4 final (npx hyperframes render) depois do meu ok.
```

No Claude Code, ajuste também a `<construcao>`: o item 1 vira "Um projeto HyperFrames, com toda a animação presa ao tempo da composição. Sem transições de CSS soltas, sem timers, sem estado carregado entre quadros. Ruído só com seed (mulberry32), nunca Math.random." e o item 6 vira "Render pelo HyperFrames a 60 fps, H.264 yuv420p." No chat, a `<construcao>` fica como está no molde.

No texto depois do bloco, diga em uma linha onde esse prompt deve ser colado (chat ou Claude Code).

## Direções

Escolha uma e adapte os nomes e as cores ao produto. Sempre feche com uma linha "Proibido:".

**A. Filme de produto com interface (padrão para apps, SaaS, sites).**
Um contêiner que nunca corta: todo estado é o mesmo elemento mudando de tamanho, de raio e de preenchimento, enquanto o conteúdo troca atrás de um desfoque curto. Um cursor conduz cada mudança. Fundo neutro e quente, uma cor de destaque. Molas com, no máximo, um rebote mínimo.
Proibido: easing quicando, brilhos, gradientes na interface, explosão de partículas, tempo morto.

**B. Marca energética / comercial (logo, serviços, telão, negócio local).**
Showreel de motion designer. Tipografia cinética grande, legível à distância. Os fundos alternam entre as cores da marca a cada bloco, e a troca de fundo É a transição (wipes, máscaras, formas que varrem a tela, cortes na batida). Fotos reais entram com máscara e se movem com zoom lento ou parallax. Uma fonte display, uma de apoio.
Proibido: título centralizado em gradiente, tudo surgindo com fade, brilhos genéricos, explosão de partículas, rótulos e molduras nos cantos, tempo morto.

**C. Lançamento editorial / premium.**
Ritmo mais respirado, cortes secos na batida, muito espaço vazio, uma ideia por tela. Texto grande, alinhado à grade, entrando por máscara. Uma cor de destaque usada com economia.
Proibido: excesso de elementos na tela, brilhos, partículas, easing quicando, gradientes.

Se o usuário mandar um vídeo de referência, acrescente em `<entradas>`: baixar com yt-dlp, extrair um quadro a cada 0,5 s com ffmpeg, escrever um guia de estilo a partir dos quadros e usar a gramática da referência — nunca o conteúdo, os logos ou os personagens dela.

## Montando a estrutura

- Cada compasso tem 4 batidas. Duração em segundos = compassos × 4 × 60 ÷ BPM.
- A 120 BPM: 8 compassos = 16 s · 12 = 24 s · 16 = 32 s · 24 = 48 s · 30 = 60 s.
- Cada estado ocupa de 2 a 8 batidas. Distribua de modo que alguma coisa mude em toda batida, mesmo dentro de um estado (um campo é digitado, um número sobe, um cartão é arrastado).
- Abra e feche com o logo. No loop, o último estado leva de volta ao primeiro.
- Com produto de interface, conte uma ação real do usuário do começo ao fim (criar → organizar → concluir → compartilhar), usando telas reais do site.
- Com marca/negócio, siga: logo → promessa/posicionamento → prova real (nota, avaliações, números) → o que oferece → oferta/clube → chamada → logo. Nunca invente números: se não houver prova publicada nem informada, o prompt manda pular essa parte.

Veja `references/exemplo-notion.md` para um prompt completo pronto, como referência de tom e nível de detalhe.
