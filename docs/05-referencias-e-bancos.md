# Sites de referência e bancos gratuitos

Listas que vieram nos PDFs do curso (aula 4.1, aula 2 do telão e bônus).

## Onde procurar referência de motion

Use dois tipos de referência sempre (aula 3.1): **design** (fonte, cores, composição) e **animação** (como as coisas se mexem). Diga ao Claude o que tirar de cada uma.

| Site | Bom pra |
|---|---|
| https://prompt-motion.com | prompts e exemplos de motion feitos com IA |
| https://skillry.dev/ai-videos/opus-5-5 | galeria de vídeos feitos com Claude (Opus 5.5) |
| https://whatships.com | lançamentos de produtos e apps (filmes de produto) |
| https://www.pinterest.com | referência rápida de design e de motion |
| https://www.behance.net | projetos completos de motion e branding |
| https://dribbble.com | interfaces e microanimações |
| https://savee.it | moodboard de design |
| https://godly.website | sites com animação forte |
| https://www.awwwards.com | sites premiados (movimento e tipografia) |
| https://mobbin.com | telas reais de apps (pra recriar interface) |
| https://motionographer.com | motion design profissional |
| https://lottiefiles.com | animações vetoriais prontas |

## Bancos de imagens e vídeos gratuitos

| Banco | O que tem | Atenção |
|---|---|---|
| Pixabay (pixabay.com) | fotos, vídeos, vetores, músicas e efeitos sonoros | sem cadastro e sem crédito obrigatório |
| Pexels (pexels.com) | fotos e vídeos, muito vertical bom pra Reels | uso livre |
| Unsplash (unsplash.com) | fotos com cara de editorial | filtre só as gratuitas (há Unsplash+) |
| Mixkit (mixkit.co) | vídeos, músicas, SFX e templates | grátis, sem cadastro |
| Coverr (coverr.co) | vídeos curtos de fundo / B-roll | |
| Videvo (videvo.net) | vídeos e elementos de motion | marque o filtro "Free" |
| Freepik (freepik.com) | vetores, ilustrações, PSDs, fotos | no grátis precisa dar crédito |

Antes de usar em trabalho de cliente, confira a licença do arquivo: foto com pessoa, marca ou logo pode ter restrição mesmo em banco grátis.

## Efeitos sonoros do kit

A pasta `sfx/` tem 20 efeitos (Pixabay, licença livre): cliques, pops, whooshes, impactos, glitches, digitação, notificação, riser. O `sfx/manifest.json` descreve cada um. O instalador copia esse pacote pra dentro das skills que usam efeitos de interface (`assets/sfx-kit/` das skills Nubank, iFood e lata 3D). Se tiver uma pasta própria de efeitos, ponha o caminho em `pasta_sfx` no `config.json`.
