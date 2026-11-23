# Erros do comercial Dane-se e a regra que evita cada um

O Dane-se levou 3 rodadas de render de horas até ser aprovado. Quase tudo que deu errado foi falta de conferir antes de gastar render, ou movimento que não seguia a música. O motor desta skill já corrige o que é técnico. O que depende de decisão está aqui, pra você ir direto ao resultado aprovado.

## Processo (o que mais custou tempo)

| Erro | O que aconteceu | Regra |
|---|---|---|
| Final sem rascunho | A v1 foi direto pro render final (~3 h). O resultado veio "bem ruim" e foi tudo refeito. | Sempre rascunho em 640×360 (~25 min) antes do final. A pessoa aprova o **movimento** no rascunho. |
| Estrutura antes da música | A v1 foi montada numa grade provisória de 120 BPM com 64 batidas (32 s). Quando a música chegou, mudou tudo. | Pegue a música **antes** de montar a estrutura. Tudo sai da batida dela. |
| Vídeo longo demais | 32 s com trocas repetidas cansou: "dos 15 aos 20 s dá pra cortar". | ~25 s (44 batidas a ~100 BPM). Cada sabor aparece uma vez. Menos é mais. |
| Forçar texto | Tentou encaixar todas as frases da marca. | Uma palavra por sabor, no máximo. Sem frase solta na tela. |
| Adivinhar o tempo | Ajustes descritos em texto davam margem pra erro. | Peça uma **edição porca** (a pessoa corta o rascunho no celular, na música). Ela vira a referência de tempo, e o resultado é "igual, só que mais fluido". |
| Pressa | "Preciso desse vídeo agora" no meio do render final. | Dê as opções com o tempo **medido** de cada uma: final cheio ou rápido (a hélice em prévia ampliada). Pergunte antes de usar a rápida. |
| Dois renders juntos | Dois Blenders abertos (~14 GB cada) estouraram a RAM de 16 GB e tudo ficou ~5× mais lento. | Um Blender por vez. O `rodar.py` espera o outro terminar. |
| Parar render pela metade | Parar a tarefa matou o shell, mas o Blender continuou e a cadeia seguiu pro vídeo com quadros faltando. | Antes de religar, confira se sobrou Blender aberto e encerre ele e o python da cadeia. Depois do `compor.py`, procure "AVISO: quadros 3D faltando". |
| Alarme no momento errado | O alarme tocou na prévia e a pessoa achou que era o vídeo final. | Alarme só no FINAL. |
| 4K | Render 4K não precisava. | Final em 1080p. |
| Amostras demais | 48 amostras levavam ~50 s/quadro na hélice. | 24 amostras dão o mesmo resultado em ~32 s/quadro (padrão do motor). |
| Arco padrão sem perguntar (Guaraná, 21/11/2026) | A pessoa mandou só a referência dela; o storyboard saiu com o arco Dane-se inteiro (cata-vento, rastro, corredor, fileira, troca de sabor) e ela disse que misturei referências que ela não queria. | **Sempre** abra a página de efeitos com as referências gerais da skill, mesmo quando ela já mandou referência própria, e monte a estrutura só com o que ela marcou "Quero". Observação vale ao pé da letra ("só a parte das frutas" = só aquele trecho). |
| Gelo e copo "de plástico" (Guaraná, 21/11/2026) | No Eevee o gelo saiu como placas escuras e o copo parecia plástico/papel; o líquido ficou bege opaco. O Eevee só refrata uma camada e a refração não enxerga o fundo do canvas (que só entra na composição). | Cena com vidro, gelo ou líquido: **fundo 3D de verdade** atrás (estúdio infinito / chão embaixo do gelo) e render no **Cycles na GPU** (OptiX, 32 amostras + denoise, `use_persistent_data`). Gelo: material com miolo leitoso, superfície ondulada, cubos amontoados (não flutuando), lata com mais gotas e fumaça fria no canvas. Cena com centenas de cubos no Cycles é lenta numa GTX 1050 Ti (~3,6 min/quadro em 1080p): renderize em 960×540 e amplie (`ampliar.py <plano>`). |
| Lata invisível nos planos novos (Guaraná, 21/11/2026) | O material da lata usa o alfa da cor do objeto pro efeito neon do Dane-se; objeto novo vem com alfa 1 e a lata vira só contorno. | Ao criar lata fora do `cena_uma_lata` antigo, zere: `o.color = (1, 1, 1, 0)` na raiz e nos filhos. |
| Abertura macro demais (Guaraná v1, 21/11/2026) | Câmera colada na lata (raio 1,3–1,9, lente 70–80): "dos 0 aos 2 s não dá pra entender nada". As chaves com `suave` em cada trecho também faziam a câmera frear em cada ponto. | Abertura em plano médio (raio ~6 da lata, lente 50), lendo tampa → logo → nome. Curva que passa pelas chaves sem parar (`spline`, Catmull-Rom) e speed ramp só na última batida, acelerando pro corte (`rampa`). |
| Frutos sem a lata (Guaraná v1) | Os frutos voavam na lente com fundo vazio e a lata só aparecia na explosão. | A lata já sobe lá no fundo enquanto os frutos passam (rápido → devagar), com a mesma câmera da explosão: o corte casa (mesmo lugar e tamanho) e o foco puxa dos frutos pra lata. |
| Respingo parecendo tinta (Guaraná v1) | O respingo era laranja chapado e opaco: "não ficou com textura de guaraná". | Líquido âmbar **transparente** (o fundo aparece por dentro), borda escura espelhada, brilho das luzes e bolhinhas (voronoi). Gotas soltas com o mesmo material. |
| Palavra cortada em cima (Guaraná v1) | A máscara da palavra usava 0,78 do corpo da fonte e a Anton é mais alta: o topo das letras sumia. | A máscara mede a altura real (`measureText().actualBoundingBoxAscent`). |
| Fruto de costas e mergulho (Guaraná v1) | A câmera dava zoom até o fruto no fim da explosão, e o fruto aparecia de lado, sem a semente. | Corte seco, com o fruto já girando e freando. A **parte preta (semente) fica de frente pra câmera** (`face_corte` da peça), mais longe da tela, com grafismo e gotas. |
| Lata estourada e fundo chapado no copo (Guaraná v1) | No Cycles, a chave de cima e a contraluz amarela lavavam o topo da lata, e o estúdio liso parecia chapado. | Chave grande e de lado, contraluzes ~metade (`luzes_chao(..., suave_lata=True)`). Fumaça atrás feita de véus com ruído animado, **só emissão**: luz com grade (spread) desenha um triângulo duro no véu. O véu não pode cortar o fundo curvo nem ficar na frente da contraluz. |
| Blender 5.x (Guaraná, 21/11/2026) | O PC só tinha o Blender 5.3; `Action.fcurves` não existe mais e a fábrica de latas quebrou. | O motor usa `curvas()` / `curva()` (em `lata_lib.py` e `fazer_lata.py`), que funcionam no 4.2 e no 5.x. Não acesse `action.fcurves` direto. |

## Movimento (correções do cliente, já embutidas no motor)

- **Abertura:** a primeira versão dava um zoom enorme direto na tampa e não tinha gota. O certo é a lata em pé, a câmera centralizada lá em cima acompanhando uma gota, freando num close forte da tampa com a gota quase encostando. Na batida, ela desce rápido e para encarando o olho/logo do rótulo. Devagar demais e fora da batida estava errado.
- **Closes:** faltavam takes diferentes. São 4 partes diferentes da lata, em **corte seco**, meia batida cada. O próximo corte já é a lata subindo.
- **Palavra:** apareceu na frente da lata. Ela fica **sempre atrás**, entrando por máscara (sem fade).
- **Frutas:** as frutas feitas por código "não ficaram legais". Use **modelos escaneados reais** e mostre antes de baixar.
- **Trocas de sabor:** tinha um zoom do nada e não seguia a música. A câmera fica no mesmo lugar, no máximo afastando devagar. A primeira troca tem mais tempo e as próximas vão acelerando, cada uma numa batida.
- **Cata-vento:** as latas ficaram coladas uma na outra. Elas ficam **separadas**, como na referência Cycle. Também não podem parar e mudar de cor a cada batida: o giro é liso, com fundo fixo.
- **Rastro:** não é um borrão. São **cópias nítidas** da lata, em leque (referência Gloria).
- **Corredor:** não precisa juntar as latas pra formar o túnel. A câmera entra no furo do meio do cata-vento, escurece e já está no corredor. O morph lento demais foi cortado.
- **Fileira:** as latas começam escuras e **uma acende por batida**, com luz que sobe suave (piscar parece travada). A câmera desliza de lado e **freia centralizada na última lata**. Terminar em espaço vazio estava errado. Nenhuma lata pode andar pra trás na tela.
- **Geral:** "ficou lento", "tem que ter mais curva de movimento", "dando umas travadinhas". A velocidade da câmera sobe e desce suave e nunca inverte. Use motion blur nos movimentos rápidos.
- **Final:** logo com animação de **stroke estilo After Effects**. Depois, só o @ da pessoa, bastante tempo (~4 s).

## Material e luz

- **Gotas artificiais:** gotas com refração ficaram cinzas e sujas. O motor usa um mapa de condensação (gotas, escorridos e névoa) desenhado por cima do rótulo.
- **Líquido branco:** o respingo de água ficou "parecendo leite". O certo é água transparente com bordas que refletem o estúdio (shader Fresnel).
- **Luz estourada:** a luz de cima estourava a tampa e o spot da fileira estourava a lata. As luzes do motor já foram calibradas. Se mudar, confira num quadro de teste.
- **Rosa lavado:** o AgX deixou a cor pastel. Use a view "Standard" com o look "Medium High Contrast".

## Som

- **Vidro quebrando:** "não coloca esse efeito". Também nada de blip, pop, bip, laser ou som infantil.
- **SFX:** só cinematográficos: whoosh, boom, hit, clique de câmera, estalo de lâmpada, soco, lâmina. Música ~3 dB abaixo dos efeitos e mix em -14 LUFS.
- **Exportar duas versões:** com e sem música (o encode é rápido; o gargalo é sempre o render). A versão sem música serve pra postar com música do Instagram.
