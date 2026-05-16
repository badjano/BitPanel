# BitPanel — web simulator

Simple browser version: **24 buttons** flip the bits of a **24-bit RGB** colour (same layout as [`pico/bits_ops.py`](../pico/bits_ops.py)).

**Play online:** [https://badjano.github.io/BitPanel/](https://badjano.github.io/BitPanel/)

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

## GitHub Pages

Pushes to `main` deploy automatically via [`.github/workflows/pages.yml`](../.github/workflows/pages.yml).  
Repo **Settings → Pages → Build and deployment** should use **GitHub Actions** (enabled on first workflow run).

← **[Project overview](../README.md)**
