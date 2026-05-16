// SPDX-License-Identifier: MIT
/** 24-bit RGB helpers (same layout as pico/bits_ops.py). */

const MASK24 = 0xffffff;

export function wordToRgb(word) {
  const w = word & MASK24;
  return { r: w & 0xff, g: (w >> 8) & 0xff, b: (w >> 16) & 0xff };
}

export function rgbToWord(r, g, b) {
  return (r & 0xff) | ((g & 0xff) << 8) | ((b & 0xff) << 16);
}

export function rgbToHex(r, g, b) {
  const n = rgbToWord(r, g, b);
  return "#" + n.toString(16).padStart(6, "0");
}

/** Bit index 0–7 = R, 8–15 = G, 16–23 = B */
export function channelBitIndex(bit) {
  return bit % 8;
}
