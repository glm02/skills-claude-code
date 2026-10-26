"""Remplit un pan de toit de panneaux photovoltaïques à l'échelle, dans Blender.

Dans Blender : sélectionner l'objet toit, passer en mode Édition, sélectionner
la ou les faces du pan (touche 3 puis clic), revenir en mode Objet (Tab),
puis Scripting → ouvrir ce fichier → Run Script.
En ligne de commande (sans interface) :
  blender maison.blend --background --python poser_panneaux.py -- --objet Toit --sauver
Options après « -- » : --objet NOM, --largeur 1.134, --hauteur 1.722,
--wc 425, --marge 0.30, --ecart 0.02, --paysage, --sauver.

Le pan est repéré par sa face sélectionnée : l'axe du faîtage est pris sur le
bord le plus horizontal, la pente sur l'autre axe. Les panneaux sont posés
en grille dans la face, à « marge » des bords (règle des pompiers et du
vent : 30 cm minimum conseillés), et seulement là où les 4 coins tombent
dans la face. Unités de la scène : mètres.
"""
import sys
import bpy
import bmesh
from mathutils import Vector


def options():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    o = {"objet": None, "largeur": 1.134, "hauteur": 1.722, "wc": 425.0, "marge": 0.30, "ecart": 0.02, "paysage": False, "sauver": False}
    i = 0
    while i < len(args):
        cle = args[i].lstrip("-")
        if cle in ("paysage", "sauver"):
            o[cle] = True
        else:
            o[cle] = args[i + 1] if cle == "objet" else float(args[i + 1])
            i += 1
        i += 1
    if o["paysage"]:
        o["largeur"], o["hauteur"] = o["hauteur"], o["largeur"]
    return o


def dans_polygone(p, poly):
    """Point (u, v) dans un polygone 2D, par lancer de rayon."""
    dedans, j = False, len(poly) - 1
    for i in range(len(poly)):
        (xi, yi), (xj, yj) = poly[i], poly[j]
        if (yi > p[1]) != (yj > p[1]) and p[0] < (xj - xi) * (p[1] - yi) / (yj - yi) + xi:
            dedans = not dedans
        j = i
    return dedans


def materiau():
    m = bpy.data.materials.get("Panneau PV") or bpy.data.materials.new("Panneau PV")
    m.diffuse_color = (0.03, 0.06, 0.16, 1)
    m.metallic, m.roughness = 0.4, 0.25
    return m


def poser(obj, face, o, collection):
    mw = obj.matrix_world
    pts = [mw @ v.co for v in face.verts]
    n = (mw.to_3x3() @ face.normal).normalized()
    # Axe du faîtage : le bord de la face le plus horizontal.
    bords = [(pts[(k + 1) % len(pts)] - pts[k]) for k in range(len(pts))]
    u = max(bords, key=lambda e: e.length * (1 - abs(e.normalized().z))).normalized()
    v = n.cross(u).normalized()  # vers le haut de la pente
    if v.z < 0:
        v = -v
    origine = pts[0]
    poly = [((p - origine).dot(u), (p - origine).dot(v)) for p in pts]
    umin, umax = min(x for x, _ in poly), max(x for x, _ in poly)
    vmin, vmax = min(y for _, y in poly), max(y for _, y in poly)

    L, H, e, m = o["largeur"], o["hauteur"], o["ecart"], o["marge"]
    nb = 0
    # Grille centrée dans la zone utile : le reste se partage entre les deux bords.
    def depart(lo, hi, taille):
        utile = hi - lo - 2 * m
        k = int((utile + e) // (taille + e))
        return lo + m + max(0.0, utile - (k * (taille + e) - e)) / 2
    y = depart(vmin, vmax, H)
    while y + H <= vmax - m + 1e-6:
        x = depart(umin, umax, L)
        while x + L <= umax - m + 1e-6:
            coins = [(x, y), (x + L, y), (x, y + H), (x + L, y + H)]
            # Chaque coin doit être dans la face, et à « marge » de ses bords.
            if all(dans_polygone(c, poly) for c in coins) and all(
                dans_polygone((cx + dx, cy + dy), poly) for cx, cy in coins for dx, dy in ((m, 0), (-m, 0), (0, m), (0, -m))
            ):
                centre = origine + u * (x + L / 2) + v * (y + H / 2) + n * 0.06
                bpy.ops.mesh.primitive_cube_add(size=1, location=centre)
                p = bpy.context.active_object
                p.name = f"Panneau {nb + 1:02d}"
                p.matrix_world = _matrice(u, v, n, centre, L, H)  # repère du pan, à l'échelle du panneau
                p.data.materials.append(materiau())
                for c in p.users_collection:
                    c.objects.unlink(p)
                collection.objects.link(p)
                nb += 1
            x += L + e
        y += H + e
    return nb


def _matrice(u, v, n, centre, L, H):
    from mathutils import Matrix
    return Matrix((
        (u.x * L, v.x * H, n.x * 0.035, centre.x),
        (u.y * L, v.y * H, n.y * 0.035, centre.y),
        (u.z * L, v.z * H, n.z * 0.035, centre.z),
        (0, 0, 0, 1),
    ))


def main():
    o = options()
    obj = bpy.data.objects[o["objet"]] if o["objet"] else bpy.context.active_object
    if obj is None or obj.type != "MESH":
        raise SystemExit("Sélectionner l'objet toit (un maillage) ou passer --objet NOM.")
    if obj.mode == "EDIT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    faces = [f for f in bm.faces if f.select] or [f for f in bm.faces if f.normal.z > 0.2 and f.calc_area() > 4]
    col = bpy.data.collections.get("Panneaux PV") or bpy.data.collections.new("Panneaux PV")
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    for ob in list(col.objects):  # relancer le script remplace la pose précédente
        bpy.data.objects.remove(ob, do_unlink=True)
    total = 0
    for f in faces:
        k = poser(obj, f, o, col)
        print(f"Pan de {f.calc_area():.1f} m² : {k} panneaux")
        total += k
    bm.free()
    print(f"TOTAL : {total} panneaux de {o['wc']:.0f} Wc = {total * o['wc'] / 1000:.2f} kWc")
    if o["sauver"]:
        bpy.ops.wm.save_mainfile()


main()
