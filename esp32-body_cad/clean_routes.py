"""Clean zero-length segments and verify TFT/gyro routing."""
from __future__ import annotations

import re
from pathlib import Path

PCB = Path(
    r"c:\Users\rawja\OneDrive\Desktop\Desktop_Robot\esp32-body_cad\pcb and schematic\esp32-body.kicad_pcb"
)
text = PCB.read_text(encoding="utf-8")

# Remove zero-length segments
pattern = re.compile(
    r"\t\(segment\n"
    r"\t\t\(start ([0-9.]+) ([0-9.]+)\)\n"
    r"\t\t\(end \1 \2\)\n"
    r"\t\t\(width [0-9.]+\)\n"
    r"\t\t\(layer \"[^\"]+\"\)\n"
    r"\t\t\(net \d+\)\n"
    r"\t\t\(uuid \"[^\"]+\"\)\n"
    r"\t\)\n?",
)
text2, n = pattern.subn("", text)
print(f"Removed {n} zero-length segments")

# Sanity checks
checks = {
    "J1 moved": '(at 174.0 43 -90)' in text2,
    "net list": '(net 1 "GND")' in text2,
    "U1.17 GND": False,
    "segments": text2.count("(segment") ,
}
# Find pad 17 net
m = re.search(
    r'\(pad "17".*?\(net ([^\n]+)\)',
    text2,
    re.S,
)
if m:
    checks["U1.17 GND"] = 'GND' in m.group(1)
    print("U1.17 net:", m.group(1))

# Count segments per net
for net in range(1, 9):
    c = len(re.findall(rf"\(net {net}\)", text2))
    print(f"net {net} refs: {c}")

PCB.write_text(text2, encoding="utf-8")
print(checks)
print("segment count:", text2.count("(segment"))
