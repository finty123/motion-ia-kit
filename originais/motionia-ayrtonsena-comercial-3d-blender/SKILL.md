---
name: motionia-ayrtonsena-comercial-3d-blender
description: "MotionIA @ayrtonsena.stg — Comercial 3D de lata (energético, refri, cerveja, água) do zero ao MP4, no padrão aprovado do comercial Dane-se, feito no Blender. Faz as perguntas em rodadas (ideia, referências, marca, sabores, tamanho, música), abre uma página pra escolher os efeitos de referência, gera o storyboard a lápis, encaixa tudo na batida da música e entrega com e sem música. O vídeo: gota na tampa, closes secos, lata trocando de sabor com frutas explodindo, cata-vento com rastro, corredor neon, fileira acendendo, logo em traço e @. Use SEMPRE que pedirem comercial 3D de lata, vídeo 3D de bebida, 'igual o da Dane-se', 'lata girando em 3D', mandarem rótulos ou fotos de lata pedindo vídeo, ou ajustes de um comercial desses, mesmo sem citar a skill. Não usar pra comercial narrado de lata em HyperFrames (motionia-ayrtonsena-lata-3d) nem motion 2D de app ou serviço."
---

# Comercial 3D de lata no Blender

Comercial de ~25 s (16:9, 1080p, 30 fps) de uma marca de bebida em lata, feito 100% por script: Blender (Eevee) nas latas, um canvas HTML nos fundos, palavras e cartão final, ffmpeg juntando tudo, e a música mandando em cada corte. O padrão é o comercial **Dane-se** (aprovado em 31/10/2026); veja `assets/exemplo-danese/folha-de-contato-final.png` pra saber onde chegar.

O motor em `scripts/motor/` já carrega todas as correções desse projeto. Adaptar é trocar o `projeto.json`, não reescrever código. Antes de começar, leia **`references/erros-e-licoes.md`**: cada erro ali custou uma rodada de render de horas.

## O caminho (não pule etapas)
1. Conferir o PC
2. Ideia: perguntas em rodadas
3. Materiais: rótulos, logo, peças 3D, música, efeitos
4. Montar o projeto e aprovar as latas
5. Estrutura na batida e aprovação
6. Rascunho e aprovação do movimento
7. Final, conferência e entrega

Em cada aprovação, **pare e espere a resposta**. Aprovar no papel e no rascunho é barato; refazer o final custa horas.

## 1. Conferir o PC
```bash
python <skill>/scripts/verificar.py
```
Ele lista o que tem e o que falta (Blender 4.2+, FFmpeg, pacotes Python, navegador do Playwright, RAM, disco) sem instalar nada. Se faltar algo, diga o comando de instalação e peça pra pessoa instalar, ou instale com o ok dela. Com menos de 16 GB de RAM, avise que a hélice vai ser lenta e que é melhor não usar o PC pesado durante o render.

**O PC manda no ritmo:** um Blender por vez, sempre em prioridade baixa (o `rodar.py` cuida). Dê previsão de horário só depois de **medir** (`rodar.py medir`), nunca no chute.

## 2. Ideia
Siga `references/perguntas.md`: 4 rodadas curtas (ideia → lata → conteúdo → som), cada pergunta com a sugestão padrão. Antes, olhe tudo o que a pessoa já mandou e só pergunte o que falta.

**A primeira mensagem sempre pergunta se a pessoa já tem uma ideia em mente e se já tem referências.** Sem referência (ou com pouca), abra a **página de efeitos no navegador de dentro do Claude** (gere com `python <skill>/scripts/escolher_referencias.py "<projeto>/referencias" [vídeos dela]`, sirva a pasta pelo `preview_start` com uma configuração no `.claude/launch.json`; detalhes em `references/referencias.md`): cada referência roda em vídeo e a pessoa marca quero / talvez / não quero, com observação, e você lê as escolhas direto da página. As referências dela entram na mesma página. Com referência, estude do jeito descrito lá: tira de quadros, uma linha de movimento por vídeo e onde cada um entra na estrutura. Use sempre só o movimento, nunca o visual de outra marca.

Até a estrutura ser aprovada não tem render: nada de Blender nessa fase.

Feche a etapa com uma tabela-resumo (marca, sabores com cor, palavra e peças, tamanho, música, pasta) e espere o ok.

## 3. Materiais
- **Rótulos:** passe o prompt de `references/rotulo-gemini.md`, com a proporção do tamanho da lata. Confira cada rótulo que voltar (textos grandes certos, arte chapada, logo no centro) antes de usar.
- **Logo:** PNG oficial com fundo transparente (do site ou da pessoa).
- **Palavras:** só as reais da marca (site, rótulo, Instagram). Nada inventado: nem slogan, nem número, nem avaliação.
- **Peças 3D:** scans grátis (`references/pecas-3d.md`). Mostre a lista com link, licença e tamanho e espere o ok. **O login no site é sempre da pessoa**; nunca crie conta nem digite senha. Guarde os créditos CC BY.
- **Música:** o MP3 que a pessoa escolher. Sem narração (o estilo é música + efeitos).
- **Efeitos:** a pasta de SFX dela, se tiver. Se não tiver, o motor gera sons cinematográficos.

## 4. Montar o projeto
```bash
python <skill>/scripts/novo_projeto.py "<pasta do projeto>" "<Marca>"
```
Isso cria a estrutura (`references/pipeline-tecnico.md`) e copia o motor pra `<projeto>/motor/`. Daqui pra frente, rode tudo de dentro de `motor/`.

1. Preencha `motor/projeto.json` com o briefing (`references/projeto-json.md`; exemplo real em `assets/exemplo-danese/projeto.json`). Tire a cor de fundo de cada sabor do próprio rótulo.
2. Rótulos em `rotulos/` → `python latas.py` → mostre cada `modelos/<sabor>/previa.jpg` e espere o ok.
3. `python condensacao.py` (mapas de gotas, uma vez só; pode copiar de outro projeto).
4. `python contorno_logo.py <logo.png>` e olhe `logs/logo_contornos.png`.
5. Peças: declare em `projeto.json` → `pecas` e rode `python rodar.py pecas`.
6. Efeitos: `python sfx_mapear.py "<pasta de SFX>"` (mostre o que ele escolheu) ou pule pra usar os sintéticos.

## 5. Estrutura na batida
Só precisa da música e da lista de sabores no `projeto.json`, sem as latas prontas. Se a pessoa pedir a estrutura primeiro, faça esta etapa antes da fábrica (passo 4.2) e volte nas latas depois do ok.
```bash
python batidas.py ../musica/<trilha>.mp3     # BPM, batidas, pausas, trecho sugerido
python linha_do_tempo.py                     # batidas de cada cena + corte da música
```
Coloque `musica.inicio` no `projeto.json` antes do segundo comando: o trecho sugerido, ou o ponto que a pessoa escolher. Mostre a tabela que ele imprime, com os segundos e o que acontece em cada cena (`references/estrutura.md` explica o arco e como adaptar).

Depois gere o **storyboard de rascunho** (sempre, não só se pedirem):
```bash
python storyboard.py      # resultados/storyboard.html + storyboard.png
```
É um rascunho a lápis, um quadro por cena, montado com os dados do projeto (sabores, cores, palavras, peças, tempos, final, @). No topo vai a regra de que é só rascunho de montagem e o visual dele não vai pro vídeo. Olhe o PNG antes de mandar e mostre a imagem pra pessoa. Se a ideia dela tiver algo fora do arco padrão, edite a lista `cenas` no `storyboard.html` (nome, tempo, câmera, tela, som; tipo de desenho ou `desenho` com texto) e rode `python storyboard.py --so-png`.

Tabela e storyboard são aprovados juntos. **Espere o "aprovado".**

## 6. Rascunho
1. Quadros soltos de cada plano em rascunho e **olhe as imagens**:
   ```bash
   python camadas.py rascunho 100,300
   python rodar.py queda rascunho 60
   python rodar.py giros rascunho <quadro de uma troca>
   python rodar.py helice rascunho <3 quadros>
   ```
   Confira: o foco do rótulo de frente no fim da queda, as peças com o corte virado pra câmera, a palavra atrás da lata, as latas separadas no cata-vento, luz sem estourar.
2. `python rodar.py tudo rascunho` em background (~25 min num PC médio). Sai o vídeo em `resultados/` e a folha de contato (1 quadro por batida).
3. Confira a folha inteira e o log (`AVISO: quadros 3D faltando`, `Traceback`). Mande o vídeo do rascunho pra pessoa.
4. Ajustes: mexa no `projeto.json` (tempos, cores, palavras) ou, se for movimento novo, no `comercial.py` da pasta do projeto. Depois de mudar uma cena, use `python rodar.py refazer <plano> rascunho`: o motor pula quadros que já existem, então os antigos precisam sair.
5. Se ela mandar uma edição porca por cima do rascunho, ela vira a referência de tempo (`references/estrutura.md`).

Repita até aprovar o movimento.

## 7. Final e entrega
1. `python rodar.py medir helice final` e diga o horário previsto (a hélice é ~70% do tempo).
2. `python rodar.py tudo final` em background. Só ele toca o alarme.
3. Se a pessoa estiver com pressa, ofereça as opções com tempo medido: final cheio, ou `python rodar.py rapido` (hélice em prévia ampliada, bem mais rápido, um pouco menos nítido no fim). Pergunte antes.
4. Confira a folha de contato do final e o log.
5. Entregue o MP4 com música e diga, na mesma mensagem:
   - onde estão os dois MP4 (com e sem música);
   - os créditos CC BY das peças, pra legenda do post;
   - o aviso de direito autoral da música (a versão sem música serve pra usar com música do Instagram);
   - que "COMERCIAL NÃO OFICIAL" já está na tela, se for o caso.

Toda correção da pessoa que valer pra próximos vídeos entra em `references/erros-e-licoes.md` na hora.

## Se for o Ayrton (@ayrtonsena.stg)
- Assinatura: `@AYRTONSENA.STG`.
- SFX: `C:\Users\Ayrton\Downloads\Efeitos sonoros` (ou o pack em `D:\Backup\Videos\#clientes\SFX-...`).
- Pasta de cliente: `D:\Backup\Videos\#clientes\<cliente>\`. O C: vive cheio, então render vai pro D:.
- O projeto Dane-se original está em `D:\Backup\Videos\#clientes\Ayrton Sena\Video 3dDanese`. Peças, mapas de condensação e o logo de lá podem ser copiados.
