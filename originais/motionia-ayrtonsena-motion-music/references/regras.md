# Regras de ouro (correções reais do Ayrton)

Toda correção nova entra aqui na hora, com data e o porquê.

## Training Season (Dua Lipa, 16:9, 31 s) — aprovado na v3 em 21/10/2026

**v1 → v2 (pedidos dele):**
- **Vermelho mais escuro** pro glow contrastar. Fundo `#7A0820`, glow `#ff2d55`, texto vermelho `#e8173f`. O vermelho vivo `#E1163C` deixava tudo chapado.
- **Abertura "carregando"**: barra LOADING 000% enchendo junto com as palavras.
- **Uma palavra por vez, quase a tela inteira** (YOU / SHOULD / KNOW), e não uma frase pequena no topo.
- **Sem efeito sonoro**, só a música e um close-up no buraco negro do final.
- **Sincronia do HOLD** estava atrasada; precisava de muito impacto (entra gigante com estouro de linhas, anel e flash e depois encolhe pra linha "HOLD ME CLOSE").
- **DEEPER** como espelho infinito (cópias com moldura neon indo pro fundo, escurecendo).
- **VULNERABLE** estilhaça em cacos de vidro pequenos e os MESMOS cacos voltam e remontam a palavra.
- **Final:** a música é SUGADA pelo buraco negro (nunca desacelerando como se parasse), com close-up, e depois a assinatura "by @<arroba da pessoa>" pequena, branca, glow (no Training Season foi o @ do autor da skill; pra outra pessoa, sempre pergunte o @ dela).

**v2 → v3 (pedidos dele):**
- **O I sobe de forma contínua**, sem degraus a cada batida. A câmera chega nele e a tela fica branca; o branco escurece sugado por um **buraco negro vermelho**.
- **HOLD no segundo exato da batida** (9,47 s, quando o bumbo volta), e não onde o Whisper marcou.
- **DEEPER entrando de forma contínua** (sem empurrões nas batidas).
- **Assinatura parada e sem fade out.**

**O que já estava certo e ele manteve:** RODEO com letras pulando nas batidas e laço; TAKE CONTROL em fundo branco com mira REC; CONVERSATION OVERLOAD com balões de chat; TRAINING SEASON'S em fundo branco + contagem 3-2-1; OVER com o maior impacto na volta do bumbo.

## Regras gerais que vêm de outros trabalhos dele
- **Prévia antes do render (Code):** abrir a prévia no HyperFrames e só renderizar depois do ok, mesmo que ele diga "já gera o vídeo".
- **Partitura antes:** em vídeo no ritmo, mostrar primeiro a partitura das batidas. Objeto ou efeito só onde tem batida, sem enfeite sobrando.
- **Efeitos sonoros (quando ele pedir):** só cinematográficos (hits, booms, whoosh, clique, glitch, close-up). Nada de blip, pop, bip, laser nem brilho "fofo". Música ~3 dB mais baixa que o de costume quando houver SFX.
- **Flash de impacto:** curto, 2 quadros, sem cauda (cauda branca vira cinza feio).
- **PC dele:** render com 4 workers e prioridade baixa; avisar antes de render pesado; temporários dentro do projeto ou no D:.
- **Letra na tela:** só palavras-chave e trechos curtos, nunca a letra inteira.
- **Tudo centralizado, nada cortado:** margem de ~140 px no topo e embaixo, já contando o giro da câmera.
- **Nenhum texto sobre texto:** um elemento sai antes do próximo ocupar o lugar (exceto no espelho infinito, onde as cópias de trás são escuras).
- **3D de verdade:** texto importante com extrusão (W3/text3D), planos com perspectiva; nada de fade 2D sozinho.

## Armadilhas técnicas (Flower In A Hurricane, 18/11/2026)
- **`const END = 26.3;` tem que ser número literal** numa linha só: o `hf_wrap.py` lê o END por regex e quebra com `END = V1 + 3.45`.
- **Fundo claro:** glow é aditivo e some no creme/pêssego. Em cena clara, texto roxo escuro com `glow: 0, flash: 0`; o impacto vem de anel, tremor e cor. Glow forte em cima de papel/calendário branco estoura e apaga o conteúdo.
- **Folha de calendário virando:** arrancar a folha (sobe, gira e vai pro fundo, `z` positivo) funciona; girar em volta da borda com `rx` sai torto.
- **Estouro de objetos (notas de dólar):** desenhe antes do texto/carimbo e mande pro fundo (`vz` positivo), senão cobre a palavra.
- **Música sem batida principal** (energia igual, nenhuma força ≥ 5): os impactos grandes saem da letra (palavra forte, sílaba segurada) e do fim.

## Armadilhas técnicas (GTA 6 — Vice neon sunset, 18/11/2026)
- **Textura desenhada à mão (coração neon, placa) tem que caber no `mk(w,h)`**: com escala grande o desenho passa da borda e o plano sai com um corte reto (o coração saiu com os lobos cortados). Confira os extremos do caminho × escala antes.
- **Legendas pequenas no topo (`L3` em y -390/-400) somem na borda** quando a câmera dá dolly-in; use y ≈ -330/-340 e tire a legenda antes da palavra grande entrar.
- **Esperar render do HyperFrames:** não use `grep error` no log (casa com "0 error(s)" do lint). Espere o MP4 existir e a pasta `.hf-transaction-*` sumir.
