# Exemplo: "Motion com IA / Comenta MOTION" (16:9, 83,5 s)

Vídeo aprovado depois de várias rodadas de correção. Use como base: copie as cenas e troque textos, índices e cores.

- `words.json`: narração já com os respiros cortados (244 palavras). Os índices `w(i)` do `scenes.js` apontam para este arquivo.
- `beats.json`: batidas da música já editada (offset 0,96 s + corte de 59,652 a 65,852 s).
- `scenes.js`: as 25 cenas (S1f…S24f) e as cues de som.

Montar e conferir este exemplo:
```bash
S=<skill>/scripts; E=<skill>/examples/motion-ia
python3 $S/preparar_logo.py logo.png /tmp/ex/logo_alpha.png
python3 $S/build.py --scenes $E/scenes.js --words $E/words.json --beats $E/beats.json --logo /tmp/ex/logo_alpha.png --out /tmp/ex/index.html
python3 $S/snap.py /tmp/ex/index.html /tmp/ex/folha.jpg 1.9,11.6,17.4,26.8,47.8,64.9,72.4,78.0
```

Mapa (fala → receita):
| Início | Fala | Receita |
|---|---|---|
| 0,00 | Tu é doido, rapaz | R1 palavra alongada + mergulho no O |
| w(4) | tá de brincadeira comigo, né? | R2 |
| w(9) | não, pô, pera aí | R3 |
| w(13) | não abri o After nenhuma vez pra fazer | R4 |
| w(24) | esse vídeo aqui | R5 |
| w(27) | e isso aqui é Claude, meu amigo | R6 |
| w(36) | eu não escrevi nenhuma linha de código | R7 |
| w(43) | não precisei de computador da NASA | R8 (buraco negro) |
| w(49) | e tu pode pedir o que tu quiser | R9 |
| w(57)−0,35 | esse quadrado aqui… vire 3D, saia voando e exploda | R10 |
| w(68) | tu pode pedir o que tu quiser, rapaz | R11 |
| w(77) | se tu pedir de um jeito genérico, vai receber genérico | R12 |
| w(94) | por que se tu pedir pro Claude… não vai sair? | R13 |
| w(111) | porque tu tá pedindo de um jeito genérico… não tem pra onde | R14 |
| w(139) | ela vai dar o resultado que dá pra todo mundo | R15 |
| w(150)−0,55 | o cara de IA | R16 |
| w(154) | pra conseguir um vídeo nesse nível, tu precisa de duas coisas | R17 |
| w(165) | prompt e referência | R18 |
| w(168) | escrever um prompt super complexo… é difícil | R19 |
| w(192) | principalmente se tá começando do zero | R20 |
| w(199) | e isso tudo eu te ensino no curso Motion com IA | R21 |
| w(210) | ele tá por R$297 | R22 |
| w(217) | mas só agora, nesse período de black, por apenas R$97 | R23 |
| w(232) | comenta Motion que eu te envio o link no direct | R24 |
| END−3,5 | (logo) | R25 |
