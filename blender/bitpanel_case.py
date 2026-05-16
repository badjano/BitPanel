# SPDX-License-Identifier: CERN-OHL-P-2.0
"""
BitPanel — parametric top plate for 32 toggles + 4 controls + LED pocket.

Run in Blender: Scripting workspace → Open → this file → Run Script (▶).
Units: millimetres in PARAMETERS; converted to metres inside Blender.

Works well with Blender MCP: paste or ``exec(open(...).read())`` via the MCP
``execute_blender_code`` tool after adapting paths.

Headless export (writes ``export/bitpanel_plate.stl`` next to this script)::

  blender --background --factory-startup --python blender/bitpanel_case.py

Use ``--factory-startup`` so user add-ons do not run in background mode (many assume a GPU UI).

References:
  https://docs.blender.org/api/current/bpy.ops.mesh.html
"""

from __future__ import annotations

import math

from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

MM = 0.001

PARAMETERS = {
    # Overall plate (XY), thickness (Z). Origin: bottom centre of plate; Z up.
    "plate_w_mm": 140.0,
    "plate_h_mm": 85.0,
    "plate_t_mm": 3.0,
    # Switch grid (cols × rows = 32). Default 8 × 4.
    "grid_cols": 8,
    "grid_rows": 4,
    "hole_pitch_x_mm": 15.0,
    "hole_pitch_y_mm": 15.0,
    # Panel-mount toggle / bush clearance — measure your hardware.
    "toggle_hole_d_mm": 12.0,
    # Modifier buttons row (below grid), centred as a block.
    "btn_row_offset_y_mm": -38.0,
    "btn_pitch_mm": 14.0,
    "btn_hole_d_mm": 8.5,
    # Single NeoPixel / frosted LED hole (front panel).
    "led_offset_x_mm": -58.0,
    "led_offset_y_mm": 34.0,
    "led_hole_d_mm": 5.0,
    # Simple corner mounting through plate (optional).
    "corner_mount_d_mm": 3.2,
    "corner_inset_mm": 6.0,
    # Underside pocket for Pico board body (no mounting bosses — use pads).
    "pico_pocket_w_mm": 54.0,
    "pico_pocket_h_mm": 24.0,
    "pico_pocket_depth_mm": 7.0,
    "pico_pocket_offset_x_mm": 0.0,
    "pico_pocket_offset_y_mm": -25.0,
}


def _purge_mesh_objects() -> None:
    bpy.ops.object.select_all(action="DESELECT")
    for obj in list(bpy.data.objects):
        if obj.type == "MESH":
            obj.select_set(True)
    bpy.ops.object.delete(use_global=False)


def _active(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def _cube(name: str, sx: float, sy: float, sz: float, loc: Vector) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name + "_mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bm.to_mesh(mesh)
    bm.free()
    obj.location = loc
    obj.scale = Vector((sx / 2.0, sy / 2.0, sz / 2.0))
    return obj


def _cylinder(name: str, diameter: float, height: float, loc: Vector) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diameter / 2.0,
        depth=height,
        vertices=64,
        location=loc,
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj


def _apply_boolean_difference(target: bpy.types.Object, cutter: bpy.types.Object) -> None:
    mod = target.modifiers.new(name="Bool_" + cutter.name, type="BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = cutter
    mod.solver = "EXACT"
    _active(target)
    bpy.ops.object.modifier_apply(modifier=mod.name)


def _join_objects(objs: list[bpy.types.Object], name: str) -> bpy.types.Object:
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    joined = bpy.context.active_object
    joined.name = name
    return joined


def build_case(p: dict[str, float]) -> bpy.types.Object:
    plate_w = p["plate_w_mm"] * MM
    plate_h = p["plate_h_mm"] * MM
    plate_t = p["plate_t_mm"] * MM

    plate = _cube(
        "BitPanel_Plate",
        plate_w,
        plate_h,
        plate_t,
        Vector((0.0, 0.0, plate_t / 2.0)),
    )
    bpy.ops.object.select_all(action="DESELECT")
    plate.select_set(True)
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.transform_apply(scale=True)

    cutters: list[bpy.types.Object] = []
    eps = 0.5 * MM
    cyl_h = plate_t + 4 * MM

    cols = int(p["grid_cols"])
    rows = int(p["grid_rows"])
    pitch_x = p["hole_pitch_x_mm"] * MM
    pitch_y = p["hole_pitch_y_mm"] * MM
    toggle_d = p["toggle_hole_d_mm"] * MM

    gx0 = -(cols - 1) * pitch_x / 2.0
    gy0 = -(rows - 1) * pitch_y / 2.0

    n = 0
    for r in range(rows):
        for c in range(cols):
            x = gx0 + c * pitch_x
            y = gy0 + r * pitch_y
            cutters.append(
                _cylinder(
                    f"Cutter_toggle_{n}",
                    toggle_d,
                    cyl_h,
                    Vector((x, y, plate_t / 2.0)),
                )
            )
            n += 1

    btn_y = p["btn_row_offset_y_mm"] * MM
    btn_pitch = p["btn_pitch_mm"] * MM
    btn_d = p["btn_hole_d_mm"] * MM
    bx0 = -(4 - 1) * btn_pitch / 2.0
    for i in range(4):
        cutters.append(
            _cylinder(
                f"Cutter_btn_{i}",
                btn_d,
                cyl_h,
                Vector((bx0 + i * btn_pitch, btn_y, plate_t / 2.0)),
            )
        )

    led_x = p["led_offset_x_mm"] * MM
    led_y = p["led_offset_y_mm"] * MM
    led_d = p["led_hole_d_mm"] * MM
    cutters.append(
        _cylinder(
            "Cutter_led",
            led_d,
            cyl_h,
            Vector((led_x, led_y, plate_t / 2.0)),
        )
    )

    inset = p["corner_inset_mm"] * MM
    md = p["corner_mount_d_mm"] * MM
    corners = [
        (plate_w / 2.0 - inset, plate_h / 2.0 - inset),
        (-plate_w / 2.0 + inset, plate_h / 2.0 - inset),
        (plate_w / 2.0 - inset, -plate_h / 2.0 + inset),
        (-plate_w / 2.0 + inset, -plate_h / 2.0 + inset),
    ]
    for i, (cx, cy) in enumerate(corners):
        cutters.append(
            _cylinder(
                f"Cutter_mount_{i}",
                md,
                cyl_h,
                Vector((cx, cy, plate_t / 2.0)),
            )
        )

    cutters_obj = _join_objects(cutters, "Cutters_All")
    cutters_obj.hide_render = True
    cutters_obj.hide_viewport = True

    _apply_boolean_difference(plate, cutters_obj)
    bpy.data.objects.remove(cutters_obj, do_unlink=True)

    pocket_w = p["pico_pocket_w_mm"] * MM
    pocket_h = p["pico_pocket_h_mm"] * MM
    pocket_d = p["pico_pocket_depth_mm"] * MM
    px = p["pico_pocket_offset_x_mm"] * MM
    py = p["pico_pocket_offset_y_mm"] * MM

    pocket = _cube(
        "Pico_Pocket_Cutter",
        pocket_w,
        pocket_h,
        pocket_d + eps,
        Vector((px, py, -(pocket_d + eps) / 2.0 + eps)),
    )
    _apply_boolean_difference(plate, pocket)
    bpy.data.objects.remove(pocket, do_unlink=True)

    bpy.ops.object.select_all(action="DESELECT")
    plate.select_set(True)
    bpy.context.view_layer.objects.active = plate
    return plate


def export_stl(obj: bpy.types.Object, filepath: str) -> None:
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Blender 4.x–5.x: exporter RNA keywords differ between releases.
    kw_variants = (
        {"filepath": filepath, "check_existing": False, "selection_only": True},
        {"filepath": filepath, "check_existing": False, "selected": True},
        {"filepath": filepath, "check_existing": False},
    )
    last_err: TypeError | None = None
    for kw in kw_variants:
        try:
            bpy.ops.wm.stl_export(**kw)
            return
        except TypeError as exc:
            last_err = exc
            continue
    assert last_err is not None
    raise last_err


def main() -> None:
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode="OBJECT")
    _purge_mesh_objects()
    plate = build_case(PARAMETERS)
    plate.location = Vector((0.0, 0.0, 0.0))
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")

    if bpy.app.background:
        try:
            script_dir = Path(__file__).resolve().parent
        except NameError:
            script_dir = Path.cwd()
        export_dir = script_dir / "export"
        export_dir.mkdir(parents=True, exist_ok=True)
        out_path = export_dir / "bitpanel_plate.stl"
        export_stl(plate, str(out_path))
        print(f"BitPanel: exported {out_path}")
        return

    # Interactive only: frame the result (optional).
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for region in area.regions:
                if region.type == "WINDOW":
                    override = bpy.context.copy()
                    override["area"] = area
                    override["region"] = region
                    try:
                        bpy.ops.view3d.view_selected(override)
                    except Exception:
                        pass
                    break


if __name__ == "__main__":
    main()
