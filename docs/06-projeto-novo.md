# Do download ao primeiro vídeo no Windows

## Preparar o computador

1. No GitHub, abra **Code → Download ZIP** e extraia a pasta completa. Se usar Git, clone o repositório. Abra o terminal na pasta que contém `INSTALAR.cmd`.
2. Abra o Codex ou o Claude Code e entre na sua própria conta. Para instalar as dependências de produção sem instalar skills no perfil do Claude, rode `.\INSTALAR.cmd -SoFerramentas`. O instalador utiliza o winget, instala as bibliotecas Python e prepara o navegador de renderização. Tenha internet na primeira instalação. Para comercial 3D de lata, acrescente `-ComBlender`.
3. Quem prefere instalar as seis skills no perfil do Claude Code pode executar `INSTALAR.cmd` com duplo clique. Os ZIPs para uso no chat são gerados em `chat/`. Para gerá-los separadamente, execute `python ferramentas/empacotar_chat.py`.

## Abrir uma produção limpa

Escolha uma pasta que ainda não exista. Este comando cria um projeto ao lado do kit:

```powershell
python ferramentas/novo_projeto.py "../Filme da minha marca"
```

Abra **Filme da minha marca** em uma nova sessão do assistente. O projeto terá as seis skills em `.agents/skills/` para Codex e em `.claude/skills/` para Claude Code. As instruções estão em `AGENTS.md` e `CLAUDE.md`. Os scripts são preparados com o caminho escolhido, então crie o projeto no local onde pretende trabalhar.

| Pasta | Conteúdo |
|---|---|
| 01-marca | Logotipo oficial, paleta, fontes e manual da marca |
| 02-produto | Site, fatos verificáveis, fotos, telas e gravações reais |
| 03-referencias | Referências com o trecho e o detalhe visual ou sonoro a aproveitar |
| 04-producao | Roteiro, locução, cenas, efeitos, trilha e prévias |
| 05-exportacoes | Vídeo final conferido |

## Iniciar pelo briefing

Preencha `BRIEFING.md` com uma ação principal, a audiência e a plataforma. Em Codex CLI ou IDE, mencione `$prompt-motion-graphics`. Em Claude Code, use `/prompt-motion-graphics`. Também é possível indicar diretamente o arquivo `SKILL.md` da skill dentro do projeto.

> Leia meu briefing e os materiais da marca. Quero que [público] entenda [mensagem] e faça [ação]. Proponha duas aberturas e monte um roteiro com tempo, imagem, fala e som. Mostre três quadros e os primeiros cinco segundos animados para eu aprovar.

A skill de briefing entrega o prompt. Para produzir o vídeo, peça ao assistente que execute o prompt com a skill apropriada. Consulte a [tabela de estilos e ferramentas](../LEIA-ME.md).

## Revisar para exportar

Ouça o nome da marca na locução. Veja a prévia no tamanho de um celular e confira se a ação que aparece na tela coincide com a fala. Ao pedir ajustes, indique o segundo e o elemento. Para o som, especifique o evento que merece destaque, como o clique em um botão, a entrada de uma oferta ou a confirmação de leitura de um QR.

Faça uma última reprodução do MP4 exportado. Confira resolução, orientação, sincronização, legibilidade, duração da chamada final e leitura do QR quando houver. Para usar um serviço externo de voz, cada pessoa precisa conectar a própria conta ou fornecer a gravação autorizada.
