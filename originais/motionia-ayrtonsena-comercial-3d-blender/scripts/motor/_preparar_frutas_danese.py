# Prepara as frutas baixadas (modelos-frutas/) numa biblioteca so: modelos-frutas/frutas.blend
# Cada objeto "fr_*" fica centrado na origem, com o maior lado = 1, leve e com material de fruta molhada.
# Uso: blender -b -P preparar_frutas.py
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy, bmesh
from mathutils import Vector, Matrix

BASE = Path(__file__).resolve().parents[1] / "modelos-frutas"
bpy.ops.wm.read_factory_settings(use_empty=True)


def importar(pasta, filtro=None):
    antes = set(bpy.data.objects)
    gl = next((BASE / pasta).glob("*.gltf"))
    bpy.ops.import_scene.gltf(filepath=str(gl))
    novos = [o for o in bpy.data.objects if o not in antes and o.type == "MESH"]
    if filtro:
        novos = [o for o in novos if filtro(o)]
    return novos


def juntar(obs, nome):
    """junta as partes, aplica transformacoes, centra e normaliza o maior lado em 1"""
    bpy.ops.object.select_all(action="DESELECT")
    for o in obs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    if len(obs) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.parent = None
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    me = ob.data
    pts = [v.co for v in me.vertices]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    c, lado = (mn + mx) / 2, max(mx - mn)
    me.transform(Matrix.Scale(1 / lado, 4) @ Matrix.Translation(-c))
    ob.location = (0, 0, 0)
    ob.name = me.name = nome
    for p in me.polygons:
        p.use_smooth = True
    return ob


def decimar(ob, alvo):
    n = len(ob.data.polygons)
    if n > alvo:
        m = ob.modifiers.new("dec", "DECIMATE"); m.ratio = alvo / n
        bpy.ops.object.select_all(action="DESELECT"); ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
        with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob]):
            bpy.ops.object.modifier_apply(modifier=m.name)
        print("decimado", ob.name, n, "->", len(ob.data.polygons))


def molhar(mat, sss=0.0, coat=0.55):
    """fruta suculenta: verniz de agua por cima e um pouco de luz passando por dentro"""
    b = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if not b:
        return
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.06
    b.inputs["Coat IOR"].default_value = 1.33
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (1.0, 0.35, 0.15)
        b.inputs["Subsurface Scale"].default_value = 0.02
    b.inputs["Metallic"].default_value = 0.0


def clarear(mat, valor=1.7, sat=1.12):
    """o limao some no fundo branco (exposicao baixa por causa do rotulo branco): sobe o brilho da cor"""
    n, l = mat.node_tree.nodes, mat.node_tree.links
    pb = next((x for x in n if x.type == "BSDF_PRINCIPLED"), None)
    if not pb or not pb.inputs["Base Color"].is_linked:
        return
    origem = pb.inputs["Base Color"].links[0].from_socket
    hsv = n.new("ShaderNodeHueSaturation"); hsv.inputs["Value"].default_value = valor; hsv.inputs["Saturation"].default_value = sat
    l.new(origem, hsv.inputs["Color"]); l.new(hsv.outputs["Color"], pb.inputs["Base Color"])


def iluminar(mat):
    """os scans da Arkify vem com material 'unlit' (ignora a luz, fica chapado): troca por um Principled com a textura"""
    n, l = mat.node_tree.nodes, mat.node_tree.links
    if any(x.type == "BSDF_PRINCIPLED" for x in n):
        return
    tex = next((x for x in n if x.type == "TEX_IMAGE"), None)
    saida = next(x for x in n if x.type == "OUTPUT_MATERIAL")
    for x in list(n):
        if x not in (tex, saida):
            n.remove(x)
    pb = n.new("ShaderNodeBsdfPrincipled")
    pb.inputs["Roughness"].default_value = 0.45
    if tex:
        l.new(tex.outputs["Color"], pb.inputs["Base Color"])
        rug = n.new("ShaderNodeBump"); rug.inputs["Strength"].default_value = 0.25; rug.inputs["Distance"].default_value = 0.002
        l.new(tex.outputs["Color"], rug.inputs["Height"]); l.new(rug.outputs["Normal"], pb.inputs["Normal"])
    l.new(pb.outputs[0], saida.inputs["Surface"])
    print("iluminado", mat.name)


def remover_resto():
    for o in list(bpy.data.objects):
        if not o.name.startswith("fr_"):
            bpy.data.objects.remove(o, do_unlink=True)


# --- limao ---
juntar(importar("09-limao-rodela"), "fr_limao_rodela")
juntar(importar("10-limao-polyhaven"), "fr_limao_inteiro")
# --- manga ---
metade = importar("05-manga-metade")
so_metade = [o for o in metade if "Half" in o.name]
so_inteira = [o for o in metade if "Half" not in o.name]
juntar(so_metade, "fr_manga_metade")
juntar(so_inteira, "fr_manga_inteira")
juntar(importar("06-manga-fatia"), "fr_manga_fatia")
# --- respingo: vira agua transparente ---
resp = juntar(importar("12-respingo"), "fr_respingo"); decimar(resp, 150000)
agua = bpy.data.materials.new("fr_agua"); agua.use_nodes = True
agua.surface_render_method = "DITHERED"
an, al = agua.node_tree.nodes, agua.node_tree.links
an.remove(an["Principled BSDF"])
# agua de anuncio: miolo transparente (mostra o que esta atras), bordas espelham a luz do estudio (Fresnel)
fr = an.new("ShaderNodeFresnel"); fr.inputs["IOR"].default_value = 1.33
lw = an.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.25
bordas = an.new("ShaderNodeMath"); bordas.operation = "MULTIPLY_ADD"
al.new(lw.outputs["Facing"], bordas.inputs[0]); bordas.inputs[1].default_value = 0.55; al.new(fr.outputs[0], bordas.inputs[2])
fator = an.new("ShaderNodeMath"); fator.operation = "MINIMUM"; fator.inputs[1].default_value = 1.0
al.new(bordas.outputs[0], fator.inputs[0])
brilho = an.new("ShaderNodeBsdfGlossy"); brilho.inputs["Roughness"].default_value = 0.02
brilho.inputs["Color"].default_value = (1, 1, 1, 1)
transp = an.new("ShaderNodeBsdfTransparent"); transp.inputs["Color"].default_value = (0.94, 0.97, 1.0, 1)
mixa = an.new("ShaderNodeMixShader"); al.new(fator.outputs[0], mixa.inputs["Fac"])
al.new(transp.outputs[0], mixa.inputs[1]); al.new(brilho.outputs[0], mixa.inputs[2])
al.new(mixa.outputs[0], an["Material Output"].inputs["Surface"])
resp.data.materials.clear(); resp.data.materials.append(agua)

# --- melancia: a inteira escaneada (malha leve + normal map) cortada em fatias com polpa ---
inteira = juntar(importar("03-melancia", lambda o: "low" in o.name), "fr_melancia_inteira")
sub = inteira.modifiers.new("sub", "SUBSURF"); sub.levels = sub.render_levels = 2
bpy.context.view_layer.objects.active = inteira
bpy.ops.object.modifier_apply(modifier="sub")
bm = bmesh.new(); bm.from_mesh(inteira.data)
bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
bm.to_mesh(inteira.data); bm.free()
orig = inteira.data.attributes.new("orig", "FLOAT_VECTOR", "POINT")
orig.data.foreach_set("vector", [c for v in inteira.data.vertices for c in v.co])

polpa = bpy.data.materials.new("fr_polpa_melancia"); polpa.use_nodes = True
n, l = polpa.node_tree.nodes, polpa.node_tree.links
pb = n["Principled BSDF"]
tc = n.new("ShaderNodeTexCoord")
# distancia ao centro (normalizada pelo raio ~0.5): define casca, faixa branca, polpa
pos = n.new("ShaderNodeAttribute"); pos.attribute_name = "orig"
so_xy = n.new("ShaderNodeVectorMath"); so_xy.operation = "MULTIPLY"; so_xy.inputs[1].default_value = (1, 1, 0.25)
l.new(pos.outputs["Vector"], so_xy.inputs[0])
dist = n.new("ShaderNodeVectorMath"); dist.operation = "LENGTH"; l.new(so_xy.outputs[0], dist.inputs[0])
rr = n.new("ShaderNodeMath"); rr.operation = "DIVIDE"; rr.inputs[1].default_value = 0.455; l.new(dist.outputs["Value"], rr.inputs[0])
rampa = n.new("ShaderNodeValToRGB"); l.new(rr.outputs[0], rampa.inputs["Fac"])
cr = rampa.color_ramp
cr.elements[0].position = 0.0; cr.elements[0].color = (0.55, 0.012, 0.03, 1)
cr.elements[1].position = 0.80; cr.elements[1].color = (0.80, 0.06, 0.07, 1)
for posr, cor in ((0.88, (0.95, 0.42, 0.40, 1)), (0.915, (0.88, 0.93, 0.78, 1)), (0.955, (0.55, 0.78, 0.38, 1)), (0.98, (0.05, 0.16, 0.04, 1))):
    e = cr.elements.new(posr); e.color = cor
# sementes: celulas voronoi so numa faixa do raio
vor = n.new("ShaderNodeTexVoronoi"); vor.feature = "F1"; vor.inputs["Scale"].default_value = 26
mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 1.0, 1.9)
l.new(pos.outputs["Vector"], mp.inputs["Vector"]); l.new(mp.outputs["Vector"], vor.inputs["Vector"])
sem = n.new("ShaderNodeMath"); sem.operation = "LESS_THAN"; sem.inputs[1].default_value = 0.11; l.new(vor.outputs["Distance"], sem.inputs[0])
faixa1 = n.new("ShaderNodeMath"); faixa1.operation = "GREATER_THAN"; faixa1.inputs[1].default_value = 0.42; l.new(rr.outputs[0], faixa1.inputs[0])
faixa2 = n.new("ShaderNodeMath"); faixa2.operation = "LESS_THAN"; faixa2.inputs[1].default_value = 0.68; l.new(rr.outputs[0], faixa2.inputs[0])
fx = n.new("ShaderNodeMath"); fx.operation = "MULTIPLY"; l.new(faixa1.outputs[0], fx.inputs[0]); l.new(faixa2.outputs[0], fx.inputs[1])
sorteio = n.new("ShaderNodeMath"); sorteio.operation = "GREATER_THAN"; sorteio.inputs[1].default_value = 0.55; l.new(vor.outputs["Color"], sorteio.inputs[0])
s1 = n.new("ShaderNodeMath"); s1.operation = "MULTIPLY"; l.new(sem.outputs[0], s1.inputs[0]); l.new(fx.outputs[0], s1.inputs[1])
s2 = n.new("ShaderNodeMath"); s2.operation = "MULTIPLY"; l.new(s1.outputs[0], s2.inputs[0]); l.new(sorteio.outputs[0], s2.inputs[1])
mixs = n.new("ShaderNodeMix"); mixs.data_type = "RGBA"
l.new(s2.outputs[0], mixs.inputs["Factor"]); l.new(rampa.outputs["Color"], mixs.inputs["A"]); mixs.inputs["B"].default_value = (0.015, 0.008, 0.006, 1)
l.new(mixs.outputs["Result"], pb.inputs["Base Color"])
# textura granulada da polpa (bump) + umida
ru = n.new("ShaderNodeTexNoise"); ru.inputs["Scale"].default_value = 160; ru.inputs["Detail"].default_value = 6
bump = n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35; bump.inputs["Distance"].default_value = 0.003
l.new(ru.outputs["Fac"], bump.inputs["Height"]); l.new(bump.outputs["Normal"], pb.inputs["Normal"])
pb.inputs["Roughness"].default_value = 0.42
pb.inputs["Subsurface Weight"].default_value = 0.45
pb.inputs["Subsurface Radius"].default_value = (1.0, 0.25, 0.2)
pb.inputs["Subsurface Scale"].default_value = 0.03
pb.inputs["Coat Weight"].default_value = 0.6
pb.inputs["Coat Roughness"].default_value = 0.05
inteira.data.materials.append(polpa)


def fatia(nome, ang0, ang1, esp):
    """fatia de verdade: disco de espessura esp no meio do melao (eixo Z) e cunha de ang0 a ang1 a partir do centro.
    Corta com planos (bisect) e tampa cada corte com a polpa (material 1)."""
    ob = inteira.copy(); ob.data = inteira.data.copy(); bpy.context.collection.objects.link(ob)
    bm = bmesh.new(); bm.from_mesh(ob.data)
    a0, a1 = math.radians(ang0), math.radians(ang1)
    planos = [((0, 0, esp / 2), (0, 0, 1)), ((0, 0, -esp / 2), (0, 0, -1)),
              ((0, 0, 0), (math.sin(a0), -math.cos(a0), 0))]
    if ang1 - ang0 < 179:
        planos.append(((0, 0, 0), (-math.sin(a1), math.cos(a1), 0)))
    for co, no in planos:
        r = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], dist=1e-5,
                                   plane_co=co, plane_no=no, clear_outer=True)
        bm.edges.ensure_lookup_table()
        noV, coV = Vector(no), Vector(co)
        borda = [e for e in bm.edges if e.is_boundary and all(abs((v.co - coV).dot(noV)) < 1e-4 for v in e.verts)]
        novo = bmesh.ops.holes_fill(bm, edges=borda, sides=0)
        faces = novo["faces"]
        if faces:
            bmesh.ops.triangulate(bm, faces=faces)
        for f in bm.faces:
            if f.material_index == 0 and all(abs((v.co - coV).dot(noV)) < 1e-4 for v in f.verts):
                f.material_index = 1
    bm.to_mesh(ob.data); bm.free()
    # os vertices novos do corte tambem precisam da posicao original
    me = ob.data
    at = me.attributes["orig"]
    at.data.foreach_set("vector", [c for v in me.vertices for c in v.co])
    pts = [v.co for v in me.vertices]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    c, lado = (mn + mx) / 2, max(mx - mn)
    me.transform(Matrix.Scale(1 / lado, 4) @ Matrix.Translation(-c))
    ob.name = me.name = nome
    print("fatia", nome, len(me.polygons), "faces", tuple(round(v, 3) for v in (mx - mn)))
    return ob


fatia("fr_melancia_fatia", 0, 50, 0.13)
fatia("fr_melancia_fatia_fina", 0, 180, 0.07)

for nome in ("fr_limao_rodela", "fr_manga_fatia"):
    for m in bpy.data.objects[nome].data.materials:
        iluminar(m)
for ob in [o for o in bpy.data.objects if o.name.startswith("fr_")]:
    for m in ob.data.materials:
        if m and m.name != "fr_agua":
            molhar(m, sss=0.35 if any(k in ob.name for k in ("rodela", "metade", "fatia")) else 0.0)
for nome, val, sat in (("fr_limao_rodela", 1.5, 1.3), ("fr_limao_inteiro", 1.7, 1.12)):
    for m in bpy.data.objects[nome].data.materials:
        clarear(m, val, sat)
        if nome == "fr_limao_rodela":   # verniz forte acinzenta a polpa clara
            pb = next((x for x in m.node_tree.nodes if x.type == "BSDF_PRINCIPLED"), None)
            if pb:
                pb.inputs["Coat Weight"].default_value = 0.25
                # luz atravessando a polpa: um pouco de emissao na propria cor
                if pb.inputs["Base Color"].is_linked:
                    m.node_tree.links.new(pb.inputs["Base Color"].links[0].from_socket, pb.inputs["Emission Color"])
                    pb.inputs["Emission Strength"].default_value = 0.15
for o in bpy.data.objects:
    print(o.name, len(o.data.vertices) if o.type == "MESH" else "", [m.name for m in o.data.materials] if o.type == "MESH" else "")
remover_resto()
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(BASE / "frutas.blend"), compress=True)
print("frutas.blend salvo")
