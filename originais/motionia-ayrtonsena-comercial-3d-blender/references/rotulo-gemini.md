# Rótulo planificado (Gemini)

O motor precisa da arte de cada lata **aberta numa folha reta**: é a textura que dá a volta na lata 3D. Quase ninguém tem esse arquivo, então a pessoa gera no Gemini a partir de fotos da lata. Passe o prompt abaixo pra ela colar junto com as fotos.

```
Vou te mandar fotos de uma lata de bebida (frente e costas). Recrie a arte do rótulo dela PLANIFICADA, como se a lata fosse cortada na vertical e aberta numa folha reta. Essa imagem vai virar textura de um modelo 3D, então siga estas regras à risca:

1. FORMATO: imagem retangular na horizontal, proporção 3:2, na maior resolução possível.
2. SEM 3D: nada de perspectiva, curvatura, reflexo de metal, brilho, sombra, gotas de água, luz ou fundo. Só a arte chapada, com cores lisas, como o arquivo de impressão que vai pra gráfica.
3. POSIÇÃO: a frente da lata (logo principal) fica bem no centro da imagem. As laterais ficam à esquerda e à direita do centro. A parte de trás fica dividida entre as duas pontas da imagem.
4. EMENDA: a borda esquerda precisa continuar na borda direita, sem corte visível, porque a imagem dá a volta completa na lata.
5. ALTURA: a arte ocupa só o corpo reto da lata. Não inclua a tampa, o pescoço afinado nem o fundo. Deixe uma faixa fina no topo e na base só com a cor de fundo do rótulo, sem logo nem texto.
6. FIDELIDADE: mantenha exatamente as cores, o logo, as fontes, os textos e os elementos gráficos da lata original. Não invente nada, não traduza e não mude a posição de nada. Se alguma parte não aparece nas fotos, repita o padrão das partes visíveis.
7. TEXTOS: escreva os textos exatamente iguais aos das fotos, letra por letra. Nos textos pequenos que não dá pra ler (ingredientes, tabela nutricional), não invente palavras: use linhas de texto pequenas e discretas no lugar.
```

**Proporção do item 1 por tamanho de lata:**

| Lata | Proporção |
|---|---|
| 350 ml fina / 250 ml fina | 3:2 |
| 269 / 310 ml fina e alta | 16:9 |
| 350 ml tradicional | 2:1 |
| 473 ml | 2:1 |

**Pra sair bom:**
- **Duas fotos por lata, frente e costas.** Com uma só, o Gemini inventa a parte de trás.
- **Resolução importa nos closes.** Se sair pequeno (o Gemini costuma entregar ~1376×768), peça "aumente a resolução dessa imagem sem mudar nada". A fábrica também amplia 2× o que tiver menos de 2000 px.
- **Confira os textos grandes** (nome, sabor, "zero açúcar"). O Gemini troca letra, e o close mostra.
- **O nome do arquivo vira o nome do modelo.** Ex.: `marca maracuja.png`. É esse nome que vai em `projeto.json` → `sabores[].modelo`.

**O que o motor faz sozinho:**
- pinta o pescoço com a cor do topo do rótulo (lata real é impressa até a borda);
- ajusta a exposição pelo brilho do rótulo (rótulo branco estoura fácil);
- nunca mostra de perto a parte de trás, porque ali os textos do Gemini vêm embaralhados.
