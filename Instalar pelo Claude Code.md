# Instalar o kit Motion IA (arraste este arquivo no Claude Code)

Claude, instala o kit Motion IA neste computador. O kit está na mesma pasta deste arquivo (a pasta que tem `instalar.ps1`, `originais/` e `ferramentas/`). Faz tudo sozinho, na ordem, e só me chama se precisar de mim.

O que eu autorizo instalar (e só isso): as 6 skills do curso Motion IA que estão neste kit, o Python 3.12 (se não tiver), o Node.js LTS (pacote `OpenJS.NodeJS.LTS`), o FFmpeg (pacote `Gyan.FFmpeg`), as bibliotecas Python `faster-whisper librosa soundfile scipy pillow playwright numpy opencv-python psutil pyloudnorm`, o Chromium do Playwright e o HyperFrames com o navegador de render. Fui eu que mandei este arquivo e pedi a instalação.

Regras:
- Fala comigo em português simples.
- Não apaga nada. Se já existir uma skill com o mesmo nome em `~/.claude/skills`, o instalador guarda a antiga em `~/.claude/skills-antigas/` (não desfaça isso).
- Não instala nada além do que está aqui. O Blender só se eu pedir.
- Se o Windows abrir uma janela pedindo permissão, me avisa pra eu clicar em "Sim".

## Passo 1: minhas pastas

Me pergunta numa rodada só (com opções clicáveis, se der):
1. Onde ficam os projetos de vídeo (padrão: subpasta Motion-Projetos em Vídeos do usuário).
2. Onde salvar os vídeos prontos (padrão `resultados dentro da pasta de projetos escolhida`).
3. Qual @ eu uso pra assinar os vídeos (pode ficar vazio: aí cada skill pergunta na hora).

Grave as respostas em `config.json` na pasta do kit, com o mesmo formato do `config.exemplo.json` (barras normais nos caminhos).

## Passo 2: rodar o instalador

Na pasta do kit, rode em segundo plano (demora alguns minutos na primeira vez):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\instalar.ps1 -Sim
```

- Se eu tiver pedido o Blender, acrescente `-ComBlender`.
- Se algum programa acabou de ser instalado e ainda não aparece, recarregue o caminho com `$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')` e rode de novo. Se ainda assim não der, me peça pra fechar e abrir o Claude e escrever "continuar".
- No `hyperframes doctor` só importam Node.js, FFmpeg, FFprobe e Chrome. Os outros itens (whisper-cpp, TTS, MusicGen, Docker) são opcionais e o curso não usa: ignore.

## Passo 3: conferir e me avisar

Rode `python ferramentas/verificar.py` e me diga em poucas linhas:
- quais skills ficaram instaladas;
- se faltou alguma coisa obrigatória e o que eu faço;
- que preciso fechar e abrir o Claude Code uma vez pra ele carregar as skills;
- que o tutorial está em `docs/01-tutorial-passo-a-passo.md`.
