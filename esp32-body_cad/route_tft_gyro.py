"""Fix J1 placement, insert net list, and route TFT + gyro copper."""
from __future__ import annotations

import math
import re
import uuid
from pathlib import Path

PCB = Path(
    r"c:\Users\rawja\OneDrive\Desktop\Desktop_Robot\esp32-body_cad\pcb and schematic\esp32-body.kicad_pcb"
)

# Board outline with 1.0 mm keep-in margin
XMIN, YMIN = 155.0, 40.0
XMAX, YMAX = 189.9, 98.3

NETS = [
    (0, ""),
    (1, "GND"),
    (2, "+3.3V"),
    (3, "/TFT_SCK"),
    (4, "/TFT_MOSI"),
    (5, "/TFT_RST"),
    (6, "/TFT_DC"),
    (7, "/I2C_SCL"),
    (8, "/I2C_SDA"),
]
BY_NAME = {n: i for i, n in NETS if n}


def uid() -> str:
    return str(uuid.uuid4())


def rot(x: float, y: float, ang: float) -> tuple[float, float]:
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    return x * c - y * s, x * s + y * c


def abs_pad(fx: float, fy: float, fr: float, px: float, py: float) -> tuple[float, float]:
    rx, ry = rot(px, py, fr)
    return round(fx + rx, 4), round(fy + ry, 4)


def seg(net: int, a: tuple[float, float], b: tuple[float, float], w: float, layer: str) -> str:
    return (
        f"\t(segment\n"
        f"\t\t(start {a[0]} {a[1]})\n"
        f"\t\t(end {b[0]} {b[1]})\n"
        f"\t\t(width {w})\n"
        f"\t\t(layer \"{layer}\")\n"
        f"\t\t(net {net})\n"
        f"\t\t(uuid \"{uid()}\")\n"
        f"\t)"
    )


def path(net: int, pts: list[tuple[float, float]], w: float, layer: str) -> list[str]:
    out = []
    for a, b in zip(pts, pts[1:]):
        out.append(seg(net, a, b, w, layer))
    return out


def clamp_pts(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(max(XMIN, min(XMAX, x)), max(YMIN, min(YMAX, y))) for x, y in pts]


# --- placements ---
# Move J1 left so pad 7 stays on board (was x=192.28, edge=190.96)
J1 = (174.0, 43.0, -90.0)
U1 = (168.92754, 72.540187, 0.0)
J2 = (187.5, 63.22, 0.0)

j1 = {i: abs_pad(*J1, 0.0, (i - 1) * 2.54) for i in range(1, 8)}
u1_local = {
    2: (-11.92754, 14.479813),
    6: (-11.92754, 4.319813),
    15: (-11.92754, -18.540187),
    16: (13.47246, 17.019813),
    17: (13.47246, 14.479813),
    19: (13.47246, 9.399813),
    24: (13.47246, -3.300187),
    26: (13.47246, -8.380187),
    29: (13.47246, -16.000187),
    30: (13.47246, -18.540187),
}
u1 = {n: abs_pad(*U1, *xy) for n, xy in u1_local.items()}
j2 = {i: abs_pad(*J2, 0.0, (i - 1) * 2.54) for i in range(1, 5)}

print("J1:", j1)
print("U1:", {k: u1[k] for k in sorted(u1)})
print("J2:", j2)
assert j1[7][0] <= XMAX, j1[7]
assert j1[1][0] >= XMIN, j1[1]

SIG, PWR = 0.25, 0.5
items: list[str] = []

# TFT_SCK U1.24 -> J1.3
items += path(
    BY_NAME["/TFT_SCK"],
    clamp_pts([u1[24], (u1[24][0], 49.0), (j1[3][0], 49.0), j1[3]]),
    SIG,
    "F.Cu",
)

# TFT_MOSI U1.30 -> J1.4
items += path(
    BY_NAME["/TFT_MOSI"],
    clamp_pts(
        [
            u1[30],
            (min(u1[30][0] + 2.0, XMAX), u1[30][1]),
            (min(u1[30][0] + 2.0, XMAX), 47.5),
            (j1[4][0], 47.5),
            j1[4],
        ]
    ),
    SIG,
    "F.Cu",
)

# TFT_RST U1.6 -> J1.5 (back copper, left then top)
items += path(
    BY_NAME["/TFT_RST"],
    clamp_pts(
        [
            u1[6],
            (156.5, u1[6][1]),
            (156.5, 45.5),
            (j1[5][0], 45.5),
            j1[5],
        ]
    ),
    SIG,
    "B.Cu",
)

# TFT_DC U1.19 -> J1.6
items += path(
    BY_NAME["/TFT_DC"],
    clamp_pts(
        [
            u1[19],
            (min(u1[19][0] + 1.8, XMAX), u1[19][1]),
            (min(u1[19][0] + 1.8, XMAX), 51.0),
            (j1[6][0], 51.0),
            j1[6],
        ]
    ),
    SIG,
    "F.Cu",
)

# I2C_SCL U1.29 -> J2.3
items += path(
    BY_NAME["/I2C_SCL"],
    clamp_pts(
        [
            u1[29],
            (min(u1[29][0] + 2.0, XMAX - 0.5), u1[29][1]),
            (min(j2[3][0] - 1.8, XMAX), u1[29][1]),
            (min(j2[3][0] - 1.8, XMAX), j2[3][1]),
            j2[3],
        ]
    ),
    SIG,
    "F.Cu",
)

# I2C_SDA U1.26 -> J2.4
items += path(
    BY_NAME["/I2C_SDA"],
    clamp_pts(
        [
            u1[26],
            (min(u1[26][0] + 2.5, XMAX - 0.5), u1[26][1]),
            (min(j2[4][0] - 2.2, XMAX), u1[26][1]),
            (min(j2[4][0] - 2.2, XMAX), j2[4][1]),
            j2[4],
        ]
    ),
    SIG,
    "F.Cu",
)

# GND: U1.17 <-> U1.2, then to J1.1 and J2.2
items += path(BY_NAME["GND"], clamp_pts([u1[17], (u1[17][0], u1[2][1]), u1[2]]), PWR, "B.Cu")
items += path(
    BY_NAME["GND"],
    clamp_pts(
        [
            u1[2],
            (156.5, u1[2][1]),
            (156.5, j1[1][1]),
            j1[1],
        ]
    ),
    PWR,
    "B.Cu",
)
items += path(
    BY_NAME["GND"],
    clamp_pts(
        [
            u1[17],
            (min(j2[2][0] - 1.8, XMAX), u1[17][1]),
            (min(j2[2][0] - 1.8, XMAX), j2[2][1]),
            j2[2],
        ]
    ),
    PWR,
    "F.Cu",
)

# +3.3V: U1.16 -> J2.1, J1.7/J1.2, and EN (U1.15)
items += path(
    BY_NAME["+3.3V"],
    clamp_pts(
        [
            u1[16],
            (min(j2[1][0] - 1.8, XMAX), u1[16][1]),
            (min(j2[1][0] - 1.8, XMAX), j2[1][1]),
            j2[1],
        ]
    ),
    PWR,
    "F.Cu",
)
items += path(
    BY_NAME["+3.3V"],
    clamp_pts(
        [
            u1[16],
            (min(u1[16][0] + 1.2, XMAX), u1[16][1]),
            (min(u1[16][0] + 1.2, XMAX), 44.8),
            (j1[7][0], 44.8),
            j1[7],
        ]
    ),
    PWR,
    "F.Cu",
)
items += path(BY_NAME["+3.3V"], clamp_pts([j1[7], (j1[2][0], j1[7][1]), j1[2]]), PWR, "F.Cu")
items += path(
    BY_NAME["+3.3V"],
    clamp_pts(
        [
            u1[15],
            (156.5, u1[15][1]),
            (156.5, 96.5),
            (min(u1[16][0] + 2.0, XMAX), 96.5),
            (min(u1[16][0] + 2.0, XMAX), u1[16][1]),
            u1[16],
        ]
    ),
    PWR,
    "B.Cu",
)

text = PCB.read_text(encoding="utf-8")

# Move J1 footprint
text = text.replace("(at 177.04 43 -90)", "(at 174.0 43 -90)", 1)

# Normalize any previous net numbering back to names, then apply final numbering
# First strip numeric form (net N "name") -> (net "name")
text = re.sub(r'\(net \d+ "([^"]+)"\)', r'(net "\1")', text)
# Fix U1 pad 17 GND if still unconnected
text = text.replace('(net "unconnected-(U1-GND-Pad17)")', '(net "GND")')
text = text.replace('(pintype "power_in+no_connect")', '(pintype "power_in")')

# Apply final net numbers for known nets
for name, num in BY_NAME.items():
    text = text.replace(f'(net "{name}")', f'(net {num} "{name}")')

# Remove existing net list if present
text = re.sub(r'(?:\t\(net \d+ "[^"]*"\)\n)+', "", text)

# Insert net list before first footprint
net_block = "".join(f'\t(net {n} "{name}")\n' for n, name in NETS)
marker = '\t(footprint "Connector_PinSocket_2.54mm:PinSocket_1x07_P2.54mm_Vertical"'
if marker not in text:
    raise SystemExit("footprint marker missing")
text = text.replace(marker, net_block + marker, 1)

# Strip old segments/vias before Edge.Cuts
edge = "\t(gr_rect\n\t\t(start 154 38.980514)"
if edge not in text:
    raise SystemExit("edge cuts missing")
idx = text.index(edge)
prefix, suffix = text[:idx], text[idx:]
prefix = re.sub(r"(?:\t\(segment\n(?:.*?\n)*?\t\)\n)+", "", prefix)
prefix = re.sub(r"(?:\t\(via\n(?:.*?\n)*?\t\)\n)+", "", prefix)
# also clean leftover blank lines at end of prefix
prefix = prefix.rstrip() + "\n"

route = "\n".join(items) + "\n"
PCB.write_text(prefix + route + suffix, encoding="utf-8")
print(f"OK: moved J1, wrote {len(items)} segments")
