# Modo chat (sem HyperFrames)

Sem terminal não dá pra renderizar, mas dá pra fazer toda a parte criativa, que é onde mais se erra. Conduza o mesmo briefing (`briefing-e-copy.md`) e entregue, depois da aprovação da copy, um **pacote de pré-produção** nesta ordem:

1. **Conceito em 2 linhas:** situação, virada e payoff.
2. **Copy final:** fala de cada trecho + texto da tela, na estrutura de 10 batidas.
3. **Texto pro ElevenLabs** num bloco de código (se a voz for gerada), ou um **guia de gravação** (o que falar, com que reação, deixando 1 s de silêncio entre os takes).
4. **Tabela de cenas:** # · tempo · fala · o que aparece · como entra e sai · asset · som. Use as receitas de `cenas.md` pelo nome ("comidas em câmera 3D", "logo letra a letra"…).
5. **Guia visual:** paleta com hex e a ordem das trocas de cor, tipografia (família, peso, tamanho em px a 1080p), o que é foto, o que é SVG flat e o que é 3D, e as regras de `regras-do-ayrton.md` que valem pra esse vídeo.
6. **Lista de materiais** que a pessoa precisa juntar (logo SVG, fotos sem fundo, telas do app, música, narração).
7. **Prompt de produção pronto pro Claude Code**, num bloco de código, pra colar numa sessão com HyperFrames. Ele começa com "Use a skill /motionia-ayrtonsena-ifood-delivery e a /hyperframes" e traz as pastas dos materiais, a tabela de cenas e as regras de som e batida.

Se o chat tiver artifacts, ofereça também uma **prévia animada** de 1–2 cenas-chave (HTML + GSAP numa página) pra aprovar o visual antes da produção. É só uma amostra, não o vídeo final.
