# SPDX-License-Identifier: MIT
"""
BitPanel controller: panel switches → 24-bit RGB NeoPixel, plus modifier buttons.

Colour is always 24 bits (R, G, B × 8). Shift registers may read more switch
lines; only the lower 24 bits are used for the LED after mapping (see MASK24).

Modifier actions (edge-triggered):
  Random     — replace working colour with random 24-bit RGB.
  Organize   — quantize RGB channels to steps (see bits_ops.organize_quantize_rgb).
  Shift up   — rotate the 24 RGB bits left by one (wraps within color bits).
  Shift down — rotate the 24 RGB bits right by one.

Base color follows the panel when switches change; modifiers rewrite ``working``.
"""

import time
from machine import Pin

from neopixel import NeoPixel

import bits_ops as bits
from hw_config import (
    BIT_PERM,
    DEBOUNCE_MS,
    MASK24,
    NEOPIXEL_COUNT,
    PIN_BTN_ORGANIZE,
    PIN_BTN_RANDOM,
    PIN_BTN_SHIFT_DOWN,
    PIN_BTN_SHIFT_UP,
    PIN_NEOPIXEL,
)
from shift165 import Shift165Chain, read_stable


class EdgeButton:
    def __init__(self, pin_num: int):
        self._pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self._debounced = self._pin.value()
        self._last_change = time.ticks_ms()

    def pressed_edge(self) -> bool:
        """True once when the debounced line settles to pressed (LOW)."""
        now = time.ticks_ms()
        raw = self._pin.value()
        if raw != self._debounced:
            if time.ticks_diff(now, self._last_change) >= DEBOUNCE_MS:
                self._debounced = raw
                self._last_change = now
                return raw == 0
            return False
        self._last_change = now
        return False


def push_led(np: NeoPixel, word: int) -> None:
    r, g, b = bits.word_to_rgb(word)
    np[0] = (r, g, b)
    np.write()


def main() -> None:
    chain = Shift165Chain(32)
    np = NeoPixel(Pin(PIN_NEOPIXEL), NEOPIXEL_COUNT)

    btn_random = EdgeButton(PIN_BTN_RANDOM)
    btn_org = EdgeButton(PIN_BTN_ORGANIZE)
    btn_up = EdgeButton(PIN_BTN_SHIFT_UP)
    btn_dn = EdgeButton(PIN_BTN_SHIFT_DOWN)

    panel_prev = -1
    working = 0

    while True:
        raw = read_stable(chain)
        panel = bits.apply_perm(raw, BIT_PERM) & MASK24

        # Panel drives baseline whenever toggled.
        if panel != panel_prev:
            panel_prev = panel
            working = panel

        if btn_random.pressed_edge():
            working = bits.random_word24()

        if btn_org.pressed_edge():
            working = bits.organize_quantize_rgb(working) & MASK24

        if btn_up.pressed_edge():
            working = bits.rol24(working, 1)

        if btn_dn.pressed_edge():
            working = bits.ror24(working, 1)

        push_led(np, working)
        time.sleep_ms(5)


if __name__ == "__main__":
    main()
