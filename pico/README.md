# BitPanel — Pico firmware & wiring

**MicroPython** on a **Raspberry Pi Pico**: read **32** switches through **four 74HC165** shift registers, four **mode buttons** on GPIO, one **NeoPixel** for RGB output.

← **[Project overview](../README.md)** · Panel plate: **[blender/README.md](../blender/README.md)**

## Firmware files

| File | Role |
|------|------|
| `main.py` | Main loop, buttons, LED update |
| `hw_config.py` | Pins, `SHIFT_MSB_FIRST`, `BIT_PERM` |
| `shift165.py` | Parallel load + clock in 32 bits |
| `bits_ops.py` | RGB pack/unpack, random / quantize / rotate |

### Behaviour

- **Panel** sets the baseline colour when any toggle changes.
- **Random** — new random 24-bit colour.
- **Organize** — quantize each RGB channel (steps of 32).
- **Shift up / down** — rotate the **24** RGB bits (colour stays in R/G/B space).

## Wiring

### Shift registers (32 inputs, 3 Pico pins)

Four **74HC165** devices chained:

- **PL** (parallel load) — shared → `PIN_SR_PL` (default GP16), active-low load pulse.
- **CLK** — shared → `PIN_SR_CP` (GP17).
- **Serial chain**: **Q7** of chip *n* → serial **in** of chip *n+1*.
- First chip serial **in** often tied **LOW** (match `SHIFT_MSB_FIRST` in `hw_config.py`).
- **CE** / inhibit: enable shifting when clocking (often tied low).

Each ’165 latches eight toggles on **parallel load**; firmware clocks **32** edges and samples **DATA** (`shift165.py`).

**Ground**: common between Pico, registers, switches, and LED return.

**Debouncing**: simple stable double-read in firmware; add RC hardware if inputs bounce badly.

### Mode buttons (4×)

Direct GPIO, **internal pull-up**, active **LOW** (default GP20–GP23 in `hw_config.py`).

### NeoPixel

Default data **GP15**. Many pixels want **5 V** data; Pico is **3.3 V** — use a **level shifter**, a **3.3 V–tolerant** pixel, or follow your part’s datasheet. **GND** common with the Pico.

## Install firmware

1. Flash **MicroPython** for Raspberry Pi Pico from [micropython.org](https://micropython.org/download/RPI_PICO/).
2. Mount USB storage; copy all `pico/*.py` files to the Pico root (so `main.py` runs at boot).
3. Confirm **`neopixel`** is available on your build.

## Bring-up

1. Optional: comment out or limit `NeoPixel` writes until wiring is verified.
2. In **Thonny** or **rshell**, toggle one switch and inspect `read_raw()` / panel word after fixing bit order.
3. Wrong colours: adjust `BIT_PERM` / `SHIFT_MSB_FIRST`, or byte order in `bits_ops.word_to_rgb`.

## Troubleshooting

| Symptom | Things to check |
|--------|-------------------|
| Wrong bit order | `SHIFT_MSB_FIRST`, chain direction, `BIT_PERM` |
| Random flicker | Power, long data line, clock/load near NeoPixel data |
| Always 0 / 255 | PL polarity, clock idle, wrong pin in `hw_config.py` |
| LED wrong colour | GRB handled by library — test pure R, G, B patterns |

## License

Firmware in this folder is under the **[MIT License](../LICENSE)**.
