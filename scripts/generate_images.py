#!/usr/bin/env python3
"""Generate the page icons (docs/img/icons/) and step-flow diagrams (docs/img/diagrams/).

Every icon is a rounded tile in its section colour with a white line glyph.
Glyphs are drawn on a 48 x 48 grid and scaled into a 120 x 120 tile.

    python3 scripts/generate_images.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "img" / "icons"

# section colours (work on both light and dark GitHub themes)
INTRO = ("#6366F1", "#4338CA")     # indigo
HARDWARE = ("#10B981", "#047857")  # emerald
OS = ("#0EA5E9", "#0369A1")        # sky
NETWORK = ("#8B5CF6", "#6D28D9")   # violet
CLUSTER = ("#14B8A6", "#0F766E")   # teal
SECURITY = ("#F43F5E", "#BE123C")  # rose
EXTRA = ("#64748B", "#334155")     # slate

# small reusable shapes (48-unit grid)
SD_CARD = "<path d='M15 5h16l6 6v31a2 2 0 0 1-2 2H15a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z'/>"
SD_PINS = "<path d='M19 9v6M24 9v6M29 9v6'/>"
ARROW_HEAD = "stroke-linejoin='round'"

GLYPHS = {
    # --- intro ---
    "purpose": (INTRO, "Target", """
        <circle cx='22' cy='26' r='16'/><circle cx='22' cy='26' r='9'/>
        <circle cx='22' cy='26' r='2.5' fill='#fff'/>
        <path d='M22 26L40 8M33 8h7v7'/>"""),
    "background": (INTRO, "Open book", """
        <path d='M24 13c-5-4-12-5-18-3v28c6-2 13-1 18 3 5-4 12-5 18-3V10c-6-2-13-1-18 3z'/>
        <path d='M24 13v28'/>"""),
    "getting-started": (INTRO, "Flag", """
        <path d='M12 43V6'/>
        <path d='M12 8h25l-6 8 6 8H12'/>"""),
    "cluster": (CLUSTER, "Stacked boards", """
        <rect x='7' y='7' width='34' height='9' rx='2'/>
        <rect x='7' y='20' width='34' height='9' rx='2'/>
        <rect x='7' y='33' width='34' height='9' rx='2'/>
        <circle cx='35' cy='11.5' r='1.6' fill='#fff' stroke='none'/>
        <circle cx='35' cy='24.5' r='1.6' fill='#fff' stroke='none'/>
        <circle cx='35' cy='37.5' r='1.6' fill='#fff' stroke='none'/>
        <path d='M12 11.5h10M12 24.5h10M12 37.5h10'/>"""),
    # --- hardware ---
    "hardware": (HARDWARE, "Circuit board", """
        <rect x='5' y='9' width='38' height='30' rx='3'/>
        <rect x='17' y='18' width='13' height='13' rx='1.5'/>
        <path d='M20 18v-3M24 18v-3M28 18v-3M20 31v3M24 31v3M28 31v3'/>
        <path d='M9 13h30' stroke-dasharray='1.5 2.5'/>
        <circle cx='9' cy='35' r='1.5' fill='#fff' stroke='none'/>
        <circle cx='39' cy='35' r='1.5' fill='#fff' stroke='none'/>"""),
    "hardware-list": (HARDWARE, "Checklist", """
        <rect x='10' y='8' width='28' height='35' rx='3'/>
        <rect x='18' y='5' width='12' height='6' rx='2'/>
        <path d='M15 21l3 3 5-6M27 21h6M15 32l3 3 5-6M27 32h6' """ + ARROW_HEAD + """/>"""),
    # --- operating system ---
    "software": (OS, "Application window", """
        <rect x='5' y='8' width='38' height='32' rx='3'/>
        <path d='M5 16h38'/>
        <circle cx='10' cy='12' r='1.3' fill='#fff' stroke='none'/>
        <circle cx='14.5' cy='12' r='1.3' fill='#fff' stroke='none'/>
        <rect x='11' y='22' width='11' height='7' rx='1.5'/>
        <rect x='26' y='22' width='11' height='7' rx='1.5'/>
        <path d='M11 34h26'/>"""),
    "format-sd-card": (OS, "SD card with check mark", SD_CARD + SD_PINS + """
        <path d='M18 29l4 4 8-9' """ + ARROW_HEAD + """/>"""),
    "read-write-images": (OS, "SD card with read and write arrows", """
        <path d='M7 9h11l4 4v24a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V11a2 2 0 0 1 2-2z'/>
        <path d='M10 13v4M15 13v4'/>
        <path d='M27 19h15M37 14l5 5-5 5M42 31H27M32 26l-5 5 5 5' """ + ARROW_HEAD + """/>"""),
    "installer": (OS, "Download arrow", """
        <path d='M24 6v24M15 21l9 9 9-9' """ + ARROW_HEAD + """/>
        <path d='M8 30v9a2 2 0 0 0 2 2h28a2 2 0 0 0 2-2v-9'/>"""),
    "install-os": (OS, "SD card with install arrow", SD_CARD + SD_PINS + """
        <path d='M25 21v13M20 29l5 5 5-5' """ + ARROW_HEAD + """/>"""),
    "install-many": (OS, "Stack of SD cards", """
        <path d='M21 4h14l5 5v25a2 2 0 0 1-2 2'/>
        <path d='M16 9h14l5 5v25a2 2 0 0 1-2 2'/>
        <path d='M11 14h14l5 5v23a2 2 0 0 1-2 2H11a2 2 0 0 1-2-2V16a2 2 0 0 1 2-2z'/>
        <path d='M14 18v5M18.5 18v5M23 18v5'/>"""),
    "clone": (OS, "Copy", """
        <rect x='16' y='16' width='26' height='26' rx='3'/>
        <path d='M32 16v-7a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v21a2 2 0 0 0 2 2h7'/>
        <path d='M29 23v12M23 29h12'/>"""),
    "updates": (OS, "Refresh arrows", """
        <path d='M39 20A16 16 0 0 0 10 17'/><path d='M9 9v8h8' """ + ARROW_HEAD + """/>
        <path d='M9 28a16 16 0 0 0 29 3'/><path d='M39 39v-8h-8' """ + ARROW_HEAD + """/>"""),
    "desktop": (EXTRA, "Monitor", """
        <rect x='5' y='7' width='38' height='26' rx='3'/>
        <path d='M17 42h14M24 33v9'/>
        <path d='M5 27h38'/>"""),
    # --- network ---
    "internet": (NETWORK, "Globe", """
        <circle cx='24' cy='24' r='18'/>
        <ellipse cx='24' cy='24' rx='8' ry='18'/>
        <path d='M7 18h34M7 30h34'/>"""),
    "netplan": (NETWORK, "Configuration file", """
        <path d='M12 5h17l9 9v27a2 2 0 0 1-2 2H12a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z'/>
        <path d='M29 5v9h9'/>
        <path d='M16 21h10M20 27h12M20 33h8M16 39h6'/>"""),
    "pi-network": (NETWORK, "Network topology", """
        <circle cx='24' cy='10' r='5.5'/>
        <circle cx='6' cy='38' r='3.5'/><circle cx='18' cy='38' r='3.5'/>
        <circle cx='30' cy='38' r='3.5'/><circle cx='42' cy='38' r='3.5'/>
        <path d='M24 15.5v8.5M6 34.5V24h36v10.5M18 34.5V24M30 34.5V24'/>"""),
    # --- cluster ---
    "cluster-commands": (CLUSTER, "Terminal prompt", """
        <rect x='5' y='8' width='38' height='32' rx='3'/>
        <path d='M12 19l7 5-7 5' """ + ARROW_HEAD + """/>
        <path d='M23 31h13'/>"""),
    "security": (SECURITY, "Shield with check mark", """
        <path d='M24 4l16 6v12c0 10-7 18-16 22C15 40 8 32 8 22V10z' """ + ARROW_HEAD + """/>
        <path d='M17 24l5 5 9-10' """ + ARROW_HEAD + """/>"""),
    # --- extras ---
    "miscellaneous": (EXTRA, "Light bulb", """
        <path d='M18 33c-4-3-7-7-7-13a13 13 0 0 1 26 0c0 6-3 10-7 13z'/>
        <path d='M19 38h10M21 43h6'/>"""),
    "references": (EXTRA, "Bookmark", """
        <path d='M14 5h20a2 2 0 0 1 2 2v36l-12-9-12 9V7a2 2 0 0 1 2-2z' """ + ARROW_HEAD + """/>
        <path d='M19 14h10M19 20h7'/>"""),
}

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect width="120" height="120" rx="28" fill="url(#g)"/>
  <rect x="1.5" y="1.5" width="117" height="117" rx="26.5" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="3"/>
  <g transform="translate(24 24) scale(1.5)" fill="none" stroke="#fff" stroke-width="3"
     stroke-linecap="round" stroke-linejoin="round">{glyph}
  </g>
</svg>
"""

# tiny inline icons (no tile) for requirement lists
INLINE = {
    "router": ("Router", """
        <rect x='4' y='26' width='40' height='14' rx='3'/>
        <path d='M14 26V12M34 26V12'/>
        <circle cx='12' cy='33' r='1.5' fill='currentColor' stroke='none'/>
        <circle cx='18' cy='33' r='1.5' fill='currentColor' stroke='none'/>
        <path d='M26 33h12'/>"""),
    "ethernet": ("Ethernet cable", """
        <path d='M14 6h20v18l-4 4H18l-4-4z'/>
        <path d='M19 6v6M24 6v6M29 6v6'/>
        <path d='M24 28v8c0 4 4 6 8 6h10'/>"""),
}

INLINE_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" role="img" aria-label="{label}">
  <style>g{{color:#334155}} @media (prefers-color-scheme: dark){{g{{color:#CBD5E1}}}}</style>
  <g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{glyph}
  </g>
</svg>
"""


# --------------------------------------------------------------------------- #
# Step-flow diagrams (replace the old Raspberry Pi Imager screenshots)
# --------------------------------------------------------------------------- #

DIAGRAMS = OUT.parent / "diagrams"

STEP_GLYPHS = {
    "card": SD_CARD + SD_PINS,
    "app": "<rect x='5' y='8' width='38' height='32' rx='3'/><path d='M5 16h38'/>"
           "<circle cx='10' cy='12' r='1.3' fill='#fff' stroke='none'/>"
           "<circle cx='14.5' cy='12' r='1.3' fill='#fff' stroke='none'/><path d='M12 25h24M12 32h16'/>",
    "os": "<rect x='5' y='8' width='38' height='26' rx='3'/><path d='M17 42h14M24 34v8'/>"
          "<path d='M12 17l6 4-6 4M21 27h9'/>",
    "erase": "<path d='M9 33l17-17a3 3 0 0 1 4 0l9 9a3 3 0 0 1 0 4L27 41H17z'/><path d='M19 23l13 13'/><path d='M27 41h14'/>",
    "file": "<path d='M12 5h17l9 9v27a2 2 0 0 1-2 2H12a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z'/><path d='M29 5v9h9'/>"
            "<path d='M16 29h16M16 35h10'/>",
    "pick": SD_CARD + SD_PINS + "<circle cx='25' cy='29' r='6'/><path d='M29.5 33.5l5 5'/>",
    "write": "<path d='M24 6v22M16 20l8 8 8-8'/><path d='M8 30v9a2 2 0 0 0 2 2h28a2 2 0 0 0 2-2v-9'/>",
    "done": "<circle cx='24' cy='24' r='18'/><path d='M16 24l6 6 11-12'/>",
}

FLOWS = {
    "imager-format-sd-card": (
        "Format a microSD card with Raspberry Pi Imager",
        [("card", "Insert card", "into your computer"),
         ("app", "Open Imager", "Raspberry Pi Imager"),
         ("erase", "Choose OS", "select Erase"),
         ("pick", "Choose storage", "your microSD card"),
         ("done", "Write", "card is formatted")]),
    "imager-install-os": (
        "Install Raspbian (Raspberry Pi OS) with Raspberry Pi Imager",
        [("app", "Open Imager", "Raspberry Pi Imager"),
         ("os", "Choose OS", "Raspbian / Lite / Full"),
         ("pick", "Choose storage", "your microSD card"),
         ("write", "Write", "image is written"),
         ("done", "Verify", "card is checked")]),
    "imager-write-custom-image": (
        "Write your own image with Raspberry Pi Imager",
        [("app", "Open Imager", "Raspberry Pi Imager"),
         ("os", "Choose OS", "select Use custom"),
         ("file", "Pick the image", ".img .zip .gz .xz"),
         ("pick", "Choose storage", "your microSD card"),
         ("done", "Write", "written and verified")]),
}

FLOW_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 280" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0F172A"/><stop offset="1" stop-color="#1E293B"/>
    </linearGradient>
  </defs>
  <rect width="880" height="280" rx="24" fill="url(#bg)"/>
  <g font-family="-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="40" y="54" fill="#F8FAFC" font-size="22" font-weight="700">{title}</text>
{steps}
  </g>
</svg>
"""

STEP_TEMPLATE = """    <g transform="translate({x} 82)">
      <rect width="140" height="160" rx="16" fill="#0B1220" stroke="#334155"/>
      <circle cx="24" cy="24" r="13" fill="#0EA5E9"/>
      <text x="24" y="29" fill="#fff" font-size="14" font-weight="700" text-anchor="middle">{n}</text>
      <g transform="translate(46 30)" fill="none" stroke="#7DD3FC" stroke-width="3"
         stroke-linecap="round" stroke-linejoin="round">{glyph}</g>
      <text x="70" y="118" fill="#F8FAFC" font-size="15" font-weight="700" text-anchor="middle">{label}</text>
      <text x="70" y="140" fill="#94A3B8" font-size="12.5" text-anchor="middle">{sub}</text>
    </g>"""

ARROW = """    <path d="M{x1} 162h12M{x2} 157l5 5-5 5" fill="none" stroke="#475569" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round"/>"""


def flow_svg(title, steps):
    parts = []
    x0, w, gap = 40, 140, 25
    for i, (glyph, label, sub) in enumerate(steps):
        x = x0 + i * (w + gap)
        parts.append(STEP_TEMPLATE.format(x=x, n=i + 1, glyph=STEP_GLYPHS[glyph].replace("#fff", "#7DD3FC"),
                                          label=label, sub=sub))
        if i < len(steps) - 1:
            ax = x + w + 6
            parts.append(ARROW.format(x1=ax, x2=ax + 7))
    alt = title + ": " + ", then ".join(f"{label} ({sub})" for _, label, sub in steps)
    return FLOW_TEMPLATE.format(label=alt, title=title, steps="\n".join(parts))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    for name, ((c1, c2), label, glyph) in GLYPHS.items():
        (OUT / f"{name}.svg").write_text(TEMPLATE.format(label=label, c1=c1, c2=c2, glyph=glyph))
    for name, (label, glyph) in INLINE.items():
        (OUT / f"{name}.svg").write_text(INLINE_TEMPLATE.format(label=label, glyph=glyph))
    for name, (title, steps) in FLOWS.items():
        (DIAGRAMS / f"{name}.svg").write_text(flow_svg(title, steps))
    print(f"wrote {len(GLYPHS) + len(INLINE)} icons and {len(FLOWS)} flow diagrams")


if __name__ == "__main__":
    main()
