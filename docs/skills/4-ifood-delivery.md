# Skill 4: `motionia-ayrtonsena-ifood-delivery` (comercial de comida e delivery)

**O que faz:** comercial horizontal (1920×1080, 30 fps, 40–50 s) de app de delivery, restaurante ou comida: cores chapadas trocando a cada cena, tipografia gigante e engraçadinha acompanhando a fala, celular 3D, logo letra a letra, app recriado em vetor, comidas reais em câmera 3D com preço, sacola, entregador, mapa e @ no final, tudo na batida da música. Padrão do "Motion iFood – Fome de madrugada" (13 cenas em `assets/modelo/`). Módulo 10 (prática com Burger King).

**Funciona em:**
- **Claude Code + HyperFrames:** briefing, copy e o vídeo inteiro até o MP4.
- **Chat:** briefing e copy + um **pacote de pré-produção** (conceito, copy, texto pro ElevenLabs, tabela de cenas, guia visual, lista de materiais e um prompt pronto pra colar no Claude Code).

## O que ter em mãos
- **Narração** (é o relógio). Pode ser bruta com vários takes: `remontar_narracao.py` monta. Áudio de WhatsApp abafado: `voz_clara.py` clareia.
- **Logo oficial em SVG** (nunca redesenhar; exemplo em `materiais/10-ifood-burger-king/`).
- **Fotos das comidas** (ela recorta e limpa bordas com `limpa_borda.py`, `so_maior.py`, `recortar_fundo_liso.py`).
- Telas reais do app e a música da marca, se tiver.

## Como chamar
```
/motionia-ayrtonsena-ifood-delivery
Quero um comercial estilo iFood pro [restaurante/app]. Logo SVG, fotos e narração anexos.
```

## O que acontece
1. Briefing (referência, estilo, cores, narração, comidas, final) → copy e roteiro com tabela de cenas (aprovação).
2. Projeto HyperFrames a partir do modelo; **batida primeiro** (`npx hyperframes beats` + `batida.py`): fala, cortes, trocas de cor e pops entram na grade.
3. Faz **o começo no nível final** e mostra (snapshots lado a lado com a referência + prévia). Só depois faz o resto.
4. Som: voz clara, efeitos pelo golpe de cada arquivo (`efeitos.py`), música com volume automático (~0,12 sob a fala, ~0,3 sem fala).
5. `npx hyperframes check` sem erros → prévia completa → aprovação → `render_leve.py` (4 workers, prioridade baixa, −14 LUFS).

## Dicas
- A skill pede pra usar junto a skill `/hyperframes`. Se quiser instalá-la: `npx -y hyperframes skills` (opcional).
- Efeitos: as tabelas dela citam a pasta pessoal do autor; neste PC ela usa os equivalentes do `sfx/` (tabela no fim do SKILL.md instalado).
