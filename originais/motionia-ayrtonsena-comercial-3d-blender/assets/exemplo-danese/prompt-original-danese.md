```
<entradas>
Produto: Dane-se, energético e água em lata (https://daneseoficial.com.br/pages/quem-somos). Comercial NÃO OFICIAL de portfólio. O vídeo tem que DIZER isso na tela: o cartão final traz "Comercial não oficial · by @ayrtonsena.stg", legível, por pelo menos 2 s.
Visita o site com Playwright e pega o logo real, as fontes e as cores. Frases que podem entrar (são do site, não inventa outras): "Sem medo. Sem frescura." e os valores "CORAGEM", "ATITUDE", "REAL".
Latas 3D já prontas, NÃO remodela: C:\Users\Ayrton\Downloads\latas-3d\modelos\ (dane-se melancia, dane-se limao, dane-se manga tropical, dane-se agua sem gas), cada uma com lata.blend. O gerador é latas-3d\fazer_lata.py (perfil da lata 350 ml fina, rótulo por UV, pescoço na cor do rótulo, gotas sem refração, exposição automática pelo brilho do rótulo). Reaproveita essa geometria e esses materiais.
Cor de cada sabor (tira o hex exato do rótulo em latas-3d\rotulos\): Melancia = rosa pink; Limão = branco + verde; Manga Tropical = laranja; Água sem gás = preto + rosa.
Storyboard de rascunho: latas-3d\comercial-danese\storyboard.png (12 quadros). Usa SÓ a ordem das cenas, os tempos, o que entra em cada cena e a direção dos movimentos de câmera e das latas. NÃO copia o visual do storyboard: nem o traço de lápis, nem a fonte manuscrita, nem o papel, nem as setas, nem a composição exata. É um rascunho de montagem; o design segue a <direcao> abaixo e as latas 3D reais.
Referências de movimento em latas-3d\Referencias\ (10 vídeos). Extrai um quadro a cada 0,5 s com ffmpeg, escreve docs/guia-de-estilo.md com a gramática delas e usa só a gramática, nunca o conteúdo, os logos nem as latas delas. As que mais importam aqui:
- lata Lit Energy: macro na borda da tampa cheia de gotas, a câmera escorrega pela curva até a lateral (estado 3);
- lata Ape Bräu: câmera desce colada no corpo inclinado, desfoque raso, foco passeando nas gotas (estado 3);
- lata Lucky F*ck, perto dos 14 s: o sabor troca com a lata parada no mesmo lugar, trocas acelerando (estados 5–7);
- lata Olipop: giro rápido e os ingredientes explodem em volta, depois flutuam em câmera lenta (estados 5–7);
- lata Gloria: rastro em leque de cópias da lata girando (estado 8);
- lata Bloom Pop, de 0 a 3 s: lata em silhueta contra a luz num chão espelhado e túnel de contornos de lata em neon (estados 9–11).
Sem narração: o vídeo é guiado só por música e efeitos sonoros.
Música: AINDA NÃO DEFINIDA. Monta tudo numa grade provisória de 120 BPM. Quando eu mandar a trilha, a grade passa a sair dela.
Formato: 1920x1080 (16:9), 30 fps.
</entradas>

<direcao>
Comercial de produto 3D com energia de showreel. A lata é a estrela de todo quadro, sempre inclinada e girando devagar, nunca reta (reta só na silhueta e na fileira final). Cada sabor tem um fundo liso ou um gradiente suave na sua cor, e a troca de fundo acontece no tempo forte. A tipografia é cinética, grande, numa fonte display condensada que combina com o logo DANE-SE, e a palavra gigante fica ATRÁS da lata, com a lata cobrindo no máximo metade dela. Luz de estúdio: brilho vertical na lata, contraluz na cor do sabor de um lado e branco do outro, gotas de condensação discretas. A câmera nunca para: despenca e freia, escorrega colada na lata nos macros, abre em arco nos planos inteiros. Closes de detalhe com desfoque bem raso aparecem ao longo do vídeo inteiro, não só no começo. Tom irreverente da marca.
Proibido: título centralizado em gradiente, texto surgindo com fade, faíscas e partículas genéricas, brilho estourado na tampa, lata parada, mostrar de perto a parte de trás do rótulo (os textos de lá são inventados), números ou avaliações inventados, narração, tempo morto.
</direcao>

<estrutura>
120 BPM, 16 compassos (64 batidas, 32 s), alguma coisa acontece em toda batida. Os quadros 1–12 do storyboard correspondem aos estados abaixo.
1. Batidas 1–4 (0–2 s): fundo escuro com contraluz rosa. A lata é a Melancia. Na batida 1 a câmera despenca de cima, RÁPIDA, em direção à tampa, e freia em câmera lenta (speed ramp) a milímetros dela: gotas e lacre enchem a tela. Nenhum texto, o movimento é o gancho.
→ 2. Batidas 5–8 (2–4 s): antes de encostar na tampa, a câmera mergulha, descendo colada no pescoço e no corpo, e para de frente pro OLHO do rótulo na batida 7, como se ele encarasse quem assiste.
→ 3. Batidas 9–12 (4–6 s): closes de detalhe. Batidas 9–10: macro na borda da tampa cheia de gotas, a câmera escorrega pela curva. Batidas 11–12: a câmera desce colada na lateral inclinada, com o foco passando de uma gota pra outra (rack focus).
→ 4. Batidas 13–16 (6–8 s): a câmera abre em arco e mostra a Melancia inteira, inclinada e girando devagar, e termina na posição fixa dos estados 5–7. "Sem medo." entra na batida 13 e "Sem frescura." na batida 15.
Dos estados 5 a 7, a LATA NÃO SAI DO LUGAR: fica no centro, inclinada, na mesma posição em que terminou o estado 4, com a câmera de frente e só um push-in lento contínuo. Quem muda é o sabor.
→ 5. Batidas 17–22 (8–11 s): na batida 17 a lata dá um giro rápido no próprio eixo. No pico do giro, escondido pelo borrão, o rótulo troca de Melancia pra Limão, o fundo vira branco e "CORAGEM" aparece gigante atrás. Rodelas e gomos de limão explodem de trás da lata e flutuam em câmera lenta. Na batida 21, punch-in rápido no olho verde e volta.
→ 6. Batidas 23–28 (11–14 s): giro rápido na batida 23. Os limões são expulsos pra fora do quadro, o rótulo troca pra Manga Tropical, o fundo vira laranja, "ATITUDE" atrás, e pedaços de manga explodem e flutuam. Na batida 27, macro rápido no fundo da lata e volta.
→ 7. Batidas 29–34 (14–17 s): giro rápido na batida 29. As mangas são expulsas, o rótulo troca pra Água sem gás, o fundo vira preto, "REAL" atrás, e gotas e respingos de água explodem e flutuam. Na batida 31, macro rápido na borda com gotas e volta. Nas batidas 33–34, aceleração: o sabor, o fundo, a palavra e as peças trocam a cada meia batida, passando pelos 4 sabores, cada vez mais rápido.
Dos estados 8 a 11 NÃO TEM CORTE: é um movimento contínuo, um vira o outro.
→ 8. Batidas 35–44 (17–22 s): na batida 35 a lata se divide em 4 (uma de cada sabor), que abrem em cruz com as tampas no centro. A hélice começa a girar e deixa um RASTRO em leque de cópias de si mesma: quando o giro acelera, o rastro abre. O fundo troca de cor a cada batida (rosa, branco, laranja, preto).
→ 9. Batidas 45–48 (22–24 s): MORPH. Na batida 45 a hélice freia e as 4 latas se fecham numa lata só, de frente pra câmera. As cópias do rastro, em vez de sumirem, viram contornos da lata em neon e se espalham em profundidade, uma atrás da outra, formando um túnel. Na batida 48 a câmera mergulha pro centro.
→ 10. Batidas 49–52 (24–26 s): a câmera atravessa o túnel (um anel passa por batida, alternando as cores dos sabores) e desacelera chegando no fim dele: a Melancia em pé, em SILHUETA contra uma luz rosa por trás, num chão espelhado escuro.
→ 11. Batidas 53–58 (26–29 s): do chão espelhado, a câmera se afasta (recua e sobe um pouco) e revela as outras 3 latas ao lado, em fileira, ainda em silhueta. Nas batidas 55–58 uma lata acende por batida (Melancia, Limão, Manga, Água), com reflexo no chão.
→ 12. Batidas 59–64 (29–32 s): logo DANE-SE + "Energy drink · Zero açúcar", depois "Comercial não oficial · by @ayrtonsena.stg" menor, e fecha no preto nas batidas 63–64.
</estrutura>

<construcao>
1. 3D no Blender 4.2 (C:\Program Files\Blender Foundation\Blender 4.2\blender.exe), Eevee, por script (blender -b -P), sempre em prioridade BelowNormal (o PC é i5-12400F + GTX 1050 Ti 4 GB e trava com render pesado). Uma cena .blend e uma pasta de frames por estado, pra refazer só o que mudar.
2. As latas saem com fundo transparente (film_transparent, PNG RGBA). Fundos, troca de cor e tipografia ficam num HTML com um canvas e window.seek(t), sem transições de CSS, sem timers, sem estado carregado entre quadros, com ruído só por seed (mulberry32). Ordem das camadas: fundo + palavra de trás (canvas) → lata (Blender) → textos da frente e assinatura (canvas). Compõe com ffmpeg. Exceção: os estados 8–11 (hélice, morph, túnel, silhueta e fileira) saem inteiros do Blender, numa cena só com uma câmera contínua, porque o rastro precisa virar o túnel em 3D e a silhueta depende do reflexo e da luz de trás.
3. A contraluz de cada lata no Blender tem a cor do fundo daquele estado, pra lata parecer estar dentro do cenário e não colada por cima.
4. Câmera e latas com keyframes Bezier (sem linear, exceto o giro contínuo). No canvas, molas de forma fechada; um valor com vários alvos é a soma de uma mola por mudança.
5. A palavra de trás entra depois que a troca de fundo começa e sai antes da próxima troca terminar.
6. Grade de batidas provisória a 120 BPM em beats.json. Quando a trilha chegar, sai dela (numpy/librosa) e começa num tempo forte. Efeitos sonoros SÓ cinematográficos (hit, boom, whoosh, clique, close-up, splash), nunca blip, pop, bip ou laser. Música uns 3 dB abaixo dos efeitos. Loudness -14 LUFS.
7. Abertura (estados 1–2): o speed ramp é feito na curva da câmera (a maior parte do caminho no primeiro 0,3 s e depois quase parada), não acelerando ou desacelerando o vídeo. Motion blur ligado na descida rápida. Desfoque bem raso no macro, com o foco nas gotas da tampa.
8. Closes de detalhe (estado 3 e os punch-ins dos estados 5–7): lente longa (100–135 mm), abertura bem aberta, foco animado (rack focus) de uma gota pra outra. Cada punch-in dentro dos giros dura 1 batida: entra, mostra o detalhe e volta pra posição fixa.
9. Troca de sabor numa lata só: um material com os 4 rótulos e um índice keyframado em CONSTANT, que muda exatamente no quadro de maior velocidade do giro rápido (com motion blur ligado, a troca some no borrão). O pescoço troca de cor junto. O giro rápido é ease-in-out forte: dura ~0,4 s e para na mesma posição de antes.
Frutas: modelos 3D escaneados de verdade (limão em rodela e gomo, pedaços de manga). ANTES de baixar qualquer modelo, me mostra a lista com o site, o link, a licença (CC0 ou CC-BY) e o tamanho de cada um, e só baixa o que eu aprovar. Na Água sem gás, gotas e respingos de água no lugar de fruta. Nunca modela fruta "de desenho" do zero.
Explosão: 8–12 peças por sabor, saindo de trás da lata em trajetórias com seed (mulberry32), girando no próprio eixo. Rápidas no primeiro 0,15 s e depois em câmera lenta (ease-out forte) flutuando até o próximo giro, quando são expulsas pra fora do quadro. Nenhuma peça na frente do logo do rótulo nem da palavra de trás por mais de meia batida.
10. Rastro da hélice em 3D (porque ele vira o túnel): 8–12 cópias da cruz como objetos de verdade (instâncias leves, sem gotas), cada uma repetindo a rotação da cruz com um atraso fixo. As cópias são opacas como na referência, só um pouco mais escuras quanto mais antigas. O espaçamento do leque sai da velocidade do giro, então o rastro abre sozinho quando acelera.
11. Morph rastro → túnel (estado 9): enquanto a cruz fecha numa lata só, cada cópia do rastro faz uma transição curta (~1 batida) do material da lata pra um material de emissão só no contorno do perfil da lata (o miolo some), e ao mesmo tempo é empurrada pra trás no eixo da câmera, uma a uma, a uma distância fixa entre elas. O resultado são anéis com o contorno da lata em fila: o túnel. Cada anel fica com a cor de um sabor.
12. Túnel → silhueta → fileira (estados 10–11): a câmera anda pelo eixo do túnel com velocidade alta no começo e freia no fim (Bezier). No fim do túnel está a Melancia real, com uma área de luz forte e larga atrás dela e quase nada de luz na frente, sobre um chão espelhado escuro (reflexo com leve rugosidade). Os anéis do túnel apagam um por um depois que a câmera passa. As outras 3 latas já estão na cena, ao lado, fora do enquadramento, também em silhueta; a câmera recua e sobe e elas entram no quadro. Cada uma acende na sua batida (luz de frente subindo rápido).
13. Prévia primeiro: 50% da resolução e 16 amostras. Final: 1920x1080, 48 amostras, motion blur do Eevee ligado (menos na hélice e no rastro). Encode H.264 yuv420p, CRF 16.
</construcao>

<pegadinhas>
Luz de cima sobre a tampa estoura fácil: mantém fraca (~12 W, como no fazer_lata.py).
A Limão (rótulo branco) estoura com a mesma luz das outras: usa a exposição automática do fazer_lata.py ou baixa a luz só nela.
Não volta as gotas pra material de refração: no Eevee elas ficam cinzas e sujas.
Com fundo transparente, o glow do compositor some na borda: aplica o brilho no canvas/ffmpeg depois de compor, não no Blender.
Na abertura, a câmera não pode atravessar a tampa nem o lacre no ponto mais perto: deixa folga e confere no quadro de menor distância.
O olho tem que ficar inteiro e de frente no fim do mergulho, sem gota grande na frente da pupila.
Nos macros, o rótulo foi ampliado de 2752 px: se o detalhe ficar mole, aproxima menos ou deixa o foco nas gotas e o rótulo desfocado atrás.
Nos estados 5–7 a lata tem que voltar EXATAMENTE pra mesma posição e inclinação depois de cada giro e de cada punch-in, senão a ideia de "mesmo lugar" se perde.
Se a troca de rótulo aparecer (um quadro com o rótulo cortado ao meio), o giro está lento demais nesse ponto: acelera o pico ou adianta a troca 1 quadro.
Frutas grandes em primeiro plano ficam desfocadas e cobrem a lata: as que passam perto da câmera têm que ser pequenas e rápidas.
Na hélice, as tampas não podem atravessar umas às outras: deixa 1–2 mm de folga.
No rastro, o motion blur do Eevee deixa as cópias borradas e o leque some: renderiza a hélice com motion blur desligado (o rastro já faz o papel do borrão). As cópias antigas não podem tampar a cruz atual.
No morph, as cópias não podem simplesmente sumir e os anéis aparecerem: cada anel tem que nascer de uma cópia visível do rastro, senão vira um corte disfarçado.
Dos estados 8 a 11 não pode ter nenhum corte de câmera: confere na folha de contato que a câmera é uma só e contínua.
O cartão final tem que trazer "Comercial não oficial" escrito, legível; não pode ficar só na legenda do post.
Na silhueta, a lata não pode ficar 100% preta: precisa de um fio de luz no contorno pra ler a forma.
No túnel, o neon não pode estourar em branco: cada anel tem que manter a cor do sabor.
Nunca usa will-change em nada que a câmera aproxima (o texto fica borrado).
Palavra atrás da lata tem que continuar legível: se a lata cobrir mais da metade, afasta a lata ou move a palavra.
O storyboard é rascunho: se algum quadro dele não funcionar em 3D, propõe a alternativa em vez de forçar o desenho.
</pegadinhas>

<comeco>
Me mostra a lista de estados na grade de batidas, em tabela, antes de escrever código.
Quando eu aprovar, faz a prévia em baixa. Antes do render final, me mostra uma folha de contato com um quadro por batida e dá nota de 1 a 10 pra: gancho nos 2 primeiros segundos, legibilidade, qualidade do movimento, variedade, fidelidade à marca e realismo das latas. Corrige os 3 piores pontos e repete até tudo ficar 8+.
Antes do render final, me pergunta qual é a trilha e ressincroniza a grade com ela.
Salva a folha de contato em latas-3d\resultados\01-danese-comercial-folha-de-contato.png e me mostra a tabela de notas de cada rodada antes do vídeo final.
Salva o vídeo final em latas-3d\resultados\01-danese-comercial.mp4.
</comeco>

Não use o HyperFrames nem nenhuma skill. Este é um projeto novo: trabalha só dentro da pasta latas-3d\comercial-danese\ e não apaga, não altera nem sobrescreve nada que já existe em latas-3d\modelos\, latas-3d\rotulos\, latas-3d\Referencias\ nem em resultados\.
```
