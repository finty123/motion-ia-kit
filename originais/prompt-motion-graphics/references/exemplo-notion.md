> Exemplo pro Claude Code (bloco de prévia com HyperFrames). No chat, troque o fim pelo bloco do chat da seção "Chat ou Claude Code" do SKILL.md.

# Exemplo completo (Notion)

```
<entradas>
Produto: Notion (https://www.notion.com). Usa como frase do produto o título principal do site.
Pega o logo real, as cores da marca, as fontes e as capturas de interface do site com Playwright. Escolhe uma cor de destaque da marca.
Música: sintetiza uma trilha original em código a 120 BPM.
Formato: 1920x1080 (16:9).
</entradas>

<direcao>
Filme de produto com interface em movimento. Um contêiner que nunca corta: todo estado é o mesmo elemento mudando de tamanho, de raio e de preenchimento, enquanto o conteúdo troca atrás de um desfoque curto.
Um cursor conduz cada mudança. Fundo neutro e quente, uma cor de destaque.
Molas com, no máximo, um rebote mínimo.
Proibido: easing quicando, brilhos, gradientes na interface, explosão de partículas, tempo morto.
</direcao>

<estrutura>
120 BPM, 8 compassos, alguma coisa acontece em toda batida.
logo → página em branco com um título sendo digitado ("Plano de lançamento") → a página vira um quadro de tarefas com três colunas
→ o cursor arrasta um cartão de "A fazer" para "Fazendo" → o cartão abre e uma caixa de seleção é marcada
→ o cartão vai para "Feito" → o quadro encolhe e vira o botão "Compartilhar" → logo.
</estrutura>

<construcao>
1. Um arquivo HTML, um canvas, window.seek(t). Sem transições de CSS, sem timers, sem estado carregado.
2. Molas de forma fechada. Um valor com vários alvos = a soma de uma mola por mudança.
3. O texto dentro de um contêiner que se transforma entra depois que a transformação começa e sai antes que ela termine.
4. Indicadores de aba: borda da frente e borda de trás em molas diferentes, pra esticar.
5. Grade de batidas tirada da trilha (numpy/librosa). Começa num tempo forte. Sons de interface nos picos medidos.
6. Render no Chrome sem janela a 60 fps, 4 subquadros por quadro, misturados pra dar desfoque de movimento.
</construcao>

<pegadinhas>
Nunca usa will-change em nada que a câmera aproxima (o texto fica borrado).
O último quadro tem que ser igual ao primeiro, incluindo a posição e a velocidade do cursor.
</pegadinhas>

<comeco>
Me mostra a lista de estados na grade de batidas, em tabela, antes de escrever código.
Quando eu aprovar, renderiza e salva em resultados/07-lista-de-estados.mp4.
</comeco>

Monta o vídeo com o HyperFrames (npx hyperframes; precisa de Node.js 22+ e FFmpeg; se faltar algo, me avisa e me ajuda a instalar). Antes do render, abre a prévia com npx hyperframes preview, me passa o link pra eu ver no navegador e espera eu aprovar. Só renderiza o MP4 final depois do meu ok.
Trabalha só dentro de uma pasta nova chamada notion-estados/ e não sobrescreve nada que já existe.
```
