# Problemas comuns (e o que fazer)

## Instalação

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| A skill não aparece no `/` do Claude Code | o Claude ainda não recarregou | feche e abra o Claude Code; confira se existe `C:\Users\<você>\.claude\skills\<skill>\SKILL.md` (`python ferramentas/verificar.py`) |
| Aparecem duas `prompt-motion-graphics` | uma versão antiga foi enviada antes no Claude.ai (Configurações > Skills) e outra está no PC | apague a antiga no Claude.ai ou desative uma das duas. A deste kit é a do módulo 1 (funciona em chat e Code) |
| `python`/`node`/`ffmpeg` "não é reconhecido" logo depois de instalar | o terminal aberto não enxerga programa novo | feche e abra o terminal/Claude e rode o `INSTALAR.cmd` de novo |
| O PowerShell bloqueia o `instalar.ps1` | política de execução | use o `INSTALAR.cmd` (ele já roda com `-ExecutionPolicy Bypass`) |
| `hyperframes doctor` diz "Some checks failed" | itens opcionais (whisper-cpp, Kokoro, MusicGen, Docker) | ignore. Só importam Node, FFmpeg, FFprobe e Chrome |
| Erro do Playwright "Executable doesn't exist" | falta o Chromium | `python -m playwright install chromium` |
| A skill 3D diz que falta o Blender | o Blender é opcional no kit | `INSTALAR.cmd -ComBlender` ou instale do blender.org (4.2+) |

## Durante a criação

| Sintoma | O que fazer |
|---|---|
| A prévia do HyperFrames trava ou fica com qualidade baixa | normal: é só prévia. O render final sai liso |
| A prévia não abre no navegador do Claude | o Claude Code precisa estar aberto na **pasta de projetos** (é lá que fica o `.claude\launch.json`). Ou peça o link e abra no seu navegador |
| O texto na tela saiu com palavra errada | o Whisper erra nomes ("caldo" = Claude, "pronto" = prompt). Diga a palavra certa: na tela vale o que foi falado |
| O PC trava no render | renders rodam em prioridade baixa, mas pesam. Evite jogos/edição pesada durante. A skill 3D é a mais pesada (horas) |
| O resultado veio genérico | faltou referência. Mande sempre **duas**: de design (site, Pinterest) e de animação (vídeo, com o trecho), e diga o que tirar de cada uma |
| O Claude gerou de novo tudo do zero a cada ajuste | isso acontece no chat. No Claude Code com HyperFrames ele mexe só na prévia (gasta menos) |
| Arquivos duplicados em Downloads | peça pro Claude **mover** (não copiar) os arquivos pra pasta do projeto. Cuidado com pedidos vagos tipo "limpa a pasta": ele tem permissão pra apagar |
| Ajustei um trecho e o render repetiu o vídeo antigo | os renders retomam por blocos. Peça pro Claude apagar só os blocos do trecho alterado (`_blocos/` ou `rodar.py refazer`) |

## Narração (ElevenLabs)

- **Pelo site** (elevenlabs.io): conta nova ganha créditos grátis. Cole o roteiro, escolha uma voz em português, gere. Ele devolve 2 versões: ouça e escolha.
- **Tags de emoção:** peça pro Claude "adiciona as tags do ElevenLabs nesse roteiro" e cole o texto com tags: a fala fica mais natural.
- **Pelo conector do ElevenLabs no Claude:** se aparecer "Free generations are busy" (`free_shared`), é fila do plano grátis. Tente mais tarde ou gere pelo site e arraste o arquivo pra conversa.
- Áudio gravado no WhatsApp/celular abafado: a skill iFood tem `voz_clara.py` pra clarear.

## Atualizar sem perder o que a skill aprendeu

As skills gravam correções suas nelas mesmas (ex.: `references/regras.md`, `references/erros-e-licoes.md` dentro de `C:\Users\<você>\.claude\skills\...`). Ao reinstalar (`INSTALAR.cmd` ou `INSTALAR.cmd -SoSkills`), o instalador:
1. roda `ferramentas/trazer_aprendizados.py`, que compara cada skill instalada com a impressão digital gravada na instalação (`.kit-manifest.json`) e copia pra `aprendizados/` tudo o que mudou ou é novo;
2. se o próprio `SKILL.md` mudou, ele **não sobrescreve**: salva `revisoes/<skill>/SKILL.md.instalado-<data>` pra você (ou o Claude) revisar e juntar;
3. guarda a versão anterior inteira em `C:\Users\<você>\.claude\skills-antigas\<skill>-<data>` antes de copiar a nova.

As correções locais em `aprendizados/` são reaplicadas nas próximas instalações. Compare as cópias de `revisoes/` antes de incorporar mudanças no texto principal de uma skill. Guarde essas duas pastas ao transferir sua instalação pessoal.
