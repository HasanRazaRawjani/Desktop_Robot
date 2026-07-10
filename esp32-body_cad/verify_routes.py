"""Final verification of TFT+gyro routing."""
from __future__ import annotations

import math
import re
from pathlib import Path

PCB = Path(
    r"c:\Users\rawja\OneDrive\Desktop\Desktop_Robot\esp32-body_cad\pcb and schematic\esp32-body.kicad_pcb"
)
text = PCB.read_text(encoding="utf-8")

# Check J1 position and pad 7 on board
assert "(at 174.0 43 -90)" in text, "J1 not moved"
assert text.count("(segment") >= 40, text.count("(segment")

# Pads that must have nets
must = [
    ('J1', '1', 'GND'),
    ('J1', '7', '+3.3V'),
    ('J2', '1', '+3.3V'),
    ('J2', '4', '/I2C_SDA'),
    ('U1', '17', 'GND'),
    ('U1', '24', '/TFT_SCK'),
    ('U1', '30', '/TFT_MOSI'),
]

# Extract footprints
fps = {}
for name, key in [
    ("PinSocket_1x07", "J1"),
    ("ESP32_30pin", "U1"),
    ("PinSocket_1x08", "J2"),
]:
    m = re.search(rf'\(footprint "[^"]*{name}[^"]*".*?(?=\n\t\(footprint |\n\t\(segment |\n\t\(gr_rect )', text, re.S)
    fps[key] = m.group(0) if m else ""

for ref, pad, net in must:
    block = fps[ref]
    pm = re.search(rf'\(pad "{pad}".*?\(net ([^\n]+)\)', block, re.S)
    got = pm.group(1) if pm else "MISSING"
    ok = net in got
    print(f"{ref}.{pad} expect {net}: {got} {'OK' if ok else 'FAIL'}")

# Check no segment outside board roughly
XMIN, YMIN, XMAX, YMAX = 153.5, 38.5, 191.5, 99.8
bad = 0
for m in re.finditer(r"\(start ([0-9.]+) ([0-9.]+)\)\n\t\t\(end ([0-9.]+) ([0-9.]+)\)", text):
    xs = [float(m.group(1)), float(m.group(3))]
    ys = [float(m.group(2)), float(m.group(4))]
    if min(xs) < XMIN or max(xs) > XMAX or min(ys) < YMIN or max(ys) > YMAX:
        bad += 1
        print("OUT:", m.groups())
print("segments:", text.count("(segment"), "out-of-board:", bad)

# Check for short across J1 y=43 between different nets - look for long horizontal at y=43
for m in re.finditer(r"\(start ([0-9.]+) 43\.0\)\n\t\t\(end ([0-9.]+) 43\.0\)", text):
    x1, x2 = float(m.group(1)), float(m.group(2))
    if abs(x1 - x2) > 3:
        print("WARN long run on y=43:", x1, x2)
print("done")
