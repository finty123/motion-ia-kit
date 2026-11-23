# Skill 3: `motion-ia-ayrton-nubank-app-style` (comercial de app, estilo Nubank)

**O que faz:** comercial horizontal (1920×1080, 60 fps, ~35 s) de app, banco, fintech ou SaaS: fundo claro com respiro, vidro estilo Liquid Glass, 3D realista (celular, moedas, caixinha), mão segurando o celular com a palavra atrás, câmera seguindo objetos, ícones girando tipo showreel, final com logo e assinatura. Parte do projeto aprovado do Motion Nubank (`assets/modelo/`). Módulo 7.

**Funciona em:** só **Claude Code** (precisa do HyperFrames no PC pra prévia e render).

## O que ter em mãos
- Marca e o que do app mostrar (ex.: Pix, cartão, caixinhas).
- Logo, cores, telas reais do app (ou referência), foto/PNG da mão com celular (há um exemplo em `materiais/7-nubank/`).
- Narração: ela escreve o roteiro e te entrega o **texto pronto pro ElevenLabs**; você gera a voz e devolve o arquivo.

## Como chamar
```
/motion-ia-ayrton-nubank-app-style
Quero um comercial estilo Nubank pro app [marca].
```
Ela conduz tudo: você só responde.

## O que acontece
1. **Briefing** (perguntas clicáveis): objetivo, tom, duração (~25 / ~35 / ~45–60 s) e final (logo + assinatura, logo + loja, ou CTA "comenta").
2. **Roteiro em 7 atos**, aprovado antes de tudo. A duração sai da contagem de palavras (~2,3 palavras/s: 35 s ≈ 65–75 palavras).
3. **Materiais** → `novo_projeto.py` cria a pasta do projeto a partir do modelo e registra a prévia.
4. **Mapa de cenas → construção → conferência** por folha de contato (texto atrás de objeto, celular cobrindo frase, moedas cortadas no rodapé).
5. **Áudio:** SFX de UI em cada ação (clique, digitação, pop, whoosh, brilho) da pasta `sfx/` do kit + música + voz.
6. **Prévia** no navegador → você aprova → **render** (`-q delivery`, ~2–3 min pra 35 s) → cópia pra pasta de resultados.

## Dicas
- Abra o Claude Code **na pasta de projetos** (a prévia depende do `.claude/launch.json` de lá; o instalador já criou).
- Leia/peça pra ela seguir `references/regras-do-ayrton.md`: são as correções de estilo aprovadas (movimento com arrasto e assentamento, abertura grande, celular à esquerda...).
- Valores na tela são ilustrativos; promessas só as que a marca faz de verdade.
