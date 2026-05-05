"""
Cinema 4D R25 script: Processing-style Emotion City.

This version follows the visual language of the adjusted Processing sketch,
but makes the contrast explicit:
- left side = park / relaxed / open
- right side = commercial / stressful / dense
- park side has green ground, trees, low soft fragments, wider spacing
- commercial side has red-orange towers, dense spacing, vertical traces

Use:
Script Manager -> paste/open this script -> Execute.
"""

import math
import random

import c4d
from c4d import documents, gui


GRID = 8
FPS = 30
END_FRAME = 1800


def lerp(a, b, t):
    return a + (b - a) * t


def map_value(v, a1, a2, b1, b2):
    if a2 - a1 == 0:
        return b1
    return b1 + (v - a1) * (b2 - b1) / (a2 - a1)


def clear_scene(doc):
    obj = doc.GetFirstObject()
    while obj:
        nxt = obj.GetNext()
        obj.Remove()
        obj = nxt
    mat = doc.GetFirstMaterial()
    while mat:
        nxt = mat.GetNext()
        mat.Remove()
        mat = nxt


def make_material(doc, name, rgb, luminance=0.0, alpha=1.0):
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    mat.SetName(name)
    mat[c4d.MATERIAL_USE_COLOR] = True
    mat[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(rgb[0], rgb[1], rgb[2])
    mat[c4d.MATERIAL_COLOR_BRIGHTNESS] = 1
    if luminance > 0:
        mat[c4d.MATERIAL_USE_LUMINANCE] = True
        mat[c4d.MATERIAL_LUMINANCE_COLOR] = c4d.Vector(rgb[0], rgb[1], rgb[2])
        mat[c4d.MATERIAL_LUMINANCE_BRIGHTNESS] = 0.15
    doc.InsertMaterial(mat)
    return mat


def add_mat(obj, mat):
    tag = c4d.TextureTag()
    tag.SetMaterial(mat)
    obj.InsertTag(tag)


def add_python_tag(obj, code):
    tag = c4d.BaseTag(c4d.Tpython)
    tag[c4d.TPYTHON_CODE] = code
    obj.InsertTag(tag)
    return tag


def insert_key(obj, desc_id, frame):
    fps = doc.GetFps()
    time = c4d.BaseTime(frame, fps)
    track = obj.FindCTrack(desc_id)
    if track is None:
        track = c4d.CTrack(obj, desc_id)
        obj.InsertTrackSorted(track)
    curve = track.GetCurve()
    key = curve.AddKey(time)["key"]
    key.SetValue(curve, obj[desc_id])


def create_cube(doc, name, pos, scale, mat, rot=(0, 0, 0)):
    obj = c4d.BaseObject(c4d.Ocube)
    obj.SetName(name)
    obj[c4d.PRIM_CUBE_LEN] = c4d.Vector(scale[0], scale[1], scale[2])
    obj.SetAbsPos(c4d.Vector(pos[0], pos[1], pos[2]))
    obj.SetAbsRot(c4d.Vector(rot[0], rot[1], rot[2]))
    add_mat(obj, mat)
    doc.InsertObject(obj)
    return obj


def setup_scene(doc):
    doc.SetFps(FPS)
    doc.SetMinTime(c4d.BaseTime(0, FPS))
    doc.SetMaxTime(c4d.BaseTime(END_FRAME, FPS))
    doc.SetTime(c4d.BaseTime(0, FPS))

    rd = doc.GetActiveRenderData()
    rd[c4d.RDATA_XRES] = 1920
    rd[c4d.RDATA_YRES] = 1080
    rd[c4d.RDATA_FRAMEFROM] = c4d.BaseTime(0, FPS)
    rd[c4d.RDATA_FRAMETO] = c4d.BaseTime(END_FRAME, FPS)


def create_ground(doc, grid_mat):
    grid_size = 7600

    ground_mat = make_material(doc, "soft_warm_ground", (0.78, 0.82, 0.86), 0.02)
    plane = c4d.BaseObject(c4d.Oplane)
    plane.SetName("emotion_city_bright_ground")
    plane[c4d.PRIM_PLANE_WIDTH] = grid_size
    plane[c4d.PRIM_PLANE_HEIGHT] = grid_size
    plane[c4d.PRIM_PLANE_SUBW] = 1
    plane[c4d.PRIM_PLANE_SUBH] = 1
    add_mat(plane, ground_mat)
    doc.InsertObject(plane)

    park_mat = make_material(doc, "park_green_zone", (0.30, 0.62, 0.42), 0.02)
    park = c4d.BaseObject(c4d.Oplane)
    park.SetName("park_relaxed_open_ground")
    park[c4d.PRIM_PLANE_WIDTH] = grid_size * 0.46
    park[c4d.PRIM_PLANE_HEIGHT] = grid_size * 0.86
    park.SetAbsPos(c4d.Vector(-grid_size * 0.26, 16, 0))
    add_mat(park, park_mat)
    doc.InsertObject(park)

    commercial_mat = make_material(doc, "commercial_warm_ground", (0.64, 0.44, 0.38), 0.02)
    commercial = c4d.BaseObject(c4d.Oplane)
    commercial.SetName("commercial_stressful_dense_ground")
    commercial[c4d.PRIM_PLANE_WIDTH] = grid_size * 0.46
    commercial[c4d.PRIM_PLANE_HEIGHT] = grid_size * 0.86
    commercial.SetAbsPos(c4d.Vector(grid_size * 0.26, 18, 0))
    add_mat(commercial, commercial_mat)
    doc.InsertObject(commercial)

    step = 420
    line_thick = 14
    count = int(grid_size / step)
    for i in range(-count // 2, count // 2 + 1):
        offset = i * step
        create_cube(doc, "grid_x", (offset, 8, 0), (line_thick, 8, grid_size), grid_mat)
        create_cube(doc, "grid_z", (0, 8, offset), (grid_size, 8, line_thick), grid_mat)


def create_tree(doc, x, z, trunk_mat, crown_mat, parent):
    trunk = c4d.BaseObject(c4d.Ocylinder)
    trunk.SetName("park_tree_trunk")
    trunk[c4d.PRIM_CYLINDER_RADIUS] = 28
    trunk[c4d.PRIM_CYLINDER_HEIGHT] = 220
    trunk.SetAbsPos(c4d.Vector(x, 110, z))
    add_mat(trunk, trunk_mat)
    doc.InsertObject(trunk)
    trunk.InsertUnder(parent)

    crown = c4d.BaseObject(c4d.Osphere)
    crown.SetName("park_tree_crown")
    crown[c4d.PRIM_SPHERE_RAD] = random.uniform(120, 190)
    crown.SetAbsPos(c4d.Vector(x, 285, z))
    add_mat(crown, crown_mat)
    doc.InsertObject(crown)
    crown.InsertUnder(parent)


def create_city(doc):
    park_body = make_material(doc, "park_low_blocks_blue_green", (0.23, 0.58, 0.68), 0.03)
    park_soft = make_material(doc, "park_soft_landscape", (0.38, 0.70, 0.48), 0.04)
    commercial_body = make_material(doc, "commercial_towers_red_orange", (0.78, 0.38, 0.30), 0.03)
    outline_mat = make_material(doc, "dark_readable_edges", (0.035, 0.045, 0.06), 0.0)
    trace_mat = make_material(doc, "commercial_vertical_light_traces", (0.95, 0.42, 0.24), 0.18)
    trunk_mat = make_material(doc, "tree_trunk_soft_brown", (0.35, 0.22, 0.14), 0.0)
    crown_mat = make_material(doc, "tree_crown_green", (0.18, 0.52, 0.28), 0.04)

    random.seed(42)
    group = c4d.BaseObject(c4d.Onull)
    group.SetName("emotion_city_park_vs_commercial")
    doc.InsertObject(group)

    for x in range(-GRID, GRID + 1):
        for z in range(-GRID, GRID + 1):
            is_park = x < 0
            if is_park:
                spacing = 620
                box_size = random.uniform(160, 310)
                height_factor = random.uniform(140, 520)
                distortion = 80
                mat = park_body if random.random() > 0.45 else park_soft
                px = x * spacing - 650 + math.sin(z * 0.7) * distortion
                pz = z * spacing + math.cos(x * 0.4) * distortion
                h = height_factor * map_value(abs(z), 0, GRID, 1.0, 0.55)
                rot_y = math.radians(math.sin(x + z) * 8)
                name = "park_relaxed_fragment_%02d_%02d" % (x + GRID, z + GRID)
            else:
                spacing = 380
                box_size = random.uniform(260, 560)
                height_factor = random.uniform(900, 2850)
                distortion = 180
                mat = commercial_body
                px = x * spacing + 680 + math.sin(z * 0.9) * distortion
                pz = z * spacing + math.cos(x * 0.9) * distortion
                centre = math.sqrt((x - 4) * (x - 4) + z * z)
                h = height_factor * map_value(centre, 0, GRID * 1.3, 1.1, 0.55)
                rot_y = math.radians((x + z) * 3.0)
                name = "commercial_stress_fragment_%02d_%02d" % (x + GRID, z + GRID)

            h = max(90, h)

            block = create_cube(
                doc,
                name,
                (px, h * 0.5, pz),
                (box_size, h, box_size),
                mat,
                (math.radians(math.sin(x) * (2 if is_park else 7)), rot_y, math.radians(math.cos(z) * (2 if is_park else 7))),
            )
            block.InsertUnder(group)

            outline = create_cube(
                doc,
                name + "_dark_base",
                (px, 12, pz),
                (box_size * 1.04, 24, box_size * 1.04),
                outline_mat,
                (0, rot_y, 0),
            )
            outline.InsertUnder(group)

            if is_park and random.random() > 0.72:
                create_tree(doc, px + random.uniform(-180, 180), pz + random.uniform(-180, 180), trunk_mat, crown_mat, group)

            if (not is_park) and (x + z) % 3 == 0:
                trace = create_cube(
                    doc,
                    name + "_vertical_trace",
                    (px, h + 470, pz),
                    (18, 760, 18),
                    trace_mat,
                )
                trace.InsertUnder(group)

    # A soft open park path, clearly contrasting with the tower field.
    path_mat = make_material(doc, "park_open_path_light", (0.72, 0.78, 0.70), 0.01)
    for i in range(-5, 6):
        path = create_cube(
            doc,
            "park_slow_curving_path",
            (-4200 + i * 360, 32, math.sin(i * 0.65) * 880),
            (300, 30, 520),
            path_mat,
            (0, math.radians(math.sin(i) * 20), 0),
        )
        path.InsertUnder(group)

    insert_key(group, c4d.ID_BASEOBJECT_ROTATION, 0)
    group.SetAbsRot(c4d.Vector(0, math.radians(360), 0))
    insert_key(group, c4d.ID_BASEOBJECT_ROTATION, END_FRAME)
    add_python_tag(
        group,
        """
import c4d, math
def main():
    obj = op.GetObject()
    frame = doc.GetTime().GetFrame(doc.GetFps())
    obj.SetRelRot(c4d.Vector(0, frame * 0.018, 0))
""",
    )


def create_lights_and_camera(doc):
    key = c4d.BaseObject(c4d.Olight)
    key.SetName("soft_key_light")
    key[c4d.LIGHT_TYPE] = c4d.LIGHT_TYPE_AREA
    key[c4d.LIGHT_BRIGHTNESS] = 1
    key.SetAbsPos(c4d.Vector(0, 5200, -4200))
    doc.InsertObject(key)

    cool = c4d.BaseObject(c4d.Olight)
    cool.SetName("cool_blue_side_light")
    cool[c4d.LIGHT_TYPE] = c4d.LIGHT_TYPE_OMNI
    cool[c4d.LIGHT_BRIGHTNESS] = 1
    cool.SetAbsPos(c4d.Vector(4200, 2400, 2600))
    doc.InsertObject(cool)

    warm = c4d.BaseObject(c4d.Olight)
    warm.SetName("warm_orange_side_light")
    warm[c4d.LIGHT_TYPE] = c4d.LIGHT_TYPE_OMNI
    warm[c4d.LIGHT_BRIGHTNESS] = 1
    warm.SetAbsPos(c4d.Vector(-4200, 2100, -1800))
    doc.InsertObject(warm)

    cam = c4d.BaseObject(c4d.Ocamera)
    cam.SetName("processing_style_camera")
    cam.SetAbsPos(c4d.Vector(0, 4300, -9800))
    cam.SetAbsRot(c4d.Vector(math.radians(-25), 0, 0))
    doc.InsertObject(cam)

    add_python_tag(
        cam,
        """
import c4d, math
def main():
    obj = op.GetObject()
    frame = doc.GetTime().GetFrame(doc.GetFps())
    t = frame / float(doc.GetFps())
    radius = 9200 + math.sin(t * 0.18) * 650
    x = math.sin(t * 0.10) * radius
    z = -math.cos(t * 0.10) * radius
    y = 4100 + math.sin(t * 0.23) * 360
    obj.SetAbsPos(c4d.Vector(x, y, z))

    target = c4d.Vector(0, 900, 0)
    direction = target - obj.GetAbsPos()
    m = c4d.utils.VectorToHPB(direction)
    obj.SetAbsRot(m)
""",
    )

    bd = doc.GetActiveBaseDraw()
    if bd:
        bd.SetSceneCamera(cam)


def main():
    global doc
    doc = documents.GetActiveDocument()
    try:
        clear_scene(doc)
        setup_scene(doc)

        grid_col = (0.42, 0.58, 0.66)
        grid_mat = make_material(doc, "processing_style_ground_grid", grid_col, 0.08, 0.65)
        create_ground(doc, grid_mat)
        create_city(doc)
        create_lights_and_camera(doc)
        c4d.EventAdd()
        gui.MessageDialog("Processing-style Cinema 4D Emotion City generated.")
    except Exception as e:
        gui.MessageDialog("Script error:\n" + str(e))
        print("Script error:", str(e))


if __name__ == "__main__":
    main()
