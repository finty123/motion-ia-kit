# Receitas de cena

Cada receita diz que tipo de frase pede aquela cena e onde está o código pronto no exemplo (`examples/motion-ia/scenes.js`, função entre parênteses). Copie a função, troque textos, índices `w(i)` e cores. Uma cena por frase. Alterne fundos (escuro com glow, cor viva, destaque) e nunca use a mesma receita duas vezes seguidas.

## Abertura / gancho

**R1. Palavra alongada com câmera seguindo** (`S1f` + `s1layout`)
- Frase: gancho com palavra enfatizada ("tu é DOOOIDO", "isso é INSAAANO", "olha que ABSUUURDO").
- Como funciona: as primeiras palavras entram girando no alto. A palavra-gancho nasce letra por letra (a letra repetida 8 a 10 vezes), com a câmera correndo atrás da cabeça. No fim, a câmera mergulha no miolo da última letra, que já tem a cor da próxima cena.
- Ajuste `chars` e `times` (distribua as letras repetidas entre o início e o fim da palavra falada).

**R2. Reação / pergunta retórica** (`S2f`)
- Frase: "tá de brincadeira?", "como assim?", "sério isso?".
- Fundo escuro com bokeh. As palavras vêm de direções diferentes (de cima girando em rx, do fundo girando em ry, da câmera). A última palavra slam na cor de destaque com anel.

**R3. Congelar / pera aí** (`S3f`)
- Frase: "não, pera aí", "calma", "volta".
- A cena anterior vira um plano 3D que tomba para trás e escurece, com barra de rebobinar e scanlines. O carimbo "PERA AÍ" slam na frente. Som: tape-stop + glitch.

## Prova / processo

**R4. Software girando + corte de lâmina** (`S4f`)
- Frase: "não abri o [programa] nenhuma vez", "sem usar [ferramenta]".
- A janela chega girando em 3D, o nome do programa slam na frente, uma lâmina de luz corta a janela e as duas metades caem. "NENHUMA" / "VEZ" entram em sequência.

**R5. Três palavras, três cores** (`S4bf`)
- Frase curta de 3 palavras ("esse vídeo aqui", "olha isso agora").
- Cada palavra tem o próprio fundo (destaque → principal → escuro), com wipe diagonal, giro de câmera e impacto. É a cena mais "referência de motion".

**R6. Sucção + nome em 3D letra por letra com reflexo** (`S5f`)
- Frase: revelação principal ("isso aqui é o [NOME]").
- As palavras da frase giram num vórtice e são sugadas, com a câmera rodando e o blur crescendo. Impacto com braam. O nome entra letra por letra girando 90° e depois passa o reflexo de luz (`glint`).

**R7. Editor de código + contagem até zero** (`S6f` + `editorTex`)
- Frase: "não escrevi nenhuma linha de código", "zero esforço".
- O editor entra girando e digitando. Na palavra de negação, as linhas são apagadas, o editor voa para longe e um número grande cai até 0 com ticks acelerando. No 0: impacto grande, anel e glow.

**R8. Objeto 3D + negação + buraco negro** (`S7f`)
- Frase: "não precisei de [coisa cara/grande]".
- O objeto (`box3`) fica bastante tempo girando, com a câmera orbitando. O nome da coisa entra como carimbo, com um X de luz. Um buraco negro suga tudo (rotação + escala), a tela fica preta com som abafado (cue `muffle`) e a cena seguinte volta com flash.

## Poder / possibilidades

**R9. Volta com impacto + frase em linhas centradas** (`S8f`)
- Frase: promessa ("e tu pode pedir o que tu quiser").
- Fundo de cor viva, linhas centradas com `rowX`, palavras alternando a direção de entrada. A palavra principal fica na cor secundária. Tudo sai voando para a câmera junto.

**R10. Objeto 2D que vira 3D, voa e explode** (`S9f`)
- Frase que descreve uma transformação ("esse quadrado vira 3D, sai voando e explode").
- O quadrado entra ANTES da fala. Na palavra "3D" ele ganha profundidade (`box3` com d crescente) e a câmera orbita. Depois sobe girando com linhas de velocidade.

**R11. Explosão em partículas que reconstroem o texto + troca de fontes** (`S10f` + `partSetup`)
- Frase seguinte à explosão.
- Partículas pequenas (4 a 10 px) voam e as MESMAS voltam formando a frase. Na palavra-chave, a fonte troca 7 vezes com clique e volta com impacto.

## Problema / contraste

**R12. Simulação de chat genérico** (`S11f` + `chatTex` + `badTex`)
- Frase: "se tu pedir de um jeito genérico…".
- O chat em 3D digita o pedido genérico e responde com o vídeo ruim proposital, que chega girando. Carimbo "GENÉRICO". A câmera vai de um lado para o outro o tempo todo.

**R13. Simulação pedindo para uma IA específica** (`S12f`)
- Frase: "por que se tu pedir pro [IA] não vai sair?".
- Pergunta no alto, o chat com o nome da IA entra, digita e responde com o mesmo vídeo ruim. Tudo voa para longe e um "?" gigante slam.

**R14. Explicação em sequência de cores** (`S13f` + `swipeBG`)
- Frases explicativas encadeadas.
- Cada frase é um segmento com cor própria (principal, escuro, destaque, escuro, roxo escuro, destaque). Palavra "ruim" em cinza com extrusão escura. Final de efeito ("NÃO TEM PRA ONDE") com impacto.

**R15. Grade 3D multiplicando** (`S14f` + `gridTexs`)
- Frase: "dá o mesmo resultado pra todo mundo".
- Um plano de grade vira e multiplica (1 → 6 → 24 → 96) a cada palavra. "TODO MUNDO" slam na frente.

**R16. Post publicado, visualizações subindo, comentário** (`S15f` + `postTex`)
- Frase: consequência do resultado ruim ("cara de IA", "ninguém vê").
- O celular gira, mostra "Publicando…", as visualizações sobem de 0 a 3 (número 3D grande ao lado) e o comentário da "tia" entra girando.

## Solução / método

**R17. Nível + número** (`S16f`)
- Frase: "pra conseguir isso tu precisa de N coisas".
- "NESSE NÍVEL" na cor de destaque com glow. O número gigante vem da câmera girando 2 voltas, com anel.

**R18. Duas cartas 3D** (`S17f` + `cardTex`)
- Frase que lista 2 itens.
- Duas cartas com espessura giram 180° e se separam para os lados, flutuando com glow.

**R19. Parede de texto como piso** (`S18f` + `wallTex`)
- Frase: "é complexo / é difícil escrever isso".
- Texto real (o próprio prompt) como piso em perspectiva (`rx` negativo), rolando e acelerando. "SUPER COMPLEXO" slam. No fim, o carimbo "DIFÍCIL" e a parede para.

**R20. Contagem regressiva até zero** (`S19f`)
- Frase: "começando do zero".
- Fundo de destaque, número 3D caindo de 9 a 0 com ticks e 0 na cor principal com impacto.

## Oferta / CTA (ritmo mais calmo, respiro)

**R21. Logo 3D** (`S20f` + `logo3`)
- Frase: "no curso / no [produto]".
- A parte 1 do logo entra devagar girando. A parte 2 bate com impacto na palavra. Reflexo de luz depois.

**R22. Preço antigo** (`S21f`)
- O número branco entra discreto e a música deve estar caindo aqui.

**R23. Tag + risco + preço novo** (`S22f`)
- A tag (BLACK, HOJE, ÚLTIMO DIA) entra no topo. Uma linha de luz risca o preço antigo, que cai em 3D. "apenas" entra entre os dois. O preço novo slam na cor de destaque com o maior impacto do vídeo.

**R24. Comenta X + simulação** (`S23f` + `ctaPhoneTex`)
- "COMENTA" e a palavra gigante pulsando nas batidas, depois sobem e viram linha. O celular sobe com comentário → notificação → DM → link → toque. Segure ~4 s depois da fala.

**R25. Logo final** (`S24f`)
- Logo 3D centralizado, reflexo, glow pulsando e fade nos últimos 0,45 s. Duração ~3,5 s.

## Como escolher

1. Liste as frases da narração (pelo words.json cortado) e marque, em cada uma, a palavra-chave.
2. Classifique cada frase: gancho, reação, prova, revelação, poder, problema, explicação, solução, oferta ou CTA.
3. Escolha a receita. Se nenhuma servir, combine peças (W3 + plane + stamp3) seguindo as regras de ouro.
4. Alterne fundo e direção de câmera entre cenas vizinhas.
