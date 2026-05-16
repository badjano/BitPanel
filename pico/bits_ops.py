# SPDX-License-Identifier: MIT
"""Bit/word helpers for RGB packing and panel modes."""

import urandom

MASK24 = 0xFFFFFF


def apply_perm(word: int, perm: tuple[int, ...]) -> int:
    """Map physical bits into logical bit positions (``perm[i]`` = physical bit index for logical bit ``i``)."""
    out = 0
    for logical_i, physical_i in enumerate(perm):
        if word >> physical_i & 1:
            out |= 1 << logical_i
    return out


def word_to_rgb(word: int) -> tuple[int, int, int]:
    w = word & MASK24
    r = w & 0xFF
    g = (w >> 8) & 0xFF
    b = (w >> 16) & 0xFF
    return r, g, b


def rgb_to_word(r: int, g: int, b: int) -> int:
    return (r & 0xFF) | ((g & 0xFF) << 8) | ((b & 0xFF) << 16)


def rol24(x: int, n: int) -> int:
    """Rotate visible RGB bits only (keeps 'color energy' on the LED)."""
    n %= 24
    x &= MASK24
    return ((x << n) | (x >> (24 - n))) & MASK24


def ror24(x: int, n: int) -> int:
    n %= 24
    x &= MASK24
    return ((x >> n) | (x << (24 - n))) & MASK24


def random_word24() -> int:
    return urandom.getrandbits(24)


def organize_quantize_rgb(word: int, step: int = 32) -> int:
    """Snap each RGB channel to nearest ladder step (feels 'tidier' on LEDs)."""

    def snap(v: int) -> int:
        v = min(255, max(0, v))
        q = (v + step // 2) // step * step
        return min(255, q)

    r, g, b = word_to_rgb(word)
    return rgb_to_word(snap(r), snap(g), snap(b))
