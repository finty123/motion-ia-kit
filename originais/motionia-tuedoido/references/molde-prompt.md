# Molde do prompt (mesmo molde da skill prompt-motion-graphics, adaptado)

Entregue num único bloco de código, em português. Ele documenta o vídeo e pode ser rodado no Claude Code. Logo depois, a própria skill constrói o vídeo.

```
<entradas>
Produto: [nome]. Objetivo: [vender/lançar/anunciar]. CTA: [comenta PALAVRA / link na bio].
Arquivos em anexo: [narração] (relógio mestre; respiros cortados, pausas intencionais em [...]),
[música] (offset X s, corte A–B; batida entra em "[palavra]", cai em "[preço]"),
[logo] (vetorizado e extrudado em 3D; parte 1 "[...]", parte 2 "[...]"), [paleta: hex].
Formato: [1920x1080]. Duração: [END] s.
</entradas>

<direcao>
Motion dinâmico 3D: tipografia cinética com extrusão real, câmera 3D sempre em movimento e mudando de ângulo a cada palavra-chave,
troca de cor de fundo a cada 1–2 cenas ([escuro com glow] / [cor viva] / [destaque]), glow e impacto (flash, anel, tremor, som) em toda
palavra-chave, desfoque gaussiano nas transições, motion blur real. Tudo centralizado; nenhum texto sobre outro; simulações de interface
no lugar de imagens paradas. Parte final (oferta/CTA) com câmera mais calma e respiro.
Proibido: alinhar à esquerda, texto sobre texto, 2D esticado fingindo 3D, fade-only, gradiente arco-íris (fora do "vídeo ruim"),
emoji/clipart, logos oficiais de terceiros, sons infantis.
</direcao>

<estrutura>
[Uma linha por cena: índice/tempo da palavra de início · fala · receita (R1–R25) · o que acontece em cada palavra-chave · sons]
1. 0,00 · "[...]" · R1 · ...
...
</estrutura>

<construcao>
HTML único + canvas 2D com motor 3D próprio (planos com perspectiva, extrusão em camadas), window.seek(t)/frame(t, sub) puros e
determinísticos; tempos sempre de words.json (w(i)); cues compartilhadas entre imagem e som; render 30 fps com 2 subquadros
(motion blur), em blocos retomáveis; SFX sintetizados (numpy) a partir das cues; mix narração > SFX > música, ducking, −14 LUFS.
</construcao>

<pegadinhas>
Margem de ~140 px no topo e na base (a câmera gira e dá zoom). Animação de impacto começa 0,07 s antes da palavra. Elemento citado
("esse X aqui") entra 0,35 s antes. Na tela vale a palavra falada de verdade, não o erro da transcrição. Partículas pequenas. Logo dividido
só na coluna vazia. Plano grande perto da câmera: as células de trás são descartadas.
</pegadinhas>

<comeco>
Primeiro a folha de contato com 16–24 quadros (1 por palavra-chave) e notas de 1 a 10 (gancho, legibilidade, texto sobre texto,
centralização, margens, variedade, 3D, impacto/glow). Corrige os 3 piores até tudo ficar 8+. Depois render completo, mix e entrega.
</comeco>
```
