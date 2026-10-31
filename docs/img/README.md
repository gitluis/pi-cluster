# Images

All images in this folder are original SVGs made for this guide and are covered by the repository's MIT license. They are stored here instead of being hotlinked, so they can't break when another site moves or deletes a file.

| Folder | Contents |
| --- | --- |
| `icons/` | One header icon per page, plus two small inline icons (`router.svg`, `ethernet.svg`) |
| `diagrams/` | Larger illustrations: cluster overview, Hadoop/Spark stack, Raspbian editions, and the Raspberry Pi Imager step flows |

## Editing

- Icons and the three `imager-*.svg` step flows are generated. Change `scripts/generate_images.py`, then run `python3 scripts/generate_images.py`.
- `cluster-overview.svg`, `hadoop-spark-stack.svg` and `os-editions.svg` are hand-written SVG; edit them directly.

## Style

- Icons: 120 × 120 rounded tile, white line glyph on a 48-unit grid. Tile colour follows the section: indigo (intro), emerald (hardware), sky (operating system), violet (network), teal (cluster), rose (security), slate (extras).
- Diagrams: dark card background so they read the same in GitHub's light and dark themes.
- No third-party logos. Reference Raspberry Pi, Hadoop and Spark by name in text instead.
