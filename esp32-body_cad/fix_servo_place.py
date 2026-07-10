"""Nudge J3/J4 up so courtyard fits inside board edge; re-route."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

PCB = Path(
    r"c:\Users\rawja\OneDrive\Desktop\Desktop_Robot\esp32-body_cad\pcb and schematic\esp32-body.kicad_pcb"
)


def uid() -> str:
    return str(uuid.uuid4())


def seg(net, a, b, w, layer):
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


def path(net, pts, w, layer):
    out = []
    for a, b in zip(pts, pts[1:]):
        if a != b:
            out.append(seg(net, a, b, w, layer))
    return out


text = PCB.read_text(encoding="utf-8")

# Move footprints
text = text.replace("(at 158.5 92.5 0.0)", "(at 158.5 91.0 0)", 1)
text = text.replace("(at 165.0 92.5 0.0)", "(at 165.0 91.0 0)", 1)

# Strip old servo net segments
for n in (9, 10, 11):
    text = re.sub(
        rf"\t\(segment\n"
        rf"\t\t\(start [^\n]+\)\n"
        rf"\t\t\(end [^\n]+\)\n"
        rf"\t\t\(width [^\n]+\)\n"
        rf"\t\t\(layer \"[^\"]+\"\)\n"
        rf"\t\t\(net {n}\)\n"
        rf"\t\t\(uuid \"[^\"]+\"\)\n"
        rf"\t\)\n?",
        "",
        text,
    )
# Also strip GND segments we added that go to J3/J4 specifically - harder.
# Re-add all servo-related routes including GND stubs.

J3 = (158.5, 91.0)
J4 = (165.0, 91.0)
j3 = {1: (J3[0], J3[1]), 2: (J3[0], J3[1] + 2.54), 3: (J3[0], J3[1] + 5.08)}
j4 = {1: (J4[0], J4[1]), 2: (J4[0], J4[1] + 2.54), 3: (J4[0], J4[1] + 5.08)}
u1_10 = (157.0, 66.7)
u1_9 = (157.0, 69.24)
u1_1 = (157.0, 89.56)
u1_2 = (157.0, 87.02)

items = []
SIG, PWR = 0.25, 0.5

items += path(9, [u1_10, (156.5, u1_10[1]), (156.5, j3[3][1]), j3[3]], SIG, "F.Cu")
items += path(
    10,
    [u1_9, (155.8, u1_9[1]), (155.8, 97.5), (j4[3][0], 97.5), j4[3]],
    SIG,
    "B.Cu",
)
items += path(1, [j3[1], (j3[1][0], u1_2[1]), u1_2], PWR, "F.Cu")
items += path(1, [j4[1], (j3[1][0], j4[1][1]), j3[1]], PWR, "F.Cu")
items += path(11, [u1_1, (156.5, u1_1[1]), (156.5, j3[2][1]), j3[2]], PWR, "B.Cu")
items += path(11, [j3[2], (j4[2][0], j3[2][1]), j4[2]], PWR, "F.Cu")

print("J3 pad3 y=", j3[3][1], "board max ~99.3")
print("courtyard end y=", J3[1] + 6.85)

edge = "\t(gr_rect\n\t\t(start 154 38.980514)"
text = text.replace(edge, "\n".join(items) + "\n" + edge, 1)
PCB.write_text(text, encoding="utf-8")
print(f"Updated: {len(items)} servo segments")
