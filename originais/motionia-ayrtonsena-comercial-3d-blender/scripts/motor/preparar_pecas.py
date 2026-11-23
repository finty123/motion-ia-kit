# Junta os modelos 3D baixados (frutas, ingredientes, respingo) numa biblioteca so: <projeto>/pecas/pecas.blend.
# Cada peca vira um objeto "pc_<nome>" centrado na origem, com o maior lado = 1, leve e com material molhado.
# O que fazer com cada arquivo vem de projeto.json -> "pecas" (veja references/pecas-3d.md).
# Uso: python rodar.py pecas   (acha o Blender e roda este script em prioridade baixa)
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy, bmesh
from mathutils import Vector, Matrix
import config as C

PECAS = C.PROJETO / "pecas"
bpy.ops.wm.read_factory_settings(use_empty=True)


def importar(arquivo):
    """importa gltf/glb, fbx, obj ou blend (um arquivo ou a primeira coisa importavel de uma pasta)"""
    p = PECAS / arquivo
    if p.is_dir():
        p = next((x for ext in ("*.gltf", "*.glb", "*.fbx", "*.obj", "*.blend") for x in p.rglob(ext)), None)
        if not p:
            raise FileNotFoundError(f"nada importavel em {arquivo}")
    antes = set(bpy.data.objects)
    ext = p.suffix.lower()
    if ext in (".gltf", ".glb"):
        bpy.ops.import_scene.gltf(filepath=str(p))
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(p))
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=str(p))
    elif ext == ".blend":
        with bpy.data.libraries.load(str(p), link=False) as (de, para):
            para.objects = list(de.objects)
        for o in para.objects:
            if o:
                bpy.context.collection.objects.link(o)
    return [o for o in bpy.data.objects if o not in antes and o.type == "MESH"]


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
        with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob]):
            bpy.ops.object.modifier_apply(modifier=m.name)
        print("decimado", ob.name, n, "->", len(ob.data.polygons))


def principled(mat):
    return next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if mat and mat.use_nodes else None


def iluminar(mat):
    """scan com material 'unlit' (ignora a luz, fica chapado): troca por um Principled com a textura"""
    n, l = mat.node_tree.nodes, mat.node_tree.links
    if principled(mat):
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


def molhar(mat, sss=0.0, coat=0.55):
    """fruta suculenta: verniz de agua por cima e um pouco de luz passando por dentro"""
    b = principled(mat)
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
    """peca clara que some no fundo claro (exposicao baixa por causa do rotulo claro): sobe o brilho da cor"""
    pb = principled(mat)
    if not pb or not pb.inputs["Base Color"].is_linked:
        return
    n, l = mat.node_tree.nodes, mat.node_tree.links
    origem = pb.inputs["Base Color"].links[0].from_socket
    hsv = n.new("ShaderNodeHueSaturation"); hsv.inputs["Value"].default_value = valor; hsv.inputs["Saturation"].default_value = sat
    l.new(origem, hsv.inputs["Color"]); l.new(hsv.outputs["Color"], pb.inputs["Base Color"])


def material_agua():
    """agua de anuncio: miolo transparente, bordas espelham a luz do estudio (Fresnel). Branco leitoso = errado."""
    agua = bpy.data.materials.new("pc_agua"); agua.use_nodes = True
    agua.surface_render_method = "DITHERED"
    an, al = agua.node_tree.nodes, agua.node_tree.links
    an.remove(an["Principled BSDF"])
    fr = an.new("ShaderNodeFresnel"); fr.inputs["IOR"].default_value = 1.33
    lw = an.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.25
    bordas = an.new("ShaderNodeMath"); bordas.operation = "MULTIPLY_ADD"
    al.new(lw.outputs["Facing"], bordas.inputs[0]); bordas.inputs[1].default_value = 0.55; al.new(fr.outputs[0], bordas.inputs[2])
    fator = an.new("ShaderNodeMath"); fator.operation = "MINIMUM"; fator.inputs[1].default_value = 1.0
    al.new(bordas.outputs[0], fator.inputs[0])
    brilho = an.new("ShaderNodeBsdfGlossy"); brilho.inputs["Roughness"].default_value = 0.02
    transp = an.new("ShaderNodeBsdfTransparent"); transp.inputs["Color"].default_value = (0.94, 0.97, 1.0, 1)
    mixa = an.new("ShaderNodeMixShader"); al.new(fator.outputs[0], mixa.inputs["Fac"])
    al.new(transp.outputs[0], mixa.inputs[1]); al.new(brilho.outputs[0], mixa.inputs[2])
    al.new(mixa.outputs[0], an["Material Output"].inputs["Surface"])
    return agua


def material_polpa(nome, cor_hex, sementes=False):
    """polpa da face cortada de uma fatia: cor, granulado, luz passando por dentro e umida"""
    m = bpy.data.materials.new(nome); m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    pb = n["Principled BSDF"]
    cor = (*C.hex_rgb(cor_hex, linear=True), 1)
    if sementes:
        vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 26
        sem = n.new("ShaderNodeMath"); sem.operation = "LESS_THAN"; sem.inputs[1].default_value = 0.09
        l.new(vor.outputs["Distance"], sem.inputs[0])
        mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"
        l.new(sem.outputs[0], mx.inputs["Factor"]); mx.inputs["A"].default_value = cor; mx.inputs["B"].default_value = (0.015, 0.008, 0.006, 1)
        l.new(mx.outputs["Result"], pb.inputs["Base Color"])
    else:
        pb.inputs["Base Color"].default_value = cor
    ru = n.new("ShaderNodeTexNoise"); ru.inputs["Scale"].default_value = 160; ru.inputs["Detail"].default_value = 6
    bump = n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35; bump.inputs["Distance"].default_value = 0.003
    l.new(ru.outputs["Fac"], bump.inputs["Height"]); l.new(bump.outputs["Normal"], pb.inputs["Normal"])
    pb.inputs["Roughness"].default_value = 0.42
    pb.inputs["Subsurface Weight"].default_value = 0.45
    pb.inputs["Subsurface Scale"].default_value = 0.03
    pb.inputs["Coat Weight"].default_value = 0.6
    pb.inputs["Coat Roughness"].default_value = 0.05
    return m


def fatiar(inteira, nome, ang0, ang1, esp, polpa):
    """fatia de verdade de uma peca inteira: disco de espessura esp no meio (eixo Z) e cunha de ang0 a ang1;
    cada corte e tampado com a polpa"""
    ob = inteira.copy(); ob.data = inteira.data.copy(); bpy.context.collection.objects.link(ob)
    if polpa.name not in [m.name for m in ob.data.materials if m]:
        ob.data.materials.append(polpa)
    i_polpa = [m.name if m else "" for m in ob.data.materials].index(polpa.name)
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)
    a0, a1 = math.radians(ang0), math.radians(ang1)
    planos = [((0, 0, esp / 2), (0, 0, 1)), ((0, 0, -esp / 2), (0, 0, -1)), ((0, 0, 0), (math.sin(a0), -math.cos(a0), 0))]
    if ang1 - ang0 < 179:
        planos.append(((0, 0, 0), (-math.sin(a1), math.cos(a1), 0)))
    for co, no in planos:
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], dist=1e-5,
                               plane_co=co, plane_no=no, clear_outer=True)
        noV, coV = Vector(no), Vector(co)
        borda = [e for e in bm.edges if e.is_boundary and all(abs((v.co - coV).dot(noV)) < 1e-4 for v in e.verts)]
        novo = bmesh.ops.holes_fill(bm, edges=borda, sides=0)
        if novo["faces"]:
            bmesh.ops.triangulate(bm, faces=novo["faces"])
        for f in bm.faces:
            if all(abs((v.co - coV).dot(noV)) < 1e-4 for v in f.verts):
                f.material_index = i_polpa
    bm.to_mesh(ob.data); bm.free()
    me = ob.data
    pts = [v.co for v in me.vertices]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    c, lado = (mn + mx) / 2, max(mx - mn)
    me.transform(Matrix.Scale(1 / lado, 4) @ Matrix.Translation(-c))
    ob.name = me.name = nome
    return ob


defs = C.CFG.get("pecas", {})
if not defs:
    sys.exit("projeto.json nao tem 'pecas'")
feitas = {}
for nome, d in defs.items():
    if "fatia_de" in d:
        continue
    obs = importar(d["arquivo"])
    if d.get("so"):        # pega so as partes com esse texto no nome (ex.: "Half")
        obs = [o for o in obs if d["so"] in o.name]
    if d.get("excluir"):
        obs = [o for o in obs if d["excluir"] not in o.name]
    if not obs:
        sys.exit(f"{nome}: nenhuma malha em {d['arquivo']}")
    ob = juntar(obs, nome)
    decimar(ob, int(d.get("max_faces", 150000)))
    if d.get("agua"):
        ob.data.materials.clear(); ob.data.materials.append(material_agua())
    else:
        for m in ob.data.materials:
            if not m:
                continue
            iluminar(m)
            molhar(m, sss=float(d.get("sss", 0.0)), coat=float(d.get("verniz", 0.55)))
            if d.get("clarear"):
                clarear(m, *d["clarear"])
    feitas[nome] = ob
    print("peca", nome, len(ob.data.polygons), "faces")
for nome, d in defs.items():       # fatias cortadas de uma peca inteira ja importada
    if "fatia_de" in d:
        polpa = material_polpa(nome + "_polpa", d.get("polpa", "#d8202a"), d.get("sementes", False))
        fatiar(feitas[d["fatia_de"]], nome, *d.get("angulos", [0, 50]), float(d.get("espessura", 0.13)), polpa)
        print("fatia", nome)
for o in list(bpy.data.objects):
    if o.name not in defs:
        bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(PECAS / "pecas.blend"), compress=True)
print("pecas.blend salvo com", len(defs), "pecas")
