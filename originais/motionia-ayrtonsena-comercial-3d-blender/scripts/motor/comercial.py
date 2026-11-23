# Cenas 3D do comercial (Blender 4.2+, Eevee). Cada "plano" e renderizado separado,
# com a numeracao global de quadros (batida 1 = quadro 0), em RENDER/<qualidade>/<plano>/f_####.png.
# Uso: blender -b -P comercial.py -- <plano> <rascunho|previa|final> [quadros de teste separados por virgula]
# (normalmente quem chama e o rodar.py). Tudo que muda de um projeto pro outro vem de projeto.json (config.py).
import sys, math, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy, bmesh
from mathutils import Vector, Matrix
import lata_lib as L
import config as C

TL = C.TL
N = C.N_SABORES

args = sys.argv[sys.argv.index("--") + 1:]
PLANO, QUALIDADE = args[0], args[1]
TESTE = [int(x) for x in args[2].split(",")] if len(args) > 2 else None

INCLINA = math.radians(-18)   # a lata fica sempre inclinada
FRENTE = math.radians(-90)    # giro que deixa o centro do rotulo de frente pra camera
CAM_FIXA = Vector((0.0, -14.6, 0.35))
CAM_FIXA_FIM = Vector((0.0, -12.0, 0.3))
Z_OLHO = (L.Z0 + C.FOCO_ROTULO * (L.Z1 - L.Z0)) - L.MEIO   # o ponto do rotulo que a camera encara


def q(b):
    return L.F(b)


# ---------- cena base: uma lata (planos 1 a 7) ----------
def cena_uma_lata():
    sc = L.limpar()
    imgs, cores, brilhos = L.carregar_rotulos()
    me = L.malha_lata()
    mat = L.material_lata(imgs, cores)
    alu, agua = L.material_aluminio(), L.material_agua()
    pose = bpy.data.objects.new("pose", None); sc.collection.objects.link(pose)
    pose.rotation_euler = (0, INCLINA, 0)
    giro = bpy.data.objects.new("giro", None); sc.collection.objects.link(giro)
    giro.parent = pose
    giro.rotation_euler = (0, 0, FRENTE)
    raiz, filhos = L.nova_lata(sc, "lata", me, mat, alu, agua)
    raiz.parent = giro
    raiz.color = (1, 1, 1, 0)
    for f in filhos:
        f.color = (1, 1, 1, 0)
    pontos = {}
    for nome, loc in (("tampa", (0.12, 0.0, L.TAMPA - L.MEIO)), ("olho", (1.0, 0.0, Z_OLHO)),
                      ("pescoco", (0.93, 0.0, 4.75 - L.MEIO)), ("borda", (0.89, 0.0, 5.0 - L.MEIO)),
                      ("fundo", (0.85, 0.0, 0.05 - L.MEIO)), ("corpo", (1.0, 0.0, -1.2))):
        e = bpy.data.objects.new("p_" + nome, None); sc.collection.objects.link(e)
        e.parent = raiz; e.location = loc
        pontos[nome] = e
    luzes = {
        "chave": L.luz_area(sc, "chave", (-6, -9, 8), (0, 0, 0), (1.0, 0.96, 0.92), 1400, 4, 4),
        "tira": L.luz_area(sc, "tira", (3.5, -7, 0.5), (0, 0, 0), (1, 1, 1), 900, 0.3, 9),
        "contra_a": L.luz_area(sc, "contra_a", (-5.5, 3.5, 0.5), (0, 0, 0), L.COR_SABOR[0], 2600, 0.35, 10),
        "contra_b": L.luz_area(sc, "contra_b", (5.5, 3.5, -0.5), (0, 0, -0.5), (1.0, 0.92, 0.85), 1800, 0.35, 6),
        "topo": L.luz_area(sc, "topo", (-2, 2, 9), (0, 0, 2), (1, 0.95, 0.9), 12, 2.2, 2.2),
        "borda": L.luz_area(sc, "borda_topo", (-3, 3, 4.2), (0, 0, 2.4), (1, 0.85, 0.75), 450, 3.5, 0.06),
    }
    w = bpy.data.worlds.new("mundo"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.006, 0.014, 1)
    cam, alvo = L.camera(sc, 50)
    L.render(sc, QUALIDADE, transparente=True)
    sc.view_settings.exposure = L.exposicao(brilhos[0])
    return dict(sc=sc, mat=mat, pose=pose, giro=giro, raiz=raiz, pontos=pontos, luzes=luzes,
                cam=cam, alvo=alvo, brilhos=brilhos, cores=cores)


def mundo(c, nome, local):
    """posicao no mundo de um ponto local da lata (com a pose atual)"""
    c["sc"].frame_set(c["sc"].frame_current)
    return c["raiz"].matrix_world @ Vector(local)


def pmundo(c, nome):
    bpy.context.view_layer.update()
    return c["pontos"][nome].matrix_world.translation.copy()


def chave(obj, prop, quadro, valor, interp="BEZIER", easing="AUTO"):
    setattr(obj, prop, valor)
    obj.keyframe_insert(prop, frame=quadro)
    for fc in L.curvas(obj.animation_data.action):
        if fc.data_path == prop:
            for k in fc.keyframe_points:
                if abs(k.co.x - quadro) < 1e-3:
                    k.interpolation = interp
                    k.easing = easing
                    k.handle_left_type = k.handle_right_type = "AUTO_CLAMPED"


def fstop(c, quadro, valor, interp="BEZIER"):
    cd = c["cam"].data
    cd.dof.aperture_fstop = valor
    cd.dof.keyframe_insert("aperture_fstop", frame=quadro)


def lente(c, quadro, valor):
    c["cam"].data.lens = valor
    c["cam"].data.keyframe_insert("lens", frame=quadro)


# ---------- planos ----------
Z_TAMPA = L.TAMPA - L.MEIO + 0.015    # topo do lacre com a lata em pe


def em_pe(c):
    """lata em pe (sem inclinacao) nos planos de abertura e detalhes"""
    c["pose"].rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()


def tremer(c, f0, dur=8, amp=0.06, semente=1):
    """tremida curta de camera no impacto (no delta do alvo, nao mexe nas chaves de posicao)"""
    rnd = random.Random(semente)
    alvo = c["alvo"]
    quadros = list(range(int(f0) - 1, int(f0) + dur + 2))
    vals = []
    for f in quadros:
        t = (f - f0) / dur
        k = 0 if t < 0 or t > 1 else (1 - t) ** 2
        vals.append((rnd.uniform(-1, 1) * amp * k, rnd.uniform(-1, 1) * amp * 0.4 * k, rnd.uniform(-1, 1) * amp * k))
    L.assar(alvo, "delta_location", quadros, vals)


def material_gota():
    """gota d'agua de anuncio: borda clara, corpo leve e brilho (no fundo escuro a refracao some)"""
    m = bpy.data.materials.new("gota"); m.use_nodes = True
    m.surface_render_method = "DITHERED"
    if hasattr(m, "use_raytrace_refraction"):
        m.use_raytrace_refraction = True
    if hasattr(m, "thickness_mode"):
        m.thickness_mode = "SPHERE"
    n, l = m.node_tree.nodes, m.node_tree.links
    b = n["Principled BSDF"]
    b.inputs["Base Color"].default_value = (1, 1, 1, 1)
    b.inputs["Roughness"].default_value = 0.0
    b.inputs["IOR"].default_value = 1.33
    b.inputs["Transmission Weight"].default_value = 1.0
    b.inputs["Specular IOR Level"].default_value = 1.0
    return m


def nova_gota(sc, raio=0.075):
    """gota em forma de lagrima (ponta pra cima, como quando cai)"""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=32, radius=raio)
    for v in bm.verts:
        z = min(1.0, v.co.z / raio)
        if z > 0:
            k = (1 - z) ** 0.9 * 0.85 + 0.15
            v.co.x *= k; v.co.y *= k
            v.co.z *= 1.0 + 0.9 * z
    me = bpy.data.meshes.new("gota"); bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(material_gota())
    ob = bpy.data.objects.new("gota", me); sc.collection.objects.link(ob)
    return ob


def plano_queda(c):
    """b1-b(detalhes): camera la em cima, centralizada, cai junto com uma gota; freia em camera lenta num close da tampa
    com a gota quase encostando; na batida 5 desce rapido pela frente e abre no olho (lata em pe)"""
    sc, cam, alvo = c["sc"], c["cam"], c["alvo"]
    em_pe(c)
    c["luzes"]["borda"].data.energy = 0
    c["luzes"]["topo"].data.energy = 0
    # luz grande e macia em cima, deslocada: vira um brilho degrade no lacre (sem estourar)
    L.luz_area(sc, "tampa_macia", (-1.5, 2.5, Z_TAMPA + 7), (0, 0, Z_TAMPA), (1, 0.95, 0.92), 130, 7, 4)
    L.luz_area(sc, "tampa_rosa", (2.5, -2.0, Z_TAMPA + 4), (0, 0, Z_TAMPA), L.COR_SABOR[0], 120, 3, 3)
    gota = nova_gota(sc)
    q3, q5, q9 = q(TL['queda_lenta']), q(TL['olho']), q(TL['revela'])
    q_olho = q(5) + 10                      # chega no olho em 10 quadros
    olho_c = Vector((0, 0, Z_OLHO))
    olho_f = Vector((0, -1.0, Z_OLHO))
    r_cima = Z_TAMPA + 2.1 - Z_OLHO
    quadros = list(range(0, int(q9) + 1))
    cams, alvos, gotas, escs, lentes, fs = [], [], [], [], [], []
    for f in quadros:
        if f < q3:                           # queda rapida que freia (ease-out cubica)
            t = f / q3
            h = 2.6 + 15.0 * (1 - t) ** 3
            g = h - (1.0 + 1.25 * t ** 1.5)  # a gota vai abrindo distancia da camera e chegando na tampa
        elif f < q5:                         # camera lenta: a gota quase encosta
            t = (f - q3) / (q5 - q3)
            h = 2.6 - 0.5 * t
            g = 0.35 - 0.29 * (1 - (1 - t) ** 2)
        else:
            h, g = 2.1, 0.06
        gp = Vector((0, 0, Z_TAMPA + g))
        if f < q5:
            cp, ap = Vector((0, -0.08, Z_TAMPA + h)), gp
            ln, fstp = 50, 2.8
        else:                                # mergulho em arco ate a frente do olho
            t = min(1.0, (f - q5) / (q_olho - q5))
            u = 1 - (1 - t) ** 4
            phi = math.radians(89) * (1 - u)
            raio = r_cima + (6.6 - r_cima) * u
            cp = olho_c + Vector((0, -math.cos(phi), math.sin(phi))) * raio
            if f > q_olho:                   # depois segue empurrando devagar
                s = (f - q_olho) / (q9 - q_olho)
                cp = olho_c + Vector((0, -1, 0)) * (6.6 - 0.9 * s) + Vector((0, 0, 0.12 * s))
            ap = gp.lerp(olho_f, u)
            ln, fstp = 50 + 5 * u, 2.8 + 1.2 * u
        cams.append(tuple(cp)); alvos.append(tuple(ap)); gotas.append(tuple(gp))
        balanco = 0.06 * math.sin(f * 0.9)  # a gota respira enquanto cai
        escs.append((1 - balanco * 0.5, 1 - balanco * 0.5, 1 + balanco) if f <= q5 else (0, 0, 0))
        lentes.append(ln); fs.append(fstp)
    L.assar(cam, "location", quadros, cams)
    L.assar(alvo, "location", quadros, alvos)
    L.assar(gota, "location", quadros, gotas)
    L.assar(gota, "scale", quadros, escs)
    L.assar(cam.data, "lens", quadros, lentes)
    L.assar(cam.data, "dof.aperture_fstop", quadros, fs)
    tremer(c, q_olho, 7, 0.05, 3)
    return 0, int(math.floor(q9))


def _em(c):
    raiz = c["raiz"]
    bpy.context.view_layer.update()   # sem isso matrix_world ainda e a identidade
    def em(ang, r, z):
        a = math.radians(ang)
        return raiz.matrix_world @ Vector((r * math.cos(a), r * math.sin(a), z))
    return em


def take(c, f0, f1, cam0, cam1, alvo0, alvo1, lente_mm=70, f_stop=2.8):
    """um take de detalhe entre f0 e f1 (corte seco nas pontas), movimento com curva suave"""
    cam, alvo = c["cam"], c["alvo"]
    chave(cam, "location", f0, cam0, "SINE", "EASE_IN_OUT")
    chave(cam, "location", f1, cam1, "CONSTANT")
    chave(alvo, "location", f0, alvo0, "SINE", "EASE_IN_OUT")
    chave(alvo, "location", f1, alvo1, "CONSTANT")
    c["cam"].data.lens = lente_mm; c["cam"].data.keyframe_insert("lens", frame=f0)
    c["cam"].data.dof.aperture_fstop = f_stop; c["cam"].data.dof.keyframe_insert("aperture_fstop", frame=f0)


def plano_detalhes(c):
    """quatro closes de partes diferentes da lata, em corte seco. Cada um e renderizado com 1 batida
    (a partir da batida da revelacao) e o compor.py usa so meia batida de cada."""
    em_pe(c)
    em = _em(c)
    c["luzes"]["borda"].data.energy = 0
    c["luzes"]["topo"].data.energy = 0
    L.luz_area(c["sc"], "tampa_macia", (-1.5, 2.5, Z_TAMPA + 7), (0, 0, Z_TAMPA), (1, 0.95, 0.92), 130, 7, 4)
    # no rasante o lacre espelha o que esta atras: uma faixa de luz baixa atras da lata
    L.luz_area(c["sc"], "tampa_atras", (0, 4.5, Z_TAMPA + 1.3), (0, 0, Z_TAMPA), (1, 0.93, 0.9), 40, 7, 1.6)
    zt = L.TAMPA - L.MEIO
    rv = TL['revela']
    cortes = [q(rv + k) for k in range(5)]
    takes = [  # lacre e anel da tampa, rasante
        (em(-16, 1.5, zt + 0.6), em(14, 1.5, zt + 0.5), em(6, 0.1, zt), em(-4, 0.1, zt), 55, 3.5),
        # logo / meio do rotulo com gotas, subindo
        (em(-26, 2.3, 1.1), em(-12, 2.3, 1.45), em(-16, 1.0, 1.2), em(-6, 1.0, 1.45), 65, 3.2),
        # raio e etiqueta do sabor, descendo na diagonal
        (em(-28, 2.4, -0.75), em(-21, 2.4, -1.1), em(-14, 1.0, -0.95), em(-9, 1.0, -1.25), 65, 3.2),
        # pescoco com os escorridos, contornando
        (em(-30, 2.2, 1.85), em(-12, 2.2, 1.95), em(-18, 0.95, 2.05), em(-4, 0.95, 2.1), 60, 3.2),
    ]
    for i, (c0, c1, a0, a1, ln, fs) in enumerate(takes):
        take(c, math.ceil(cortes[i]), math.ceil(cortes[i + 1]) - 1, c0, c1, a0, a1, ln, fs)
    for fc in L.curvas(c["cam"].data.animation_data.action):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT"
    return int(math.ceil(q(rv))), int(math.ceil(q(rv + 4))) - 1


def plano_revela(c):
    """b9-b10: a lata sobe de baixo girando em meia batida e ja emenda no primeiro giro com explosao"""
    sc, cam, alvo = c["sc"], c["cam"], c["alvo"]
    pose, giro = c["pose"], c["giro"]
    f0, f_chega, f1 = math.ceil(q(B_REVELA)), G0, G0 - 1
    pose.location = (0, 0, -7.5); pose.rotation_euler = (0, math.radians(25), 0)
    pose.keyframe_insert("location", frame=f0); pose.keyframe_insert("rotation_euler", frame=f0)
    pose.location = (0, 0, 0); pose.rotation_euler = (0, INCLINA, 0)
    pose.keyframe_insert("location", frame=f_chega); pose.keyframe_insert("rotation_euler", frame=f_chega)
    for fc in L.curvas(pose.animation_data.action):
        for k in fc.keyframe_points:
            if abs(k.co.x - f0) < 0.5:
                k.interpolation = "BACK"; k.easing = "EASE_OUT"; k.back = 1.3
    giro.rotation_euler = (0, 0, FRENTE + math.tau)
    giro.keyframe_insert("rotation_euler", frame=f0)
    giro.rotation_euler = (0, 0, FRENTE)
    giro.keyframe_insert("rotation_euler", frame=G0)
    for fc in L.curvas(giro.animation_data.action):
        for k in fc.keyframe_points:
            if abs(k.co.x - f0) < 0.5:
                k.interpolation = "QUAD"; k.easing = "EASE_OUT"
    chave(cam, "location", f0, CAM_FIXA + Vector((0, 1.2, 0)), "SINE", "EASE_OUT")
    chave(cam, "location", G0, CAM_FIXA)
    chave(alvo, "location", f0, Vector((0, 0, 0)))
    lente(c, f0, 50)
    fstop(c, f0, 9.0)
    tremer(c, f_chega, 8, 0.07, 5)
    return int(f0), int(f1)


# trocas de sabor: (batida, indice do rotulo, duracao do giro em quadros). Cada troca explode as frutas;
# a primeira e lenta e vao encurtando. Sem a sequencia de trocas rapidas (ele achou repetitivo).
_DUR_GIRO = [15, 12, 11, 10]
TROCAS = [(b, i, _DUR_GIRO[min(k, 3)]) for k, (b, i) in enumerate(zip(TL["trocas"], C.ordem_trocas()))]
EXPLOSOES = [(b, i, 1 if C.SABORES[i].get("respingo") else int(C.SABORES[i].get("qtd", 12)))
             for b, i, _ in TROCAS]
B_REVELA = TL["revela"]                         # a lata sobe aqui (depois dos closes)
B_CRUZ = TL["cruz"]                             # a cruz entra aqui (fim dos giros)
G0 = int(math.ceil(q(TROCAS[0][0]))) - 8        # primeiro quadro dos giros (a lata ja parada de frente)
CAM_GIROS_FIM = Vector((0.0, -17.2, 0.45))


def plano_giros(c):
    """b15-b26: lata parada no mesmo lugar, camera fixa recuando devagar; cada giro troca rotulo, luz e explode as frutas"""
    sc, giro, mat = c["sc"], c["giro"], c["mat"]
    q0, q1 = G0, int(math.floor(q(B_CRUZ))) + 2
    quadros = list(range(q0, q1 + 1))
    angs = []
    for f in quadros:
        a = FRENTE
        for b, _, d in TROCAS:
            t = (f - (q(b) - d / 2)) / d
            if t >= 1:
                a += math.tau
            elif t > 0:
                s = t * t * t * (t * (t * 6 - 15) + 10)
                a += math.tau * s
        anteriores = [q(b) for b, _, _ in TROCAS if q(b) <= f]
        ini = anteriores[-1] if anteriores else q(TROCAS[0][0])
        prox = [q(b) for b, _, _ in TROCAS if q(b) > f]
        fim = prox[0] if prox else q(B_CRUZ)
        a += math.radians(8) * math.sin(math.pi * (f - ini) / max(1, fim - ini)) * (1 if fim - ini > 30 else 0)
        angs.append((0, 0, a))
    L.assar(giro, "rotation_euler", quadros, angs)
    ind = mat.node_tree.nodes["indice"].outputs[0]
    ind.default_value = 0
    ind.keyframe_insert("default_value", frame=q0)
    luz = c["luzes"]["contra_a"].data
    for b, i, _ in TROCAS:
        ind.default_value = i
        ind.keyframe_insert("default_value", frame=q(b))
        luz.color = L.COR_SABOR[i]
        luz.keyframe_insert("color", frame=q(b))
        sc.view_settings.exposure = L.exposicao(c["brilhos"][i])
        sc.view_settings.keyframe_insert("exposure", frame=q(b))
    for dono in (mat.node_tree, luz, sc):
        ad = dono.animation_data
        if ad and ad.action:
            for fc in L.curvas(ad.action):
                for k in fc.keyframe_points:
                    k.interpolation = "CONSTANT"
    # camera: no mesmo lugar, so recuando devagar o tempo todo (sem zoom nos detalhes)
    cam, alvo = c["cam"], c["alvo"]
    chave(cam, "location", G0, CAM_FIXA, "LINEAR")
    chave(cam, "location", q(B_CRUZ) + 2, CAM_GIROS_FIM, "LINEAR")
    chave(alvo, "location", G0, Vector((0, 0, 0)))
    lente(c, G0, 50)
    fstop(c, G0, 9.0)
    for n_, (b, _, _) in enumerate(TROCAS[:4]):
        tremer(c, q(b), 6, 0.05, 10 + n_) if n_ == 0 else None
    L.painel_estudio(sc)   # a agua do respingo precisa de luz pra refletir nas bordas
    explosoes(c)
    return G0, int(math.floor(q(B_CRUZ)))


# pecas de cada sabor: (malha, peso no sorteio, tamanho), de projeto.json
PECAS_SABOR = {i: [tuple(p) for p in s.get("pecas", [])] for i, s in enumerate(C.SABORES)}


def explosoes(c):
    """Frutas reais saem de tras da lata, rapidas no comeco e em camera lenta depois, com o corte virado pra camera;
    no proximo giro sao expulsas. Agua sem gas: um respingo grande que abre."""
    sc = c["sc"]
    malhas = L.carregar_frutas()
    rnd = random.Random(31)
    grupo = bpy.data.objects.new("pecas", None); sc.collection.objects.link(grupo)
    fim_cena = q(B_CRUZ) + 2
    for n_exp, (b, sabor, qtd) in enumerate(EXPLOSOES):
        t0 = q(b)
        t_exp = q(EXPLOSOES[n_exp + 1][0]) if n_exp + 1 < len(EXPLOSOES) else q(B_CRUZ)
        if C.SABORES[sabor].get("respingo"):
            resp = malhas.get("pc_respingo") or malhas.get("fr_respingo")
            if not resp:
                continue
            ob = bpy.data.objects.new("respingo", resp); ob.parent = grupo
            sc.collection.objects.link(ob)
            quadros, locs, rots, escs = [], [], [], []
            for f in range(int(t0) - 2, int(min(fim_cena, t_exp + 10)) + 1):
                t = (f - t0) / L.FPS
                abre = 0 if t < 0 else 1 - math.exp(-t / 0.12)
                some = 1.0 if f < t_exp else max(0.0, 1 - (f - t_exp) / 6)
                quadros.append(f); locs.append((0, 0.7, 0.1))
                rots.append((math.radians(80), 0, math.radians(20) + 0.25 * t))
                escs.append(((0.2 + 7.3 * abre) * some,) * 3)
            L.assar(ob, "location", quadros, locs)
            L.assar(ob, "rotation_euler", quadros, rots)
            L.assar(ob, "scale", quadros, escs)
            continue
        opcoes = [o for o in PECAS_SABOR.get(sabor, []) if o[0] in malhas]
        if not opcoes:
            continue
        tot = sum(o[1] for o in opcoes)
        opcoes = [(nm, pe / tot, tm) for nm, pe, tm in opcoes]
        for k in range(qtd):
            r_ = rnd.random(); acum = 0
            for nome, peso, tam in opcoes:
                acum += peso
                if r_ <= acum:
                    break
            ob = bpy.data.objects.new(f"peca_{sabor}_{k}", malhas[nome])
            ob.parent = grupo
            sc.collection.objects.link(ob)
            ang = (k + rnd.uniform(-0.3, 0.3)) / qtd * math.tau
            d = Vector((math.cos(ang), 0, math.sin(ang)))
            prof = rnd.uniform(-1.2, 3.0)
            alvo = Vector((d.x * rnd.uniform(2.4, 4.6), prof, d.z * rnd.uniform(1.6, 2.6)))
            if prof < 0 and abs(alvo.x) < 1.9:
                alvo.x = math.copysign(1.9 + rnd.random() * 0.6, alvo.x or 1)
            inicio = Vector((rnd.uniform(-0.3, 0.3), rnd.uniform(0.4, 1.0), rnd.uniform(-0.6, 0.6)))
            deriva = (alvo - inicio).normalized() * rnd.uniform(0.15, 0.35)
            rot0 = Vector(L.virar_corte(nome, rnd))
            w = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))).normalized() * rnd.uniform(2.0, 4.0)
            s = tam * rnd.uniform(0.8, 1.15)
            quadros, locs, rots, escs = [], [], [], []
            for f in range(int(t0) - 2, int(min(fim_cena, t_exp + 16)) + 1):
                t = (f - t0) / L.FPS
                if t < 0:
                    p, e, r = inicio, 0.0, rot0 - w * 0.5
                elif f < t_exp:
                    sai = 1 - math.exp(-t / 0.11)
                    p = inicio.lerp(alvo, sai) + deriva * t + Vector((0, 0, 0.08 * math.sin(t * 2.3 + k)))
                    e = min(1.0, (f - t0 + 1) / 3)
                    r = rot0 - w * 0.5 * (1 - sai) + w * 0.05 * t
                else:
                    t1 = (t_exp - t0) / L.FPS
                    sai = 1 - math.exp(-t1 / 0.11)
                    p1 = inicio.lerp(alvo, sai) + deriva * t1
                    te = (f - t_exp) / L.FPS
                    dirx = (p1 - Vector((0, 0, 0))).normalized()
                    p = p1 + dirx * (8 * te + 45 * te * te)
                    e = 1.0 if te < 0.5 else 0.0
                    r = rot0 + w * (0.05 * t1 + 0.6 * te)
                quadros.append(f); locs.append(tuple(p)); rots.append(tuple(r)); escs.append((s * e,) * 3)
            L.assar(ob, "location", quadros, locs)
            L.assar(ob, "rotation_euler", quadros, rots)
            L.assar(ob, "scale", quadros, escs)


# ---------- cata-vento -> rastro -> camera entra no furo -> corredor -> fileira (b27-b50, camera continua) ----------
N_COPIAS = 6
ATRASO = 1.5            # quadros de atraso entre uma copia e a proxima (~12 graus: copias nitidas, em leque)
RC = L.MEIO + 0.55 + (L.RAIO - 1)   # do centro da cruz ao meio da lata: as latas ficam separadas, sem encostar
DESLOCA = 0.8           # deslocamento de lado de cada lata (cata-vento, igual a referencia)
ABRE_FURO = 3.0         # no mergulho o cata-vento abre e o furo do meio cresce pra camera passar
B_RASTRO, B_MERGULHO, B_FURO, B_FIM_CORREDOR, B_FILEIRA = (TL[k] for k in ("rastro", "mergulho", "furo", "fim_corredor", "fileira"))   # furo = pausa da musica
N_ANEIS, ESPACO_ANEL, ESC_ANEL, Y_ANEL0 = 6, 5.0, 2.2, 3.5
ACENDE = list(TL["acende"])        # batida em que cada lata da fileira acende
B_LOGO = TL["logo"]
B_PARA = ACENDE[-1] + 1            # a camera para na ultima lata e segura ate o logo
SPOT_W = 2600
DIST_FIL = 13.4                     # distancia da camera a fileira (enquadramento do print)
B_LADO = B_FURO + 1.5               # a camera ja comeca a deslizar de lado ainda no corredor
PAN, B_PAN = 0.35, B_FURO + 1.0     # e vira pra direita enquanto freia: a fileira so anda pra um lado, sem parar e voltar
FUNDO_CRUZ = (C.hex_rgb(C.CFG["fundo_cruz"]) if C.CFG.get("fundo_cruz")
              else tuple(0.9 * v for v in C.COR_SABOR[0]))   # fundo fixo da cruz (sem trocar de cor a cada batida)
QB = q(2) - q(1)


def _ease_out_back(t, s=1.4):
    t -= 1
    return 1 + t * t * ((s + 1) * t + s)


def _suave(t):
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def _orient_cruz(phi):
    radial = Vector((math.cos(phi), 0, math.sin(phi)))
    z = -radial
    x = Vector((0, -1, 0))
    y = z.cross(x)
    return Matrix((x, y, z)).transposed()


ORIENT_POSE = (Matrix.Rotation(INCLINA, 3, "Y") @ Matrix.Rotation(FRENTE, 3, "Z"))
ORIENT_EM_PE = Matrix.Rotation(FRENTE, 3, "Z")


def tabela_giro(q0, q1):
    """angulo da cruz por quadro: ja sai girando no b27 e acelera liso ate ~8 graus/quadro; no mergulho
    acelera mais um pouco. Nunca para nem da tranco."""
    ang, a = {}, 0.0
    for f in range(q0 - 40, q1 + 1):
        if f < q0:
            w = 0.0
        else:
            w = 3.0 + 5.0 * _suave((f - q0) / (q(B_CRUZ + 3) - q0)) + 3.0 * _suave((f - q(B_MERGULHO)) / (q(B_FURO) - q(B_MERGULHO)))
        a += math.radians(w)
        ang[f] = a
    return ang


def balanco_3d(f):
    """a cruz tomba devagar em 3D enquanto acelera e volta a ficar de frente antes do mergulho"""
    t = (f - q(B_CRUZ)) / (q(B_CRUZ + 5) - q(B_CRUZ))
    if t <= 0 or t >= 1:
        return Matrix.Identity(3)
    amp = math.sin(math.pi * t)
    return (Matrix.Rotation(math.radians(28) * amp, 3, "Z") @ Matrix.Rotation(math.radians(-12) * amp, 3, "X"))


def estado(i, f, ang):
    """posicao e orientacao (3x3) da lata i do cata-vento no quadro f (pode ser fracionario)"""
    fi = int(math.floor(f))
    th = ang.get(fi, 0.0) + (ang.get(fi + 1, 0.0) - ang.get(fi, 0.0)) * (f - fi)
    phi = math.pi / 2 - i * math.pi / 2
    rc = RC + ABRE_FURO * _suave((f - q(B_MERGULHO + 0.5)) / (q(B_FURO) - q(B_MERGULHO + 0.5)))
    def slot_p(t_):
        radial = Vector((math.cos(phi + t_), 0, math.sin(phi + t_)))
        lado = Vector((-math.sin(phi + t_), 0, math.cos(phi + t_)))
        return balanco_3d(f) @ (radial * rc + lado * DESLOCA)
    slot_r = lambda t_: balanco_3d(f) @ _orient_cruz(phi + t_)
    if f < q(B_CRUZ):
        return Vector((0, 0, 0)), ORIENT_POSE
    if f < q(B_CRUZ) + 10:
        t = _ease_out_back((f - q(B_CRUZ)) / 10)
        p = Vector((0, 0, 0)).lerp(slot_p(th), t)
        r = ORIENT_POSE.to_quaternion().slerp(slot_r(th).to_quaternion(), min(1.0, max(0.0, t))).to_matrix()
        return p, r
    return slot_p(th), slot_r(th)


def trajeto_camera(q0, q1):
    """camera por quadro (local, alvo, lente). Abre na cruz, empurra devagar, mergulha acelerando ate passar
    pelo furo do meio no b37, atravessa o corredor e freia na fileira ja deslizando de lado.
    Tudo pela velocidade (que nunca pula), entao nao tem travada nem volta."""
    v_lenta, v_max, v_lado = 0.8 / QB, 10.0 / QB, 3.4 / QB
    f_abre = q0 + 8
    ys, xs, y, x = {}, {}, 0.0, 0.0
    for f in range(f_abre, q1 + 1):
        if f < q(B_MERGULHO):
            v = v_lenta
        elif f < q(B_FURO):
            v = v_lenta + (v_max - v_lenta) * _suave((f - q(B_MERGULHO)) / (q(B_FURO) - q(B_MERGULHO)))
        elif f < q(B_FIM_CORREDOR):
            v = v_max
        else:
            v = v_max * (1 - _suave((f - q(B_FIM_CORREDOR)) / (q(B_FILEIRA) - q(B_FIM_CORREDOR))))
        if f < q(B_LADO):
            vx = 0.0
        elif f < q(ACENDE[-2]):
            vx = v_lado * _suave((f - q(B_LADO)) / (q(B_FILEIRA) - q(B_LADO)))
        else:   # freia em 2 batidas e para com a ultima lata no meio (anda exatamente um espaco entre latas)
            vx = v_lado * (1 - _suave((f - q(ACENDE[-2])) / (q(B_PARA) - q(ACENDE[-2]))))
        ys[f], xs[f] = y, x
        y += v; x += vx
    # interpola pra achar o y exato no furo e desloca tudo pra la (furo em y = 0)
    ff = q(B_FURO); fl = int(math.floor(ff))
    y_furo = ys[fl] + (ys[fl + 1] - ys[fl]) * (ff - fl)
    for f in ys:
        ys[f] -= y_furo
    res = {}
    for f in range(q0 - 2, q1 + 1):
        if f < f_abre:                       # abertura: recua e abre a lente quando a cruz explode
            t = _suave((f - (q0 - 2)) / (f_abre - (q0 - 2)))
            u = 1 - (1 - t) ** 2
            loc = Vector((0, -12.0 + (ys[f_abre] + 12.0) * u, 0.3 * (1 - u)))
            ln = 50 + (26 - 50) * u
            s = 0.0
        else:
            s = _suave((f - q(B_FIM_CORREDOR)) / (q(B_FILEIRA) - q(B_FIM_CORREDOR)))
            loc = Vector((xs[f], ys[f], -0.15 * s))
            ln = 26 + (40 - 26) * s
        pan = PAN * _suave((f - q(B_PAN)) / (q(B_FILEIRA + 0.5) - q(B_PAN)))
        alvo = loc + Vector((DIST_FIL * math.tan(pan), DIST_FIL, -0.2 * s))
        res[f] = (loc, alvo, ln)
    return res, xs, ys


def plano_helice(_c=None):
    sc = L.limpar()
    imgs, cores, brilhos = L.carregar_rotulos()
    me = L.malha_lata()
    mat = L.material_lata(imgs, cores)
    alu, agua = L.material_aluminio(), L.material_agua()
    mats = []
    for i in range(N):
        m = mat.copy()
        m.node_tree.nodes["indice"].outputs[0].default_value = i
        mats.append(m)
    q0, q1 = int(math.ceil(q(B_CRUZ))), int(math.floor(q(B_LOGO)))
    quadros = list(range(q0 - 2, q1 + 1))
    ang = tabela_giro(q0, q1)
    traj, xs, ys = trajeto_camera(q0, q1)
    f_some_cruz = int(q(B_FURO)) + 2           # a camera ja passou pelo furo: a cruz fica pra tras
    y_fileira = ys[int(round(q(B_FILEIRA)))] + DIST_FIL
    # cada lata no meio do quadro na batida dela; a ultima fica no meio onde a camera para
    x_fileira = [xs[int(round(q(b)))] + DIST_FIL * math.tan(PAN) for b in ACENDE[:-1] + [B_PARA]]
    x_meio = sum(x_fileira) / len(x_fileira)

    def com_rotulo(filhos, i):
        corpo = filhos[0]
        corpo.material_slots[0].link = "OBJECT"
        corpo.material_slots[0].material = mats[i % N]

    def assar_matriz(ob, lista, escalas=None):
        locs = [tuple(p) for p, r in lista]
        rots, ant = [], None
        for p, r in lista:
            e = r.to_euler("XYZ", ant) if ant else r.to_euler("XYZ")
            rots.append(tuple(e)); ant = e
        L.assar(ob, "location", quadros, locs)
        L.assar(ob, "rotation_euler", quadros, rots)
        if escalas:
            L.assar(ob, "scale", quadros, escalas)

    def esconder_depois(obs, quadro):
        for ob in obs:
            ob.hide_render = False
            ob.keyframe_insert("hide_render", frame=q0 - 2)
            ob.hide_render = True
            ob.keyframe_insert("hide_render", frame=quadro)

    # 4 latas do cata-vento
    for i in range(4):
        raiz, filhos = L.nova_lata(sc, f"helice_{i}", me, mat, alu, agua, gotas=False)
        com_rotulo(filhos, i)
        for ob in [raiz] + filhos:
            ob.color = (1, 1, 1, 0)
        assar_matriz(raiz, [estado(i, f, ang) for f in quadros])
        esconder_depois(filhos, f_some_cruz)
    # rastro: copias atrasadas (so o corpo), nascem uma a uma enquanto o giro acelera
    for k in range(1, N_COPIAS + 1):
        g = max(0.6, 1 - 0.035 * k)
        for i in range(4):
            raiz, filhos = L.nova_lata(sc, f"copia_{k}_{i}", me, mat, detalhes=False, gotas=False, sub=1)
            com_rotulo(filhos, i)
            filhos[0].color = (g, g, g, 0)
            lista, escs = [], []
            for f in quadros:
                p, r = estado(i, f - k * ATRASO, ang)
                lista.append((p + Vector((0, 0.06 * k, 0)), r))
                e_ = _suave((f - q(B_RASTRO) - k * 3) / 5)
                escs.append((e_ * L.RAIO, e_ * L.RAIO, e_))
            assar_matriz(raiz, lista, escs)
            esconder_depois(filhos, f_some_cruz)
    # corredor: latas neon gigantes em fila atras da cruz; aparecem quando o fundo ja escureceu
    aneis = []
    for k in range(N_ANEIS):
        raiz, filhos = L.nova_lata(sc, f"anel_{k}", me, mat, detalhes=False, gotas=False, sub=1)
        com_rotulo(filhos, k % N)
        raiz.location = (0, Y_ANEL0 + k * ESPACO_ANEL, 0)
        raiz.rotation_euler = ORIENT_EM_PE.to_euler()
        raiz.scale = (ESC_ANEL * L.RAIO, ESC_ANEL * L.RAIO, ESC_ANEL)
        filhos[0].color = (*L.COR_SABOR[k % N], 1.0)
        for ob in filhos:
            ob.hide_render = True
            ob.keyframe_insert("hide_render", frame=q0 - 2)
            ob.hide_render = False
            ob.keyframe_insert("hide_render", frame=int(q(B_FURO - 0.8)))
        aneis.append((filhos, Y_ANEL0 + k * ESPACO_ANEL))
    # fileira final, comecando em silhueta; cada lata acende na sua batida
    chao_objs = []
    for i, x in enumerate(x_fileira):
        raiz, filhos = L.nova_lata(sc, f"fileira_{i}", me, mat, alu, agua, gotas_qtd=0.35)
        com_rotulo(filhos, i)
        raiz.location = (x, y_fileira, 0)
        raiz.rotation_euler = ORIENT_EM_PE.to_euler()
        b = ACENDE[i]
        for ob in [raiz] + filhos:   # silhueta preta ate a batida dela, depois acende junto com o spot (sem piscar)
            ob.color = (0.02, 0.02, 0.02, 0)
            ob.keyframe_insert("color", frame=q(b) - 2)
            ob.color = (1, 1, 1, 0)
            ob.keyframe_insert("color", frame=q(b) + 4)
        chao_objs += [raiz] + filhos
        sd = bpy.data.lights.new(f"spot_{i}", "SPOT")
        sd.spot_size = math.radians(38); sd.spot_blend = 0.45; sd.color = (1, 0.97, 0.93)
        luz = bpy.data.objects.new(f"spot_{i}", sd); sc.collection.objects.link(luz)
        luz.location = (x - 0.6, y_fileira - 4.5, 6.0)
        luz.rotation_euler = (Vector((x, y_fileira, -0.3)) - luz.location).to_track_quat("-Z", "Y").to_euler()
        for df, fator in ((-2, 0.0), (4, 1.0)):   # liga liso, sem piscada
            sd.energy = SPOT_W * fator
            sd.keyframe_insert("energy", frame=q(b) + df)
    # chao espelhado escuro e brilho rosa atras da fileira
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x_meio, y_fileira + 43, -L.MEIO))
    chao = bpy.context.object
    chao.scale = (300, 130, 1)
    mch = bpy.data.materials.new("chao")
    n, l = L.nos(mch)
    b_ = n["Principled BSDF"]
    b_.inputs["Base Color"].default_value = (0.002, 0.0015, 0.002, 1)
    b_.inputs["Roughness"].default_value = 0.06
    b_.inputs["Specular IOR Level"].default_value = 0.6
    # some aos poucos na borda da frente, pra nao virar uma linha vista do corredor
    tc = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ")
    l.new(tc.outputs["Generated"], sep.inputs[0])
    rampa = n.new("ShaderNodeMapRange"); rampa.inputs["From Min"].default_value = 0.0
    rampa.inputs["From Max"].default_value = 0.06; rampa.interpolation_type = "SMOOTHSTEP"
    l.new(sep.outputs["Y"], rampa.inputs["Value"])
    transp = n.new("ShaderNodeBsdfTransparent"); mixc = n.new("ShaderNodeMixShader")
    l.new(rampa.outputs["Result"], mixc.inputs["Fac"])
    l.new(transp.outputs[0], mixc.inputs[1]); l.new(b_.outputs[0], mixc.inputs[2])
    l.new(mixc.outputs[0], n["Material Output"].inputs["Surface"])
    chao.data.materials.append(mch)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x_meio, y_fileira + 16, 6), rotation=(math.radians(90), 0, 0))
    painel = bpy.context.object
    painel.scale = (200, 60, 1)
    mp = bpy.data.materials.new("brilho_rosa")
    n, l = L.nos(mp)
    n.remove(n["Principled BSDF"])
    tcf = n.new("ShaderNodeTexCoord"); mpn = n.new("ShaderNodeMapping")
    mpn.inputs["Location"].default_value = (-1, -0.75, 0); mpn.inputs["Scale"].default_value = (2, 2.6, 1)
    l.new(tcf.outputs["Generated"], mpn.inputs["Vector"])
    gr = n.new("ShaderNodeTexGradient"); gr.gradient_type = "SPHERICAL"; l.new(mpn.outputs["Vector"], gr.inputs["Vector"])
    pw = n.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 1.6; l.new(gr.outputs["Fac"], pw.inputs[0])
    mul = n.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 1.1; l.new(pw.outputs[0], mul.inputs[0])
    em = n.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (*L.COR_SABOR[0], 1)
    l.new(mul.outputs[0], em.inputs["Strength"]); l.new(em.outputs[0], n["Material Output"].inputs["Surface"])
    painel.data.materials.append(mp)
    contra = L.luz_area(sc, "contra_fileira", (x_meio, y_fileira + 7, 9), (x_meio, y_fileira, 0.5),
                        L.COR_SABOR[0], 4200, 22, 6)
    # a fileira aparece quando a camera entra no ultimo anel (sem buraco preto); o brilho rosa e a contraluz sobem
    f_sai_corredor = next(f for f in range(int(q(B_FURO)), q1) if ys[f] > aneis[-1][1] - ESC_ANEL - ESPACO_ANEL) + 6
    for ob in chao_objs + [chao, painel, contra]:
        ob.hide_render = True
        ob.keyframe_insert("hide_render", frame=q0 - 2)
        ob.hide_render = False
        ob.keyframe_insert("hide_render", frame=f_sai_corredor - 6)
    mul.inputs[1].default_value = 0.0; mul.inputs[1].keyframe_insert("default_value", frame=f_sai_corredor - 6)
    mul.inputs[1].default_value = 1.1; mul.inputs[1].keyframe_insert("default_value", frame=f_sai_corredor + 10)
    contra.data.energy = 0; contra.data.keyframe_insert("energy", frame=f_sai_corredor - 6)
    contra.data.energy = 4200; contra.data.keyframe_insert("energy", frame=f_sai_corredor + 10)
    # luzes do cata-vento (apagam quando a camera entra no furo)
    luzes = [L.luz_area(sc, "chave", (-6, -11, 8), (0, 0, 0), (1.0, 0.96, 0.92), 2200, 5, 5),
             L.luz_area(sc, "tira", (4, -9, 0.5), (0, 0, 0), (1, 1, 1), 1200, 0.3, 12),
             L.luz_area(sc, "contra_a", (-7, 4, 0), (0, 0, 0), L.COR_SABOR[0], 3000, 0.4, 14),
             L.luz_area(sc, "contra_b", (7, 4, 0), (0, 0, 0), (1.0, 0.92, 0.85), 2200, 0.4, 14)]
    for lz in luzes:
        e = lz.data.energy
        lz.data.keyframe_insert("energy", frame=q(B_FURO - 0.5))
        lz.data.energy = 0
        lz.data.keyframe_insert("energy", frame=f_some_cruz)
        lz.data.energy = e
    # mundo: a camera ve o fundo rosa (fixo), que escurece enquanto ela entra no furo; a iluminacao ve escuro
    w = bpy.data.worlds.new("mundo"); sc.world = w; w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    lp = nt.nodes.new("ShaderNodeLightPath")
    cor_cam = nt.nodes.new("ShaderNodeRGB"); cor_cam.name = "cor_fundo"
    escuro = nt.nodes.new("ShaderNodeRGB"); escuro.outputs[0].default_value = (0.01, 0.004, 0.008, 1)
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs["Factor"])
    nt.links.new(escuro.outputs[0], mx.inputs["A"]); nt.links.new(cor_cam.outputs[0], mx.inputs["B"])
    nt.links.new(mx.outputs["Result"], bg.inputs["Color"])
    sock = cor_cam.outputs[0]
    sock.default_value = (*FUNDO_CRUZ, 1); sock.keyframe_insert("default_value", frame=q(B_FURO - 1.2))
    sock.default_value = (0.008, 0.003, 0.006, 1); sock.keyframe_insert("default_value", frame=q(B_FURO - 0.1))
    # camera: trajeto assado quadro a quadro (velocidade continua)
    cam, alvo = L.camera(sc, 50)
    cam.data.dof.use_dof = False
    L.assar(cam, "location", quadros, [tuple(traj[f][0]) for f in quadros])
    L.assar(alvo, "location", quadros, [tuple(traj[f][1]) for f in quadros])
    L.assar(cam.data, "lens", quadros, [traj[f][2] for f in quadros])
    # copias nitidas no giro (borrao curto); mergulho, corredor e fileira com borrao normal
    for f_, sh in ((q0, 0.5), (q(B_RASTRO) - 1, 0.5), (q(B_RASTRO), 0.12), (q(B_FURO - 1), 0.12), (q(B_FURO - 0.4), 0.5)):
        sc.render.motion_blur_shutter = sh
        sc.render.keyframe_insert("motion_blur_shutter", frame=f_)
    # aneis que a camera ja passou nao podem aparecer
    for filhos, y_anel in aneis:
        passou = next((f for f in range(int(q(B_FURO)), q1) if ys[f] > y_anel + 0.5), None)
        if passou:
            for ob in filhos:
                ob.keyframe_insert("hide_render", frame=passou - 1)
                ob.hide_render = True
                ob.keyframe_insert("hide_render", frame=passou)
    L.render(sc, QUALIDADE, transparente=False, mblur=True)
    sc.view_settings.exposure = -0.35
    return {"sc": sc}, q0, q1


# ---------- execucao ----------
PLANOS = {"queda": plano_queda, "detalhes": plano_detalhes, "revela": plano_revela, "giros": plano_giros}

if PLANO == "helice":
    c, q0, q1 = plano_helice()
    if TESTE:
        pasta = L.RENDER / "testes"
        pasta.mkdir(parents=True, exist_ok=True)
        for f in TESTE:
            c["sc"].frame_set(f)
            c["sc"].render.filepath = str(pasta / f"helice_{QUALIDADE}_{f:04d}.png")
            bpy.ops.render.render(write_still=True)
    else:
        L.renderizar(c["sc"], L.RENDER / QUALIDADE / "helice", q0, q1)
    print(f"PLANO helice: quadros {q0}-{q1}")

if PLANO in PLANOS:
    c = cena_uma_lata()
    q0, q1 = PLANOS[PLANO](c)
    if TESTE:
        L.renderizar(c["sc"], L.RENDER / "testes", 0, 0, so=None) if False else None
        pasta = L.RENDER / "testes"
        pasta.mkdir(parents=True, exist_ok=True)
        for f in TESTE:
            c["sc"].frame_set(f)
            c["sc"].render.filepath = str(pasta / f"{PLANO}_{QUALIDADE}_{f:04d}.png")
            bpy.ops.render.render(write_still=True)
    else:
        L.renderizar(c["sc"], L.RENDER / QUALIDADE / PLANO, q0, q1)
    print(f"PLANO {PLANO}: quadros {q0}-{q1}")
