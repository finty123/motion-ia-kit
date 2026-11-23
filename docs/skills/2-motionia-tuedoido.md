# Skill 2: `motionia-tuedoido` (motion narrado com tipografia 3D)

**O que faz:** transforma uma **narração** num vídeo completo, até o MP4: cada palavra importante vira tipografia 3D que entra girando com impacto, câmera 3D sempre em movimento, fundo trocando de cor a cada ideia, glow, desfoque, simulações de interface (chat, post, DM) e CTA "comenta X". Estilo do vídeo "Motion com IA" do módulo 5.

**Funciona em:** feita pro chat do Claude.ai; neste kit ela também roda no Claude Code (o instalador ajustou os scripts pro Windows e explicou os caminhos no fim do SKILL.md).

## O que ter em mãos
| Material | Obrigatório? | Se faltar |
|---|---|---|
| Narração (mp3/wav/m4a) | sim, é o relógio do vídeo | grave no celular num lugar quieto; sem voz ela usa a música como relógio (fica menos sincronizado) |
| Música | não | sai só com voz e efeitos |
| Paleta (2–4 cores hex) | sim | ela propõe uma e confirma |
| Logo PNG (fundo transparente) | recomendado | fecha com o nome em 3D |
| Objetivo, preço e palavra do CTA | sim | ela pergunta |

## Como chamar
```
/motionia-tuedoido
Faz o motion dessa narração [arraste o áudio]. Música anexa. Produto: [x], preço [de/por], CTA "comenta [PALAVRA]". Formato 16:9.
```

## O que acontece
1. **Inventário + uma rodada de perguntas:** intensidade (máxima / forte / elegante), final (com respiro ou tudo cortado), formato.
2. **Análise automática:** transcrição palavra por palavra (Whisper), corte dos respiros da fala, BPM e picos da música (ela alinha a batida forte no nome do produto e a queda no preço), logo com fundo removido.
3. **Mapa de cenas + prompt** (no molde da skill 1), uma cena por frase.
4. **Construção:** escreve o `scenes.js` em cima do motor pronto, tira uma folha de contato e se dá nota (gancho, legibilidade, nada de texto sobre texto, centralização, margens, variedade, 3D real, glow). Corrige os 3 piores até tudo 8+.
5. **Render em segundo plano + mix** (voz > efeitos > música, −14 LUFS) e entrega.

## Peso no PC
Render a 30 fps com desfoque de movimento, em blocos de 5 s que retomam se cair. Um vídeo de 80 s leva uns 15–25 min. Ajuste de um trecho = apagar só os blocos daquele trecho em `_blocos/`.

## Dicas
- O Whisper erra nomes ("caldo" no lugar de Claude). Na tela vale o que foi falado: confira a lista de palavras que ela mostra.
- Pausas que você quer manter (depois do nome, do preço, antes do CTA) vão no `--keep`; o resto dos respiros ela corta.
