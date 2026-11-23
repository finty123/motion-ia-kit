# Skill 6: `motionia-ayrtonsena-motion-music` (motion na batida da música)

**O que faz:** um motion de uma **música** (ou trecho): a música é o relógio, a letra vira imagem e cada movimento tem motivo no que se ouve. Palavras-chave da letra em 3D nas batidas fortes, tensão nos respiros (vórtice, buraco negro, tela esvaziando) e final com vácuo + assinatura. Padrão do "Training Season" e dos edits de referência See You Again e Juno. Bônus 11.2 (prática com a música do GTA 6).

**Funciona em:** Claude Code (prévia e render no HyperFrames 0.9.5) e chat (exporta o MP4 direto, sem prévia).

## O que ter em mãos
- A música (mp3, m4a, wav ou vídeo) e o **trecho exato** (início e fim).
- Formato: 16:9, 9:16, 1:1 ou quadrado dentro do vertical (cena borrada com retícula em cima e embaixo).
- Seu @ pra assinatura (ela nunca inventa; sem resposta, sai sem).
- Opcional: capa do álbum, fotos do artista, logo, PNGs, fontes, uma referência de edit.

## Como chamar
```
/motionia-ayrtonsena-motion-music
Faz um motion dessa música na batida [arraste o arquivo]. Trecho de 0:12 a 0:42, formato 9:16.
```

## O que acontece
1. **Primeira rodada:** onde está rodando, música e trecho, formato, final/assinatura, materiais. Ela **não sugere estilo antes de ouvir** a música.
2. **Raio-x da música:** recorta o trecho, letra com tempo por palavra (Whisper large-v3), BPM, batidas principais, respiros e uma **partitura.png**.
3. **3 ou 4 estilos** nascidos da música (paleta, fontes, momentos-chave) → você escolhe.
4. Partitura + roteiro de cenas (o que acontece em cada batida).
5. Construção no motor 3D + `kit_musica.js`, folha de contato e autoavaliação.
6. **Mix:** só a música + o close-up no buraco negro (os outros SFX ficam desligados nesse estilo).
7. **Prévia** no HyperFrames (`hf_wrap.py` → `preview`), aprovação e **render** (`--workers 4`).

## Dicas
- "Já gera o vídeo" quer dizer não parar nas etapas do meio, mas ela **sempre** mostra a prévia antes do render.
- Toda correção sua que valer pros próximos vídeos ela grava em `references/regras.md` da skill instalada. Isso faz a skill aprender seu gosto (veja "Atualizar sem perder o que a skill aprendeu" no tutorial).
