# BitPanel

BitPanel is a small **open-source toy**: thirty-two toggles form a colour playground for one RGB LED, with a **Raspberry Pi Pico** (MicroPython) reading switches via shift registers and applying a few playful transforms.

This repo exists so **other people can build it**. Nothing here is sold or warranted—see **[Disclaimer](#disclaimer)** below.

## Contents

| Path | What |
|------|------|
| `pico/` | MicroPython firmware (`main.py` boots at power-on once copied to the Pico) |
| `blender/` | Parametric plate (`bitpanel_case.py`; UI or `--background` export → `blender/export/bitpanel_plate.stl`) |
| `docs/SETUP_AND_ASSEMBLY.md` | BOM-style notes, wiring concepts, firmware, assembly order |

## Quick start (builders)

Read **`docs/SETUP_AND_ASSEMBLY.md`**. Tune `pico/hw_config.py` to match how you wired the toggles and shift-register chain; tune **`PARAMETERS`** in `blender/bitpanel_case.py` to match your hardware geometry before exporting STL/3MF.

## Licensing

- **Software** (`pico/`): **[MIT License](LICENSE)**
- **Hardware design materials** (e.g. `blender/` and printed artefacts derived from them): **[CERN-OHL-P-Version-2](LICENSE-HARDWARE)** (CERN Open Hardware Licence v2 — Permissive)

SPDX:

- Software: `SPDX-License-Identifier: MIT`
- Hardware: `SPDX-License-Identifier: CERN-OHL-P-2.0`

If you redistribute adapted hardware designs, follow the notice requirements in **`LICENSE-HARDWARE`**.

## Disclaimer

**Use at your own risk.** BitPanel is **just a fun project**: hobby-grade firmware, generic mechanical assumptions, and no certification or compliance guarantees (electrical safety, EMC, eye safety from LEDs, etc.). You are responsible for how you power it, wire it, mount it, and who uses it. The authors and contributors are **not liable** for damage or injury arising from building or using this project.
