# Skill 1: `prompt-motion-graphics` (o gerador de prompt)

**O que faz:** entrevista você e devolve um **prompt** pronto, no formato de tags (`<entradas>`, `<direcao>`, `<estrutura>`, `<construcao>`, `<pegadinhas>`, `<comeco>`), pra outra conversa do Claude gerar o vídeo por código. **Ela não faz o vídeo**, só o pedido bem feito. É a skill dos módulos 1, 4 e 6 (telão).

**Funciona em:** chat e Claude Code (ela pergunta onde o prompt vai rodar e troca o bloco final: no Code usa o HyperFrames pra prévia; no chat, a prévia é por quadros).

## Quando usar
- Qualquer motion que não tenha uma skill de estilo pronta (filme de produto, logo animada, vinheta, telão de loja, lançamento).
- Quando você quer controlar o vídeo do zero (aula 4.1) e depois transformar o resultado numa skill sua (aula 4.3).

## O que ter em mãos
1. **Referência de design:** o site da marca (o prompt manda o Claude tirar logo, cores, fontes e telas com Playwright) ou, sem site, logo + cores em hex + fontes + frase + imagens.
2. **Referência de animação:** um vídeo cujo movimento você quer (diga o trecho: "dos 0 aos 5 s, o efeito de digitar e o site surgir").
3. Formato, duração e música (ou deixe ela sugerir: 120 BPM, 8 compassos = 16 s, trilha sintetizada).

## Como chamar
```
/prompt-motion-graphics
Quero um motion de [marca] ([site]). Referência de design: o site. Referência de animação: o vídeo anexo, principalmente [trecho].
Formato 16:9, ~30 s, com narração que eu vou gerar no ElevenLabs. Vai rodar no Claude Code.
```

## O que acontece
1. Ela pergunta só o que falta (produto/site, onde vai passar, formato, duração, música, história de 8–12 momentos, estilo, chat ou Code, pasta e nome do arquivo).
2. Entrega o prompt num bloco só + o que você precisa anexar + o que ela assumiu.
3. Você cola o prompt numa conversa nova (no Claude Code, aberto na pasta de projetos) e o Claude constrói o vídeo: mostra a tabela de estados na batida → prévia (HyperFrames) → ajustes → render.

## Direções de estilo que ela conhece
- **A. Filme de produto com interface** (apps, SaaS, sites): um contêiner que nunca corta, cursor conduzindo, fundo neutro, uma cor de destaque.
- **B. Marca energética / comercial** (logo, negócio local, telão): tipografia cinética grande, troca de fundo como transição, fotos com máscara.
- **C. Editorial / premium:** respiro, cortes secos, uma ideia por tela.

## Dicas do curso
- Faça **um formato primeiro** (ex.: horizontal), aprove tudo e só depois peça o outro a partir da mesma linha do tempo: gera menos e gasta menos.
- Se não gostar do roteiro que ela propôs, diga a sua ideia com as suas palavras e peça pra reescrever antes de gravar a voz.
- Peça ajustes **com o tempo exato** ("lá pelos 7 s...") e, se não souber o nome do efeito, mande um vídeo com o efeito.
