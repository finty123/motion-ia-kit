# Resumo das aulas

Notas de estudo das 22 aulas em vídeo, na ordem dos módulos. As [transcrições automáticas das 21 aulas com fala](../estudo/transcricoes/) têm marcações de tempo. Na aula 8.2, os quadros e o texto exibido na tela servem de base para o [registro visual](../estudo/8.2-nota-visual.md).

---

## Boas-vindas

### 1.1 Boas-vindas e como o curso funciona (1 min)
- O curso vai do zero ao motion pronto, com ou sem experiência de edição.
- Ordem: entender o Claude → o que faz um motion ser bom → **primeiro motion do zero, sem skill**.
- As aulas com skills prontas (3D, Nubank etc.) liberam depois de 7 dias, pra você treinar antes o processo sem depender de skill. As skills são "pré-configurações" de estilos que ele já fez do zero do mesmo jeito.

## Módulo 1: instalar

### 1.0 Instalando o Claude e os materiais (2 min)
- Baixe e instale o app do Claude, entre na conta.
- **Claude Code:** na aba Code, arraste o arquivo "Instalar no Claude Code" e mande; o próprio Claude instala a skill de prompt e o HyperFrames (Node.js, FFmpeg, navegador de render), pedindo permissão quando precisa.
- **Só chat (celular):** Configurações → Habilidades/Skills → Adicionar → escolher o zip da skill.
- *No kit:* o `INSTALAR.cmd` faz isso tudo, pras 6 skills de uma vez.

## Módulo 2: como funciona o Claude

### 2.1 O que é cada coisa (4 min)
Analogia do restaurante: **Claude** = chef; **chat** = o chef cozinha na cozinha dele (servidor), seu PC não faz força; **Claude Code** = o chef cozinha na sua casa, com suas pastas e seu PC; **prompt** = o pedido (quanto mais detalhado, melhor o prato); **skill** = a receita da casa, já testada; **referência** = a foto do prato (de design e/ou de animação: mande as duas e diga o que é cada uma); **prévia** = provar antes de servir; **render** = o prato pronto.

### 2.2 Chat ou Claude Code (4 min)
- Chat: funciona em qualquer lugar e não precisa instalar nada, mas você manda os arquivos toda vez e cada ajuste costuma gerar o vídeo de novo (gasta mais).
- Code: lê suas pastas (efeitos, músicas, fila de vídeos), usa o **HyperFrames** pra prévia com linha do tempo (ajusta sem renderizar), gasta menos; mas só no computador e o render pesa.
- Recomendação: Code se tiver computador. Veja [02-chat-ou-claude-code.md](02-chat-ou-claude-code.md).

### 2.3 Plano Pro do Claude (1 min)
- O curso usa o **Opus 5.5**, disponível a partir do **Pro** (o mensal basta, não precisa do Max). Deixe o Opus 5.5 selecionado.

## Módulo 3

### 3.1 O que faz um motion ser bom (3 min)
- Começa antes de abrir o Claude: ideia + referências.
- Duas referências sempre: **design** (fonte, cor, composição; ex.: Pinterest, site da marca) e **animação** (o movimento, com o minuto do efeito). Diga o que tirar de cada uma, senão ele mistura.
- Junte as duas num pedido e use `/prompt-motion-graphics`: ela faz perguntas e devolve um prompt sofisticado.

## Módulo 4: seu primeiro motion

### 4.1 Seu primeiro motion (27 min)
Recria um comercial do Wix ("crie seu site em segundos, literalmente") a partir de um vídeo de referência de outra marca.
1. Cola o site da marca e pede análise do design, da copy e do jeito de se comunicar.
2. Manda o vídeo de referência e diz exatamente o trecho que gostou (a pesquisa digitada → enter → o site surge).
3. Pede um roteiro de 30 s; não gosta, explica a própria ideia e pede reescrita.
4. `/prompt-motion-graphics`: horizontal primeiro (o outro formato só depois de aprovado, pra não gerar dois), trilha feita pelo Claude, rodando no Claude Code.
5. Narração no **ElevenLabs** (conta nova ganha créditos; voz em PT-BR). Pede pro Claude **adicionar as tags do ElevenLabs** ao texto: a fala fica mais natural. Escolhe uma das duas versões geradas.
6. Arrasta o áudio e pede pra **mover** dos Downloads pra pasta do projeto (centralizar, sem duplicar). Alerta: o Claude tem permissão nas pastas; peça coisas específicas pra ele não apagar nada sem querer.
7. Aprova o resumo → o Claude monta no **HyperFrames** → abre a prévia (dá pra pedir pra abrir dentro do Claude). A prévia trava e tem qualidade menor: normal.
8. **Ajustes por tempo**: abertura sem tela branca (o chat já centralizado digitando), botão com glow igual à referência, efeito de brilhos pixelados formando o site, site com pessoa e profundidade pra fazer parallax (o Claude propôs 6 opções pra escolher), mockup de MacBook (anexo da aula), mascote em 3D com princípios da animação, showreel de sites em anel 3D em volta do "300 milhões", assinatura no final.
9. Segunda rodada: parallax mais suave e pros dois lados, perspectiva do notebook, fundo mais escuro, **speed ramp** (rápido → devagar), sites desfocados passando atrás. Print de tela com Win+Shift+S pra mostrar.
10. Aprovado → render.
- Lição: o tempo vai quase todo em **pedir bem os ajustes**. Termo técnico ajuda; sem saber o nome, mande um vídeo do efeito.

### 4.3 Transformando o seu motion em skill (2 min)
- Depois de chegar num estilo bom, peça: "cria uma skill usando o /skill-creator (instala se não tiver) com esse estilo de motion, com as mesmas etapas e as perguntas do início".
- Da próxima vez é só ativar a skill: sai mais rápido e com menos ajustes. É o caminho pra criar os seus próprios estilos.

## Módulo 5: Motion "Tu é Doido"

### 5.1 Como vai funcionar (1 min)
- Recriar um vídeo narrado viral sem abrir o After Effects, usando outro vídeo como base de **ritmo e edição**. O conteúdo de cada cena vem de você (sua narração, sua personalidade). Não é copiar.

### 5.2 Análise e estratégia (9 min)
- Analisa **por que** a referência funciona: gancho de curiosidade logo no início, um segundo gancho que aumenta a curiosidade, quebras de objeção ("não é um MCP controlando o After"), construção até revelar o produto e provas na própria tela (pede algo e mostra acontecendo).
- Pra não virar cópia: troca cores, roteiro e o que apresenta, e põe a **personalidade** (bordões próprios). O que é único em você não dá pra copiar.
- Roteiro dele: gancho ("tu é doido") → 2º gancho (não abri o After) → isso é o Claude → quebra de objeções (sem código, sem PC da NASA) → provas (o quadrado vira 3D, voa e explode) → pedido genérico gera vídeo genérico → solução (prompt + referência é difícil; o curso ensina) → preço → CTA **"comenta MOTION que eu te mando o link no direct"** (mais fácil de entregar o link).

### 5.3 Recriando na prática (28 min)
Feito no **chat**.
1. Envia narração, música e vídeo de referência e **diz o que é cada arquivo** (evita confusão, principalmente com nomes estranhos).
2. Descreve frase por frase o que quer ver (ex.: muitos "O" em "doido", a câmera entra no último O; tela do After Effects cortada; "Claude" em 3D sugando com impacto; PC gamer 3D no espaço; quadrado 2D que vira 3D com partículas de velocidade; pedido genérico → vídeo ruim → comentário da tia "que lindo, meu filho"; preço riscado e novo em 3D; simulação de alguém comentando MOTION e recebendo o link na DM).
3. Escolhe uma **paleta** num site de paletas (preto, violeta e limão) e anexa. Anexa o logo e pede em 3D.
4. Som: **sem efeito infantil**, muitos efeitos cinematográficos (hit, whoosh, clique, glow). Prioridade: **narração > efeitos > música** (música baixa). Palavras sincronizadas com a fala.
5. Usa a skill de prompt pra transformar tudo num prompt técnico. Pensa no **objetivo** (anúncio pra vender o curso → chamativo, pra viralizar) e no **estilo da marca** (a Apple nunca faria assim).
6. No chat, quando bate o limite, clique em **Continuar**. Gerar o vídeo leva 20–30 min.
7. Primeiros quadros com "cara de IA": pede **tudo centralizado**, nada de texto na frente de texto, abusar da **câmera 3D**.
8. Ajustes finais **todos numa mensagem só** (economiza uso e tempo): gancho mais caprichado (é o que segura a pessoa), roxo mais escuro pro glow aparecer, Gaussian blur na hora certa, letras 3D com reflexo, número caindo até zero com impacto, buraco negro sugando tudo com voz distorcida, **cortar os respiros**, o objeto entra um pouco **antes** da palavra, partículas menores, "quiser" trocando de fonte 7 vezes com clique, contador de visualizações subindo, impacto nas palavras.
- Dessas correções nasceu a skill `motionia-tuedoido` (as regras estão em `references/regras-de-ouro.md` dela).

## Módulo 6: motion pra cliente real (telão)

### Como vai funcionar (2 min)
- Vídeo real de um cliente, em duas partes: (1) clube, serviço e preço; (2) como contratar pelo QR Code, com um efeito vindo de uma referência.
- A parte 1 é feita **sem referência**, só com o site do cliente; a parte 2 **com vídeo de referência**.
- Vai passar num **telão**: animações mais lentas e suaves. Em rede social seria tudo mais rápido. O ritmo sempre depende de onde o vídeo vai passar, e isso entra no pedido.

### Aula 1: Fazendo o motion, sem referência (24 min)
Cliente real: uma barbearia com clube de assinatura. Tudo no **chat**, com a skill de prompt.
1. Diz à skill (digitando ou falando no microfone): vídeo horizontal pra um cliente de barbearia; objetivo é mostrar os serviços e vender o **clube**; o site do cliente tem paleta, fontes, serviços, preços e nota do Google, então **"tire todas as informações do site"**; começar animando o logo (anexado, tirado do site); verde como cor principal, alternando com branco e preto.
2. Respostas da entrevista: horizontal primeiro, ~60 s, motion graphics mostrando os benefícios do plano, CTA pra assinar, vai passar **num telão da barbearia, em loop**, trilha sintetizada com cara de barbearia + efeitos.
3. Regra de ouro: **o que você imagina, você precisa dizer**; o que não disser, ele inventa (e fica com "cara de IA").
4. A skill devolve o prompt (entradas, cores, serviços, proibições...). Revise se quiser e cole numa **conversa nova**, junto com os anexos.
5. O Claude primeiro mostra a grade de batidas e **quadros das cenas, antes de animar**. Ajustar nessa fase é bem mais barato que depois do vídeo.
6. Ajustes pedidos: tirar a "cara de IA"; cortes na batida, mas **suaves** (é telão); dias da semana se preenchendo (menos domingo, fechado); **tudo centralizado**; frase gigante com impacto; meses do ano passando; serviços passando de forma dinâmica; primeira tela com fundo verde; nota do Google como se alguém estivesse dando 5 estrelas.
7. Depois do vídeo: troca a abertura, estrelas todas de uma vez, **tira o número de serviços** (um número abaixo de ~50 passa a sensação de pouco), um serviço por tela trocando a cor de fundo, fundo da frase final na cor da letra.
8. **Vertical só no fim:** pedir a versão vertical depois de tudo aprovado saiu barato, porque ele reaproveita a horizontal.
- Telão = mais lento e mais longo, porque fica repetindo. Pra rede social seria 30–40 s e bem mais rápido.

### Aula 2: Motion com referência (13 min)
Segunda parte do vídeo da barbearia: como agendar pelo QR Code.
1. Referência de animação tirada do **whatships.com** (vídeos feitos com Claude). O pulo do gato: usar a referência pra **criar algo novo**, não "faz igual".
2. Pedido numa conversa nova: link do vídeo de referência (visual), "pegue fontes e cores do site [site do cliente]" (ou uma foto/paleta), telão, 60 s, objetivo = mostrar como agendar. Anexa **prints de cada tela do agendamento** e descreve o fluxo: o celular lê o QR Code → tela inicial → Agendar → escolhe a filial → escolhe o barbeiro → serviço (corte R$ 40) → data e hora → cartão de confirmação com cliente, barbeiro, data, hora e serviço.
3. Detalhe de cliente real: no telão, barbeiros com **ícones e nomes genéricos**, pra não promover um barbeiro específico. O item clicado fica verde.
4. Trilha estilo trap + efeitos. Opus 5.5 selecionado.
5. A skill gera o prompt → conversa nova com o prompt + prints. Ele manda o relatório e os quadros; pediu horizontal (em vez de vertical), mandou o logo que tinha esquecido, tirou o gancho de "agendado em 2 s" (no telão não precisa de gancho) e corrigiu um detalhe visual.
6. Depois do vídeo: animação de **entrada e de saída** dos elementos (QR Code, textos) no começo e no fim, e o celular lendo o QR Code na abertura.
- Fechamento: dá pra fazer tudo isso até pelo celular, sem abrir outro programa. Seguindo as etapas (estilo, referência, detalhes), dá pra fazer qualquer outro tipo de vídeo.

## Módulo 7 — Comercial de aplicativo no estilo Nubank

### Aula prática Nubank + Materiais (11 min)

O exercício usa a linguagem visual de uma campanha do Nubank para apresentar o Banco Inter. O briefing começa pela função que o comercial vai vender e pelas telas que o espectador precisa reconhecer. O instrutor pede cerca de 35 segundos e reúne imagens da marca, do aplicativo e do porquinho usado como personagem.

A primeira entrega é o roteiro. Leia a fala imaginando o que estará na tela em cada frase. Nesse ponto ainda dá para trocar o gancho, cortar uma função ou dar mais tempo a uma ação. O instrutor gera a voz no ElevenLabs e envia o áudio, a marca e as imagens ao Claude Code. A gravação da voz passa a determinar o tempo das cenas.

Na prévia, confira a legibilidade da interface e se os movimentos acompanham o que é dito. A mão com o celular e os efeitos sonoros estão entre os materiais do exercício. Depois da aprovação, indique a pasta em que o vídeo final deve ser salvo. [Guia da skill de aplicativo](skills/3-nubank-app-style.md).

## Módulo 8 — Motion 3D Monster

### 8.1 Como vai funcionar (prévia narrada)

Assista primeiro ao comercial inteiro para entender sua estrutura. A abertura apresenta a lata. A voz passa pelos ingredientes do rótulo e associa cada um a uma situação, enquanto palavras curtas mudam na tela. O fechamento retoma a marca. Para estudar a montagem, marque os instantes em que a locução introduz um novo ingrediente e observe o que muda na imagem.

### 8.2 Motion 3D pelo Claude (33,5 s, sem áudio)

O arquivo reúne uma prévia do comercial e um aviso de que a prática ainda estava em finalização quando a gravação foi feita. Dá para observar a rotação da lata, os destaques em verde, o cronômetro e a referência a videogame. A gravação termina sem mostrar os comandos ou a montagem da cena. [Ver quadros da aula](../estudo/8.2-nota-visual.md).

## Módulo 9 — Comercial 3D de lata

### 9.1 Como vai funcionar (introdução)

O instrutor apresenta dois resultados produzidos com o mesmo processo. Observe o que identifica cada marca, como rótulo, cor e apresentação da lata. A aula seguinte usa Guaraná Antarctica para demonstrar como adaptar a peça a outro produto.

### 9.2 Comercial 3D de lata (27 min)

O instrutor instala o Blender e usa o Claude Code para conduzir a modelagem. Reúne referências e consulta o site do Guaraná Antarctica para identificar as cores, a fonte e o jeito como a marca fala. As artes das versões Original e Zero, o logotipo e a faixa de música estão em `materiais/9-lata-3d-guarana/`. Leve ao briefing tanto as imagens que identificam o produto quanto exemplos do tipo de enquadramento desejado.

Aos 9 min, ele escolhe um acento da música para servir de gancho visual. Aos 12 min, mostra como gerar o rótulo planificado a partir de uma foto da lata. Aos 13–16 min, corrige o storyboard porque o Claude trouxe um olho de outra referência para uma lata que não tem esse elemento. Ele escolhe só os efeitos que pertencem à nova campanha.

Na prévia colorida, pede gelo, fumaça e copo mais realistas. Uma correção bem específica aparece perto de 22min30s. Quando a fruta avança em direção à câmera, a lata já deve estar visível ao fundo. Só depois dessas revisões ele confere o vídeo exportado. [Guia da skill Blender](skills/5-comercial-3d-blender.md).

## Módulo 10 — Motion de comida e delivery

### 10.1 Como vai funcionar (prévia Burger King)

O exemplo abre com o preparo do hambúrguer no fogo, passa pela personalização do pedido e termina no aplicativo, com cupom e retirada. A locução liga o atributo do produto à ação de compra. Depois do anúncio há uma chamada do próprio instrutor para o curso. Ao planejar um vídeo de cliente, identifique onde termina a mensagem da marca.

### 10.2 Motion Burger King pelo Claude (18 min)

O instrutor adapta o estilo do comercial de delivery ao Burger King. Busca referências da marca, consulta o site e reúne logo, fotos e exemplos do visual pretendido. O briefing descreve produto, linguagem e canal. Aos 6min30s, ele devolve a primeira versão do texto porque o tom soa genérico para a marca. Usa fotos oficiais dos lanches, confere os recortes, reúne fontes e embalagem, gera a locução no ElevenLabs e concentra os arquivos na pasta do projeto.

Depois de aprovar o teste da abertura com fogo, pede a peça inteira. Aos 14 min, volta à referência para mostrar que o hambúrguer precisa aparecer logo no primeiro plano. Na revisão seguinte, pede uma transição lateral no lugar da diagonal aos 15 segundos do anúncio e um mockup de iPhone visível aos 17 segundos. Só então manda exportar. O arquivo de logo usado no exercício fica em `materiais/10-ifood-burger-king/`. [Guia da skill de delivery](skills/4-ifood-delivery.md).

## Bônus: motion musical

### 11.2 Motion na batida da música (6 min)
- Skill `motionia-ayrtonsena-motion-music`, no Claude Code (no chat funciona igual, sem a prévia).
- É só chamar a skill e arrastar a música: ela lê a música inteira, transcreve a letra, entende o tema e as batidas e monta um **lyric video** na batida, com elementos que combinam com a letra.
- Perguntas: trecho (ou a música inteira), formato (horizontal na aula), final/assinatura com o seu @, se quer usar cenas do clipe ou deixar ela desenhar tudo, estilo (tipografia cinética etc.), paleta e intensidade.
- A prévia abre no navegador (ou dentro do Claude). Gostou: "pode renderizar".
- Dá pra fazer no modo simples (só responder as perguntas) ou mandar mais coisas: fotos, elementos, o próprio clipe.
