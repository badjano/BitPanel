# BitPanel — panel plate (Blender)

Parametric **top plate** for an **8×4** toggle grid (32 holes on the default layout), four mode buttons, one LED hole, corner mounts, and an underside **Pico pocket**. Firmware colour is **24-bit RGB** — wire **24** toggles to colour bits or map 32 positions via `pico/hw_config.py` (`BIT_PERM`).

← **[Project overview](../README.md)** · Firmware & wiring: **[pico/README.md](../pico/README.md)**

## Files

| File | Role |
|------|------|
| `bitpanel_case.py` | Build geometry; edit `PARAMETERS` at the top (millimetres) |
| `export/bitpanel_plate.stl` | Example export — see **[export/README.md](export/README.md)** |

## Interactive (Blender UI)

1. Install **Blender 3 LTS or newer** (4.x / 5.x is fine).
2. **Scripting** workspace → **Text → Open** → `bitpanel_case.py` → **Run Script**.

You get mesh **`BitPanel_Plate`**: **8×4** toggle holes, **four** button holes, **one** LED hole, **corner** through-holes, **Pico pocket** on the underside.

### Tune `PARAMETERS`

- `toggle_hole_d_mm` — panel hole for your toggle bushings  
- `hole_pitch_x_mm` / `hole_pitch_y_mm` — centre spacing  
- `btn_*` — mode button row position and diameters  
- `led_*` — LED hole position and diameter  
- `pico_pocket_*` — clearance under the plate (no screw bosses; use pads or a tray)

Export: select plate → **File → Export → STL** (or 3MF).

## Headless STL export

Regenerate without opening the UI:

```bash
blender --background --factory-startup --python blender/bitpanel_case.py
```

`--factory-startup` skips personal add-ons (many fail in `--background` without a GPU UI).

**Steam (Windows PowerShell):**

```powershell
& 'C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe' --background --factory-startup --python 'path\to\BitPanel\blender\bitpanel_case.py'
```

Output: **`export/bitpanel_plate.stl`** (folder created automatically).

## Blender MCP (optional)

Blender MCP lets an IDE run Python in Blender (`execute_blender_code`). Typical flow:

1. Install the **Blender addon** from your MCP project → enable in **Edit → Preferences → Add-ons**.
2. Connect from Blender’s MCP sidebar.
3. In **Cursor**: **Settings → MCP → Add server** (follow your MCP package README).

You can run this script via MCP or paste `bitpanel_case.py` into an execute-code action. If MCP is unavailable, use the UI or headless command above.

## Mechanical assembly

1. **Print** the plate; remove supports; test **one** toggle hole and **one** button before mounting all 32.
2. **Mount toggles** from the front; note **which physical position is bit 0** (map in `pico/hw_config.py` via `BIT_PERM` if needed).
3. **Mount** four tactile mode switches.
4. **Install** LED from the front (diffuser optional).
5. **Mount Pico** under the panel (adhesive, standoffs, or separate tray — the script only cuts a **pocket**).
6. **USB** exit is not modelled by default — slot in CAD, drill, or file as needed.

Electronics and firmware: **[pico/README.md](../pico/README.md)**.

## License

Hardware design materials in this folder are under **[CERN-OHL-P-Version-2](../LICENSE-HARDWARE)**.
