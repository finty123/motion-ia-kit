# projeto.json (fica em `<projeto>/motor/`)

Tudo o que muda de uma marca pra outra está aqui; os scripts leem dele. Exemplo completo e real: `assets/exemplo-danese/projeto.json`.

| Campo | O que é |
|---|---|
| `marca` | Nome usado nos arquivos de saída ("<marca> comercial 3D (com musica).mp4"). |
| `nao_oficial` | `true` em comercial de portfólio. Lembrete pra manter `final.aviso`. |
| `assinatura` | O @ que fecha o vídeo (ex.: `@AYRTONSENA.STG`). Vazio = sem assinatura. |
| `cor_marca` | Cor do brilho do stroke do logo. |
| `fontes.display` / `display_peso` / `texto` | Google Fonts. A display é a da palavra gigante (condensada, pesada); a de texto é a das linhas finais. Confira se a display tem acento (Ç, Ã): se não tiver, evite palavra com acento ou troque a fonte. |
| `lata.altura_mm` / `diametro_mm` | Tamanho real. A cena mantém a altura e escala o diâmetro. |
| `lata.foco_rotulo` | Altura do ponto do rótulo que a câmera encara no fim da queda (0 = pé do rótulo, 1 = topo). Dane-se: 0,46 (o olho). Ajuste pro logo de cada lata. |
| `fundo_abertura` | Gradiente da abertura (escuro, puxando pra cor do sabor 1). |
| `fundo_cruz` | Cor do fundo fixo do cata-vento. Padrão: a cor do sabor 1. |
| `sabores[]` | Na ordem em que aparecem. O 1º é o da abertura. |
| `sabores[].modelo` | Nome da pasta em `modelos/` (= nome do arquivo do rótulo sem extensão). |
| `sabores[].cor` | Cor de luz do sabor (contraluz, neon). Hex direto, vibrante. |
| `sabores[].fundo` | `[centro, borda]` do fundo nas trocas. Tirado da cor de fundo do rótulo. |
| `sabores[].palavra` / `cor_palavra` | Palavra gigante atrás da lata (só palavra real da marca; vazio = sem palavra). |
| `sabores[].pecas` / `qtd` / `respingo` | O que explode (veja `pecas-3d.md`). |
| `pecas` | Como montar cada peça a partir dos arquivos baixados (veja `pecas-3d.md`). |
| `final.linha` / `final.aviso` | Linha do produto e o aviso "COMERCIAL NÃO OFICIAL". |
| `musica.arquivo` | Caminho relativo à pasta do projeto (ex.: `musica/trilha.mp3`). Vazio = só efeitos. |
| `musica.inicio` | Segundo da música onde começa o vídeo (batida 1). Use um tempo forte. |
| `musica.corte` | `[batida do vídeo, batida do trecho]`: pula a música nesse ponto (o `linha_do_tempo.py` sugere). `null` = sem corte. |
| `musica.volume_db` | Volume da música em relação aos efeitos (padrão -5). |
| `musica.bpm` | Só se o `batidas.py` errar o BPM (ele às vezes pega o dobro ou a metade). |
| `sfx.pasta` / `sfx.arquivos` | Preenchido pelo `sfx_mapear.py`. Tipo sem arquivo = som sintético. |
| `linha_do_tempo` | Batidas de cada cena (gerado). Edite à mão pra ajustar o tempo. |
| `blender` | Caminho do blender, se ele não for achado sozinho. |
