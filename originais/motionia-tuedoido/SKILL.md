---
name: motionia-tuedoido
description: Gera do zero, ATÉ O MP4 FINAL, vídeos de motion graphics dinâmicos narrados — tipografia cinética em 3D real, câmera 3D sempre em movimento, glow, impactos, desfoque gaussiano, simulações de interface (chat, post, DM) e CTA "comenta X" — no estilo do vídeo "Motion com IA". Use SEMPRE que pedirem vídeo de motion com narração, vídeo de vendas/lançamento animado, textos animados em cima de uma locução, "motion dinâmico", "anima essa narração", "faz o vídeo do meu curso/produto com motion", ou mandarem narração + música + logo pedindo vídeo, mesmo sem dizer "skill". Confere o que foi enviado, pede o que falta (narração, música, paleta, logo, objetivo, CTA), faz um questionário curto, escreve o prompt no molde da prompt-motion-graphics e já constrói e renderiza o vídeo com som mixado. Referência é opcional. Não use pra só escrever prompt (prompt-motion-graphics), notícia com maquete 3D (video-noticia-3d), Reels falado ou carrossel.
compatibility: Precisa de execução de código (bash), ffmpeg, Python com playwright+chromium, faster-whisper, librosa, soundfile, scipy, pillow.
---

# MotionIA_ TuéDoido

Esta skill transforma uma narração em um vídeo de motion graphics no mesmo padrão do vídeo "Motion com IA": cada palavra importante vira tipografia 3D que entra girando com impacto, a câmera nunca para, as cores de fundo trocam a cada ideia, e o som (narração, efeitos cinematográficos e música) é sincronizado palavra por palavra.

O padrão de qualidade veio de várias rodadas de correção com um motion designer. Essas correções estão em `references/regras-de-ouro.md`, e seguir esse arquivo é o que faz o vídeo sair bom de primeira. Leia ele inteiro antes de escrever qualquer cena.

## Visão geral do fluxo

1. **Inventário**: veja o que a pessoa já mandou.
2. **Pedido do que falta + questionário**, numa única rodada.
3. **Análise automática**: transcrição palavra por palavra, corte de respiros, análise da música, logo.
4. **Roteiro de cenas + prompt**: o prompt é entregue no molde da prompt-motion-graphics.
5. **Construção**: `scenes.js`, depois folha de contato, autoavaliação e correção dos 3 piores pontos.
6. **Render completo + mix + entrega**.
7. **Ajustes finos**, só no que a pessoa pedir.

Os passos 5 e 6 são longos. Num ambiente de 1 CPU, um vídeo de 80 s leva cerca de 15 a 25 min de render. Por isso o render roda em segundo plano, em blocos retomáveis. Se a resposta acabar antes do fim, diga isso com honestidade e continue quando a pessoa mandar "continuar". Nunca diga que entregou o que ainda não foi entregue.

## 1. Inventário

Antes de perguntar qualquer coisa, monte para você uma tabela do que veio (mensagem e anexos em `/mnt/user-data/uploads`):

| Item | Obrigatório? | Padrão se faltar |
|---|---|---|
| Narração (áudio) | sim, é o relógio do vídeo | sem padrão: pedir. Se a pessoa só tiver o texto, ver "Sem narração" abaixo |
| Música | não | o vídeo fica só com narração e efeitos (avise) |
| Paleta (hex) | sim | propor uma de 3 cores (escura, destaque vivo, secundária) e confirmar |
| Logo | recomendado | sem logo: o final usa o nome do produto em 3D |
| Objetivo e CTA | sim | perguntar: o que vender, preço, palavra do "comenta X" |
| Formato | sim | 16:9 (1920x1080). Vertical só se pedirem |
| Referência | opcional | não depende dela |

Leia `references/questionario.md`. Ele tem a lista de perguntas e como usar a ferramenta de opções clicáveis.

## 2. Pedir o que falta + questionário

Faça tudo **numa rodada só**:

- Uma lista curta do que falta anexar: narração, música, logo, paleta.
- Até 3 perguntas fechadas na ferramenta de opções: intensidade, final com respiro ou direto, formato.
- No máximo 3 perguntas abertas no texto: CTA e oferta, palavra-gancho, trechos que a pessoa já imagina.

O que a pessoa já disse não se pergunta de novo. Se faltar só detalhe pequeno, assuma o padrão e diga no fim o que assumiu.

**Sem narração:** este estilo depende da voz como relógio. Se a pessoa só tiver roteiro, peça para ela gravar (celular serve, num lugar silencioso). Se ela recusar, use a música como relógio: as palavras do roteiro entram nas batidas, 1 ideia a cada 2 batidas. Avise que o resultado fica menos sincronizado que com voz.

## 3. Análise automática (rode, não pergunte)

Os scripts ficam em `scripts/` (caminho da skill). Crie uma pasta de projeto em `/home/claude/<projeto>/`.

```bash
S=<caminho-da-skill>/scripts; P=/home/claude/<projeto>
pip install faster-whisper librosa soundfile scipy pillow playwright --break-system-packages -q; python3 -m playwright install chromium
python3 $S/transcrever.py narracao.mp3 $P/words_raw.json --modelo small      # tempo por palavra
python3 $S/cortar_respiros.py narracao.mp3 $P/words_raw.json $P --gap 0.15 --keep "IDX:0.9,..."
python3 $S/musica.py analisar musica.mp3                                       # BPM + onde SOBE/CAI
python3 $S/musica.py editar musica.mp3 $P --offset X [--cortar A:B]            # alinhar marcos
python3 $S/preparar_logo.py logo.png $P/logo_alpha.png
```

Cuidados nesta etapa:

- **Transcrição:** confira a lista impressa (índice:palavra@tempo). O Whisper erra nomes, como "caldo" no lugar de Claude ou "pronto" no lugar de prompt. Na tela vale sempre o que a pessoa FALOU de verdade. Se uma frase ficou estranha (ex.: "entende pra onde" quando foi dito "não tem pra onde"), use a forma correta no texto e confirme com a pessoa.
- **Respiros:** cortar os silêncios é o padrão, porque deixa o vídeo dinâmico. Use `--keep` só para pausas intencionais (depois do nome do produto, do preço e antes do CTA), que dão respiro no final. Também use para momentos de efeito como "buraco negro" e tela preta.
- **Música:**
  - Veja os marcos que o script imprime. A batida forte deve entrar na palavra de maior impacto da primeira metade, como o nome do produto.
  - A música deve CAIR no preço.
  - Use `--offset` para adiantar e `--cortar` para remover compassos inteiros (múltiplos de 4 batidas) até os marcos caírem nas palavras certas.
  - Se não der para alinhar tudo, priorize o impacto principal e o preço.

## 4. Roteiro de cenas + prompt

Leia `references/receitas-de-cena.md`, o catálogo de cenas prontas. Ele mostra que tipo de frase vira que tipo de cena.

Monte o mapa de palavra para cena: uma cena por frase da narração, com início em um índice de palavra (`w(i)`). Cada palavra-chave da cena vira um impacto. Regras de composição: a cena muda a cada frase, a cor de fundo muda a cada 1 ou 2 cenas, e as simulações de interface são preferíveis a imagens paradas.

Depois escreva o prompt no molde de `references/molde-prompt.md`. É o mesmo molde da skill prompt-motion-graphics, adaptado a este estilo, com as tags `<entradas>`, `<direcao>`, `<estrutura>`, `<construcao>`, `<pegadinhas>` e `<comeco>`. Entregue o prompt num bloco de código, para a pessoa ter a documentação e poder rodar no Claude Code se quiser.

**Não pare para pedir aprovação do prompt.** Siga direto para a construção, a menos que a pessoa tenha pedido para revisar antes.

## 5. Construção

O motor está pronto em `scripts/engine/` e o `build.py` junta tudo. Você só escreve o `scenes.js` do projeto. Antes de escrever:

- Leia `references/api-do-motor.md` (funções e parâmetros).
- Abra `examples/motion-ia/scenes.js`, o vídeo completo de referência com 25 cenas, e o `examples/motion-ia/README.md`. Copie e adapte as cenas de lá. É mais rápido e mais seguro do que inventar do zero.

```bash
python3 $S/build.py --scenes $P/scenes.js --words $P/words.json --beats $P/beats.json --logo $P/logo_alpha.png --out $P/index.html
python3 $S/snap.py $P/index.html $P/folha.jpg 0.5,1.4,2.6,...   # 16 a 24 tempos: 1 por palavra-chave
```

Abra a folha com `view` e dê notas de 1 a 10 para:

- gancho nos 2 primeiros segundos;
- legibilidade;
- nada de texto sobre texto;
- tudo centralizado;
- texto dentro da margem (nada cortado no topo ou embaixo);
- variedade de cor e câmera;
- 3D real;
- impacto e glow.

Corrija os 3 piores pontos, gere a folha de novo e repita até tudo ficar com 8 ou mais. O `snap.py` também imprime erros de JavaScript e salva `cues.json`.

## 6. Render, mix e entrega

```bash
setsid nohup python3 $S/render.py $P/index.html $P/video_mudo.mp4 > $P/render.log 2>&1 < /dev/null &
python3 $S/mix.py --narr $P/narracao-cortada.wav --music $P/musica-editada.wav --cues $P/cues.json --end <END> --out $P/mix.wav --music-lift <fim_da_fala>:<fim_da_fala+2>
# acompanhe:  sleep 290; tail -1 $P/render.log    (até aparecer PRONTO)
sh $S/mux.sh $P/video_mudo.mp4 $P/mix.wav /mnt/user-data/outputs/<nome>.mp4
```

Rode o render SEMPRE em segundo plano, com `setsid nohup`. Processo comum morre quando a ferramenta termina. Faça o mix enquanto o render roda.

Antes de entregar, gere uma folha do MP4 final (`ffmpeg -vf "fps=1/3.5,scale=320:-1,tile=6x4"`) e confira com `view`. Depois entregue com `present_files`, em poucas linhas:

- o que o vídeo tem;
- duração;
- o que você assumiu;
- 1 ou 2 decisões para a pessoa confirmar.

## 7. Ajustes

Peça o segundo e o que mudar. Mexa só na cena citada, gere a folha daquele trecho e renderize de novo. O render retoma por blocos: apague só os blocos afetados em `_blocos/`, que têm 150 quadros cada, ou seja, 5 s a 30 fps.

## Referências

- `references/regras-de-ouro.md`: TODAS as correções do cliente. É obrigatório ler.
- `references/questionario.md`: perguntas e uso das opções clicáveis.
- `references/receitas-de-cena.md`: catálogo de cenas por tipo de frase.
- `references/api-do-motor.md`: funções do motor 3D e parâmetros.
- `references/audio.md`: efeitos sonoros disponíveis, cues, mix, música.
- `references/molde-prompt.md`: molde do prompt (tags).
- `examples/motion-ia/`: vídeo completo de exemplo (cenas, palavras, batidas).
