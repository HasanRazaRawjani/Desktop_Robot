"""Fix +3.3V short across J1 header pads; keep J1.2 and J1.7 connected around the strip."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

PCB = Path(
    r"c:\Users\rawja\OneDrive\Desktop\Desktop_Robot\esp32-body_cad\pcb and schematic\esp32-body.kicad_pcb"
)


def uid() -> str:
    return str(uuid.uuid4())


def seg(net: int, a, b, w: float, layer: str) -> str:
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


text = PCB.read_text(encoding="utf-8")

# Remove the bad +3.3V run that shorts across J1 pads:
# (189.24 43.0) -> (176.54 43.0) and the zero-length leftover if any
bad = re.compile(
    r"\t\(segment\n"
    r"\t\t\(start 189\.24 43\.0\)\n"
    r"\t\t\(end 176\.54 43\.0\)\n"
    r"\t\t\(width 0\.5\)\n"
    r"\t\t\(layer \"F\.Cu\"\)\n"
    r"\t\t\(net 2\)\n"
    r"\t\t\(uuid \"[^\"]+\"\)\n"
    r"\t\)\n?"
)
text2, n = bad.subn("", text)
print(f"Removed bad J1 short segments: {n}")

# Also remove any segment that runs exactly along y=43 between J1 pad x-range on net 2
# Safer: add a proper bypass north of the header connecting J1.7 to J1.2
# J1.7=(189.24,43), J1.2=(176.54,43)
# Route: J1.7 -> (189.24, 41.2) -> (176.54, 41.2) -> J1.2  (above header, still on board y>=40)

bypass = "\n".join(
    [
        seg(2, (189.24, 43.0), (189.24, 41.2), 0.5, "F.Cu"),
        seg(2, (189.24, 41.2), (176.54, 41.2), 0.5, "F.Cu"),
        seg(2, (176.54, 41.2), (176.54, 43.0), 0.5, "F.Cu"),
    ]
)

edge = "\t(gr_rect\n\t\t(start 154 38.980514)"
if edge not in text2:
    raise SystemExit("edge missing")
text2 = text2.replace(edge, bypass + "\n" + edge, 1)

PCB.write_text(text2, encoding="utf-8")
print("Added J1.2<->J1.7 +3.3V bypass above header")
print("segments:", text2.count("(segment"))
