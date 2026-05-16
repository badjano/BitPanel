# SPDX-License-Identifier: MIT
"""
Hardware mapping for BitPanel + Raspberry Pi Pico (MicroPython).

32 panel switches are read via four chained 74HC165 SIPO shift registers
(8 bits each, MSB or LSB first — tune SHIFT_MSB_FIRST to match your wiring).

NeoPixel: one WS2812-class LED on a single GPIO (GRB order handled by library).

Action buttons: direct GPIO with internal pull-ups, active LOW.
"""

# 74HC165 → Pico
PIN_SR_PL = 16  # parallel load (active low on 165)
PIN_SR_CP = 17  # clock
PIN_SR_DATA = 18  # serial out Q7 from last chip in chain

# WS2812 data line
PIN_NEOPIXEL = 15
NEOPIXEL_COUNT = 1

# How parallel inputs map into the 32-bit word read first → last clock pulse.
# True: first clock bit is MSB of the 32-bit word (common with some layouts).
SHIFT_MSB_FIRST = True

# Optional: remap physical switch index → logical bit index (identity = no remap).
# logical_bit_i comes from physical bit BIT_PERM[i].
BIT_PERM = tuple(range(32))

# Direct buttons (active LOW)
PIN_BTN_RANDOM = 20
PIN_BTN_ORGANIZE = 21
PIN_BTN_SHIFT_UP = 22
PIN_BTN_SHIFT_DOWN = 23

# Debouncing
DEBOUNCE_MS = 25
SHIFT_READ_DELAY_US = 2
