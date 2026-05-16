# Exported plate mesh

| File | Description |
|------|-------------|
| `bitpanel_plate.stl` | Plate generated from default `PARAMETERS` in [`../bitpanel_case.py`](../bitpanel_case.py) |

← **[Blender guide](../README.md)** · **[Project overview](../../README.md)**

Regenerate after changing switch spacing or hole sizes:

```bash
blender --background --factory-startup --python blender/bitpanel_case.py
```

Commit an updated STL only if you want makers to skip Blender; otherwise they can export locally.
