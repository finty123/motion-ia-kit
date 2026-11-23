# Fabrica de latas em 3D a partir do rotulo planificado: giro 360 + closes (Blender 4.2+, Eevee), vertical 1080x1920.
# O tamanho vem da variavel RAIO_LATA (diametro relativo a lata fina de 350 ml; o latas.py calcula).
# Uso: blender -b -P fazer_lata.py -- <rotulo> <pasta_saida> [previa | anim | frames separados por virgula]
import bpy, bmesh, math, os, random, sys
import numpy as np
from mathutils import Vector, Matrix

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


args = sys.argv[sys.argv.index("--") + 1:]
ROTULO, OUT = args[0], args[1]
MODO = args[2] if len(args) > 2 else "previa"
QUADROS_PREVIA = {"frente": 300, "giro": 60, "tampa": 240}

random.seed(11)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

_h = os.environ.get("COR_LATA", "#ff0f6b").lstrip("#")
ROSA = tuple(int(_h[i:i + 2], 16) / 255 for i in (0, 2, 4))   # cor do sabor (contraluz e bokeh)
LIMA = (0.85, 0.92, 1.0)                                       # contraluz fria do outro lado

RAIO = float(os.environ.get("RAIO_LATA", "1"))

# ---------- perfil da lata fina 350 ml (raio 1 = 29 mm); outros tamanhos escalam o diametro ----------
perfil = [
    (0.001, 0.28), (0.5, 0.2), (0.76, 0.07), (0.86, 0.0), (0.94, 0.04),
    (0.985, 0.15), (1.0, 0.30), (1.0, 4.45), (0.995, 4.53), (0.975, 4.62),
    (0.935, 4.73), (0.895, 4.83), (0.878, 4.90), (0.88, 4.94), (0.892, 4.975),
    (0.897, 4.995), (0.888, 5.015), (0.870, 5.018), (0.856, 5.0), (0.85, 4.97),
    (0.842, 4.925), (0.826, 4.895), (0.805, 4.885), (0.785, 4.892), (0.77, 4.902),
    (0.70, 4.906), (0.45, 4.908), (0.001, 4.91),
]
TAMPA = 4.908
Z0, Z1 = 0.17, 4.50  # faixa da arte do rotulo
PESCOCO = 4.895      # acima de Z1 a lata e impressa na cor de fundo ate a borda

bm = bmesh.new()
vs = [bm.verts.new((r, 0, z)) for r, z in perfil]
es = [bm.edges.new((vs[i], vs[i + 1])) for i in range(len(vs) - 1)]
bmesh.ops.spin(bm, geom=vs + es, cent=(0, 0, 0), axis=(0, 0, 1),
               angle=math.tau, steps=192, use_merge=True)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
# UV: u = volta em torno da lata (frente do rotulo em +x), v = altura dentro da faixa
uvl = bm.loops.layers.uv.new()
for f in bm.faces:
    us = []
    for lo in f.loops:
        x, y, z = lo.vert.co
        us.append((math.atan2(y, x) + math.pi) / math.tau)
    if max(us) - min(us) > 0.5:
        us = [u + 1 if u < 0.5 else u for u in us]
    for lo, u in zip(f.loops, us):
        lo[uvl].uv = (u, (lo.vert.co.z - Z0) / (Z1 - Z0))
me = bpy.data.meshes.new("lata")
bm.to_mesh(me); bm.free()
lata = bpy.data.objects.new("lata", me)
sc.collection.objects.link(lata)
for p in me.polygons:
    p.use_smooth = True
sub = lata.modifiers.new("sub", "SUBSURF")
sub.levels = sub.render_levels = 2


def nos(mat):
    mat.use_nodes = True
    return mat.node_tree.nodes, mat.node_tree.links


# material: rotulo impresso (verniz brilhante) na faixa, aluminio fora dela
mat = bpy.data.materials.new("lata")
n, l = nos(mat)
saida = n["Material Output"]
n.remove(n["Principled BSDF"])
img = n.new("ShaderNodeTexImage")
img.image = bpy.data.images.load(ROTULO)
img.extension = "REPEAT"
img.interpolation = "Cubic"
uvn = n.new("ShaderNodeUVMap")
l.new(uvn.outputs["UV"], img.inputs["Vector"])


def cor_de_fundo(im):
    # cor mais frequente na faixa de cima do rotulo (o fundo que sobe pelo pescoco)
    w_, h_ = im.size
    px = np.empty(w_ * h_ * 4, dtype=np.float32)
    im.pixels.foreach_get(px)
    topo = px.reshape(h_, w_, 4)[int(h_ * 0.96):, :, :3].reshape(-1, 3)
    q = np.round(topo * 15).astype(int)
    chaves, contagem = np.unique(q, axis=0, return_counts=True)
    escolhida = chaves[contagem.argmax()]
    srgb = topo[(q == escolhida).all(axis=1)].mean(axis=0)
    return [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]


def brilho_medio(im):
    w_, h_ = im.size
    px = np.empty(w_ * h_ * 4, dtype=np.float32)
    im.pixels.foreach_get(px)
    rgb = px.reshape(-1, 4)[::7, :3]
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return float((lin @ np.array([0.2126, 0.7152, 0.0722])).mean())


# rotulo claro (branco/prata) estoura com a mesma luz: baixa a exposicao conforme o brilho
BRILHO = brilho_medio(img.image)
EXPOSICAO = -0.35 - max(0.0, BRILHO - 0.3) * 1.6
print("BRILHO DO ROTULO:", round(BRILHO, 3), "EXPOSICAO:", round(EXPOSICAO, 2))
fundo_rgb = cor_de_fundo(img.image)
print("COR DO PESCOCO (linear):", [round(c, 3) for c in fundo_rgb])
cor_pescoco = n.new("ShaderNodeRGB")
cor_pescoco.outputs[0].default_value = (*fundo_rgb, 1)
tc = n.new("ShaderNodeTexCoord")
sep = n.new("ShaderNodeSeparateXYZ")
l.new(tc.outputs["Object"], sep.inputs[0])
no_pescoco = n.new("ShaderNodeMath"); no_pescoco.operation = "GREATER_THAN"
no_pescoco.inputs[1].default_value = Z1
l.new(sep.outputs["Z"], no_pescoco.inputs[0])
cor_final = n.new("ShaderNodeMix")
cor_final.data_type = "RGBA"
l.new(no_pescoco.outputs[0], cor_final.inputs["Factor"])
l.new(img.outputs["Color"], cor_final.inputs["A"])
l.new(cor_pescoco.outputs[0], cor_final.inputs["B"])
tinta = n.new("ShaderNodeBsdfPrincipled")
l.new(cor_final.outputs["Result"], tinta.inputs["Base Color"])
tinta.inputs["Metallic"].default_value = 0.25
tinta.inputs["Roughness"].default_value = 0.32
tinta.inputs["Coat Weight"].default_value = 0.8
tinta.inputs["Coat Roughness"].default_value = 0.06
alu = n.new("ShaderNodeBsdfPrincipled")
alu.inputs["Base Color"].default_value = (0.86, 0.85, 0.84, 1)
alu.inputs["Metallic"].default_value = 1.0
alu.inputs["Roughness"].default_value = 0.14
acima = n.new("ShaderNodeMath"); acima.operation = "GREATER_THAN"
acima.inputs[1].default_value = Z0
abaixo = n.new("ShaderNodeMath"); abaixo.operation = "LESS_THAN"
abaixo.inputs[1].default_value = PESCOCO
l.new(sep.outputs["Z"], acima.inputs[0])
l.new(sep.outputs["Z"], abaixo.inputs[0])
faixa = n.new("ShaderNodeMath"); faixa.operation = "MULTIPLY"
l.new(acima.outputs[0], faixa.inputs[0])
l.new(abaixo.outputs[0], faixa.inputs[1])
mix = n.new("ShaderNodeMixShader")
l.new(faixa.outputs[0], mix.inputs["Fac"])
l.new(alu.outputs[0], mix.inputs[1])
l.new(tinta.outputs[0], mix.inputs[2])
l.new(mix.outputs[0], saida.inputs["Surface"])
lata.data.materials.append(mat)

mat_alu = bpy.data.materials.new("aluminio")
n, l = nos(mat_alu)
b = n["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.85, 0.84, 0.82, 1)
b.inputs["Metallic"].default_value = 1.0
b.inputs["Roughness"].default_value = 0.12


# ---------- lacre, rebite e linha de abertura ----------
def estadio(x0, x1, larg, pts=24):
    rr_ = larg / 2
    out = []
    for i in range(pts + 1):
        a = -math.pi / 2 + math.pi * i / pts
        out.append((x1 - rr_ + rr_ * math.cos(a), rr_ * math.sin(a)))
    for i in range(pts + 1):
        a = math.pi / 2 + math.pi * i / pts
        out.append((x0 + rr_ + rr_ * math.cos(a), rr_ * math.sin(a)))
    return out


cu = bpy.data.curves.new("lacre", "CURVE")
cu.dimensions = "2D"
cu.fill_mode = "BOTH"
cu.extrude = 0.006
cu.bevel_depth = 0.004
cu.bevel_resolution = 3
for contorno in (estadio(-0.44, 0.34, 0.40), estadio(-0.37, -0.12, 0.25)):
    sp = cu.splines.new("POLY")
    sp.points.add(len(contorno) - 1)
    for p, (x, y) in zip(sp.points, contorno):
        p.co = (x, y, 0, 1)
    sp.use_cyclic_u = True
lacre = bpy.data.objects.new("lacre", cu)
lacre.location = (0, 0, TAMPA + 0.017)
lacre.rotation_euler = (0, math.radians(-3), 0)
sc.collection.objects.link(lacre)
cu.materials.append(mat_alu)

bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.06, depth=0.03, location=(0, 0, TAMPA + 0.007))
rebite = bpy.context.object
rebite.modifiers.new("bv", "BEVEL").width = 0.01
rebite.data.materials.append(mat_alu)
for p in rebite.data.polygons:
    p.use_smooth = True

cl = bpy.data.curves.new("abertura", "CURVE")
cl.dimensions = "3D"
cl.bevel_depth = 0.007
cl.bevel_resolution = 3
sp = cl.splines.new("POLY")
pts = []
for i in range(64):
    a = math.tau * i / 64
    pts.append((0.42 + 0.27 * math.cos(a), 0.24 * math.sin(a) * (0.75 + 0.25 * math.cos(a))))
sp.points.add(len(pts) - 1)
for p, (x, y) in zip(sp.points, pts):
    p.co = (x, y, TAMPA - 0.001, 1)
sp.use_cyclic_u = True
abertura = bpy.data.objects.new("abertura", cl)
sc.collection.objects.link(abertura)
cl.materials.append(mat_alu)


# ---------- gotas de condensacao ----------
def molde(sub_):
    tb = bmesh.new()
    bmesh.ops.create_icosphere(tb, subdivisions=sub_, radius=1.0)
    v = [x.co.copy() for x in tb.verts]
    f = [[x.index for x in fa.verts] for fa in tb.faces]
    tb.free()
    return v, f


ICO2, ICO1 = molde(2), molde(1)
verts, faces = [], []


def gota(pos, normal, raio, achata=0.6, m_=ICO2):
    tv, tf = m_
    normal = Vector(normal).normalized()
    rot = normal.to_track_quat("Z", "Y").to_matrix()
    m = rot @ Matrix.Diagonal((raio, raio * random.uniform(0.85, 1.15), raio * achata))
    base = len(verts)
    c = Vector(pos) + normal * raio * achata * 0.35
    verts.extend([tuple(c + m @ v) for v in tv])
    faces.extend([[base + i for i in f] for f in tf])


def raio_em(z):
    for (r0, z0), (r1, z1) in zip(perfil, perfil[1:]):
        if z0 <= z <= z1 and z1 > z0:
            t = (z - z0) / (z1 - z0)
            return r0 + (r1 - r0) * t, (r1 - r0) / (z1 - z0)
    return 1.0, 0.0


def gota_corpo(z, raio, m_=ICO2):
    a = random.uniform(0, math.tau)
    rz, incl = raio_em(z)
    gota((math.cos(a) * rz, math.sin(a) * rz, z), (math.cos(a), math.sin(a), -incl), raio, m_=m_)


for i in range(6500):
    z = random.uniform(0.25, 4.85)
    s = random.random() ** 2.6
    gota_corpo(z, 0.006 + s * (0.034 if z < 4.5 else 0.02))
for i in range(9000):
    gota_corpo(random.uniform(0.25, 4.88), random.uniform(0.003, 0.007), ICO1)
for i in range(140):
    a = random.uniform(0, math.tau)
    r = math.sqrt(random.random()) * 0.74
    x, y = r * math.cos(a), r * math.sin(a)
    if -0.5 < x < 0.4 and abs(y) < 0.24:
        continue
    gota((x, y, TAMPA), (0, 0, 1), 0.005 + random.random() ** 3 * 0.03, 0.5)

gm = bpy.data.meshes.new("gotas")
gm.from_pydata(verts, [], faces)
for p in gm.polygons:
    p.use_smooth = True
gotas = bpy.data.objects.new("gotas", gm)
sc.collection.objects.link(gotas)
mat_agua = bpy.data.materials.new("agua")
n, l = nos(mat_agua)
# sem refracao (no Eevee ela puxa o fundo escuro e a gota vira mancha cinza em rotulo claro):
# miolo transparente mostra o rotulo, borda reflete o ambiente com brilho nitido
b = n["Principled BSDF"]
b.inputs["Base Color"].default_value = (0, 0, 0, 1)  # agua nao tem cor propria, so reflexo
b.inputs["Roughness"].default_value = 0.03
b.inputs["IOR"].default_value = 1.33
camada = n.new("ShaderNodeLayerWeight")
camada.inputs["Blend"].default_value = 0.5
alfa = n.new("ShaderNodeMapRange")
alfa.inputs["To Min"].default_value = 0.0
alfa.inputs["To Max"].default_value = 0.6
l.new(camada.outputs["Facing"], alfa.inputs["Value"])
l.new(alfa.outputs["Result"], b.inputs["Alpha"])
mat_agua.surface_render_method = "DITHERED"
gm.materials.append(mat_agua)


# ---------- faiscas (bokeh rosa e lima) ----------
def mat_emissao(nome, cor, forca):
    m = bpy.data.materials.new(nome)
    n_, l_ = nos(m)
    n_.remove(n_["Principled BSDF"])
    em = n_.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*cor, 1)
    em.inputs["Strength"].default_value = forca
    l_.new(em.outputs[0], n_["Material Output"].inputs["Surface"])
    return m


for nome, cor, qtd in (("faisca_rosa", ROSA, 90), ("faisca_lima", LIMA, 45)):
    fv, ff = [], []
    tv, tf = ICO1
    for i in range(qtd):
        a = random.uniform(0, math.tau)
        r = random.uniform(1.6, 5.0)
        c = Vector((r * math.cos(a), r * math.sin(a), random.uniform(-0.5, 6.5)))
        raio = random.uniform(0.006, 0.02)
        base = len(fv)
        fv.extend([tuple(c + v * raio) for v in tv])
        ff.extend([[base + j for j in f] for f in tf])
    fm = bpy.data.meshes.new(nome)
    fm.from_pydata(fv, [], ff)
    ob = bpy.data.objects.new(nome, fm)
    sc.collection.objects.link(ob)
    fm.materials.append(mat_emissao(nome, cor, 18))

# fundo: brilho rosa radial atras da lata
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 9, 2.5), rotation=(math.radians(90), 0, 0))
fundo = bpy.context.object
fundo.scale = (22, 30, 1)
mf = bpy.data.materials.new("fundo")
n, l = nos(mf)
n.remove(n["Principled BSDF"])
tcf = n.new("ShaderNodeTexCoord")
mp = n.new("ShaderNodeMapping")
mp.inputs["Location"].default_value = (-1, -1, 0)
mp.inputs["Scale"].default_value = (2, 2, 1)
l.new(tcf.outputs["Generated"], mp.inputs["Vector"])
gr = n.new("ShaderNodeTexGradient")
gr.gradient_type = "SPHERICAL"
l.new(mp.outputs["Vector"], gr.inputs["Vector"])
pw = n.new("ShaderNodeMath"); pw.operation = "POWER"
pw.inputs[1].default_value = 2.2
l.new(gr.outputs["Fac"], pw.inputs[0])
em = n.new("ShaderNodeEmission")
em.inputs["Color"].default_value = (*ROSA, 1)
l.new(pw.outputs[0], em.inputs["Strength"])
mulf = n.new("ShaderNodeMath"); mulf.operation = "MULTIPLY"
mulf.inputs[1].default_value = 0.9
l.new(pw.outputs[0], mulf.inputs[0])
l.new(mulf.outputs[0], em.inputs["Strength"])
l.new(em.outputs[0], n["Material Output"].inputs["Surface"])
fundo.data.materials.append(mf)
fundo.visible_shadow = False


# ---------- luzes ----------
def luz_area(nome, loc, alvo_, cor, forca, sx, sy):
    ld = bpy.data.lights.new(nome, "AREA")
    ld.shape = "RECTANGLE"
    ld.size, ld.size_y = sx, sy
    ld.color = cor
    ld.energy = forca
    ob = bpy.data.objects.new(nome, ld)
    ob.location = loc
    ob.rotation_euler = (Vector(alvo_) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    sc.collection.objects.link(ob)
    return ob


luz_area("chave", (-4.0, -6.0, 7.0), (0, 0, 2.5), (1.0, 0.95, 0.92), 1100, 3.0, 3.0)
luz_area("tira_frente", (2.6, -5.0, 2.5), (0, 0, 2.5), (1.0, 1.0, 1.0), 700, 0.25, 7.0)
luz_area("contra_lima", (-4.5, 2.5, 2.6), (0, 0, 2.6), LIMA, 2200, 0.3, 8.0)
luz_area("contra_rosa", (4.5, 2.5, 2.6), (0, 0, 2.6), ROSA, 2600, 0.3, 8.0)
luz_area("topo", (-1.6, 1.8, 7.2), (0, 0, 5.0), (1.0, 0.95, 0.9), 12, 2.2, 2.2)
luz_area("borda_topo", (-2.4, 2.4, 5.4), (0, 0, 5.0), (1.0, 0.85, 0.75), 500, 3.0, 0.06)

w = bpy.data.worlds.new("mundo")
sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.004, 0.001, 0.003, 1)

# ---------- animacao ----------
grupo = bpy.data.objects.new("giro", None)
sc.collection.objects.link(grupo)
for ob in (lata, lacre, rebite, abertura, gotas):
    ob.parent = grupo
grupo.scale = (RAIO, RAIO, 1.0)

alvo = bpy.data.objects.new("alvo", None)
sc.collection.objects.link(alvo)
camd = bpy.data.cameras.new("cam")
camd.lens = 85
camd.sensor_fit = "VERTICAL"
camd.sensor_height = 36
camd.dof.use_dof = True
camd.dof.focus_object = alvo
camd.dof.aperture_blades = 7
cam = bpy.data.objects.new("cam", camd)
sc.collection.objects.link(cam)
sc.camera = cam
tr = cam.constraints.new("TRACK_TO")
tr.target = alvo
tr.track_axis = "TRACK_NEGATIVE_Z"
tr.up_axis = "UP_Y"

sc.frame_start, sc.frame_end = 1, 300
sc.render.fps = 30
# (frame, camera, alvo, giro da lata em graus, abertura f)
roteiro = [
    (1,   (0.0, -17.5, 3.0),  (0.0, 0.0, 2.55),  -450, 7.0),   # lata inteira girando
    (110, (0.0, -15.0, 2.9),  (0.0, 0.0, 2.55),  -90,  7.0),   # fecha o 360 de frente
    (150, (0.8, -4.4, 2.0),   (0.0, -1.0, 1.95), -82,  2.8),   # close no olho
    (195, (-0.7, -4.7, 3.55), (0.0, -1.0, 3.45), -96,  2.8),   # sobe pelo DANE-SE
    (240, (1.5, -2.3, 6.6),   (0.1, -0.1, 4.9),  -104, 1.8),   # tampa e lacre
    (300, (2.4, -13.5, 1.4),  (0.0, 0.0, 2.6),   -84,  5.6),   # heroi de baixo
]
for f, cpos, apos, giro, fst in roteiro:
    cam.location = cpos; cam.keyframe_insert("location", frame=f)
    alvo.location = apos; alvo.keyframe_insert("location", frame=f)
    grupo.rotation_euler = (0, 0, math.radians(giro)); grupo.keyframe_insert("rotation_euler", frame=f)
    camd.dof.aperture_fstop = fst; camd.dof.keyframe_insert("aperture_fstop", frame=f)
for dono in (cam, alvo, grupo, camd):
    for fc in curvas(dono.animation_data.action):
        for k in fc.keyframe_points:
            k.interpolation = "BEZIER"
            k.handle_left_type = k.handle_right_type = "AUTO_CLAMPED"

# ---------- render ----------
r = sc.render
try:
    r.engine = "BLENDER_EEVEE_NEXT"
except TypeError:
    r.engine = "BLENDER_EEVEE"
r.resolution_x, r.resolution_y = 1080, 1920
r.use_motion_blur = True
ee = sc.eevee
ee.taa_render_samples = 48
ee.use_raytracing = True
ee.use_shadows = True
ee.ray_tracing_options.resolution_scale = "1"
ee.ray_tracing_options.use_denoise = True
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "Medium High Contrast"
sc.view_settings.exposure = EXPOSICAO

try:   # brilho leve (a API do compositor mudou nas versoes novas: sem ele a previa sai do mesmo jeito)
    sc.use_nodes = True
    nt = sc.node_tree
    for k in list(nt.nodes):
        nt.nodes.remove(k)
    rl = nt.nodes.new("CompositorNodeRLayers")
    gl = nt.nodes.new("CompositorNodeGlare")
    gl.glare_type = "FOG_GLOW"
    gl.quality = "HIGH"
    gl.threshold = 0.9
    gl.size = 8
    gl.mix = -0.7
    co = nt.nodes.new("CompositorNodeComposite")
    nt.links.new(rl.outputs["Image"], gl.inputs["Image"])
    nt.links.new(gl.outputs["Image"], co.inputs["Image"])
except Exception as e:
    print("sem glow no compositor:", e)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "lata.blend"))

r.image_settings.file_format = "PNG"
if MODO == "anim":
    r.filepath = os.path.join(OUT, "frames", "f_")
    bpy.ops.render.render(animation=True)
elif MODO == "previa":
    for nome, f in QUADROS_PREVIA.items():
        sc.frame_set(f)
        r.filepath = os.path.join(OUT, f"previa_{nome}.png")
        bpy.ops.render.render(write_still=True)
else:
    for f in [int(x) for x in MODO.split(",")]:
        sc.frame_set(f)
        r.filepath = os.path.join(OUT, f"teste_{f:03d}.png")
        bpy.ops.render.render(write_still=True)
