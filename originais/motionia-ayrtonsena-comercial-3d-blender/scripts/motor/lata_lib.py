# Pecas compartilhadas das cenas do comercial: lata com os rotulos trocaveis, condensacao,
# luz, camera e configuracao de render. Importado pelo Blender (comercial.py).
import bpy, bmesh, math, os, random, json, sys
import numpy as np
from mathutils import Vector, Matrix
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import config as C

def curvas(acao):
    """fcurves de uma acao no Blender 4.2 (acao.fcurves) e no 5.x (camadas > strips > channelbags)"""
    fcs = getattr(acao, "fcurves", None)
    if fcs is not None:
        return list(fcs)
    out = []
    for camada in getattr(acao, "layers", []):
        for strip in camada.strips:
            for cb in getattr(strip, "channelbags", []):
                out += list(cb.fcurves)
    return out


def curva(acao, dono, caminho, i):
    """acha ou cria a fcurve (caminho, i) da acao do dono, nas duas APIs"""
    fcs = getattr(acao, "fcurves", None)
    if fcs is not None:
        return fcs.find(caminho, index=i) or fcs.new(caminho, index=i)
    return acao.fcurve_ensure_for_datablock(dono, caminho, index=i)


PROJETO, RENDER = C.PROJETO, C.RENDER
SABORES = [s.get("modelo", s.get("nome")) for s in C.SABORES]
COR_SABOR = C.COR_SABOR
RAIO = C.RAIO

PERFIL = [
    (0.001, 0.28), (0.5, 0.2), (0.76, 0.07), (0.86, 0.0), (0.94, 0.04),
    (0.985, 0.15), (1.0, 0.30), (1.0, 4.45), (0.995, 4.53), (0.975, 4.62),
    (0.935, 4.73), (0.895, 4.83), (0.878, 4.90), (0.88, 4.94), (0.892, 4.975),
    (0.897, 4.995), (0.888, 5.015), (0.870, 5.018), (0.856, 5.0), (0.85, 4.97),
    (0.842, 4.925), (0.826, 4.895), (0.805, 4.885), (0.785, 4.892), (0.77, 4.902),
    (0.70, 4.906), (0.45, 4.908), (0.001, 4.91),
]
TAMPA, Z0, Z1, PESCOCO = 4.908, 0.17, 4.50, 4.895
MEIO = 2.5  # altura do centro da lata

FPS = C.FPS
F = C.F
TOTAL = C.TOTAL


def limpar():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def nos(mat):
    mat.use_nodes = True
    return mat.node_tree.nodes, mat.node_tree.links


def _pixels(im):
    w, h = im.size
    px = np.empty(w * h * 4, dtype=np.float32)
    im.pixels.foreach_get(px)
    return px.reshape(h, w, 4)


def _lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def cor_de_fundo(im):
    px = _pixels(im)
    topo = px[int(px.shape[0] * 0.96):, :, :3].reshape(-1, 3)
    q = np.round(topo * 15).astype(int)
    chaves, cont = np.unique(q, axis=0, return_counts=True)
    srgb = topo[(q == chaves[cont.argmax()]).all(axis=1)].mean(axis=0)
    return [float(v) for v in _lin(srgb)]


def brilho_medio(im):
    rgb = _pixels(im).reshape(-1, 4)[::7, :3]
    return float((_lin(rgb) @ np.array([0.2126, 0.7152, 0.0722])).mean())


def exposicao(brilho):
    return -0.35 - max(0.0, brilho - 0.3) * 1.6


def carregar_rotulos():
    imgs = [bpy.data.images.load(str(PROJETO / "modelos" / s / "rotulo_2x.png")) for s in SABORES]
    return imgs, [cor_de_fundo(i) for i in imgs], [brilho_medio(i) for i in imgs]


def malha_lata():
    bm = bmesh.new()
    vs = [bm.verts.new((r, 0, z)) for r, z in PERFIL]
    es = [bm.edges.new((vs[i], vs[i + 1])) for i in range(len(vs) - 1)]
    bmesh.ops.spin(bm, geom=vs + es, cent=(0, 0, 0), axis=(0, 0, 1), angle=math.tau, steps=192, use_merge=True)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    uvl = bm.loops.layers.uv.new()
    for f in bm.faces:
        us = [(math.atan2(lo.vert.co.y, lo.vert.co.x) + math.pi) / math.tau for lo in f.loops]
        if max(us) - min(us) > 0.5:
            us = [u + 1 if u < 0.5 else u for u in us]
        for lo, u in zip(f.loops, us):
            lo[uvl].uv = (u, (lo.vert.co.z - Z0) / (Z1 - Z0))
    me = bpy.data.meshes.new("lata")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    return me


def material_lata(imgs, cores):
    """Rotulo trocavel (no 'indice', 0..3). Object Info: cor RGB tinge (copias do rastro mais escuras;
    no morph vira a cor do neon) e alfa = morph (0 lata normal, 1 so o contorno em neon)."""
    mat = bpy.data.materials.new("lata")
    mat.surface_render_method = "DITHERED"
    n, l = nos(mat)
    saida = n["Material Output"]
    n.remove(n["Principled BSDF"])
    indice = n.new("ShaderNodeValue")
    indice.name = indice.label = "indice"
    uvn = n.new("ShaderNodeUVMap")
    tc = n.new("ShaderNodeTexCoord")
    sep = n.new("ShaderNodeSeparateXYZ")
    l.new(tc.outputs["Object"], sep.inputs[0])
    no_pesc = n.new("ShaderNodeMath"); no_pesc.operation = "GREATER_THAN"; no_pesc.inputs[1].default_value = Z1
    l.new(sep.outputs["Z"], no_pesc.inputs[0])
    # condensacao: mapa em (u, z/5); normal so no verniz (a agua fica por cima do rotulo)
    ju = n.new("ShaderNodeSeparateXYZ"); l.new(uvn.outputs["UV"], ju.inputs[0])
    zr = n.new("ShaderNodeMath"); zr.operation = "DIVIDE"; zr.inputs[1].default_value = 5.0
    l.new(sep.outputs["Z"], zr.inputs[0])
    vc = n.new("ShaderNodeCombineXYZ"); l.new(ju.outputs["X"], vc.inputs["X"]); l.new(zr.outputs[0], vc.inputs["Y"])
    def mapa(nome):
        im_ = bpy.data.images.load(str(AQUI / "assets" / nome), check_existing=True)
        im_.colorspace_settings.name = "Non-Color"
        t = n.new("ShaderNodeTexImage"); t.image = im_; t.extension = "REPEAT"; t.interpolation = "Cubic"
        l.new(vc.outputs[0], t.inputs["Vector"])
        return t
    tn, tm = mapa("condensacao_normal.png"), mapa("condensacao_mascara.png")
    nm = n.new("ShaderNodeNormalMap"); nm.space = "TANGENT"; nm.inputs["Strength"].default_value = 1.0
    l.new(tn.outputs["Color"], nm.inputs["Color"])
    cm = n.new("ShaderNodeSeparateColor"); l.new(tm.outputs["Color"], cm.inputs[0])
    agua_, nevoa_, alt_ = cm.outputs[0], cm.outputs[1], cm.outputs[2]
    # falsa refracao: o rotulo dentro da gota aparece deslocado pela inclinacao da agua
    inc = n.new("ShaderNodeVectorMath"); inc.operation = "MULTIPLY_ADD"
    l.new(tn.outputs["Color"], inc.inputs[0]); inc.inputs[1].default_value = (2, 2, 0); inc.inputs[2].default_value = (-1, -1, 0)
    ka = n.new("ShaderNodeMath"); ka.operation = "MULTIPLY"; ka.inputs[1].default_value = -0.003
    l.new(agua_, ka.inputs[0])
    desl = n.new("ShaderNodeVectorMath"); desl.operation = "SCALE"
    l.new(inc.outputs[0], desl.inputs[0]); l.new(ka.outputs[0], desl.inputs["Scale"])
    uv_ref = n.new("ShaderNodeVectorMath"); uv_ref.operation = "ADD"
    l.new(uvn.outputs["UV"], uv_ref.inputs[0]); l.new(desl.outputs[0], uv_ref.inputs[1])
    cor_total = None
    for i, (im, cp) in enumerate(zip(imgs, cores)):
        tx = n.new("ShaderNodeTexImage"); tx.image = im; tx.extension = "REPEAT"; tx.interpolation = "Cubic"
        l.new(uv_ref.outputs[0], tx.inputs["Vector"])
        rgb = n.new("ShaderNodeRGB"); rgb.outputs[0].default_value = (*cp, 1)
        mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"
        l.new(no_pesc.outputs[0], mx.inputs["Factor"]); l.new(tx.outputs["Color"], mx.inputs["A"]); l.new(rgb.outputs[0], mx.inputs["B"])
        # peso = 1 quando |indice - i| < 0.5
        d = n.new("ShaderNodeMath"); d.operation = "SUBTRACT"; d.inputs[1].default_value = i
        l.new(indice.outputs[0], d.inputs[0])
        a = n.new("ShaderNodeMath"); a.operation = "ABSOLUTE"; l.new(d.outputs[0], a.inputs[0])
        w = n.new("ShaderNodeMath"); w.operation = "LESS_THAN"; w.inputs[1].default_value = 0.5; l.new(a.outputs[0], w.inputs[0])
        pond = n.new("ShaderNodeVectorMath"); pond.operation = "SCALE"
        l.new(mx.outputs["Result"], pond.inputs[0]); l.new(w.outputs[0], pond.inputs["Scale"])
        if cor_total is None:
            cor_total = pond.outputs[0]
        else:
            soma = n.new("ShaderNodeVectorMath"); soma.operation = "ADD"
            l.new(cor_total, soma.inputs[0]); l.new(pond.outputs[0], soma.inputs[1]); cor_total = soma.outputs[0]
    info = n.new("ShaderNodeObjectInfo")
    tinta = n.new("ShaderNodeVectorMath"); tinta.operation = "MULTIPLY"
    l.new(cor_total, tinta.inputs[0]); l.new(info.outputs["Color"], tinta.inputs[1])
    # borda da gota um pouco mais escura, miolo um pouco mais claro; nevoa fosca e clareia
    um_h = n.new("ShaderNodeMath"); um_h.operation = "SUBTRACT"; um_h.inputs[0].default_value = 1.0
    l.new(alt_, um_h.inputs[1])
    aro = n.new("ShaderNodeMath"); aro.operation = "MULTIPLY"; l.new(um_h.outputs[0], aro.inputs[0]); l.new(agua_, aro.inputs[1])
    escur = n.new("ShaderNodeMath"); escur.operation = "MULTIPLY_ADD"
    l.new(aro.outputs[0], escur.inputs[0]); escur.inputs[1].default_value = -0.3; escur.inputs[2].default_value = 1.0
    claro = n.new("ShaderNodeMath"); claro.operation = "MULTIPLY_ADD"
    l.new(alt_, claro.inputs[0]); claro.inputs[1].default_value = 0.12; claro.inputs[2].default_value = 1.0
    fator = n.new("ShaderNodeMath"); fator.operation = "MULTIPLY"; l.new(escur.outputs[0], fator.inputs[0]); l.new(claro.outputs[0], fator.inputs[1])
    cor_g = n.new("ShaderNodeVectorMath"); cor_g.operation = "SCALE"
    l.new(tinta.outputs[0], cor_g.inputs[0]); l.new(fator.outputs[0], cor_g.inputs["Scale"])
    nev_k = n.new("ShaderNodeMath"); nev_k.operation = "MULTIPLY"; nev_k.inputs[1].default_value = 0.16
    l.new(nevoa_, nev_k.inputs[0])
    cor_n = n.new("ShaderNodeMix"); cor_n.data_type = "RGBA"
    l.new(nev_k.outputs[0], cor_n.inputs["Factor"]); l.new(cor_g.outputs[0], cor_n.inputs["A"])
    cor_n.inputs["B"].default_value = (0.82, 0.84, 0.87, 1)
    rough = n.new("ShaderNodeMath"); rough.operation = "MULTIPLY_ADD"
    l.new(nevoa_, rough.inputs[0]); rough.inputs[1].default_value = 0.3; rough.inputs[2].default_value = 0.32
    c_rough = n.new("ShaderNodeMath"); c_rough.operation = "MULTIPLY_ADD"
    l.new(nevoa_, c_rough.inputs[0]); c_rough.inputs[1].default_value = 0.24; c_rough.inputs[2].default_value = 0.06
    c_rough2 = n.new("ShaderNodeMix"); c_rough2.data_type = "FLOAT"
    l.new(agua_, c_rough2.inputs["Factor"]); l.new(c_rough.outputs[0], c_rough2.inputs["A"]); c_rough2.inputs["B"].default_value = 0.012
    c_peso = n.new("ShaderNodeMath"); c_peso.operation = "MULTIPLY_ADD"
    l.new(agua_, c_peso.inputs[0]); c_peso.inputs[1].default_value = 0.2; c_peso.inputs[2].default_value = 0.8
    tintab = n.new("ShaderNodeBsdfPrincipled")
    l.new(cor_n.outputs["Result"], tintab.inputs["Base Color"])
    tintab.inputs["Metallic"].default_value = 0.25
    l.new(rough.outputs[0], tintab.inputs["Roughness"])
    l.new(c_peso.outputs[0], tintab.inputs["Coat Weight"])
    l.new(c_rough2.outputs["Result"], tintab.inputs["Coat Roughness"])
    tintab.inputs["Coat IOR"].default_value = 1.33
    l.new(nm.outputs["Normal"], tintab.inputs["Coat Normal"])
    alu = n.new("ShaderNodeBsdfPrincipled")
    alu.inputs["Base Color"].default_value = (0.86, 0.85, 0.84, 1)
    alu.inputs["Metallic"].default_value = 1.0
    alu.inputs["Roughness"].default_value = 0.14
    acima = n.new("ShaderNodeMath"); acima.operation = "GREATER_THAN"; acima.inputs[1].default_value = Z0
    abaixo = n.new("ShaderNodeMath"); abaixo.operation = "LESS_THAN"; abaixo.inputs[1].default_value = PESCOCO
    l.new(sep.outputs["Z"], acima.inputs[0]); l.new(sep.outputs["Z"], abaixo.inputs[0])
    faixa = n.new("ShaderNodeMath"); faixa.operation = "MULTIPLY"
    l.new(acima.outputs[0], faixa.inputs[0]); l.new(abaixo.outputs[0], faixa.inputs[1])
    normal = n.new("ShaderNodeMixShader")
    l.new(faixa.outputs[0], normal.inputs["Fac"]); l.new(alu.outputs[0], normal.inputs[1]); l.new(tintab.outputs[0], normal.inputs[2])
    # morph: so a borda da silhueta acende (neon), o miolo fica transparente
    lw = n.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
    borda = n.new("ShaderNodeMapRange")
    borda.inputs["From Min"].default_value = 0.78; borda.inputs["From Max"].default_value = 0.93
    l.new(lw.outputs["Facing"], borda.inputs["Value"])
    em = n.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 9.0
    l.new(info.outputs["Color"], em.inputs["Color"])
    transp = n.new("ShaderNodeBsdfTransparent")
    neon = n.new("ShaderNodeMixShader")
    l.new(borda.outputs["Result"], neon.inputs["Fac"]); l.new(transp.outputs[0], neon.inputs[1]); l.new(em.outputs[0], neon.inputs[2])
    final = n.new("ShaderNodeMixShader")
    l.new(info.outputs["Alpha"], final.inputs["Fac"]); l.new(normal.outputs[0], final.inputs[1]); l.new(neon.outputs[0], final.inputs[2])
    l.new(final.outputs[0], saida.inputs["Surface"])
    return mat


def material_aluminio():
    m = bpy.data.materials.new("aluminio")
    n, l = nos(m)
    b = n["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.85, 0.84, 0.82, 1)
    b.inputs["Metallic"].default_value = 1.0
    b.inputs["Roughness"].default_value = 0.12
    return m


def material_agua():
    m = bpy.data.materials.new("agua")
    m.surface_render_method = "DITHERED"
    n, l = nos(m)
    b = n["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.55, 0.56, 0.58, 1)
    b.inputs["Metallic"].default_value = 0.6
    b.inputs["Roughness"].default_value = 0.02
    lw = n.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.4
    a = n.new("ShaderNodeMapRange"); a.inputs["To Min"].default_value = 0.35; a.inputs["To Max"].default_value = 0.75
    l.new(lw.outputs["Facing"], a.inputs["Value"]); l.new(a.outputs["Result"], b.inputs["Alpha"])
    return m


def _estadio(x0, x1, larg, pts=24):
    r = larg / 2
    out = [(x1 - r + r * math.cos(-math.pi / 2 + math.pi * i / pts), r * math.sin(-math.pi / 2 + math.pi * i / pts)) for i in range(pts + 1)]
    out += [(x0 + r + r * math.cos(math.pi / 2 + math.pi * i / pts), r * math.sin(math.pi / 2 + math.pi * i / pts)) for i in range(pts + 1)]
    return out


_CACHE = {}


def dados_detalhes(mat_alu):
    if "lacre" in _CACHE:
        return _CACHE["lacre"], _CACHE["rebite"], _CACHE["abertura"]
    cu = bpy.data.curves.new("lacre", "CURVE"); cu.dimensions = "2D"; cu.fill_mode = "BOTH"
    cu.extrude = 0.006; cu.bevel_depth = 0.004; cu.bevel_resolution = 3
    for cont in (_estadio(-0.44, 0.34, 0.40), _estadio(-0.37, -0.12, 0.25)):
        sp = cu.splines.new("POLY"); sp.points.add(len(cont) - 1)
        for p, (x, y) in zip(sp.points, cont):
            p.co = (x, y, 0, 1)
        sp.use_cyclic_u = True
    cu.materials.append(mat_alu)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=48, radius1=0.06, radius2=0.06, depth=0.03)
    rb = bpy.data.meshes.new("rebite"); bm.to_mesh(rb); bm.free(); rb.materials.append(mat_alu)
    cl = bpy.data.curves.new("abertura", "CURVE"); cl.dimensions = "3D"; cl.bevel_depth = 0.007; cl.bevel_resolution = 3
    sp = cl.splines.new("POLY")
    pts = [(0.42 + 0.27 * math.cos(a), 0.24 * math.sin(a) * (0.75 + 0.25 * math.cos(a))) for a in [math.tau * i / 64 for i in range(64)]]
    sp.points.add(len(pts) - 1)
    for p, (x, y) in zip(sp.points, pts):
        p.co = (x, y, TAMPA - 0.001, 1)
    sp.use_cyclic_u = True
    cl.materials.append(mat_alu)
    _CACHE.update(lacre=cu, rebite=rb, abertura=cl)
    return cu, rb, cl


def _molde(sub):
    tb = bmesh.new()
    bmesh.ops.create_icosphere(tb, subdivisions=sub, radius=1.0)
    v = [x.co.copy() for x in tb.verts]
    f = [[x.index for x in fa.verts] for fa in tb.faces]
    tb.free()
    return v, f


def _raio_em(z):
    for (r0, z0), (r1, z1) in zip(PERFIL, PERFIL[1:]):
        if z0 <= z <= z1 and z1 > z0:
            t = (z - z0) / (z1 - z0)
            return r0 + (r1 - r0) * t, (r1 - r0) / (z1 - z0)
    return 1.0, 0.0


def dados_gotas(mat_agua, qtd=1.0):
    chave_c = f"gotas{qtd}"
    if chave_c in _CACHE:
        return _CACHE[chave_c]
    rnd = random.Random(11)
    ico2, ico1 = _molde(2), _molde(1)
    verts, faces = [], []

    def gota(pos, normal, raio, achata=0.6, m=ico2):
        tv, tf = m
        normal = Vector(normal).normalized()
        rot = normal.to_track_quat("Z", "Y").to_matrix()
        mm = rot @ Matrix.Diagonal((raio, raio * rnd.uniform(0.85, 1.15), raio * achata))
        base = len(verts)
        c = Vector(pos) + normal * raio * achata * 0.35
        verts.extend([tuple(c + mm @ v) for v in tv])
        faces.extend([[base + i for i in f] for f in tf])

    def no_corpo(z, raio, m=ico2):
        a = rnd.uniform(0, math.tau)
        rz, incl = _raio_em(z)
        gota((math.cos(a) * rz, math.sin(a) * rz, z), (math.cos(a), math.sin(a), -incl), raio, m=m)

    for _ in range(140):
        a = rnd.uniform(0, math.tau); r = math.sqrt(rnd.random()) * 0.74
        x, y = r * math.cos(a), r * math.sin(a)
        if -0.5 < x < 0.4 and abs(y) < 0.24:
            continue
        gota((x, y, TAMPA), (0, 0, 1), 0.005 + rnd.random() ** 3 * 0.03, 0.5)
    gm = bpy.data.meshes.new("gotas")
    gm.from_pydata(verts, [], faces)
    for p in gm.polygons:
        p.use_smooth = True
    gm.materials.append(mat_agua)
    _CACHE[chave_c] = gm
    return gm


def nova_lata(sc, nome, me_lata, mat, mat_alu=None, mat_agua=None, detalhes=True, gotas=True, sub=2, gotas_qtd=1.0):
    """Cria uma lata com o centro (meio da altura) na origem do empty retornado."""
    raiz = bpy.data.objects.new(nome, None)
    sc.collection.objects.link(raiz)
    raiz.scale = (RAIO, RAIO, 1.0)   # tamanho da lata: a altura fica fixa e o diametro escala
    corpo = bpy.data.objects.new(nome + "_corpo", me_lata)
    corpo.data.materials.clear() if False else None
    if not me_lata.materials:
        me_lata.materials.append(mat)
    corpo.location = (0, 0, -MEIO)
    corpo.parent = raiz
    sc.collection.objects.link(corpo)
    m = corpo.modifiers.new("sub", "SUBSURF"); m.levels = m.render_levels = sub
    filhos = [corpo]
    if detalhes:
        cu, rb, cl = dados_detalhes(mat_alu)
        for dado, z, nm in ((cu, TAMPA + 0.017, "_lacre"), (rb, TAMPA + 0.007, "_rebite"), (cl, 0.0, "_abertura")):
            ob = bpy.data.objects.new(nome + nm, dado)
            ob.location = (0, 0, z - MEIO)
            if nm == "_lacre":
                ob.rotation_euler = (0, math.radians(-3), 0)
            ob.parent = raiz
            sc.collection.objects.link(ob)
            filhos.append(ob)
    if gotas:
        ob = bpy.data.objects.new(nome + "_gotas", dados_gotas(mat_agua, gotas_qtd))
        ob.location = (0, 0, -MEIO)
        ob.parent = raiz
        sc.collection.objects.link(ob)
        filhos.append(ob)
    return raiz, filhos


# ---------- frutas procedurais (pecas da explosao) ----------
def _mat_fruta(nome, polpa, casca, entrecasca, sementes=False, gomos=0):
    """Material radial pra rodela/fatia: r normalizado pelo raio (atributo do objeto em coords de objeto)."""
    m = bpy.data.materials.new(nome)
    n, l = nos(m)
    b = n["Principled BSDF"]
    tc = n.new("ShaderNodeTexCoord")
    sep = n.new("ShaderNodeSeparateXYZ"); l.new(tc.outputs["Object"], sep.inputs[0])
    comb = n.new("ShaderNodeCombineXYZ"); l.new(sep.outputs["X"], comb.inputs["X"]); l.new(sep.outputs["Y"], comb.inputs["Y"])
    raio = n.new("ShaderNodeVectorMath"); raio.operation = "LENGTH"; l.new(comb.outputs[0], raio.inputs[0])
    rampa = n.new("ShaderNodeValToRGB"); rampa.color_ramp.interpolation = "LINEAR"
    e = rampa.color_ramp.elements
    e[0].position = 0.0; e[0].color = (*polpa, 1)
    e[1].position = 0.80; e[1].color = (*polpa, 1)
    e.new(0.86).color = (*entrecasca, 1)
    e.new(0.92).color = (*entrecasca, 1)
    e.new(0.95).color = (*casca, 1)
    l.new(raio.outputs[0], rampa.inputs["Fac"])
    cor = rampa.outputs["Color"]
    if gomos:
        # membranas brancas entre os gomos
        ang = n.new("ShaderNodeMath"); ang.operation = "ARCTAN2"
        l.new(sep.outputs["Y"], ang.inputs[0]); l.new(sep.outputs["X"], ang.inputs[1])
        mul = n.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = gomos / math.tau
        l.new(ang.outputs[0], mul.inputs[0])
        fr = n.new("ShaderNodeMath"); fr.operation = "FRACT"; l.new(mul.outputs[0], fr.inputs[0])
        dist = n.new("ShaderNodeMath"); dist.operation = "PINGPONG"; dist.inputs[1].default_value = 0.5
        l.new(fr.outputs[0], dist.inputs[0])
        lin = n.new("ShaderNodeMath"); lin.operation = "LESS_THAN"; lin.inputs[1].default_value = 0.035
        l.new(dist.outputs[0], lin.inputs[0])
        dentro = n.new("ShaderNodeMath"); dentro.operation = "LESS_THAN"; dentro.inputs[1].default_value = 0.82
        l.new(raio.outputs[0], dentro.inputs[0])
        centro = n.new("ShaderNodeMath"); centro.operation = "LESS_THAN"; centro.inputs[1].default_value = 0.08
        l.new(raio.outputs[0], centro.inputs[0])
        memb = n.new("ShaderNodeMath"); memb.operation = "MULTIPLY"
        l.new(lin.outputs[0], memb.inputs[0]); l.new(dentro.outputs[0], memb.inputs[1])
        memb2 = n.new("ShaderNodeMath"); memb2.operation = "MAXIMUM"
        l.new(memb.outputs[0], memb2.inputs[0]); l.new(centro.outputs[0], memb2.inputs[1])
        mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"
        l.new(memb2.outputs[0], mx.inputs["Factor"]); l.new(cor, mx.inputs["A"]); mx.inputs["B"].default_value = (*entrecasca, 1)
        cor = mx.outputs["Result"]
    if sementes:
        vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 9.0
        l.new(tc.outputs["Object"], vor.inputs["Vector"])
        sem = n.new("ShaderNodeMath"); sem.operation = "LESS_THAN"; sem.inputs[1].default_value = 0.07
        l.new(vor.outputs["Distance"], sem.inputs[0])
        zona = n.new("ShaderNodeMath"); zona.operation = "LESS_THAN"; zona.inputs[1].default_value = 0.62
        l.new(raio.outputs[0], zona.inputs[0])
        zona2 = n.new("ShaderNodeMath"); zona2.operation = "GREATER_THAN"; zona2.inputs[1].default_value = 0.3
        l.new(raio.outputs[0], zona2.inputs[0])
        z3 = n.new("ShaderNodeMath"); z3.operation = "MULTIPLY"; l.new(zona.outputs[0], z3.inputs[0]); l.new(zona2.outputs[0], z3.inputs[1])
        s2 = n.new("ShaderNodeMath"); s2.operation = "MULTIPLY"; l.new(sem.outputs[0], s2.inputs[0]); l.new(z3.outputs[0], s2.inputs[1])
        mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"
        l.new(s2.outputs[0], mx.inputs["Factor"]); l.new(cor, mx.inputs["A"]); mx.inputs["B"].default_value = (0.01, 0.008, 0.006, 1)
        cor = mx.outputs["Result"]
    l.new(cor, b.inputs["Base Color"])
    l.new(cor, b.inputs["Subsurface Radius"]) if False else None
    b.inputs["Subsurface Weight"].default_value = 0.35
    b.inputs["Subsurface Scale"].default_value = 0.05
    b.inputs["Roughness"].default_value = 0.22
    b.inputs["Coat Weight"].default_value = 0.5
    b.inputs["Coat Roughness"].default_value = 0.05
    # vesiculas de suco
    ns = n.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 60; ns.inputs["Detail"].default_value = 4
    l.new(tc.outputs["Object"], ns.inputs["Vector"])
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.25; bp.inputs["Distance"].default_value = 0.004
    l.new(ns.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def malha_disco(nome, raio, esp, angulo=math.tau, seg=48):
    """Disco (rodela) ou fatia de pizza (angulo < tau), raio 1 em coords de objeto antes da escala."""
    bm = bmesh.new()
    pts = [(0.0, 0.0)] + [(math.cos(angulo * i / seg - angulo / 2), math.sin(angulo * i / seg - angulo / 2)) for i in range(seg + (0 if angulo >= math.tau else 1))]
    if angulo >= math.tau:
        pts = pts[1:]
    base = [bm.verts.new((x, y, -esp / 2)) for x, y in pts]
    face = bm.faces.new(base)
    r = bmesh.ops.extrude_face_region(bm, geom=[face])
    for v in [g for g in r["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z += esp
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(nome)
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = False
    return me


def pecas_fruta():
    """Retorna dict sabor -> lista de (malha, material, escala) pra explosao."""
    if "frutas" in _CACHE:
        return _CACHE["frutas"]
    lim = _mat_fruta("limao", polpa=(0.62, 0.78, 0.12), casca=(0.05, 0.22, 0.03), entrecasca=(0.85, 0.9, 0.7), gomos=10)
    man = bpy.data.materials.new("manga")
    n, l = nos(man)
    b = n["Principled BSDF"]
    b.inputs["Base Color"].default_value = (1.0, 0.45, 0.02, 1)
    b.inputs["Subsurface Weight"].default_value = 0.5
    b.inputs["Subsurface Scale"].default_value = 0.08
    b.inputs["Roughness"].default_value = 0.28
    b.inputs["Coat Weight"].default_value = 0.6
    b.inputs["Coat Roughness"].default_value = 0.05
    ns = n.new("ShaderNodeTexWave"); ns.inputs["Scale"].default_value = 18; ns.inputs["Distortion"].default_value = 6
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.15
    l.new(ns.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    mel = _mat_fruta("melancia", polpa=(0.85, 0.06, 0.08), casca=(0.03, 0.16, 0.04), entrecasca=(0.75, 0.85, 0.6), sementes=True)
    disco = malha_disco("rodela", 1.0, 0.16)
    disco.materials.append(lim)
    bv = bmesh.new()
    bmesh.ops.create_cube(bv, size=1.0)
    bmesh.ops.bevel(bv, geom=bv.edges[:], offset=0.18, segments=4, affect="EDGES")
    cubo = bpy.data.meshes.new("cubo_manga"); bv.to_mesh(cubo); bv.free()
    for p in cubo.polygons:
        p.use_smooth = True
    cubo.materials.append(man)
    fatia = malha_disco("fatia", 1.0, 0.22, angulo=math.radians(55))
    fatia.materials.append(mel)
    agua = material_agua()
    bmw = bmesh.new()
    bmesh.ops.create_icosphere(bmw, subdivisions=3, radius=1.0)
    gm = bpy.data.meshes.new("gota_solta"); bmw.to_mesh(gm); bmw.free()
    for p in gm.polygons:
        p.use_smooth = True
    gm.materials.append(agua)
    _CACHE["frutas"] = {0: [(fatia, 0.55)], 1: [(disco, 0.36)], 2: [(cubo, 0.42)], 3: [(gm, 0.15)]}
    return _CACHE["frutas"]


# ---------- luz, camera, render ----------
def luz_area(sc, nome, loc, alvo, cor, forca, sx, sy):
    ld = bpy.data.lights.new(nome, "AREA")
    ld.shape = "RECTANGLE"; ld.size, ld.size_y = sx, sy
    ld.color = cor; ld.energy = forca
    ob = bpy.data.objects.new(nome, ld)
    ob.location = loc
    ob.rotation_euler = (Vector(alvo) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    sc.collection.objects.link(ob)
    return ob


def camera(sc, lente=50):
    alvo = bpy.data.objects.new("alvo", None)
    sc.collection.objects.link(alvo)
    cd = bpy.data.cameras.new("cam")
    cd.lens = lente
    cd.dof.use_dof = True
    cd.dof.focus_object = alvo
    cd.dof.aperture_blades = 7
    cd.clip_start = 0.01
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    tr = cam.constraints.new("TRACK_TO"); tr.target = alvo
    tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"
    return cam, alvo


def render(sc, qualidade, transparente=True, mblur=True):
    r = sc.render
    try:
        r.engine = "BLENDER_EEVEE_NEXT"   # Blender 4.2 a 4.4
    except TypeError:
        r.engine = "BLENDER_EEVEE"        # versoes mais novas voltaram o nome
    if qualidade == "final":
        r.resolution_x, r.resolution_y = 1920, 1080
        sc.eevee.taa_render_samples = int(os.environ.get("AMOSTRAS_FINAL", 24))   # 24 fica igual a 48 na pratica e leva metade do tempo
    elif qualidade == "rascunho":   # so pra conferir movimento e tempo
        r.resolution_x, r.resolution_y = 640, 360
        sc.eevee.taa_render_samples = 6
    else:
        r.resolution_x, r.resolution_y = 960, 540
        sc.eevee.taa_render_samples = 16
    r.resolution_percentage = 100
    r.fps = FPS
    r.film_transparent = transparente
    r.use_motion_blur = mblur
    r.motion_blur_position = "START"   # o borrao nao invade o quadro anterior nos cortes secos
    sc.eevee.use_raytracing = True
    sc.eevee.use_shadows = True
    sc.eevee.ray_tracing_options.resolution_scale = {"final": "1", "previa": "2"}.get(qualidade, "4")
    sc.eevee.ray_tracing_options.use_denoise = True
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "Medium High Contrast"
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGBA" if transparente else "RGB"


def chave_constante(dono, caminho, quadro, valor, indice=-1):
    """Insere chave e deixa a curva em CONSTANT (troca seca)."""
    if indice >= 0:
        getattr_set(dono, caminho, valor, indice)
    else:
        setattr_path(dono, caminho, valor)
    dono.keyframe_insert(caminho, frame=quadro, index=indice)
    ad = dono.animation_data if hasattr(dono, "animation_data") else None
    if ad and ad.action:
        for fc in curvas(ad.action):
            if fc.data_path == caminho:
                for k in fc.keyframe_points:
                    k.interpolation = "CONSTANT"


def setattr_path(dono, caminho, valor):
    partes = caminho.split(".")
    alvo = dono
    for p in partes[:-1]:
        alvo = getattr(alvo, p)
    setattr(alvo, partes[-1], valor)


def getattr_set(dono, caminho, valor, i):
    getattr(dono, caminho)[i] = valor


def assar(dono, caminho, quadros, valores, interp="LINEAR"):
    """Cria uma curva com uma chave por quadro (rapido, via foreach_set). valores: lista de float ou de tuplas."""
    if not dono.animation_data:
        dono.animation_data_create()
    if not dono.animation_data.action:
        dono.animation_data.action = bpy.data.actions.new(dono.name + "_acao")
    acao = dono.animation_data.action
    vals = [v if isinstance(v, (tuple, list)) else (v,) for v in valores]
    for i in range(len(vals[0])):
        fc = curva(acao, dono, caminho, i)
        fc.keyframe_points.add(len(quadros))
        co = np.empty(2 * len(quadros), dtype=np.float32)
        co[0::2] = quadros
        co[1::2] = [v[i] for v in vals]
        fc.keyframe_points.foreach_set("co", co)
        for k in fc.keyframe_points:
            k.interpolation = interp
        fc.update()


def renderizar(sc, pasta, q0, q1, so=None):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    quadros = so if so else range(q0, q1 + 1)
    for q in quadros:
        alvo = pasta / f"f_{q:04d}.png"
        if alvo.exists() and not so:
            continue  # retoma de onde parou
        sc.frame_set(q)
        sc.render.filepath = str(alvo)
        bpy.ops.render.render(write_still=True)


PECAS = PROJETO / "pecas" / "pecas.blend"


def carregar_frutas():
    """Malhas das pecas da explosao (preparar_pecas.py), centradas e com maior lado = 1. Retorna {nome: malha}."""
    if not PECAS.exists():
        return {}
    with bpy.data.libraries.load(str(PECAS), link=False) as (de, para):
        para.meshes = [m for m in de.meshes if m.startswith(("pc_", "fr_"))]
    return {m.name: m for m in para.meshes if m}


# lado do corte de cada peca (normal local, definido em preparar_pecas): o corte fica virado pra camera
FACE_CORTE = {k: tuple(v["face_corte"]) for k, v in C.CFG.get("pecas", {}).items() if v.get("face_corte")}


def virar_corte(nome, rnd, abertura=0.75, para=(0, -1, 0)):
    """rotacao (quaternion) que deixa o corte da fruta virado pra camera, com inclinacao e giro aleatorios"""
    alvo = Vector(para) + Vector((rnd.uniform(-1, 1), 0, rnd.uniform(-1, 1))) * abertura
    giro = Matrix.Rotation(rnd.uniform(0, math.tau), 4, alvo.normalized()).to_quaternion()
    if nome not in FACE_CORTE:
        return Vector((rnd.uniform(0, 6.3), rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)))
    q = Vector(FACE_CORTE[nome]).rotation_difference(alvo.normalized())
    return (giro @ q).to_euler()


def painel_estudio(sc, loc=(0, 9, 0), tam=(34, 22), forca=2.2, cor=(1, 1, 1)):
    """Painel de luz de estudio atras da cena: a camera nao ve, mas a agua refrata e a lata reflete
    (sem ele a agua no fundo escuro fica preta, porque refrata o preto)."""
    me = bpy.data.meshes.new("painel_estudio")
    w, h = tam[0] / 2, tam[1] / 2
    me.from_pydata([(-w, 0, -h), (w, 0, -h), (w, 0, h), (-w, 0, h)], [], [(0, 1, 2, 3)])
    m = bpy.data.materials.new("painel_estudio"); m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    n.remove(n["Principled BSDF"])
    tc = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(tc.outputs["Generated"], sep.inputs[0])
    # faixas macias verticais (como softboxes) com centro mais forte
    onda = n.new("ShaderNodeMath"); onda.operation = "SINE"
    mul = n.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 9.0
    l.new(sep.outputs["X"], mul.inputs[0]); l.new(mul.outputs[0], onda.inputs[0])
    faixa = n.new("ShaderNodeMapRange"); faixa.inputs["From Min"].default_value = -1; faixa.inputs["To Min"].default_value = 0.35
    l.new(onda.outputs[0], faixa.inputs["Value"])
    em = n.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (*cor, 1)
    forca_n = n.new("ShaderNodeMath"); forca_n.operation = "MULTIPLY"; forca_n.inputs[1].default_value = forca
    l.new(faixa.outputs["Result"], forca_n.inputs[0]); l.new(forca_n.outputs[0], em.inputs["Strength"])
    l.new(em.outputs[0], n["Material Output"].inputs["Surface"])
    me.materials.append(m)
    ob = bpy.data.objects.new("painel_estudio", me); sc.collection.objects.link(ob)
    ob.location = loc
    ob.visible_camera = False
    ob.visible_shadow = False
    # a refracao do Eevee so ve o que esta na tela; o resto vem da sonda, que enxerga o painel
    sd = bpy.data.lightprobes.new("sonda_estudio", "SPHERE")
    try:
        sd.influence_distance = 30
    except AttributeError:
        pass
    so = bpy.data.objects.new("sonda_estudio", sd); sc.collection.objects.link(so)
    so.location = (0, 0, 0)
    return ob
