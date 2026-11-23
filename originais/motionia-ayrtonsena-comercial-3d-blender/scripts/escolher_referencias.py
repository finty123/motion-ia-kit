# Abre uma pagina com cada efeito de referencia rodando em video pra pessoa marcar "quero / nao quero / talvez"
# e escrever observacoes. No fim, "Copiar escolhas" (pra colar no chat) e "Baixar" (escolhas-referencias.json).
# Uso: python escolher_referencias.py "<pasta de saida>" [videos de referencia da pessoa...]
#      As referencias da pessoa tambem aparecem na pagina, junto com as da skill.
#      A pagina abre no navegador DENTRO do Claude (veja references/referencias.md): o script so gera o arquivo.
#      --abrir-fora abre no navegador do sistema (so se a pessoa pedir).
import base64, html, json, os, platform, shutil, subprocess, sys, webbrowser
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REF = SKILL / "assets" / "referencias"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
saida = Path(args[0])
saida.mkdir(parents=True, exist_ok=True)
proprias = [Path(a) for a in args[1:]]

itens = json.loads((REF / "referencias.json").read_text(encoding="utf-8"))
for it in itens:
    v = REF / "videos" / f"{it['id']}.mp4"
    it["src"] = "data:video/mp4;base64," + base64.b64encode(v.read_bytes()).decode() if v.exists() else ""
pasta_v = saida / "_videos"
for i, p in enumerate(proprias, 1):
    pasta_v.mkdir(exist_ok=True)
    destino = pasta_v / p.name
    if p.resolve() != destino.resolve():
        shutil.copy2(p, destino)
    itens.append({"id": f"sua-{i}", "titulo": p.stem[:60], "marca": "Sua referência", "efeito": "",
                  "parte": "A definir", "status": "sua", "src": f"_videos/{p.name}"})

SELO = {"motor": ("Já faz parte do vídeo", "ok"), "extra": ("Extra: cena nova, mais tempo de produção", "extra"),
        "sua": ("Referência sua", "sua")}
cards = []
for it in itens:
    selo, cls = SELO[it["status"]]
    cards.append(f"""
  <article class="card" data-id="{html.escape(it['id'])}" data-titulo="{html.escape(it['titulo'])}" data-parte="{html.escape(it['parte'])}">
    <div class="video"><video src="{it['src']}" autoplay muted loop playsinline></video></div>
    <div class="corpo">
      <div class="topo"><span class="parte">{html.escape(it['parte'])}</span><span class="selo {cls}">{selo}</span></div>
      <h2>{html.escape(it['titulo'])}</h2>
      <p class="marca">{html.escape(it['marca'])}</p>
      <p class="efeito">{html.escape(it['efeito'])}</p>
      <div class="botoes" role="group" aria-label="Escolha">
        <button data-v="quero">Quero</button><button data-v="talvez">Talvez</button><button data-v="nao">Não quero</button>
      </div>
      <textarea placeholder="Observação (ex.: só o começo, mais rápido, com outra cor...)"></textarea>
    </div>
  </article>""")

pagina = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Escolha os efeitos</title>
<style>
  :root {{ --fundo:#0e0e10; --card:#18181c; --linha:#2a2a30; --texto:#f2f2f2; --suave:#a3a3ad; --acento:#ff2e93; --ok:#3ddc84; --talvez:#ffc93c; --nao:#ff5a5a; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--fundo); color:var(--texto); font:16px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; padding:0 16px 110px; }}
  header {{ max-width:1180px; margin:0 auto; padding:36px 0 20px; }}
  h1 {{ font-size:clamp(26px,4vw,40px); margin:0 0 8px; letter-spacing:-.02em; }}
  header p {{ color:var(--suave); margin:0; max-width:720px; }}
  .grade {{ max-width:1180px; margin:0 auto; display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:18px; }}
  .card {{ background:var(--card); border:1px solid var(--linha); border-radius:14px; overflow:hidden; display:flex; flex-direction:column; transition:border-color .2s; }}
  .card[data-escolha="quero"] {{ border-color:var(--ok); }} .card[data-escolha="talvez"] {{ border-color:var(--talvez); }} .card[data-escolha="nao"] {{ opacity:.55; }}
  .video {{ background:#000; aspect-ratio:4/5; display:flex; align-items:center; justify-content:center; }}
  .video video {{ width:100%; height:100%; object-fit:contain; }}
  .corpo {{ padding:14px 16px 16px; display:flex; flex-direction:column; gap:6px; flex:1; }}
  .topo {{ display:flex; gap:8px; flex-wrap:wrap; align-items:center; }}
  .parte {{ font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--acento); font-weight:700; }}
  .selo {{ font-size:12px; padding:2px 8px; border-radius:99px; border:1px solid var(--linha); color:var(--suave); }}
  .selo.extra {{ color:var(--talvez); border-color:#5a4a1a; }}
  h2 {{ font-size:19px; margin:2px 0 0; }}
  .marca {{ margin:0; color:var(--suave); font-size:13px; }}
  .efeito {{ margin:4px 0 6px; font-size:14px; color:#d6d6dc; flex:1; }}
  .botoes {{ display:grid; grid-template-columns:repeat(3,1fr); gap:6px; }}
  .botoes button {{ background:#222228; color:var(--texto); border:1px solid var(--linha); border-radius:9px; padding:9px 4px; font:600 14px system-ui; cursor:pointer; }}
  .botoes button:hover {{ border-color:#55555f; }}
  .card[data-escolha="quero"] [data-v="quero"] {{ background:var(--ok); color:#06210f; border-color:var(--ok); }}
  .card[data-escolha="talvez"] [data-v="talvez"] {{ background:var(--talvez); color:#2a1f00; border-color:var(--talvez); }}
  .card[data-escolha="nao"] [data-v="nao"] {{ background:var(--nao); color:#2a0505; border-color:var(--nao); }}
  textarea {{ background:#111114; color:var(--texto); border:1px solid var(--linha); border-radius:9px; padding:8px 10px; font:14px system-ui; min-height:54px; resize:vertical; }}
  .barra {{ position:fixed; left:0; right:0; bottom:0; background:rgba(14,14,16,.94); border-top:1px solid var(--linha); padding:12px 16px; }}
  .barra div {{ max-width:1180px; margin:0 auto; display:flex; gap:10px; align-items:center; flex-wrap:wrap; }}
  .barra span {{ color:var(--suave); flex:1; min-width:160px; }}
  .barra button {{ border:0; border-radius:10px; padding:11px 16px; font:700 15px system-ui; cursor:pointer; }}
  #copiar {{ background:var(--acento); color:#fff; }} #baixar {{ background:#2a2a30; color:var(--texto); }}
</style></head><body>
<header>
  <h1>Escolha os efeitos do seu comercial</h1>
  <p>Cada vídeo mostra um movimento de referência. Marque o que você quer no seu comercial e escreva o que mudaria. Os marcados como "Extra" pedem uma cena nova e aumentam o tempo de produção. Quando terminar, clique em <b>Copiar escolhas</b> e cole no chat.</p>
</header>
<main class="grade">{''.join(cards)}
</main>
<div class="barra"><div><span id="conta">Nada marcado ainda</span><button id="baixar">Baixar arquivo</button><button id="copiar">Copiar escolhas</button></div></div>
<script>
const CHAVE = "escolhas-referencias";
let salvo = {{}};
try {{ salvo = JSON.parse(localStorage.getItem(CHAVE) || "{{}}"); }} catch (e) {{}}
const cards = [...document.querySelectorAll(".card")];
function guardar() {{
  const dados = {{}};
  cards.forEach(c => dados[c.dataset.id] = {{ escolha: c.dataset.escolha || "", obs: c.querySelector("textarea").value }});
  try {{ localStorage.setItem(CHAVE, JSON.stringify(dados)); }} catch (e) {{}}
  const n = cards.filter(c => c.dataset.escolha === "quero").length, t = cards.filter(c => c.dataset.escolha).length;
  document.getElementById("conta").textContent = t ? `${{n}} quero · ${{t}} de ${{cards.length}} respondidos` : "Nada marcado ainda";
  return dados;
}}
cards.forEach(c => {{
  const s = salvo[c.dataset.id];
  if (s) {{ if (s.escolha) c.dataset.escolha = s.escolha; c.querySelector("textarea").value = s.obs || ""; }}
  c.querySelectorAll("button").forEach(b => b.onclick = () => {{ c.dataset.escolha = c.dataset.escolha === b.dataset.v ? "" : b.dataset.v; guardar(); }});
  c.querySelector("textarea").oninput = guardar;
}});
guardar();
const NOMES = {{ quero: "QUERO", talvez: "TALVEZ", nao: "NÃO QUERO" }};
function texto() {{
  const linhas = ["Minhas escolhas de efeitos:"];
  cards.forEach(c => {{
    const e = c.dataset.escolha, o = c.querySelector("textarea").value.trim();
    if (!e && !o) return;
    linhas.push(`- ${{c.dataset.titulo}} (${{c.dataset.parte}}): ${{NOMES[e] || "sem marcar"}}${{o ? " | obs: " + o : ""}}`);
  }});
  return linhas.join("\\n");
}}
document.getElementById("copiar").onclick = async () => {{
  const b = document.getElementById("copiar");
  try {{ await navigator.clipboard.writeText(texto()); b.textContent = "Copiado! Cole no chat"; }}
  catch (e) {{ prompt("Copie o texto abaixo:", texto()); }}
  setTimeout(() => b.textContent = "Copiar escolhas", 2500);
}};
document.getElementById("baixar").onclick = () => {{
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(guardar(), null, 1)], {{ type: "application/json" }}));
  a.download = "escolhas-referencias.json"; a.click();
}};
</script></body></html>"""
arq = saida / "escolher-efeitos.html"
arq.write_text(pagina, encoding="utf-8")
print("pagina:", arq)
if "--abrir-fora" in sys.argv:
    try:
        if platform.system() == "Windows":
            os.startfile(arq)
        elif platform.system() == "Darwin":
            subprocess.run(["open", str(arq)])
        else:
            webbrowser.open(arq.as_uri())
    except Exception:
        print("abra no navegador:", arq)
