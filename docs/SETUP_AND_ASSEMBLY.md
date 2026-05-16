# BitPanel — setup and assembly

BitPanel is a 32-toggle “bit playground” that drives an RGB LED from the logical colour formed by the switches, with a Raspberry Pi Pico handling scanning and modes (random colour, quantized “organized” colour, and rotating bits within the 24-bit RGB word).

This guide covers:

1. Making the panel case in Blender (including optional **Blender MCP** in Cursor).
2. Wiring the electronics.
3. Installing firmware on the Pico.

---

## 1. Parts (starting point)

| Item | Notes |
|------|--------|
| Raspberry Pi Pico | MicroPython build with `neopixel` support |
| 74HC165 shift registers × 4 | 32 parallel inputs, three-wire serial chain to the Pico |
| Toggles × 32 | Match hole size in Blender script (default assumes ~12 mm bush; measure yours) |
| Tactile switches × 4 | Random / Organize / Shift up / Shift down |
| WS2812 (“NeoPixel”) LED × 1 | Or small NeoPixel PCB |
| Resistors | Pull-ups as needed (chip inputs, buttons — Pico has internal pulls on GPIO buttons) |
| Power | USB for Pico; NeoPixel at 5 V often needs level shifting — many builds use a 3.3 V–tolerant pixel or a single level-shifted data line |
| Fasteners | Panel screws for toggles; M3 or similar for corner holes if used |
| Wire, solder, perfboard or PCB | Optional custom PCB for shift registers |

Always measure **your** switch bushings and pixels before printing.

---

## 2. Case in Blender

### 2.1 Parametric script (recommended)

The repo includes `blender/bitpanel_case.py`.

1. Install **Blender 3 LTS or newer** (4.x is fine).
2. Open Blender → top menu **Scripting**.
3. **Text → Open** and choose `bitpanel_case.py`, or paste its contents into the default text block.
4. Click **Run Script**.

You should get one mesh `BitPanel_Plate`: holes for a **8×4** grid (32 toggles), **four** button holes, **one** LED hole, **corner** through-holes, and an **underside pocket** sized roughly for a Pico body.

**Tune geometry** by editing the `PARAMETERS` dict at the top of the script (all dimensions in millimetres):

- `toggle_hole_d_mm` — must match panel drill size for your toggles.
- `hole_pitch_*` — centre-to-centre spacing so switches do not collide.
- `btn_*` — positions and diameters for the four mode buttons.
- `led_*` — LED hole position and diameter.
- `pico_pocket_*` — clearance pocket under the plate (does not include standoffs; add adhesive pads or a separate carrier).

Then export for printing: select the plate → **File → Export → STL** (or 3MF).

### 2.1.1 Headless STL export (optional)

If Blender is installed locally, you can regenerate the mesh and write an STL **without opening the UI**:

```bash
blender --background --factory-startup --python blender/bitpanel_case.py
```

`--factory-startup` skips your personal add-ons (many break in `--background` without a GPU UI).

On Windows (PowerShell), **Steam** installs Blender here:

```powershell
& 'C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe' --background --factory-startup --python 'F:\Projects\Badjano\Toys\BitPanel\blender\bitpanel_case.py'
```

Adjust the `--python` path if your repo lives elsewhere. Installers from blender.org usually land under `C:\Program Files\Blender Foundation\Blender *`.

That creates `blender/export/bitpanel_plate.stl` next to the script (the folder is created automatically).

### 2.2 Blender MCP from Cursor (optional)

Blender MCP connects Blender to an MCP client (such as Cursor) so an assistant can inspect the scene and run Python via tools like `execute_blender_code`.

**Typical setup** (verify against the server you install; names vary):

1. Install the **Blender addon** shipped with your chosen Blender MCP project (often via **Edit → Preferences → Add-ons → Install…** then enable it).
2. In Blender’s 3D View sidebar, open the MCP panel and **connect** to the IDE server when prompted.
3. In **Cursor**: **Settings → MCP → Add server**. On Windows, many guides use a wrapper such as running `uvx` via `cmd` (example pattern: command `cmd`, arguments `["/c", "uvx", "blender-mcp"]`). Exact package name and flags depend on the upstream repo you pick — follow its README.
4. Once connected, you can either:
   - paste the contents of `bitpanel_case.py` into an MCP “execute code” action, or  
   - run `exec(open(r"F:\path\to\bitpanel_case.py").read())` after adjusting the path.

If MCP is unavailable, running the script directly in Blender (section 2.1) produces the same geometry.

---

## 3. Electronics overview

### 3.1 Shift registers (32 inputs, 3 Pico pins)

Four **74HC165** devices are chained:

- Tie **parallel load** inputs (**PL** / **SH/~LD**) together → one Pico GPIO (`PIN_SR_PL`), active-low load pulse.
- Shared **clock** (**CLK**) → `PIN_SR_CP`.
- **Serial chain**: **Q7** (or labelled serial out) of chip *n* → **serial data in** of chip *n+1*.
- First chip’s serial input can be tied **LOW** (or last-out topology depending on datasheet convention — match your clocking order to `SHIFT_MSB_FIRST` in `pico/hw_config.py`).
- **CE** / inhibit pins: wired so shifting is enabled when clocking (often tied low if not used).

Each ’165 captures eight toggles on **parallel load**, then you clock **32** edges and sample **DATA** each cycle — see `pico/shift165.py`.

**Ground**: common ground between Pico, registers, switches, and LED supply return.

**Debouncing**: firmware does a simple stable double-read; heavy bouncing may need RC or hardware debounce on the shift-register inputs.

### 3.2 Four mode buttons

Directly to Pico GPIO with **internal pull-ups** (configured in `main.py`): active **LOW**. Default pins: GP20–GP23 (`hw_config.py`).

### 3.3 NeoPixel

Default data pin **GP15**. Many strips expect **5 V** logic; the Pico is **3.3 V**. Options:

- Use a **level shifter** on the data line, or  
- A pixel / breakout documented as **3.3 V data compatible**, or  
- Power arrangement per your strip’s datasheet.

Connect **GND** common with the Pico.

---

## 4. Firmware

### 4.1 Files

Copy everything under `pico/` to the Pico filesystem (same layout):

- `main.py` — entry loop  
- `hw_config.py` — pins and mapping  
- `shift165.py` — ’165 reader  
- `bits_ops.py` — RGB helpers and transforms  

### 4.2 MicroPython

1. Flash a **MicroPython** UF2 for Raspberry Pi Pico from [micropython.org](https://micropython.org/download/RPI_PICO/).
2. Mount USB storage and copy the `pico/*.py` files to the root (or ensure `main.py` runs at boot).
3. Confirm **`neopixel`** module exists on your build (common on Pico builds).

### 4.3 First tests

1. With **no NeoPixel** attached yet, you can temporarily comment out `NeoPixel` writes or lower brightness in code to avoid hot pixels during mistakes.
2. Open **Thonny** (or `rshell`) and run `import shift165` tests — easiest check is printing `read_raw()` while toggling one switch (after fixing bit order if inverted).
3. If colours channel-swap, swap bytes in `bits_ops.word_to_rgb` / wiring — or adjust `BIT_PERM` / `SHIFT_MSB_FIRST` in `hw_config.py`.

---

## 5. Mechanical assembly (suggested order)

1. **Print** the plate; remove brim/supports; verify hole sizes with **one** toggle and **one** button before mounting all 32.
2. **Mount toggles** from the front according to your grid labelling (keep a drawing of **which physical column is bit 0** — map via `BIT_PERM` if needed).
3. **Mount** four tactile switches for modes.
4. **Install** LED from front (diffuser optional).
5. **Solder** ’165 chain and flies to toggles; keep leads short and grouped by chip.
6. **Mount Pico** under the panel (adhesive, standoffs on a base plate, or a second printed tray — the script only cuts a **pocket**, not screw bosses).
7. **Dress** NeoPixel data wire away from clock/load lines if you see glitches.
8. **USB** through slot or side opening (not modelled by default — add in CAD or drill/file).

---

## 6. Troubleshooting

| Symptom | Things to check |
|--------|-------------------|
| Wrong bit order | `SHIFT_MSB_FIRST`, chain direction, `BIT_PERM` |
| Random flicker | power stability, long unshielded data line, clock noise near NeoPixel data |
| Always reads 0 / 255 | PL pulse polarity, clock idle level, wrong pin in `hw_config.py` |
| LED wrong colour | NeoPixel GRB order handled by library — compare pure R/G/B patterns |

---

## 7. Safety

- Double-check **power polarity** before applying USB or LED supply.
- NeoPixels can draw **surprising current** at full white — size wiring and USB supply accordingly.

---

## 8. License and disclaimer

- **Firmware** in `pico/` is under the **MIT License** — see `LICENSE` in the repo root.
- **Hardware design materials** (for example `blender/bitpanel_case.py` and meshes exported from it) are under **CERN-OHL-P-Version-2** — see `LICENSE-HARDWARE`.

**Disclaimer:** this documentation describes a **hobby project**. Building or running BitPanel is **at your own risk**. There is **no warranty**; verify wiring, component ratings, and safety for your situation.

---

When your exact switch model and pixel part numbers are fixed, update `PARAMETERS` in `bitpanel_case.py` once and re-export for a clean fit.
