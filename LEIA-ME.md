# Kit Motion IA

As 6 skills do curso **Motion IA** organizadas num repositório só, com instalador de 1 clique, versões prontas pro chat do Claude.ai e um tutorial passo a passo.

> O kit reúne materiais do curso e ferramentas para Windows. Os seis originais ficam em `originais/`. Consulte os créditos e as condições de uso dos anexos para cada produção.

Para criar um projeto no **Codex ou Claude Code**, siga [Do download ao primeiro vídeo](docs/06-projeto-novo.md).

## Instalar (3 passos)

1. Extraia o ZIP completo em uma pasta onde você possa gravar arquivos. Use **Windows com internet e Claude Code instalado e autenticado** em uma conta com acesso ao recurso. O instalador usa o winget para obter programas ausentes. Você pode escolher sua pasta de projetos ou aceitar a pasta Vídeos do perfil.
2. **Clique duas vezes em `INSTALAR.cmd`.** Ele confere e instala o que faltar (Python, Node.js, FFmpeg, bibliotecas, HyperFrames), pergunta suas pastas e seu @, adapta as skills pro seu PC e copia tudo pra `C:\Users\<você>\.claude\skills\`.
   - Prefere que o Claude faça? Abra o Claude Code nesta pasta e arraste o arquivo **`Instalar pelo Claude Code.md`** na conversa.
   - Vai usar o comercial 3D de lata? Rode `INSTALAR.cmd -ComBlender` (instala o Blender).
3. **Feche e abra o Claude Code** uma vez. Digite `/` e as skills aparecem.

Pra usar no **chat do Claude.ai** (inclusive no celular): use os [pacotes prontos](pacotes-chat/) ou as cópias geradas pelo instalador em `chat/`. Envie o ZIP da skill em Personalizar > Habilidades.

## As 6 skills

| Skill | Faz | Onde roda | Guia |
|---|---|---|---|
| `prompt-motion-graphics` | o prompt perfeito pra qualquer motion por código | chat e Code | [docs/skills/1](docs/skills/1-prompt-motion-graphics.md) |
| `motionia-tuedoido` | vídeo narrado com tipografia 3D e CTA "comenta X" | chat e Code | [docs/skills/2](docs/skills/2-motionia-tuedoido.md) |
| `motion-ia-ayrton-nubank-app-style` | comercial de app estilo Nubank (vidro, 3D, celular) | Code | [docs/skills/3](docs/skills/3-nubank-app-style.md) |
| `motionia-ayrtonsena-ifood-delivery` | comercial de comida/delivery estilo iFood | Code (chat faz a pré-produção) | [docs/skills/4](docs/skills/4-ifood-delivery.md) |
| `motionia-ayrtonsena-comercial-3d-blender` | comercial 3D de lata no Blender | Code + Blender | [docs/skills/5](docs/skills/5-comercial-3d-blender.md) |
| `motionia-ayrtonsena-motion-music` | motion de música, na batida | chat e Code | [docs/skills/6](docs/skills/6-motion-music.md) |

## Documentação

1. [Tutorial passo a passo](docs/01-tutorial-passo-a-passo.md): da instalação ao primeiro vídeo, e o roteiro de uso de cada skill.
2. [Chat ou Claude Code?](docs/02-chat-ou-claude-code.md)
3. [Resumo das 22 aulas](docs/03-resumo-das-aulas.md), [transcrições com minutagem](estudo/transcricoes/) e [registro visual da aula 8.2](estudo/8.2-nota-visual.md).
4. [Problemas comuns](docs/04-problemas-comuns.md)
5. [Sites de referência e bancos gratuitos](docs/05-referencias-e-bancos.md)

## O que tem na pasta

```
motion-ia-kit/
├─ INSTALAR.cmd                  ← clique duas vezes
├─ instalar.ps1                  ← o instalador (opções: -Sim, -SoSkills, -ComBlender)
├─ Instalar pelo Claude Code.md  ← arraste no Claude Code pra ele instalar
├─ config.exemplo.json           ← modelo das suas pastas e do seu @ (o instalador cria o config.json)
├─ originais/                    ← as 6 skills exatamente como vieram do curso (não mexa)
├─ skills/                       ← as 6 skills adaptadas a este PC (geradas pelo instalador)
├─ chat/                         ← zips pra subir no Claude.ai (gerados pelo instalador)
├─ sfx/                          ← 20 efeitos sonoros (Pixabay) + manifest.json
├─ materiais/                    ← arquivos das aulas práticas (mockup, mão com celular, rótulos, músicas, referências)
├─ ferramentas/                  ← adaptar.py, empacotar_chat.py, verificar.py, trazer_aprendizados.py
└─ docs/                         ← tutorial, resumos e guias de cada skill
```

## O que o instalador muda nas skills (e por quê)

O Git guarda os originais e as ferramentas que geram as versões pessoais. As pastas `skills/` e `chat/` são geradas na instalação. Os ajustes locais ficam em `aprendizados/` e as alterações manuais de SKILL.md em `revisoes/`.

As skills originais citam pastas e a assinatura do autor do curso (`C:\Users\Ayrton\...`, `D:\Backup\...`, `@ayrtonsena.stg`) e uma delas foi escrita pro Linux do chat. O `ferramentas/adaptar.py` gera a pasta `skills/` a partir de `originais/` trocando só isso:
- pastas do autor → as suas (do `config.json`); assinatura do autor → a sua (ou a skill pergunta);
- efeitos da pasta pessoal do autor → o pacote `sfx/` do kit, copiado pra dentro das skills Nubank, iFood e lata 3D (`assets/sfx-kit/`), com tabela de equivalência;
- scripts com `/tmp` e `file://` do Linux → funcionam no Windows;
- no fim de cada `SKILL.md` entra a seção "Configuração deste computador".

Mudou de pasta ou de @? Edite o `config.json` e rode `INSTALAR.cmd -SoSkills`.

## Conferir se está tudo certo

```powershell
python ferramentas\verificar.py
```
