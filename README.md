# Motion IA para Windows

Kit para criar vídeos em motion com **Claude Code ou Codex**. Inclui seis skills, instruções para os dois assistentes, materiais de prática, efeitos sonoros, guias por estilo e notas de estudo das 22 aulas.

## Primeiro vídeo

1. Baixe o repositório em **Code → Download ZIP** e extraia tudo. Abra o terminal na pasta que contém `INSTALAR.cmd`.
2. Entre no Codex ou Claude Code com sua própria conta. Execute `.\INSTALAR.cmd -SoFerramentas` para preparar o computador. Tenha internet e permissão para instalar programas. Para modelagem e render 3D de lata, acrescente `-ComBlender`.
3. Crie uma pasta independente para o cliente:

   ```powershell
   python ferramentas/novo_projeto.py "../Video da minha marca"
   ```

4. Abra **Video da minha marca** no assistente, preencha `BRIEFING.md` e coloque logo, telas e referências nas pastas correspondentes. Comece com a skill `prompt-motion-graphics`. Ela produz o briefing e o prompt que orientam a execução.

Para instalar as skills no perfil do Claude Code, execute `INSTALAR.cmd` sem parâmetros. Para usar o chat, baixe o ZIP da skill em [pacotes-chat](pacotes-chat/) e consulte o guia de compatibilidade. Cada pessoa usa as próprias contas de IA e de locução.

| Quero… | Guia |
|---|---|
| Criar um projeto limpo, escolher um estilo e exportar | [Do download ao primeiro vídeo](docs/06-projeto-novo.md) |
| Conhecer as seis skills, os arquivos e as dependências | [Guia do kit](LEIA-ME.md) |
| Acompanhar o tutorial de produção | [Passo a passo](docs/01-tutorial-passo-a-passo.md) |
| Entender o que funciona no chat e localmente | [Modos de uso](docs/02-chat-ou-claude-code.md) |
| Consultar os guias individuais | [Guias das skills](docs/skills/) |
| Resolver um problema | [Solução de problemas](docs/04-problemas-comuns.md) |
| Estudar as aulas | [Resumos e links para as transcrições](docs/03-resumo-das-aulas.md) |

As aulas em vídeo ficam no acervo local do curso. O repositório inclui os tutoriais, resumos, transcrições, arquivos de prática e materiais de terceiros. Consulte os créditos e as condições dos materiais antes de incorporá-los a uma peça comercial.
