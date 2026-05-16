# SPDX-License-Identifier: MIT
"""Read parallel inputs from a chain of 74HC165 shift registers."""

import time
from machine import Pin

from hw_config import (
    PIN_SR_CP,
    PIN_SR_DATA,
    PIN_SR_PL,
    SHIFT_MSB_FIRST,
    SHIFT_READ_DELAY_US,
)


def _delay():
    if SHIFT_READ_DELAY_US > 0:
        time.sleep_us(SHIFT_READ_DELAY_US)


class Shift165Chain:
    def __init__(self, num_bits: int = 32):
        self._n = num_bits
        self._pl = Pin(PIN_SR_PL, Pin.OUT, value=1)
        self._cp = Pin(PIN_SR_CP, Pin.OUT, value=0)
        self._data = Pin(PIN_SR_DATA, Pin.IN)

    def read_raw(self) -> int:
        """Return unsigned word from chained registers (width ``num_bits``)."""
        self._pl.value(0)
        _delay()
        self._pl.value(1)
        _delay()

        value = 0
        for _ in range(self._n):
            self._cp.value(1)
            _delay()
            bit = self._data.value()
            self._cp.value(0)
            _delay()
            if SHIFT_MSB_FIRST:
                value = (value << 1) | bit
            else:
                value |= bit << _
        return value & ((1 << self._n) - 1)


def read_stable(chain: Shift165Chain, samples: int = 2, gap_ms: int = 5) -> int:
    """Two identical reads wins (cheap debounce for the whole word)."""
    a = chain.read_raw()
    for _ in range(samples - 1):
        time.sleep_ms(gap_ms)
        b = chain.read_raw()
        if a != b:
            a = b
    return a
