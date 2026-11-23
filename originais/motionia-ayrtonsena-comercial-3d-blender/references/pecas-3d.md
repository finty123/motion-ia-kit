# Peças 3D (frutas, ingredientes, respingo)

As peças explodem de trás da lata a cada troca de sabor. O que decide se fica realista é o modelo: fruta modelada por código fica "de desenho" (o cliente reprovou). Use **scans reais e grátis**.

## Onde buscar
- **Poly Haven** (polyhaven.com/models): tudo CC0, sem login, sem crédito obrigatório. Pouca variedade de comida.
- **Sketchfab** (sketchfab.com, filtro "Downloadable" + licença CC): muita fruta escaneada. Quase tudo é **CC BY**, então o crédito é obrigatório na legenda do post. O download pede login.
- Busque em inglês: "lime slice scan", "mango photogrammetry", "watermelon 4k", "coffee beans", "ice cube", "mint leaf", "liquid splash".

## Antes de baixar
Mostre uma lista com, pra cada modelo: o que é, link, licença, tamanho do arquivo e quantas faces. Prefira **fatias e metades** (o corte colorido vira pra câmera) e, pra cada sabor, uma peça inteira e uma cortada. Pergunte e espere o ok.

**O login é sempre da pessoa.** Abra o navegador dela, ela entra na conta e você só clica em baixar. Nunca crie conta nem digite senha.

## Organizar
```
<projeto>/pecas/
├── 01-limao-rodela/      (o que veio no zip, descompactado)
├── 02-manga-metade/
├── ...
└── CREDITOS.txt          nome do modelo, autor, licença e link de cada um
```
Salve cada download na sua própria pasta e descompacte lá dentro.

## Declarar em projeto.json → "pecas"
Cada peça vira um objeto `pc_<nome>`. Campos:

| Campo | Pra quê |
|---|---|
| `arquivo` | pasta ou arquivo dentro de `pecas/` (gltf, glb, fbx, obj ou blend) |
| `so` / `excluir` | quando o arquivo traz várias partes: pega só as que têm (ou não têm) esse texto no nome |
| `sss` | luz passando por dentro (0,3–0,45 em polpa e fatia) |
| `verniz` | camada molhada (padrão 0,55; 0,25 em polpa clara, senão acinzenta) |
| `clarear` | `[valor, saturação]` pra peça clara que some em fundo claro (ex.: limão `[1.5, 1.3]`) |
| `agua` | `true` no respingo: vira água transparente com bordas brilhando (nunca branco leitoso) |
| `face_corte` | direção do corte no objeto (ex.: `[0, 0, -1]`), pra o corte virar pra câmera. Descubra num quadro de teste das trocas: se a casca aparece no lugar do corte, inverta o sinal. |
| `max_faces` | reduz scans pesados (padrão 150 mil) |
| `fatia_de` + `angulos` + `espessura` + `polpa` + `sementes` | corta fatias de uma peça inteira (ex.: melancia) e pinta a face cortada |

Depois, em cada sabor: `"pecas": [["pc_limao_rodela", 0.65, 1.35], ["pc_limao_inteiro", 0.35, 1.35]]`, que quer dizer nome, chance no sorteio e tamanho (a lata tem ~5 de altura). Use `"qtd"` pro número de peças (padrão 12). Num sabor de água, use `"respingo": true` em vez de peças.

Rode `python rodar.py pecas` e confira o log: cada peça tem que aparecer com o número de faces. Pra ver as peças, renderize um quadro de teste das trocas (`python rodar.py giros rascunho <quadro>`).

## Exemplo real (Dane-se)
Veja `assets/exemplo-danese/projeto.json`. Lá estão limão (rodela + inteiro), manga (fatia, metade, inteira), melancia (scan inteiro cortado em fatias com polpa e sementes) e respingo de água. Os créditos que foram na legenda:

> Modelos 3D: "FREE Low poly - Watermelon photogrammetry 4K" por Naked Singularity, "Mango & Cut Half Mango Fruit" por Kami Rapacz, "Mango Slice Without Pit 3D Fruit Scan" e "Lime Slice 3D Scan" por Arkify, "Liquid Splash 2" por MAMA's Sneaker Stop (CC BY 4.0, Sketchfab). Limão: Poly Haven (CC0).
