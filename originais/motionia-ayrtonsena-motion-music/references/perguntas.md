# Perguntas e sugestões

## Rodada 1: antes da música

Uma rodada só. O que a pessoa já disse não se pergunta de novo.

**Opções clicáveis (no Code, `AskUserQuestion`; até 4 perguntas):**

1. *Onde estamos?* (header "Ambiente")
   - "Claude Code (Recomendado)": prévia e render no HyperFrames, com aprovação antes do MP4.
   - "Chat": exporta o MP4 direto, sem prévia.
2. *Formato?* (header "Formato")
   - "16:9 horizontal"
   - "9:16 vertical"
   - "1:1 quadrado"
   - "Quadrado dentro do vertical": cena 1:1 no meio e a mesma cena borrada com retícula em cima e embaixo.
3. *Final?* (header "Final")
   - "Vácuo + assinatura (Recomendado)": buraco negro suga a música com close-up e entra "by @<teu arroba>" parado com glow.
   - "Só assinatura": "by @<teu arroba>" parado com glow, sem o vácuo.
   - "Sem final": termina no último impacto.
4. *Quer mandar materiais?* (header "Materiais", multiSelect)
   - "Capa do álbum / fotos do artista"
   - "Logo ou PNGs"
   - "Vídeos ou referência de edit"
   - "Não, pode desenhar tudo"

**Em texto, junto:**
- Se escolheu um final com assinatura: **qual é o teu @** (ou o nome que vai assinar)? Nunca preencha com um @ que a pessoa não deu, e nunca use o `@ayrtonsena.stg` dos exemplos (é do autor da skill). Sem resposta, o vídeo sai sem assinatura.
- Manda a música (mp3, m4a, wav ou vídeo) e diz o trecho exato (de que segundo a que segundo), ou se é a música inteira.
- Se tiver: a letra certa (ajuda quando o Whisper erra) e algum momento que já imagina ("quando ela fala X, quero Y").

Detecção do ambiente: `/mnt/user-data` existe = chat; Windows com `C:\Users\...\Downloads` = Code. Se detectar, diga "pelo que vejo estamos no Code" e pergunte só pra confirmar.

**Não sugira estilo, paleta nem cena nesta rodada.** Sem ouvir a música, qualquer sugestão é chute.

## Rodada 2: depois do raio-x (molde da resposta)

```
**A música:** <BPM> BPM, <clima em 3–5 palavras>. Começa <como>, respira em <a–b s>, as batidas principais caem em <t1>, <t2>, <t3>.

**A letra em imagens** (só palavras-chave na tela):
- <PALAVRA> (<t> s): <o que vira: objeto/ação/cenário>
- ... (5 a 8 itens)

**Estilos que combinam com ela:**
1. **<Nome do estilo>**: <por que combina com esta música, 1 frase>.
   Paleta: <fundo #hex> · <destaque #hex> · <apoio #hex> · glow <#hex>
   Fontes: <principal> (palavra forte) · <apoio> · <script/detalhe>
   Cenas: <t> s <palavra> → <cena>; <t> s <palavra> → <cena>
   Transições/lente: <...>
2. ...
3. ...
(4. opcional)

Pode misturar (ex.: abertura do 1 e refrão do 3). Se quiser mandar capa, fotos ou fontes, manda que eu encaixo.
```

Depois, opções clicáveis: estilo (os sugeridos + "Misturar"), paleta (a do estilo escolhido, uma alternativa mais escura e uma mais clara) e intensidade ("Bem dinâmico (Recomendado)", "Médio", "Mais calmo").

**Como escolher os estilos:** pelo clima da música, não pelo gosto pessoal.
- Pop dançante, BPM 110–130, letra de atitude → tipografia 3D cinética, glitch digital.
- R&B / indie quente, lo-fi, nostalgia → mundo da capa com neon, colagem retrô.
- Fofo, romântico, pop leve → colagem retrô (pílulas, corações, retícula).
- Eletrônica, trap, drop pesado → objetos 3D na batida, glitch.
- Balada, voz em primeiro plano, letra séria → editorial P&B, mundo da capa.
Sempre ofereça pelo menos um estilo fora do óbvio, pra pessoa ter contraste na escolha.

## Rodada 3: partitura

Mostre a `partitura.png` e a tabela de cenas (ver SKILL.md, passo 4). Pergunta única: "Posso montar assim?" (botões "Pode montar" / "Ajustar antes").
