# Pipeline técnico

## Pasta do projeto
```
<projeto>/
├── motor/            scripts (copiados da skill) + projeto.json + beats.json + assets/
│   └── assets/       logo.png, logo_contornos.js, condensacao_*.png, sfx/, cfg.js (gerado)
├── rotulos/          rótulos planificados (nome do arquivo = nome do sabor no projeto.json)
├── modelos/<sabor>/  rotulo_2x.png (o que a cena usa), lata.blend, previa.jpg
├── pecas/            modelos baixados + pecas.blend + CREDITOS.txt
├── musica/           a trilha
├── referencias/      referências da pessoa
├── render/<qualidade>/<plano>/f_####.png   tras/ e frente/ (canvas), lata3d/ (junção), testes/
├── resultados/       folhas de contato, vídeos de rascunho e prévia
├── logs/
└── <Marca> comercial 3D (com musica).mp4 / (sem musica).mp4   o final
```

## Scripts (motor/)
| Script | Faz |
|---|---|
| `config.py` / `linha_do_tempo.py` | Lê `projeto.json` + `beats.json`; calcula batidas, quadros, cores, tamanho da lata. `python linha_do_tempo.py` grava a linha do tempo e sugere o corte da música. |
| `batidas.py <mp3> [batidas]` | BPM, batidas, força, **pausas** e trecho sugerido → `beats.json`. Sem librosa. |
| `latas.py` + `fazer_lata.py` | Fábrica: rótulo → `modelos/<sabor>/` com prévia (frente, giro, tampa), ~40 s por lata. |
| `condensacao.py` | Mapas de gotas/escorridos/névoa (assets/, ~45 MB). Roda uma vez; pode copiar de outro projeto. |
| `contorno_logo.py <logo>` | Logo centralizado em 500×500 + contorno das letras pro stroke. Confira `logs/logo_contornos.png`. |
| `preparar_pecas.py` | Peças baixadas → `pecas/pecas.blend` (via `rodar.py pecas`). |
| `lata_lib.py` | Lata, materiais (rótulos trocáveis, condensação, neon), luz, câmera, `render()`, `renderizar()` (pula quadros prontos, então retoma de onde parou). |
| `comercial.py` | Os 5 planos: `queda`, `detalhes`, `revela`, `giros`, `helice`. |
| `camadas.html` + `camadas.py` | Canvas por quadro (`window.seek`): fundos, palavra atrás (`tras`), cartão final com stroke (`frente`). Playwright + Chrome. |
| `mixar.py` | Efeitos nas batidas (alinhados por início, pico ou fim) + música com corte, -14 LUFS → `render/audio_*.wav`. |
| `sfx_mapear.py <pasta>` / `sfx_sintetico.py` | Escolhe os SFX da pasta da pessoa / gera os que faltarem. |
| `storyboard.py [--so-png]` | Rascunho a lápis (um quadro por cena) a partir da estrutura → `resultados/storyboard.html` + `.png`, com a regra de não copiar o visual. |
| `compor.py <qualidade>` | Junta trás + 3D + frente, glow leve, áudio → MP4 com e sem música + folha de contato. |
| `rodar.py` | Orquestra: um Blender por vez, prioridade baixa, log, tempo por quadro, alarme só no final. |
| `ampliar.py` | Versão com pressa: hélice da prévia ampliada pra 1080p onde falta o quadro final. |
| `sistema.py` | Acha o Blender (Windows/Mac/Linux), confere se já tem um aberto, prioridade baixa, alarme. |

## Comandos
```bash
python rodar.py <plano> rascunho 300,420,520   # quadros soltos (render/testes) - OLHE as imagens
python rodar.py medir helice final             # 3 quadros -> estimativa real do plano
python rodar.py tudo rascunho                  # vídeo inteiro em 640x360 (~25 min num PC médio)
python rodar.py tudo final                     # 1080p, alarme no fim
python rodar.py rapido                         # planos leves em 1080p, hélice em prévia ampliada
python rodar.py refazer giros rascunho         # apaga os quadros do plano e renderiza de novo (depois de um ajuste)
python compor.py final --so-com-musica         # remonta o vídeo sem renderizar nada
```
Rode render longo em background e acompanhe pelas pastas de quadros, sem checar a cada minuto.

## Qualidades (tempo medido no PC de referência: i5-12400F, 16 GB, GTX 1050 Ti)
| | resolução | amostras | hélice por quadro | vídeo inteiro |
|---|---|---|---|---|
| rascunho | 640×360 | 6 | ~6 s | ~25 min |
| previa | 960×540 | 16 | ~11 s | ~1 h |
| final | 1920×1080 | 24 (`AMOSTRAS_FINAL`) | ~32 s | ~3–4 h |
A hélice (~300 quadros, dezenas de latas) é ~70% do tempo; o custo é a cena, não as amostras. Em outro PC, meça com `rodar.py medir` antes de prometer horário.

## Montagem (compor.py)
- Antes dos detalhes: `queda`. Nos detalhes: 4 closes, cada um renderizado com 1 batida a partir da revelação e usado por meia batida.
- Depois: o primeiro que existir em `revela`, `giros`, `helice`, `helice_rapido`.
- Quadro 3D faltando antes do logo gera `AVISO: quadros 3D faltando`. Não entregue com esse aviso.
- O glow é feito em RGB (`format=gbrp`). Em YUV, o blend screen deixa tudo magenta.

## Hélice (o plano pesado)
- Câmera por **velocidade integrada quadro a quadro** (`trajeto_camera`). Curva Bézier dá overshoot e faz a câmera voltar; a velocidade nunca pula, então nunca há travada nem volta. Simule a trajetória antes de renderizar se mudar algo.
- O furo abre aumentando o raio do cata-vento (`ABRE_FURO`). Cruz e cópias somem 2 quadros depois do furo; o fundo vai da cor do sabor pro escuro em ~1 batida.
- A fileira aparece assim que a câmera passa o último anel (+6 quadros), senão vira um buraco preto.
- Motion blur: obturador 0,12 no rastro (cópias nítidas), 0,5 no resto, `motion_blur_position = "START"` pra não vazar nos cortes secos.

## Bugs já resolvidos (não repetir)
- `matrix_world` sem `view_layer.update()` é a identidade: os closes miravam a parte de trás da lata.
- View "Standard" + look "Medium High Contrast". O AgX deixava o rosa pastel.
- Luz de cima sobre a tampa estoura fácil.
- Refração do Eevee fica preta em fundo escuro e cinza/suja em rótulo claro: gotas viram mapa de condensação, água vira Fresnel + painel de estúdio invisível.
- Blender 4.2–4.4 usa `BLENDER_EEVEE_NEXT`; versões mais novas voltaram pra `BLENDER_EEVEE` (o motor tenta os dois).
- Logo sem arquivo travava as camadas (a página esperava o carregamento pra sempre). Agora segue sem logo, mas rode o `contorno_logo.py` antes do final.
- Corte de música no meio da batida desloca o ritmo inteiro: o cata-vento (e portanto o furo) sempre cai em batida inteira.
- No Windows deste PC, WMI/tasklist estavam quebrados ("Classe inválida"). O `sistema.py` usa psutil ou `Get-Process`.
- Parar a tarefa do terminal não mata o Blender filho; mate o python da cadeia e o Blender antes de religar.
- Script Python longo dentro de heredoc no Bash quebra com aspas e barras: escreva o script num arquivo e rode.

## Mexendo no motor
Pra pedidos fora do arco (outra cena, outro movimento), edite `comercial.py` **na pasta do projeto**, não na skill. Teste com quadros soltos em rascunho, olhe, e só então rode o vídeo. Se a mudança servir pra todo projeto, leve pra skill depois, junto com a regra em `erros-e-licoes.md`.
