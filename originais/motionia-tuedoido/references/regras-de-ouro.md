# Regras de ouro

Estas regras vieram de rodadas reais de correção com um motion designer exigente. Cada uma resolve uma reclamação que já aconteceu. Siga todas: elas são o motivo do vídeo sair bom sem precisar de várias versões.

## 1. Gancho (primeiros 3 s): é a parte mais importante

- **Abertura limpa.** A atenção fica 100% na frase de abertura. Nada de enfeites que disputam o olhar: sem olhos, figuras ou ícones espalhados. O fundo pode ter só linhas de velocidade bem discretas e um glow suave.
- **Palavra-gancho com ênfase.** Se a pessoa alonga a palavra na fala ("tu é dooooido"), a tela também alonga: letras repetidas (D-O-O-O-O-O-O-I-D-O) nascendo uma a uma no ritmo da fala, com a câmera correndo atrás da cabeça da palavra até a última letra.
- **Cada letra entra em 3D.** Ela gira, tem extrusão, flash de glow e som (tick ou whoosh).
- **Transição de saída:** a câmera MERGULHA dentro de uma letra com miolo (O, A, D). O miolo tem a cor do fundo da próxima cena e vira a tela.
- **Dinamismo.** O gancho tem que ser o trecho mais dinâmico do vídeo. Gaste mais esforço nele.

## 2. Composição

- **Tudo centralizado.** Nunca alinhe à esquerda. Linhas de várias palavras são linhas centradas. Duas colunas só se forem simétricas (ex.: PEDIDO = RESULTADO).
- **Nenhum texto na frente de outro texto.** Um elemento sai (voando para a câmera, com `out`) antes do próximo ocupar o mesmo lugar. Vale também para tag e preço, título e card, e "COISAS" embaixo do "2".
- **Margem de segurança.** A câmera gira e dá zoom, então nada importante fica a menos de ~140 px do topo ou da base. Linhas de apoio ficam em y entre -400 e +400 (coordenadas do mundo, centro = 0). Se cortar na folha de contato, suba ou desça.
- **Tamanho mínimo.** Texto de apoio pequeno tem pelo menos 46 px. Palavra-chave fica entre 150 e 340 px. Número de impacto fica entre 440 e 640 px.

## 3. 3D de verdade, nunca 2D esticado

- **Texto.** Tudo que é texto importante é `W3`/`text3D`: extrusão real em camadas, perspectiva e giro na entrada.
- **Planos 3D com perspectiva.** Janelas, cards, celulares, editor de código, chat e grade de vídeos são `plane()`. Eles chegam girando (ry de 1,3 a 3,6 rad) e vindo do fundo (z de 1500 a 3200).
- **Proibido** usar skew/escala 2D para "fingir" 3D, e proibido texto que só aparece com fade in ou fade out.

## 4. Câmera 3D sempre em movimento

- **Câmera própria por cena.** Cada cena tem seu `setCam3` com órbita (`ry` ±0,3 a 0,5), dolly (`z`), leve `rx` e `rz`.
- **Muda de ângulo a cada frase ou palavra-chave.** Use molas ou senos de frequências diferentes. Uma câmera parada por mais de 0,5 s é erro.
- **Ritmo.** Nas partes de ação: movimentos maiores e mais rápidos. Na parte do curso, do logo e do preço: movimentos menores e mais lentos (respiro), mas nunca parados.
- **Impactos.** O motor já aplica tremor e soco de zoom em toda cue com `sh`.

## 5. Cor, glow, blur

- **Fundo troca de cor com frequência,** a cada 1 ou 2 cenas: escuro, cor viva e cor de destaque. Use `swipeBG` (wipe diagonal) ou corte seco na palavra.
- **Fundo escuro para o glow aparecer.** Prefira um tom escuro da cor da marca, como o roxo escuro `DV`, ao preto puro sempre que houver glow. Quando a pessoa pede "roxo", ele fica mais escuro para dar contraste.
- **Glow** na palavra-chave de cada cena, com flash forte no impacto (`flash`) e brilho base baixo (`glow` de 0,1 a 0,5). Não coloque glow em todas as palavras.
- **Desfoque gaussiano.**
  - Já entra sozinho em toda troca de cena (`blurcue`).
  - Use bokeh desfocado (`bokeh()`) ao fundo nas cenas escuras.
  - Use `bl` nas cues de transições grandes.
- **Motion blur real.** O render usa 2 subquadros por quadro.

## 6. Impacto em letra

- **Palavra-chave = impacto completo:** entrada com mola, flash de glow, anel (`ring`), cue com tremor (`sh`), aberração (`ch`) e efeito sonoro de impacto.
- **Palavras de apoio** recebem só tick ou whoosh, sem tremor.
- **O impacto acontece NA sílaba falada.** Comece a animação ~0,07 s antes da palavra (`w(i) - 0.07`), porque a mola leva esse tempo para "bater".

## 7. Sincronia

- **Tudo vem dos índices das palavras** (`w(i)`). Nunca use segundos soltos digitados à mão.
- **Elemento citado com dêitico entra ANTES da fala.** Se a pessoa fala "esse quadrado aqui", o quadrado já está na tela ~0,3 s antes. Vale para "esse", "isso aqui" e "olha esse".
- **Contagem.** Quando a fala diz "nenhuma / zero / do zero", o número CAI até 0 (ex.: 1.284 → 0 ou 9 → 0) com ticks acelerando, e o 0 chega com impacto grande na palavra exata.

## 8. Simulações no lugar de imagens paradas

- **Nada de miniatura do próprio vídeo** nem screenshot parado. Troque por uma animação com cor ou por uma simulação.
- **Simulações prontas no kit:**
  - **Chat de IA:** o texto é digitado, enviado, aparecem os 3 pontinhos e chega a resposta.
  - **Post publicado:** barra "Publicando…", visualizações subindo de 0 a N e comentário entrando.
  - **CTA:** a pessoa comenta a palavra, chega a notificação "Dá uma olhada no seu direct", abre a DM, aparece o card do link e o dedo toca.
- **Interfaces genéricas.** Nunca use logos oficiais de terceiros (Instagram, Adobe, Anthropic, NASA…). O nome de um produto pode aparecer como texto.

## 9. Efeitos especiais que funcionaram

- **Explosão → reconstrução.** As partículas são PEQUENAS (4 a 10 px) e as MESMAS da explosão voltam e formam o texto seguinte, por amostragem do texto. Só no fim viram texto sólido.
- **Troca de fontes.** Numa palavra-chave ("QUISER", "QUALQUER", "TUDO") a fonte troca 7 vezes, ~0,115 s cada, com clique de seleção em cada troca, e volta à fonte principal com impacto.
- **Buraco negro.** Quando a fala nega algo grande ("não precisei de computador da NASA"), o objeto fica bastante tempo na tela e depois um buraco negro suga tudo.
  - A tela fica preta com som abafado "embaixo d'água": cue `muffle` com a duração.
  - Volta com flash e impacto na frase seguinte.
- **Sucção antes do nome principal.** Vórtice de partículas girando, câmera rodando (`rz` até ~1,6), palavras da frase sendo sugadas e blur crescendo. Depois vem o impacto com o nome em 3D: letra por letra, cada uma girando, e um reflexo de luz (`glint`) passando.
- **Janela de software** (editor, timeline): chega girando em 3D e é cortada por uma lâmina de luz em duas metades que caem.

## 10. Narração e respiros

- **Corte os respiros** (silêncios) da narração. Isso é o padrão e deixa o vídeo dinâmico.
- **Pausas intencionais** (`--keep`), só onde fazem sentido:
  - depois do nome do produto ou curso;
  - depois do preço antigo;
  - depois do preço novo;
  - no momento do buraco negro.
- **Pergunte** se a pessoa quer respiro no final (logo, preço e CTA) ou tudo cortado.
- **Respiro visual no fim:** o CTA segura ~4 s depois da última palavra e o logo final ~3,5 s.

## 11. Som

- **Hierarquia:** narração > efeitos > música. A música abaixa ~11 dB quando há voz e os efeitos ~5 dB. Master em -14 LUFS e pico em -1 dBTP.
- **Efeitos cinematográficos e MUITOS:** whoosh em toda troca de cena, tick e clique em interface e digitação, impacto em palavra-chave, braam no nome principal, explosão, lâmina, glitch, tape-stop e notificação grave.
- **Proibido som infantil:** boing, pop, plim agudo, xilofone.
- **Música alinhada:** a batida entra no impacto principal e cai no preço. Use `musica.py` com offset e corte de compassos.

## 12. CTA

- **Sequência do CTA:**
  - "COMENTA" entra em 3D.
  - A palavra (ex.: "MOTION") vem GIGANTE na cor de destaque, pulsando com glow nas batidas.
  - Depois as duas sobem e viram uma linha só no topo.
  - O celular sobe com a simulação comentário → DM → link.
- **Preço:** o antigo é riscado por uma linha de luz e cai em 3D. O novo slam na cor de destaque com o maior impacto do vídeo. Uma tag (ex.: BLACK) entra antes, em cima, sem tocar nos números.

## 13. Logo

- **Animação.** O logo é animado em 3D real: extrusão em camadas e giro. Se tiver duas partes (ex.: MOTION | IA), a primeira entra devagar e a segunda bate com impacto na palavra falada. Um reflexo de luz passa depois.
- **Divisão.** É automática pela maior coluna vazia (`logoSplit`). Para forçar, defina `const LOGO_SPLIT = <px>;` no `scenes.js`. Nunca corte dentro de uma letra, porque aparece um filete antes da hora.

## 14. Evitar "cara de IA"

- **Proibido:**
  - gradiente arco-íris (só dentro do "vídeo ruim" proposital);
  - texto genérico centralizado parado;
  - tudo entrando com fade;
  - estrelas, clipart, emoji como elemento gráfico.
- **Cada movimento tem motivo:** acompanha a fala, revela a próxima ideia ou dá impacto.
- **Palavras em tela:** use a palavra forte da frase, não a frase inteira. O resto entra como linha pequena de apoio.
