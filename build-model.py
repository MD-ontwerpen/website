# -*- coding: utf-8 -*-
"""
Generates a layered building model as GLB, one layer per service.

Every mesh is named `layer_<slug>__<part>` so the viewer can group meshes by
service and highlight one layer while dimming the rest. That is the same idea as
the 2D service drawings: one building, thirteen readings of it.

PLACEHOLDER GEOMETRY. This is a generic massing model, not a real project.
Replace it with an actual building exported from ArchiCAD when one is available.

Run from the website/ folder:  python build-model.py
"""
import json
import os

import numpy as np
import trimesh

# Site palette
INK = [24, 24, 27, 255]
PAPER = [252, 252, 253, 255]
MUTED = [226, 232, 240, 255]
SOFT = [148, 163, 184, 255]
ACCENT = [37, 99, 235, 255]
WARM = [244, 244, 245, 255]
GROUND = [240, 243, 246, 255]

W, D = 12.0, 8.0
FLOOR_H = 3.0
FLOORS = 3
WALL_H = FLOOR_H * FLOORS
RIDGE = 3.0

parts = []          # (name, mesh)


def add(slug, part, mesh, colour, rough=0.82, metal=0.0):
    # A PBR material rather than face colours: face colours would be baked to
    # per-vertex data on export (which needs scipy and bloats the file), and a
    # single material per mesh is what the viewer swaps when highlighting.
    # Roughness is varied per element - uniform roughness is what makes an
    # untextured model read as a pile of boxes.
    mesh.visual = trimesh.visual.TextureVisuals(
        material=trimesh.visual.material.PBRMaterial(
            name=f'{slug}_{part}',
            baseColorFactor=[c / 255.0 for c in colour],
            metallicFactor=metal,
            roughnessFactor=rough,
        )
    )
    parts.append((f'layer_{slug}__{part}', mesh))


def box(size, at, ):
    m = trimesh.creation.box(extents=size)
    m.apply_translation(at)
    return m


# ---------------------------------------------------------------- landschap
add('landschap', 'terras', box([22, 16, 0.22], [0, 0, -0.11]), GROUND, rough=0.95)
add('landschap', 'gazon', box([32, 24, 0.10], [0, 0, -0.21]), [237, 241, 236, 255], rough=1.0)
for i, (x, y) in enumerate(((-11, 6), (11.5, -5), (10, 7), (-12, -6))):
    t = trimesh.creation.cylinder(radius=0.15, height=2.0)
    t.apply_translation([x, y, 1.0])
    add('landschap', f'stam{i}', t, SOFT)
    c = trimesh.creation.icosphere(subdivisions=1, radius=1.4)
    c.apply_translation([x, y, 3.0])
    add('landschap', f'kroon{i}', c, MUTED)
add('landschap', 'pad', box([3.0, 7.0, 0.12], [0, D / 2 + 4.0, 0.06]), MUTED)

# ----------------------------------------------------------- constructieleer
add('constructieleer', 'fundering', box([W + 1.2, D + 1.2, 0.8], [0, 0, -0.4]), SOFT)
for i, x in enumerate((-W / 2 + 0.6, 0.0, W / 2 - 0.6)):
    for j, y in enumerate((-D / 2 + 0.6, D / 2 - 0.6)):
        col = box([0.45, 0.45, WALL_H], [x, y, WALL_H / 2])
        add('constructieleer', f'kolom{i}{j}', col, SOFT)
for f in range(1, FLOORS + 1):
    add('constructieleer', f'vloer{f}', box([W - 0.2, D - 0.2, 0.26], [0, 0, f * FLOOR_H]), SOFT, rough=0.94)

# ------------------------------------------------------------------ bouwkunde
# Facade: piers with recessed glazing between them. A flat panel is what makes
# a massing model read as a crate; the reveal depth is what catches shadow.
GLASS = [58, 72, 92, 255]
PIER_W, REVEAL = 0.7, 0.16
PIERS_X = [-W / 2 + PIER_W / 2, -W / 6, W / 6, W / 2 - PIER_W / 2]
PIERS_Y = [-D / 2 + PIER_W / 2, 0.0, D / 2 - PIER_W / 2]

for f in range(FLOORS):
    z = f * FLOOR_H + FLOOR_H / 2
    h = FLOOR_H - 0.3

    # long facades (north / south)
    for y, tag in ((D / 2, 'n'), (-D / 2, 'z')):
        add('bouwkunde', f'glas_{tag}{f}',
            box([W - 0.1, 0.16, h - 0.12], [0, y - np.sign(y) * REVEAL, z]),
            GLASS, rough=0.12, metal=0.35)
        for i, x in enumerate(PIERS_X):
            add('bouwkunde', f'penant_{tag}{f}_{i}',
                box([PIER_W, 0.34, h], [x, y, z]), PAPER, rough=0.78)
        add('bouwkunde', f'borst_{tag}{f}',
            box([W, 0.34, 0.55], [0, y, z - h / 2 + 0.27]), PAPER, rough=0.78)

    # short facades (east / west)
    for x, tag in ((W / 2, 'o'), (-W / 2, 'w')):
        add('bouwkunde', f'glas_{tag}{f}',
            box([0.16, D - 0.1, h - 0.12], [x - np.sign(x) * REVEAL, 0, z]),
            GLASS, rough=0.12, metal=0.35)
        for i, y in enumerate(PIERS_Y):
            add('bouwkunde', f'penant_{tag}{f}_{i}',
                box([0.34, PIER_W, h], [x, y, z]), PAPER, rough=0.78)
        add('bouwkunde', f'borst_{tag}{f}',
            box([0.34, D, 0.55], [x, 0, z - h / 2 + 0.27]), PAPER, rough=0.78)
for f in range(1, FLOORS):
    add('bouwkunde', f'band{f}', box([W + 0.62, D + 0.62, 0.24], [0, 0, f * FLOOR_H]), INK, rough=0.55)

# ---------------------------------------------------------------- architectuur
# The massing read: envelope volume plus roof
env = box([W + 0.34, D + 0.34, WALL_H], [0, 0, WALL_H / 2])
add('architectuur', 'volume', env, WARM, rough=0.88)
profile = np.array([[-D / 2 - 0.3, 0.0], [D / 2 + 0.3, 0.0], [0.0, RIDGE]])
roof = trimesh.creation.extrude_triangulation(
    vertices=profile, faces=np.array([[0, 1, 2]]), height=W + 0.6)
# extrude_triangulation builds along +Z, so the prism comes out lying down.
# -90 about X stands the profile up, +90 about Z turns the ridge along the
# width. Verified by span: X=12.6 (breedte), Y=8.6 (diepte), Z=3.0 (nok).
roof.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))
roof.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1]))
# Seat it on the walls and centre it, from the actual bounds rather than
# hand-computed offsets that drift whenever the profile changes.
_b = roof.bounds
roof.apply_translation([
    -(_b[0][0] + _b[1][0]) / 2,
    -(_b[0][1] + _b[1][1]) / 2,
    WALL_H - _b[0][2],
])
add('architectuur', 'dak', roof, INK, rough=0.6)
add('architectuur', 'entree', box([2.6, 0.6, 2.7], [0, D / 2 + 0.3, 1.35]), ACCENT, rough=0.35, metal=0.15)
add('architectuur', 'luifel', box([4.4, 1.8, 0.22], [0, D / 2 + 0.9, 2.95]), INK, rough=0.5)

# ------------------------------------------------------------------ bouwfysica
# The thermal skin: a shell offset outside the envelope
shell = box([W + 0.7, D + 0.7, WALL_H + 0.35], [0, 0, (WALL_H + 0.35) / 2])
add('bouwfysica', 'schil', shell, ACCENT)

# -------------------------------------------------------------------- interieur
for f in range(FLOORS):
    z = f * FLOOR_H + FLOOR_H / 2
    add('interieur', f'wand_a{f}', box([0.16, D - 1.4, FLOOR_H - 0.4], [-2.0, 0.4, z]), MUTED)
    add('interieur', f'wand_b{f}', box([W - 5.0, 0.16, FLOOR_H - 0.4], [2.2, -0.8, z]), MUTED)
    add('interieur', f'vloerafw{f}', box([W - 1.0, D - 1.0, 0.06], [0, 0, f * FLOOR_H + 0.16]), WARM)

# ------------------------------------------------------------ brandveiligheid
add('brandveiligheid', 'trappenhuis', box([2.4, 2.4, WALL_H], [-W / 2 + 1.8, -D / 2 + 1.8, WALL_H / 2]), ACCENT)
for f in range(FLOORS):
    z = f * FLOOR_H + FLOOR_H / 2
    add('brandveiligheid', f'vluchtroute{f}',
        box([W - 5.0, 0.5, 0.08], [1.0, -D / 2 + 1.8, z - FLOOR_H / 2 + 0.3]), ACCENT)
add('brandveiligheid', 'uitgang', box([1.4, 0.4, 2.2], [-W / 2 + 1.8, -D / 2 - 0.2, 1.1]), ACCENT)

# ------------------------------------------------------- installatietechniek
add('installatietechniek', 'schacht', box([1.1, 1.1, WALL_H], [W / 2 - 1.6, D / 2 - 1.6, WALL_H / 2]), ACCENT)
for f in range(FLOORS):
    z = f * FLOOR_H + FLOOR_H - 0.5
    add('installatietechniek', f'kanaal{f}', box([W - 4.0, 0.42, 0.42], [-0.5, D / 2 - 1.6, z]), ACCENT)
    add('installatietechniek', f'aftak{f}', box([0.34, D - 4.0, 0.34], [W / 2 - 1.6, -0.4, z]), ACCENT)
unit = box([2.2, 1.6, 1.0], [W / 2 - 2.2, D / 2 - 2.0, WALL_H + 0.6])
add('installatietechniek', 'unit', unit, ACCENT)

# --------------------------------------------------------- informatiemodel
# A model grid: thin edges describing the building envelope as data
gx, gy, gz = W + 1.4, D + 1.4, WALL_H + RIDGE
e = 0.05
for xs in (-gx / 2, gx / 2):
    for ys in (-gy / 2, gy / 2):
        add('informatiemodel', f'rib_v{xs:.0f}{ys:.0f}', box([e, e, gz], [xs, ys, gz / 2]), ACCENT)
for z in (0, WALL_H, gz):
    for ys in (-gy / 2, gy / 2):
        add('informatiemodel', f'rib_x{z:.0f}{ys:.0f}', box([gx, e, e], [0, ys, z]), ACCENT)
    for xs in (-gx / 2, gx / 2):
        add('informatiemodel', f'rib_y{z:.0f}{xs:.0f}', box([e, gy, e], [xs, 0, z]), ACCENT)

# ------------------------------------------------------------------- vergunnen
# Plot boundary: the legal envelope the plan is tested against
for ys in (-11.5, 11.5):
    add('vergunnen', f'grens_x{ys:.0f}', box([26, 0.14, 0.14], [0, ys, 0.07]), ACCENT)
for xs in (-13, 13):
    add('vergunnen', f'grens_y{xs:.0f}', box([0.14, 23, 0.14], [xs, 0, 0.07]), ACCENT)
for i, (x, y) in enumerate(((-13, -11.5), (13, -11.5), (-13, 11.5), (13, 11.5))):
    pin = trimesh.creation.cylinder(radius=0.2, height=1.6)
    pin.apply_translation([x, y, 0.8])
    add('vergunnen', f'piket{i}', pin, ACCENT)

# ----------------------------------------------------------------- aanbesteden
for i, x in enumerate((-7.0, -0.5, 6.0)):
    h = (1.6, 2.4, 1.9)[i]
    add('aanbesteden', f'inschrijving{i}', box([3.0, 2.0, h], [x, -13.5, h / 2]), ACCENT if i == 1 else MUTED)

# ---------------------------------------------------------------------- bouwen
mast = box([0.7, 0.7, 18.0], [W / 2 + 5.0, -D / 2 - 3.0, 9.0])
add('bouwen', 'kraanmast', mast, ACCENT)
add('bouwen', 'kraanarm', box([16.0, 0.5, 0.5], [W / 2 - 2.0, -D / 2 - 3.0, 17.6]), ACCENT)
add('bouwen', 'contragewicht', box([2.4, 1.2, 1.2], [W / 2 + 11.5, -D / 2 - 3.0, 17.6]), MUTED)
add('bouwen', 'hijskabel', box([0.08, 0.08, 6.0], [W / 2 - 6.0, -D / 2 - 3.0, 14.4]), SOFT)
add('bouwen', 'element', box([2.6, 1.4, 0.3], [W / 2 - 6.0, -D / 2 - 3.0, 11.2]), ACCENT)

# ------------------------------------------------------------------- opleveren
key = trimesh.creation.icosphere(subdivisions=2, radius=1.1)
key.apply_translation([0, 0, WALL_H + RIDGE + 2.6])
add('opleveren', 'markering', key, ACCENT)
add('opleveren', 'sokkel', box([0.16, 0.16, 2.2], [0, 0, WALL_H + RIDGE + 0.9]), SOFT)


def main():
    # The model is authored Z-up (the convention in building software), but
    # glTF is Y-up. Rotate before export so the GLB is spec-correct and stands
    # upright in any viewer, rather than patching it in one consumer.
    to_y_up = trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])

    scene = trimesh.Scene()
    for name, mesh in parts:
        m = mesh.copy()
        m.apply_transform(to_y_up)
        scene.add_geometry(m, geom_name=name, node_name=name)

    out = 'assets/models/gebouw-lagen.glb'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    scene.export(out)

    layers = {}
    for name, mesh in parts:
        slug = name.split('__')[0].replace('layer_', '')
        layers.setdefault(slug, 0)
        layers[slug] += len(mesh.faces)

    print(f'  {out}  ({os.path.getsize(out) / 1024:.0f} KB)')
    print(f'  meshes    : {len(parts)}')
    print(f'  triangles : {sum(len(m.faces) for _, m in parts):,}')
    print(f'  layers    : {len(layers)}')
    for slug, tris in sorted(layers.items()):
        print(f'    {slug:22s} {tris:>6,} tris')

    io_path = 'assets/models/lagen.json'
    with open(io_path, 'w', encoding='utf-8') as f:
        json.dump(sorted(layers), f, ensure_ascii=False, indent=2)
    print(f'  layer index -> {io_path}')


if __name__ == '__main__':
    main()
