# Perguntas do briefing

Pergunte em **rodadas curtas**: no máximo 4 perguntas por vez, cada uma já com a sugestão padrão, pra pessoa só confirmar ou trocar. Antes de perguntar, olhe o que ela já mandou (imagens, links, pasta) e só pergunte o que falta. Use o AskUserQuestion quando as respostas forem opções. Explique termos técnicos na hora (ex.: "rótulo planificado = a arte da lata aberta numa folha reta").

## Rodada 1: a ideia (sempre a primeira mensagem)
Comece pela cabeça da pessoa, não pela ficha técnica. Quem já imaginou o vídeo se sente ouvido; quem não imaginou ganha um ponto de partida.
1. **Você já tem uma ideia em mente?** Como imagina o comercial, que sensação quer passar, alguma cena que não pode faltar. Pode ser só um "quero aquele estilo de lata girando com fruta voando".
2. **Já tem referências?** Vídeos, links do Pinterest/Instagram/TikTok ou prints. Peça pra mandar ou salvar na pasta de referências do projeto.
   - **Se tiver:** estude cada uma (`references/referencias.md`, "Quando a pessoa manda as referências dela") e diga em qual parte da estrutura cada movimento entra.
   - **Se não tiver, ou tiver pouca:** abra a página de efeitos (`scripts/escolher_referencias.py`, veja `references/referencias.md`), onde cada referência da skill roda em vídeo e ela marca o que quer. Diga que a estrutura padrão já junta os melhores e que os "Extras" pedem cena nova.
   - **Nos dois casos** dá pra juntar as dela com as da skill na mesma página.
3. **Qual o produto e a marca?** Lata de energético, refrigerante, água, cerveja, suco... Peça o site ou o Instagram da marca, de onde saem as palavras e o logo.
4. **É comercial oficial ou de portfólio (não oficial)?** Se for não oficial, o aviso "COMERCIAL NÃO OFICIAL" fica legível no final e nada no vídeo finge ser da marca.

Se a pessoa já respondeu alguma dessas no pedido, não pergunte de novo: confirme o que entendeu e siga pra próxima. A pasta do projeto você pergunta no fim da rodada 2 (ou sugere uma). Tudo o que for usado fica nela.

## Rodada 2: a lata
5. **Quantos sabores e quais?** De 1 a 6. Com 4, o cata-vento fecha perfeito (uma lata por braço). Com menos, as latas se repetem; com mais, o vídeo cresce ~1,5 batida por sabor.
6. **Tamanho da lata?** Padrões (altura × diâmetro):
   - 350 ml fina/sleek (tipo Dane-se, Red Bull alto): 146 × 58 mm, o padrão do motor.
   - 350 ml tradicional (tipo Coca): 122 × 66 mm.
   - 473 ml (latão): 157 × 66 mm.
   - 269 ml / 250 ml fina: peça as medidas ou uma foto com régua.
   Se a pessoa tiver a lata na mão, peça as medidas reais.
7. **Tem o rótulo planificado?** Quase ninguém tem. Passe o prompt do Gemini (`references/rotulo-gemini.md`) e peça foto da frente **e** das costas de cada lata.
8. **Logo em PNG com fundo transparente?** Se não tiver, pegue do site (o arquivo oficial) e confirme com a pessoa.

## Rodada 3: o conteúdo
9. **Palavra de cada sabor (a palavra gigante atrás da lata).** Só palavras reais da marca: site, rótulo, Instagram. Nunca invente slogan, número ou avaliação. Pode ficar sabor sem palavra.
10. **Ingredientes que explodem em cada sabor.** Frutas, grãos, folhas, gelo, respingo de água... Busque modelos escaneados grátis e mostre a lista antes de baixar (`references/pecas-3d.md`). Se não quiser peça nenhuma, o giro troca o sabor sem explosão.
11. **Linha do produto no final** (ex.: "ENERGY DRINK · ZERO AÇÚCAR") e **a assinatura (@)** que fecha o vídeo.
12. **Narração?** O padrão é **sem narração**: esse estilo é guiado pela música e pelos efeitos. Se a pessoa insistir, avise que muda o ritmo inteiro e que a estrutura aprovada é sem.

## Rodada 4: o som
13. **Qual a música?** MP3 ou link. Peça pra ela escolher, porque a batida manda em tudo. Se pedir sugestão, pesquise músicas em alta no estilo que ela quer e avise sobre direito autoral (a versão sem música resolve no Instagram).
14. **Tem pasta de efeitos sonoros?** Se tiver, o `sfx_mapear.py` escolhe os sons certos. Se não, o motor gera sons cinematográficos sozinho.

## Depois das respostas
Resuma tudo numa tabela curta (marca, sabores + cores + palavras + peças, tamanho, música, pasta) e só então monte o projeto. As cores de cada sabor você tira do próprio rótulo (a cor de fundo dele) e mostra junto, pra ela aprovar.
