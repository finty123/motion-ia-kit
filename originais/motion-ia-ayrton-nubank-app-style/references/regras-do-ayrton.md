# Regras do Ayrton (correções que ele fez no Motion Nubank)

Cada regra veio de uma rodada de ajuste. Seguir isso é o que faz o vídeo ser aprovado de primeira.

## Ritmo e movimento
- **Nada parado quando a câmera mexe.** Em todo pan, zoom ou troca de cena vale princípio de animação: camadas em velocidades diferentes (parallax), o que sai fica pra trás e inclina (arrasto, `skewX`, `rotation`), o que chega vem atrasado e passa um pouco do ponto antes de assentar (`back.out(1.4–1.6)`, mola). Ele reclamou de "paradão" quando tudo andava junto, rígido.
- **Zoom in e zoom out entre as cenas**, como na referência: entrada com zoom out vindo de escala 1,15–1,85 (começa acelerado, `expo.out`), saída mergulhando com zoom in (escala 1,45–1,7 + blur, `power3.in`).
- **Câmera que segue o objeto**: quando algo "corre" (a moeda), a câmera acompanha e a próxima informação já está lá esperando ("Abre o nu"). O DOM anda junto com a câmera 3D (ver cenas.md, "corrida").
- **Fluido e suave**: 60 fps, entradas mais longas (0,5–0,9 s), desfoque de movimento nos movimentos rápidos.

## Abertura
- Começa **grande no quadro 0**, sem entrar do nada. Sem o "vidro canelado / gradezinha": ele não gostou. Fundo roxo, a palavra gigante, e a frase continua no MESMO tamanho com a câmera acompanhando ("Você" → "Você correu").
- Depois **corte seco** pra mão segurando o celular, com zoom out contínuo que começa acelerado.

## Plano da mão (estilo "A business" da referência)
- **Fundo branco** e a palavra grande **atrás da mão** (texto escuro, palavra de destaque em gradiente roxo). Precisa recortar a mão + celular da foto (`npx hyperframes remove-background`).
- A tela da foto costuma vir com texto falso/inglês: troque pela tela do app em português na mesma perspectiva (`scripts/tela_na_foto.py` → `matrix3d`).
- Ícones de vidro flutuando em volta (atrás e na frente da mão), com parallax.
- Daí a câmera vai pra **esquerda**, onde está o celular 3D.

## Layout
- **Celular 3D bem à esquerda** (≈ x 520 px de 1920), frase em cima à direita e notificações empilhadas à direita. Ele achou "muito no meio" quando estava centralizado.
- **Dia / noite / fim de semana**: texto centralizado em cima e celular EM PÉ, de frente, centralizado, cortado na parte de baixo do quadro (o desenho dele).
- **Ícones girando como showreel** em volta de um título ("No automático"): peças menores, numa elipse em pé em volta do título, longe do nome (como "An idea" da referência). Peças sempre de frente pra câmera.

## Marca e final
- 3D **realista** no padrão da marca (moedas metálicas, plástico brilhante, celular de verdade). Nunca ícone chapado onde a referência tem 3D.
- Logo da marca é o arquivo que ele manda (tirar o fundo com `scripts/logo_alpha.py`), nunca redesenhado de memória.
- Final: tela na cor da marca entrando em íris, **logo se desenhando** (máscara de traço) e, uns 1,5 s depois, a logo sai e entra **"by @ayrtonsena.stg"** em branco com glow, **parado até o fim**, sem fade out (uns 3 s). Embaixo, pequeno: "COMERCIAL NÃO OFICIAL" quando a marca não é cliente.

## Áudio
- **Narração começa no 0** (ele estranhou começar sem voz).
- Música de fundo calma, da pasta dele (`D:\Backup\Music\mÚSICAS DE FUNDO\`), com a batida entrando numa palavra forte.
- **SFX só da pasta UI** (`D:\Backup\Videos\Edição de video\SFX\Ui`) e **bastante**: pop-up em notificação, digitação do iPhone, clique em item de lista, clique no toggle, contagem no contador, whoosh digital em toda passagem, brilho no logo. Nada dos efeitos antigos.
- Mix única (narração na frente, música com sidechain), −14 LUFS.

## Entrega
- Prévia no HyperFrames antes de renderizar; render só com "aprovado".
- Render em 1080p60 qualidade `delivery`, salvo na pasta que ele indicar (ex.: `D:\Backup\Videos\#clientes\Ayrton Sena\Motions\Motion <Marca>.mp4`).
