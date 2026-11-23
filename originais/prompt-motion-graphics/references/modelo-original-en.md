# Modelo original (inglês)

Estrutura de referência que a skill reproduz em português. O trecho veio cortado nas bordas; o que vale é a ordem das seções e o tipo de instrução em cada uma.

```
<inputs>
Ask me for: my product + URL, 8 to 12 UI states that tell its story, [what happens in] each state, brand colors + fonts + one accent, a royalty-free track nea[r the BPM]
</inputs>

<direction>
Product-film UI motion. One container never cuts: every state is the sa[me element changing] size, radius and fill while its content swaps behind a short blur. A cu[rsor drives every change].
Warm neutral canvas, one accent. Springs with at most a tiny overshoot.
Banned: bouncy easing, glows, gradients on UI chrome, particle bursts, [dead time].
</direction>

<structure>
120 BPM, 8 bars, something happens on every beat.
logo -> CTA button -> email field (typed) -> loader -> success check -> dash[board]
-> chart draws itself -> tooltip on hover -> ⌘K palette -> toast -> logo.
</structure>

<build>
1. One HTML file, one canvas, window.seek(t). No CSS transitions, no ti[mers, no carried state].
2. Closed-form springs. A value with many targets = sum of one spring p[er change].
3. Text inside a morphing container enters after the morph starts, leav[es before it ends].
4. Tab indicators: leading and trailing edges on different springs so t[hey stretch].
5. Beat grid from the track (numpy/librosa). Start on a downbeat. UI sc[ounds on measured peaks].
6. Render in headless Chrome at 60 fps, 4 subframes per frame, blended [for motion blur].
</build>
```

Regras de estúdio que costumam acompanhar esse modelo (fonte: prints de referência):
- Todo filme é função pura do tempo: window.seek(t) pinta o quadro t. Ruído só com seed (mulberry32), nunca Math.random. H.264 yuv420p, CRF 16.
- Proibido o padrão genérico: título centralizado em gradiente, tudo com fade, rótulos e molduras nos cantos, brilho na interface, partículas genéricas.
- Uma fonte display, uma de interface, uma cor de destaque. A cada 2 a 4 s algo novo na tela.
- Trilha e efeitos sintetizados em código se não houver trilha. Batidas em beats.json. -14 LUFS.
- Antes de mostrar: folha de contato (um quadro por batida), nota 1–10 em gancho, legibilidade no celular, movimento, variedade, fidelidade à marca e sincronia; corrige os 3 piores; repete até 8+; só então render final.
