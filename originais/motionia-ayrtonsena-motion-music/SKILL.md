---
name: motionia-ayrtonsena-motion-music
description: >-
  MotionIA @ayrtonsena.stg — Motion Music. Transforma uma MÚSICA (ou trecho) num motion/lyric video todo no ritmo: palavras-chave entrando na sílaba cantada, impacto nas batidas fortes, um cenário por frase, câmera 3D, lente fisheye, motion blur, glow e final com vácuo + assinatura. Primeiro pergunta (chat ou Claude Code, formato, trecho, materiais); SÓ depois da música analisa letra e batida e sugere estilos baseados nela (tipografia 3D, colagem retrô, neon, objetos 3D, glitch, editorial), paletas e fontes. No Code usa prévia e render no HyperFrames; no chat exporta MP4 direto. Use SEMPRE que mandarem uma música pedindo motion, clipe, lyric video, "tudo na batida", "igual o Training Season", "estilo See You Again / Juno", edit de música ou ilustrar a letra em vídeo, mesmo sem citar a skill. Não usar pra Reels falados (edicao-videos-ayrton-reels), narração sem música (motionia-tuedoido) nem comercial narrado.
---

# Motion Music

Faz o vídeo de motion de uma música: a música é o relógio, a letra vira imagem e cada movimento tem motivo no que se ouve. O padrão de qualidade vem do **Training Season** (aprovado na v3, 21/10/2026) e dos dois edits de referência que o Ayrton analisou: **See You Again** (Tyler) e **Juno** (Sabrina). O exemplo completo e aprovado está em `examples/training-season/`.

Leia `references/regras.md` antes de escrever qualquer cena: são as correções reais dele, e seguir isso é o que faz sair bom na primeira versão.

## Visão geral

1. **Primeira rodada de perguntas** (antes da música): onde está rodando, música e trecho, formato, final, materiais.
2. **Raio-x da música**: letra com tempo por palavra, BPM, batidas fortes, respiros, partitura.
3. **Sugestões baseadas na música**: 3 ou 4 estilos diferentes, paleta, fontes e momentos-chave. A pessoa escolhe.
4. **Partitura + roteiro de cenas**: o que acontece em cada batida.
5. **Construção**: `scenes.js` no motor 3D + `kit_musica.js`, folha de contato, autoavaliação.
6. **Prévia e render**: no Code pelo HyperFrames (só renderiza depois do ok); no chat exporta MP4 direto.
7. **Ajustes** e aprendizado salvo na skill.

## 1. Primeira rodada (antes de sugerir qualquer coisa)

Faça tudo numa rodada só. Use a ferramenta de opções clicáveis se existir (no Code é `AskUserQuestion`); no chat, liste as perguntas numeradas. Roteiro completo em `references/perguntas.md`.

Pergunte:
- **Onde está rodando:** Claude Code ou chat? Isso muda o fim do fluxo. No Code a prévia e o render são no HyperFrames. No chat não existe HyperFrames: o vídeo é exportado direto em MP4, sem prévia nem player. Se der pra ver sozinho (pasta `/mnt/user-data` = chat; terminal com Windows/Downloads = Code), diga o que detectou e só confirme.
- **A música:** o arquivo (mp3, m4a, wav ou vídeo) e o **trecho exato** (início e fim, ou a música inteira).
- **Formato:** 16:9, 9:16, 1:1, ou quadrado dentro do vertical (como no See You Again: quadrado no meio e a mesma cena borrada com retícula em cima e embaixo).
- **Final:** padrão aprovado = vácuo (buraco negro sugando a música, com close-up) + assinatura "by @<arroba da pessoa>" pequena, branca, glow, parada. **Pergunte qual é o @ da pessoa** (ou o nome que ela quer assinar) e se ela quer assinatura. Nunca coloque um @ que ela não deu: sem resposta, o vídeo sai sem assinatura. O `by @ayrtonsena.stg` que aparece em `examples/` é a assinatura do autor da skill, só serve de exemplo e nunca vai pro vídeo de outra pessoa.
- **Materiais (opcional, pergunte se quer mandar):** capa do álbum, fotos do artista, logo, PNGs, vídeos, fontes, uma referência de edit. Diga que não é obrigatório: sem material a skill desenha tudo.

**Não sugira estilo, paleta ou cena nesta rodada.** As sugestões têm que nascer da música (clima, BPM, letra), então espere ela chegar. Se a pessoa já mandou a música junto, pule direto pro raio-x e faça só as perguntas que faltarem.

## 2. Raio-x da música (rode, não pergunte)

**Antes, veja se essa música já foi feita:** compare com `examples/` (o Training Season usa `Downloadsideoplayback.m4a`) e com a memória e os projetos anteriores da pessoa. Se já existe, diga qual versão foi aprovada e pergunte se é refazer no mesmo estilo ou uma versão nova; numa versão nova, sugira estilos diferentes do já usado.

`S` = pasta da skill (os scripts ficam em `S/scripts/`). Projeto: no Code, `Downloads/<nome>-motion/`; no chat, `/home/claude/<nome>/`.

```bash
# dependências (uma vez): pip install faster-whisper librosa soundfile scipy pillow playwright && python -m playwright install chromium
#   (no chat: pip install ... --break-system-packages)
python S/scripts/musica.py editar musica.m4a P --offset INI --ate FIM   # recorta o trecho (sem --ate = até o fim) -> P/musica-editada.wav + P/beats.json
python S/scripts/transcrever_letra.py P/musica-editada.wav P/words_raw.json --modelo large-v3
python S/scripts/analisar_musica.py P/musica-editada.wav P --words P/words_raw.json   # -> analise.json + partitura.png
```

Os temporários ficam em `P/_cache/` (regra dele: nada solto na pasta temporária do sistema). Leia `references/ritmo.md` (como ler a análise e casar com a imagem). O essencial:
- **Batidas principais** (vermelho grosso na partitura) são onde vão os impactos grandes. No Training Season elas caíram exatamente onde o Ayrton pediu: HOLD em 9,47 s, RODEO em 13,15 s, OVER em 25,1 s.
- **Respiros** (azul) pedem tensão: vórtice, buraco negro, câmera girando, tela esvaziando.
- **Palavras** saem presas no ataque da voz, em ordem, mas o Whisper erra em música cantada. Quando a palavra forte cai até ~0,8 s de uma batida principal, quem manda é a batida que se ouve.
- **Sílaba segurada** (`segura: true` na análise, com o fim estimado): candidata a letra repetida ou objeto que cresce sem parar.
- **Letra na tela = palavras-chave e trechos curtos** (2 a 4 palavras), nunca a letra inteira.

Abra a `partitura.png` e olhe antes de planejar.

## 3. Sugestões baseadas na música

Monte uma resposta curta com:
1. **O que a música é:** BPM, clima, energia, onde sobe, onde respira, onde estão as batidas principais (com segundos).
2. **A letra em imagens:** as 5 a 8 palavras com mais força visual e o que cada uma pode virar (objeto, ação, cenário). Mesmo raciocínio do Training Season: RODEO = laço e letras pulando, VULNERABLE = vidro estilhaçando, DEEPER = espelho infinito.
3. **3 ou 4 estilos diferentes**, escolhidos pelo clima da música no catálogo `references/estilos.md` (tipografia 3D cinética, mundo da capa com neon, colagem retrô, objetos 3D na batida, glitch digital, editorial P&B). Cada um com:
   - por que combina com ESTA música;
   - paleta em hex (fundo, destaque, apoio, cor do glow);
   - trio de fontes com papel fixo (ver `references/fontes.md`);
   - 2 ou 3 cenas-exemplo amarradas a palavras e segundos reais;
   - transições e lente.
4. Pergunte: qual estilo (pode misturar) e qual paleta, com opções clicáveis. Só repita o convite pros materiais se a pessoa ainda não respondeu sobre eles.

## 4. Partitura e roteiro de cenas

Com o estilo escolhido, monte a tabela (uma linha por frase cantada):

| Tempo | O que se ouve | Na tela | Cena / cenário | Animação | Transição |

Regras de montagem (detalhes em `references/ritmo.md` e `references/regras.md`):
- Uma cena nova por frase cantada (a cada 1,5–2 s, 3 a 4 batidas). Cor ou cenário muda a cada 1 ou 2 cenas.
- A palavra entra na sílaba (`w(i) - 0.07`); a batida principal leva o maior impacto da cena.
- Sílaba esticada vira letra repetida (I-I-I, Foreverrrr, círculo de "ooooh").
- Movimento contínuo: nada cresce ou empurra em degraus a cada batida.
- Mostre a partitura + a tabela. No Code, siga pra construção depois do ok (ou direto, se a pessoa disse pra não parar).

## 5. Construção

O motor é o mesmo da motionia-tuedoido (canvas + 3D próprio, função pura do tempo) mais o `kit_musica.js`. Antes de escrever:
- `references/api-do-motor.md`: W3, L3, text3D, plane, box3, glow, câmera, cues.
- `references/kit-musica.md`: fisheye, retícula, write-on neon, pílulas, texto em círculo, letra repetida, íris, objeto na lente, starburst, chão de grade, chuva de objetos, buraco vermelho, loading, assinatura.
- `examples/training-season/scenes.js`: o clipe aprovado inteiro (copie as cenas: loading, I subindo, buraco vermelho, HOLD com estouro, espelho infinito, rodeio, mira, vidro, chat, contagem, OVER + vácuo, assinatura).
- `examples/demo-kit/scenes.js`: uma vitrine curta de cada efeito novo.

```bash
python S/scripts/build.py --scenes P/scenes.js --words P/words.json --beats P/beats.json --out P/index.html \
  --size 1920x1080 --paleta "principal=#7A0820,destaque=#FFFFFF" [--fonte "Chamberi=D:/.../ChamberiDisplay-Bold.otf"]
python S/scripts/snap.py P/index.html P/folha.jpg 0.5,1.2,...   # 16 a 24 tempos: um por palavra-chave e um em cada batida principal
```

`words.json` = só os marcadores que o `scenes.js` usa (`[[início, fim, "PALAVRA"], ...]`), com os tempos corrigidos pela batida. Abra a folha e dê nota de 1 a 10 em: abertura, legibilidade, texto sobre texto, margem (nada cortado), variedade de cena/cor, 3D real, impacto e glow, sincronia com a partitura. Corrija os 3 piores e repita até tudo ficar com 8 ou mais.

## 6. Prévia, mix e render

**Mix** (nos dois ambientes): só a música + o close-up no buraco negro. Os outros efeitos sonoros ficam desligados, porque o Ayrton aprovou assim (ver `references/audio.md`).

```bash
python S/scripts/mix_musica.py --music P/musica-editada.wav --end END --vacuo INI:FIM --closeup S/assets/sfx/closeup.wav --out P/mix.wav
```

**Claude Code: HyperFrames, sempre com prévia.**
```bash
python S/scripts/hf_wrap.py P/index.html P/hf --audio P/mix.wav
cd P/hf && npx --yes hyperframes@0.9.5 check
npx --yes hyperframes@0.9.5 snapshot --at 1.0,9.5,20.0 --no-end -o snaps     # confere se o canvas desenhou
npx --yes hyperframes@0.9.5 preview --port 3031                                # em segundo plano; abra a URL no navegador dele
```
Mande o link da prévia e **espere o ok antes de renderizar**, mesmo que ele tenha dito "já gera o vídeo" (isso quer dizer não parar nas etapas do meio). Depois do ok:
```bash
npx --yes hyperframes@0.9.5 render --workers 4 -o ../resultados/<nome>.mp4     # prioridade baixa; avise antes, o PC dele trava com render pesado
```
Confira se o MP4 saiu com áudio (`ffprobe`). Se o render do HyperFrames falhar, use o caminho do chat abaixo.

**Chat: exporta o MP4 direto** (sem HyperFrames, sem player, sem prévia).
```bash
python S/scripts/render.py P/index.html P/video_mudo.mp4 > P/render.log 2>&1 &     # em segundo plano (setsid nohup no Linux); retoma por blocos
sh S/scripts/mux.sh P/video_mudo.mp4 P/mix.wav /mnt/user-data/outputs/<nome>.mp4
```
Entregue com `present_files`.

**Formato quadrado dentro do vertical:** construa e renderize em `--size 1080x1080` e componha no fim com `python S/scripts/compor_quadrado.py quadrado.mp4 final.mp4` (a mesma cena borrada, escurecida e com retícula em cima e embaixo, como no See You Again). No Code, a prévia do HyperFrames mostra só o quadrado.

Antes de entregar, gere a folha do MP4 final (`ffmpeg -vf "fps=1/1.3,scale=320:-1,tile=6x4"`) e confira. Na entrega, em poucas linhas: o que tem, duração, o que você assumiu e 1 ou 2 pontos pra ele confirmar. Diga que conferiu por folha de contato se não ouviu o áudio.

## 7. Ajustes e aprendizado

Mexa só no que ele pedir, gere a folha daquele trecho e renderize de novo (o `render.py` retoma: apague só os blocos afetados em `_blocos/`, cada um com 150 quadros = 5 s a 30 fps).

Toda correção nova da pessoa vai **na hora** pra `references/regras.md`, com data e o porquê, e todo script novo vai pra `scripts/`. A skill é o jeito de o próximo vídeo já sair no olho de quem usa.

## Referências

- `references/perguntas.md`: primeira rodada, molde das sugestões e as opções clicáveis.
- `references/estilos.md`: catálogo de estilos (quando usar, paleta, fontes, recursos, transições).
- `references/ritmo.md`: ler a análise, prender palavra na voz, impacto na batida, respiros.
- `references/regras.md`: correções aprovadas (obrigatório).
- `references/fontes.md`: fontes por papel e onde estão.
- `references/kit-musica.md`: API do kit novo.
- `references/api-do-motor.md`: API do motor 3D.
- `references/audio.md`: mix, vácuo, close-up, quando usar SFX.
- `examples/training-season/`: clipe aprovado (cenas, palavras, batidas). A história das versões (o que ele reprovou na v1 e na v2) está em `regras.md`.
- `examples/demo-kit/`: vitrine dos efeitos do `kit_musica.js`.
