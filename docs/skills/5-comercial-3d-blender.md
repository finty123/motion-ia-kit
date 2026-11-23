# Skill 5: `motionia-ayrtonsena-comercial-3d-blender` (comercial 3D de lata no Blender)

**O que faz:** comercial de ~25 s (16:9, 1080p, 30 fps) de bebida em lata (energético, refri, cerveja, água), 100% por script: Blender (Eevee) nas latas, canvas HTML nos fundos e palavras, FFmpeg juntando, música mandando nos cortes. Cenas: gota na tampa, closes secos, lata trocando de sabor com frutas explodindo, cata-vento com rastro, corredor neon, fileira acendendo, logo em traço e @. Entrega **com e sem música**. Padrão do comercial Dane-se. Módulo 9 (prática com Guaraná Antarctica).

**Funciona em:** só **Claude Code**, com **Blender 4.2+** instalado (`INSTALAR.cmd -ComBlender` ou blender.org).

## O que ter em mãos
- Ideia e referências (se não tiver, ela abre uma **página de efeitos** no navegador do Claude pra você marcar "quero / talvez / não quero").
- Marca, sabores (1 a 6; com 4 o cata-vento fecha perfeito), tamanho da lata.
- **Rótulos planificados:** quase ninguém tem; ela te dá um prompt pro Gemini gerar a partir de fotos da frente e das costas.
- Logo PNG transparente, a música (MP3) e, se tiver, uma pasta de efeitos.
- Materiais da aula de exemplo: `materiais/9-lata-3d-guarana/` (logo, 2 rótulos, música).

## Como chamar
```
/motionia-ayrtonsena-comercial-3d-blender
Quero um comercial 3D de lata da [marca], sabores [x, y]. Rótulos e logo anexos, música [arquivo].
```

## O que acontece (não pule etapas)
1. `verificar.py` confere o PC (Blender, FFmpeg, Python, RAM, disco).
2. Ideia em 4 rodadas curtas (ideia → lata → conteúdo → som), tabela-resumo, ok.
3. Materiais: rótulos, logo, peças 3D gratuitas (ela mostra link, licença e tamanho antes; **login no site é sempre seu**), música, efeitos.
4. `novo_projeto.py` → `projeto.json` → latas (prévia de cada uma pra aprovar).
5. **Estrutura na batida** (`batidas.py`, `linha_do_tempo.py`) + **storyboard a lápis** → aprovação.
6. **Rascunho** (~25 min num PC médio) → ajustes no `projeto.json` → aprovação do movimento.
7. **Final:** ela mede o tempo antes de prometer horário (a hélice é ~70% do render). Opção rápida existe, mas ela pergunta.

## Peso no PC
É a skill mais pesada: horas no final. Um Blender por vez, em prioridade baixa. Com 16 GB de RAM funciona, mas evite usar o PC pesado durante o render.

## Na entrega
Os dois MP4 (com e sem música), créditos CC BY das peças pra legenda, aviso de direito autoral da música e o "COMERCIAL NÃO OFICIAL" na tela quando for o caso.
