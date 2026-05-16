# BitPanel — web simulator

Simple browser version: **24 buttons** flip the bits of a **24-bit RGB** colour (same layout as [`pico/bits_ops.py`](../pico/bits_ops.py)).

| Bit index | Channel |
|-----------|---------|
| 0–7 | Red |
| 8–15 | Green |
| 16–23 | Blue |

## Run locally

ES modules need a local server (opening `index.html` as `file://` may block imports).

```bash
cd web
python -m http.server 8080
```

Then open **http://localhost:8080/**

## Deploy

Host the `web/` folder on any static host (GitHub Pages, Netlify, etc.). No build step.

← **[Project overview](../README.md)**
