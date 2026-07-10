"""Re-add J3/J4 servo male headers + routes. Safe for KiCad name-based nets."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

PCB = Path(
    r"c:\Users\rawja\OneDrive\Desktop\Desktop_Robot\esp32-body_cad\pcb and schematic\esp32-body.kicad_pcb"
)
BACKUP = PCB.with_suffix(".kicad_pcb.bak_before_servos")


def uid() -> str:
    return str(uuid.uuid4())


def seg(net: str, a, b, w: float, layer: str) -> str:
    return (
        f"\t(segment\n"
        f"\t\t(start {a[0]} {a[1]})\n"
        f"\t\t(end {b[0]} {b[1]})\n"
        f"\t\t(width {w})\n"
        f"\t\t(layer \"{layer}\")\n"
        f"\t\t(net \"{net}\")\n"
        f"\t\t(uuid \"{uid()}\")\n"
        f"\t)"
    )


def path(net: str, pts, w: float, layer: str) -> list[str]:
    out = []
    for a, b in zip(pts, pts[1:]):
        if a != b:
            out.append(seg(net, a, b, w, layer))
    return out


def header_fp(ref: str, value: str, path_uuid: str, x: float, y: float, nets: list[str]) -> str:
    pads = []
    shapes = ["rect", "oval", "oval"]
    for i, (net, shape) in enumerate(zip(nets, shapes), start=1):
        py = (i - 1) * 2.54
        pads.append(
            f'''\t\t(pad "{i}" thru_hole {shape}
\t\t\t(at 0 {py})
\t\t\t(size 1.7 1.7)
\t\t\t(drill 1)
\t\t\t(layers "*.Cu" "*.Mask")
\t\t\t(remove_unused_layers no)
\t\t\t(net "{net}")
\t\t\t(pintype "passive")
\t\t\t(uuid "{uid()}")
\t\t)'''
        )
    pads_txt = "\n".join(pads)
    return f'''\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"
\t\t(layer "F.Cu")
\t\t(uuid "{uid()}")
\t\t(at {x} {y})
\t\t(descr "Through hole straight pin header, 1x03, 2.54mm pitch, single row")
\t\t(tags "Through hole pin header THT 1x03 2.54mm single row")
\t\t(path "/{path_uuid}")
\t\t(sheetname "/")
\t\t(sheetfile "esp32-body.kicad_sch")
\t\t(property "Reference" "{ref}"
\t\t\t(at 0 -2.33)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1 1)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at 0 7.41)
\t\t\t(layer "F.Fab")
\t\t\t(uuid "{uid()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1 1)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(attr through_hole)
\t\t(fp_line
\t\t\t(start -1.33 1.27)
\t\t\t(end -1.33 6.41)
\t\t\t(stroke (width 0.12) (type solid))
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start -1.33 1.27)
\t\t\t(end 1.33 1.27)
\t\t\t(stroke (width 0.12) (type solid))
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start -1.33 6.41)
\t\t\t(end 1.33 6.41)
\t\t\t(stroke (width 0.12) (type solid))
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start 1.33 1.27)
\t\t\t(end 1.33 6.41)
\t\t\t(stroke (width 0.12) (type solid))
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start -1.33 0)
\t\t\t(end -1.33 -1.33)
\t\t\t(stroke (width 0.12) (type solid))
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start -1.33 -1.33)
\t\t\t(end 0 -1.33)
\t\t\t(stroke (width 0.12) (type solid))
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_rect
\t\t\t(start -1.8 -1.8)
\t\t\t(end 1.8 6.85)
\t\t\t(stroke (width 0.05) (type default))
\t\t\t(fill no)
\t\t\t(layer "F.CrtYd")
\t\t\t(uuid "{uid()}")
\t\t)
{pads_txt}
\t\t(embedded_fonts no)
\t\t(model "${{KICAD10_3DMODEL_DIR}}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x03_P2.54mm_Vertical.step"
\t\t\t(offset (xyz 0 0 0))
\t\t\t(scale (xyz 1 1 1))
\t\t\t(rotate (xyz 0 0 0))
\t\t)
\t)
'''


text = PCB.read_text(encoding="utf-8")
BACKUP.write_text(text, encoding="utf-8")
print("Backup:", BACKUP)

# Remove old PinHeader_1x03 if any
text = re.sub(
    r'\t\(footprint "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"[\s\S]*?\n\t\)\n',
    "",
    text,
)

# Assign U1 nets
for old, new in [
    ('(net "unconnected-(U1-VIN-Pad1)")', '(net "+5V")'),
    ('(net "unconnected-(U1-GPIO33-Pad9)")', '(net "/SERVO2")'),
    ('(net "unconnected-(U1-GPIO32-Pad10)")', '(net "/SERVO1")'),
    ('(net "unconnected-(U1-GND-Pad17)")', '(net "GND")'),
]:
    if old in text:
        text = text.replace(old, new, 1)
        print("pad net:", new)
    elif new in text:
        print("already:", new)
    else:
        print("WARN missing:", old)

J3 = (158.5, 91.0)
J4 = (165.0, 91.0)
fps = header_fp(
    "J3", "SERVO1", "af634168-65ad-4845-8390-6b38a8128340", *J3, ["GND", "+5V", "/SERVO1"]
)
fps += header_fp(
    "J4", "SERVO2", "d330271a-3ffe-4c54-81fb-b5e1a28daf97", *J4, ["GND", "+5V", "/SERVO2"]
)

edge = "\t(gr_rect\n\t\t(start 154 38.980514)"
if edge not in text:
    raise SystemExit("Edge.Cuts not found")
text = text.replace(edge, fps + edge, 1)

# Remove previous servo routes
for net in ("/SERVO1", "/SERVO2", "+5V"):
    text = re.sub(
        rf"\t\(segment\n"
        rf"\t\t\(start [^\n]+\)\n"
        rf"\t\t\(end [^\n]+\)\n"
        rf"\t\t\(width [^\n]+\)\n"
        rf"\t\t\(layer \"[^\"]+\"\)\n"
        rf"\t\t\(net \"{re.escape(net)}\"\)\n"
        rf"\t\t\(uuid \"[^\"]+\"\)\n"
        rf"\t\)\n?",
        "",
        text,
    )

j3 = {1: (J3[0], J3[1]), 2: (J3[0], J3[1] + 2.54), 3: (J3[0], J3[1] + 5.08)}
j4 = {1: (J4[0], J4[1]), 2: (J4[0], J4[1] + 2.54), 3: (J4[0], J4[1] + 5.08)}
u1_10, u1_9, u1_1, u1_2, u1_17 = (
    (157.0, 66.7),
    (157.0, 69.24),
    (157.0, 89.56),
    (157.0, 87.02),
    (182.4, 87.02),
)

items: list[str] = []
SIG, PWR = 0.25, 0.5
items += path("/SERVO1", [u1_10, (156.5, u1_10[1]), (156.5, j3[3][1]), j3[3]], SIG, "F.Cu")
items += path(
    "/SERVO2",
    [u1_9, (155.8, u1_9[1]), (155.8, 97.5), (j4[3][0], 97.5), j4[3]],
    SIG,
    "B.Cu",
)
items += path("GND", [j3[1], (j3[1][0], u1_2[1]), u1_2], PWR, "F.Cu")
items += path("GND", [j4[1], (j3[1][0], j4[1][1]), j3[1]], PWR, "F.Cu")
# only add U1.17 GND if not already connected somehow - additive is fine
items += path("GND", [u1_17, u1_2], PWR, "B.Cu")
items += path("+5V", [u1_1, (156.5, u1_1[1]), (156.5, j3[2][1]), j3[2]], PWR, "B.Cu")
items += path("+5V", [j3[2], (j4[2][0], j3[2][1]), j4[2]], PWR, "F.Cu")

# Insert segments before final embedded_fonts / )
text = re.sub(r"\n\t\(embedded_fonts no\)\n\)\s*\Z", "\n", text)
text = text.rstrip() + "\n" + "\n".join(items) + "\n\t(embedded_fonts no)\n)\n"

PCB.write_text(text, encoding="utf-8")

final = PCB.read_text(encoding="utf-8")
print("J3:", '(property "Reference" "J3"' in final)
print("J4:", '(property "Reference" "J4"' in final)
print("SERVO1 refs:", final.count('"/SERVO1"'))
print("SERVO2 refs:", final.count('"/SERVO2"'))
print("+5V refs:", final.count('"+5V"'))
print("segments:", final.count("(segment"))
print("OK — close KiCad WITHOUT saving, then reopen this file")
