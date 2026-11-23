# Tutorial passo a passo

Do zero ao vídeo pronto, na ordem do curso. Cada parte diz **o que fazer**, **o que mandar pro Claude** e **o que esperar**.

---

## Parte 0: preparar o computador (uma vez só)

### 0.1 Claude
1. Instale o app do Claude (claude.ai/download) e entre na sua conta.
2. Entre com uma conta que tenha acesso ao Claude Code.
3. No app, a aba **Code** é o Claude Code (roda no seu PC). A aba de conversa é o chat.

### 0.2 Kit
1. Clique duas vezes em **`INSTALAR.cmd`** (na pasta do kit).
2. Responda as 3 perguntas (ou Enter pra aceitar o padrão):
   - pasta dos projetos (padrão: pasta Vídeos do seu usuário, subpasta `Motion-Projetos`);
   - pasta dos vídeos prontos (padrão `.../Motion-Projetos/resultados`);
   - seu @ pra assinatura (Enter = a skill pergunta em cada vídeo).
3. Espere terminar. No fim aparece a conferência: tudo `[ok]`, menos itens marcados como `[opcional]`.
4. **Feche e abra o Claude** pra ele carregar as skills.

> Alternativa: abra o Claude Code na pasta do kit e arraste `Instalar pelo Claude Code.md` na conversa. Ele instala sozinho e pede permissão quando precisar.

### 0.3 Abrir o Claude Code no lugar certo
Sempre que for criar vídeo, abra o Claude Code na **pasta de projetos** escolhida na instalação. É lá que ficam os projetos e o arquivo que faz a prévia abrir no navegador do Claude.

Digite `/` na caixa de mensagem: as skills `prompt-motion-graphics`, `motionia-...` e `motion-ia-...` devem aparecer.

### 0.4 Usar no chat (opcional, pra celular ou PC fraco)
1. Abra o Claude (site ou app) → **Personalizar → Habilidades** (no app em português pode aparecer como "Habilidades") → **Adicionar / Enviar skill**.
2. Envie os zips da pasta `chat/` do kit, um por vez. Os de Nubank e lata 3D não funcionam no chat (precisam de HyperFrames/Blender no PC).
3. Se você já tinha subido uma versão antiga da `prompt-motion-graphics`, apague a antiga pra não ficar duplicada.

### 0.5 Narração (ElevenLabs)
Várias skills usam narração. O curso gera no **elevenlabs.io**: conta nova ganha créditos grátis, voz em português do Brasil, cola o texto e gera. Ele devolve duas versões; escolha a melhor e baixe o MP3.
Dica: peça pro Claude **"adiciona as tags do ElevenLabs nesse roteiro"** antes de colar; a fala fica mais natural e dinâmica.

---

## Parte 1: o que faz um motion ficar bom (aula 3.1)

Pedido genérico gera vídeo genérico. Sempre mande **duas referências** e diga o que tirar de cada uma:

1. **Referência de design:** cores, fontes, composição. Pode ser o site da marca, um print do Pinterest, telas do app.
2. **Referência de animação:** um vídeo cujo **movimento** você quer. Diga o trecho ("aos 18 s, o botão com brilho que ele clica").

Se você não separar, o Claude mistura tudo. Depois use a skill `prompt-motion-graphics` pra transformar isso num pedido completo. Listas de sites de referência e bancos gratuitos: [05-referencias-e-bancos.md](05-referencias-e-bancos.md).

---

## Parte 2: seu primeiro motion do zero (aula 4.1)

Exemplo da aula: um comercial do Wix no estilo de um vídeo de referência ("crie seu site em segundos, literalmente"). Material da aula em `materiais/4.1-primeiro-motion/` (vídeo de referência e o mockup de MacBook).

1. **Crie a pasta do projeto** e peça pro Claude centralizar tudo nela: "trabalhe só na pasta `wix-segundos dentro da pasta de projetos`".
2. **Referência de design:** cole o site da marca e peça:
   `Analise todo o design desse site: cores, fontes, jeito de se comunicar, copy. Vamos fazer um vídeo baseado nisso.`
3. **Referência de animação:** arraste o vídeo e diga o que gostou:
   `Essa é a referência de animação. Gostei do começo: ele digita uma pesquisa, aperta enter e o site surge. Quero desse jeito, com o site do [marca]. Analise ritmo, efeitos e cortes.`
4. **Roteiro:** `Escreve um roteiro de 30 s com essa ideia: [sua ideia em uma frase]. Me manda que eu devolvo a narração.` Não gostou? Explique a sua ideia com as suas palavras e peça pra reescrever.
5. **Ative a skill:** digite `/prompt-motion-graphics`. Ela pergunta:
   - formato → faça **um** primeiro (ex.: horizontal); o outro só depois de tudo aprovado;
   - música → ela sintetiza uma trilha, ou você manda a sua;
   - onde vai rodar → **Claude Code**.
6. **Narração:** cole o roteiro (com as tags) no ElevenLabs, gere, baixe e arraste o MP3 na conversa. Peça: `Move esse arquivo dos Downloads pra pasta do projeto` (assim nada fica duplicado).
7. **Aprove o resumo** que ele mostra (a tabela de estados/cenas) e peça pra montar no HyperFrames.
8. **Prévia:** ele abre o HyperFrames (no navegador ou dentro do Claude: peça "abre a prévia aqui dentro do Claude"). A prévia pode travar e ter qualidade menor: é normal.
9. **Ajustes:** assista algumas vezes e peça **com o segundo exato**:
   - `Aos 0 s, não quero tela branca: o chat entra centralizado e já digitando.`
   - `Aos 4 s, quero o efeito da referência: brilhos pixelados formando o site.`
   - `Aos 7 s, o site ficou básico. Me mostra opções parecidas com a referência pra eu escolher.`
   - `Aos 14 s, usa o mockup de MacBook anexo, fundo mais escuro e speed ramp (começa rápido e termina devagar).`
   - Termos que ajudam: câmera 3D, parallax, speed ramp, princípios da animação (arrasto, assentamento), desfoque de movimento, glow. Não sabe o nome? Mande um vídeo com o efeito e diga "quero parecido com isso".
   - Pra mostrar um detalhe: print com **Win + Shift + S** e cole na conversa.
10. Quando gostar: `Pode renderizar.` O MP4 sai na pasta do projeto (ou em `resultados/`).

**Cuidado:** o Claude Code tem permissão nas suas pastas. Peça coisas específicas ("move o arquivo X pra pasta Y"); evite "limpa essa pasta".

---

## Parte 3: transforme o seu motion numa skill (aula 4.3)

Gostou do estilo? Na mesma conversa, peça:

```
Cria pra mim uma skill usando o /skill-creator (se ele não estiver instalado, instala) com o estilo de motion que a gente acabou de criar.
Ela deve fazer as perguntas do início, seguir as mesmas etapas e já vir com todos os ajustes que fizemos aqui.
```

Da próxima vez, é só chamar essa skill: o vídeo sai bem mais rápido e com menos ajustes. É assim que as outras skills do curso nasceram.

---

## Parte 4: motion narrado "Tu é Doido" (módulo 5)

Skill: `motionia-tuedoido` → guia: [skills/2-motionia-tuedoido.md](skills/2-motionia-tuedoido.md). Referência da aula: `materiais/5-tu-e-doido/`.

1. **Estude a estratégia da referência, não só o visual** (aula 5.2): gancho de curiosidade logo no início, um segundo gancho que aumenta a curiosidade, quebras de objeção ("não precisei abrir o After Effects", "não precisa de PC potente"), provas mostrando na tela o que dá pra fazer, e o CTA "comenta PALAVRA que eu te mando o link no direct".
2. **Não copie:** troque cores, roteiro, o que é apresentado e coloque a **sua personalidade** (seus bordões, seu jeito de falar). É isso que deixa o vídeo único.
3. Grave a narração (ou gere no ElevenLabs) e separe a música.
4. Chame a skill e mande narração + música + referência + logo:
   `/motionia-tuedoido Faz o motion dessa narração. Música e logo anexos. CTA: comenta MOTION.`
5. Ela analisa sozinha (transcrição, cortes de respiro, batidas), monta as cenas, se avalia por folha de contato, renderiza e mixa. Você só aprova e pede ajustes.

---

## Parte 5: as skills de estilo (módulos 6 a 11)

Todas seguem o mesmo ritmo: **você chama a skill → ela pergunta → você aprova roteiro/estrutura → ela mostra prévia → você ajusta → ela renderiza.**

| Módulo | Estilo | Skill | Guia |
|---|---|---|---|
| 6 | Motion pra cliente real (telão de loja) | `prompt-motion-graphics` (direção B, em loop) | [skills/1](skills/1-prompt-motion-graphics.md) |
| 7 | Comercial de app estilo Nubank | `motion-ia-ayrton-nubank-app-style` | [skills/3](skills/3-nubank-app-style.md) |
| 8–9 | Comercial 3D de lata (Blender) | `motionia-ayrtonsena-comercial-3d-blender` | [skills/5](skills/5-comercial-3d-blender.md) |
| 10 | Comida e delivery estilo iFood | `motionia-ayrtonsena-ifood-delivery` | [skills/4](skills/4-ifood-delivery.md) |
| 11 | Motion na batida da música | `motionia-ayrtonsena-motion-music` | [skills/6](skills/6-motion-music.md) |

O resumo do que cada aula mostra na prática está em [03-resumo-das-aulas.md](03-resumo-das-aulas.md).

---

## Parte 6: boas práticas que valem pra tudo

- **Uma pasta por vídeo**, e mande o Claude **mover** os arquivos pra ela.
- **Um formato por vez.** Aprove o principal e só depois peça a versão vertical/quadrada a partir da mesma linha do tempo.
- **Aprove no papel antes do render.** Roteiro, tabela de cenas e prévia são baratos; render é caro (tempo e uso).
- **Ajuste com tempo e motivo:** "aos 8 s o parallax está forte demais e só de um lado; quero suave, pros dois lados".
- **Use só o que é real da marca:** frases, números e avaliações reais. Nada inventado.
- **Música com direito autoral:** entregue também uma versão sem música (pra usar a música do Instagram).
- **A skill aprende:** quando você corrige algo que vale pros próximos vídeos, diga "salva isso nas regras da skill". Veja como guardar isso ao reinstalar em [04-problemas-comuns.md](04-problemas-comuns.md).
