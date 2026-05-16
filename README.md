# BitPanel

BitPanel is a small **open-source toy**: toggles set a **24-bit RGB** colour (8 bits per channel) on one LED, with a **Raspberry Pi Pico** (MicroPython) reading switches via shift registers and applying a few playful transforms.

This repo exists so **other people can build it**. Nothing here is sold or warranted—see **[Disclaimer](#disclaimer)** below.

**Play in the browser:** [https://badjano.github.io/BitPanel/](https://badjano.github.io/BitPanel/) (GitHub Pages — 24-bit RGB toggles, no install).

## Documentation

| Guide | Contents |
|-------|----------|
| **[web/README.md](web/README.md)** | Browser sim — 24 toggles, flip RGB bits (no hardware) |
| **[blender/README.md](blender/README.md)** | Parametric panel plate, STL export, printing and mechanical fit-up |
| **[pico/README.md](pico/README.md)** | Wiring (shift registers, buttons, NeoPixel), firmware, bring-up |
| **[blender/export/README.md](blender/export/README.md)** | Pre-built `bitpanel_plate.stl` (optional; regenerate from the script) |

## Parts (starting point)

| Item | Notes |
|------|--------|
| Raspberry Pi Pico | MicroPython build with `neopixel` support |
| 74HC165 shift registers × 4 | Panel switch inputs (32 lines on default plate; **24 bits** drive RGB) |
| Toggles | **24** for colour (R/G/B × 8), or **32** on the default plate with eight spare / unmapped — match `BIT_PERM` in `pico/hw_config.py` |
| Tactile switches × 4 | Random / Organize / Shift up / Shift down |
| WS2812 (“NeoPixel”) LED × 1 | Or small NeoPixel PCB |
| Resistors | Pull-ups as needed (Pico has internal pulls on GPIO buttons) |
| Power | USB for Pico; NeoPixel level / voltage per your pixel datasheet |
| Fasteners | Panel screws for toggles; M3 or similar for corner holes if used |
| Wire, solder, perfboard or PCB | Optional custom PCB for shift registers |

Always measure **your** switch bushings and pixels before printing. See **[blender/README.md](blender/README.md)** for plate geometry.

## Assembly order (overview)

1. Print and dry-fit the plate — **[blender/README.md](blender/README.md)**
2. Mount toggles, mode buttons, and LED
3. Wire electronics and flash firmware — **[pico/README.md](pico/README.md)**
4. Tune `hw_config.py` and `PARAMETERS` in `bitpanel_case.py` to match your build

## Troubleshooting

| Symptom | Where to look |
|--------|----------------|
| Wrong bit order | [pico/README.md](pico/README.md) — `SHIFT_MSB_FIRST`, `BIT_PERM` |
| Random flicker / bad reads | [pico/README.md](pico/README.md) — power, wiring length, clock vs data |
| LED wrong colour | [pico/README.md](pico/README.md) — RGB packing, NeoPixel wiring |
| Holes / fit wrong | [blender/README.md](blender/README.md) — `PARAMETERS`, re-export STL |

## Safety

- Double-check **power polarity** before applying USB or LED supply.
- NeoPixels can draw **surprising current** at full white — size wiring and USB supply accordingly.

## Licensing

- **Software** (`pico/`): **[MIT License](LICENSE)**
- **Hardware design materials** (`blender/` and derivatives): **[CERN-OHL-P-Version-2](LICENSE-HARDWARE)**

SPDX: `MIT` (software), `CERN-OHL-P-2.0` (hardware). If you redistribute adapted hardware designs, follow the notice requirements in **`LICENSE-HARDWARE`**.

## Disclaimer

**Use at your own risk.** BitPanel is **just a fun project**: hobby-grade firmware, generic mechanical assumptions, and no certification or compliance guarantees (electrical safety, EMC, eye safety from LEDs, etc.). You are responsible for how you power it, wire it, mount it, and who uses it. The authors and contributors are **not liable** for damage or injury arising from building or using this project.
