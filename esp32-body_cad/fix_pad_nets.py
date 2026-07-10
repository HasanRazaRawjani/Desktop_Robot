"""Audit and repair pad nets for TFT/gyro routing."""
from __future__ import annotations

import re
from pathlib import Path

PCB = Path(
    r"c:\Users\rawja\OneDrive\Desktop\Desktop_Robot\esp32-body_cad\pcb and schematic\esp32-body.kicad_pcb"
)
text = PCB.read_text(encoding="utf-8")

# Expected nets for pads that should be connected for TFT+gyro
# pad number -> (net_num, net_name) for U1
U1_NETS = {
    2: (1, "GND"),
    6: (5, "/TFT_RST"),
    15: (2, "+3.3V"),  # EN
    16: (2, "+3.3V"),
    17: (1, "GND"),
    19: (6, "/TFT_DC"),
    24: (3, "/TFT_SCK"),
    26: (8, "/I2C_SDA"),
    29: (7, "/I2C_SCL"),
    30: (4, "/TFT_MOSI"),
}
J1_NETS = {
    1: (1, "GND"),
    2: (2, "+3.3V"),
    3: (3, "/TFT_SCK"),
    4: (4, "/TFT_MOSI"),
    5: (5, "/TFT_RST"),
    6: (6, "/TFT_DC"),
    7: (2, "+3.3V"),
}
J2_NETS = {
    1: (2, "+3.3V"),
    2: (1, "GND"),
    3: (7, "/I2C_SCL"),
    4: (8, "/I2C_SDA"),
}


def fix_fp_pads(src: str, fp_name: str, expected: dict[int, tuple[int, str]]) -> str:
    # Isolate footprint block
    m = re.search(
        rf'\(footprint "{re.escape(fp_name)}".*?(?=\n\t\(footprint |\n\t\(segment |\n\t\(gr_rect |\n\t\(via )',
        src,
        re.S,
    )
    if not m:
        print("Footprint not found:", fp_name)
        return src
    block = m.group(0)
    new_block = block
    for pad, (num, name) in expected.items():
        pm = re.search(
            rf'(\(pad "{pad}" thru_hole.*?)(\n\t\t\))',
            new_block,
            re.S,
        )
        if not pm:
            print(f"  pad {pad} missing in {fp_name}")
            continue
        pad_body = pm.group(1)
        # Remove any existing net line
        pad_body2 = re.sub(r'\n\t\t\t\(net [^\n]+\)', "", pad_body)
        # Insert net after remove_unused_layers line if present, else after layers
        if "(remove_unused_layers" in pad_body2:
            pad_body2 = re.sub(
                r'(\(remove_unused_layers [^\)]+\))',
                rf'\1\n\t\t\t(net {num} "{name}")',
                pad_body2,
                count=1,
            )
        else:
            pad_body2 = re.sub(
                r'(\(layers [^\)]+\))',
                rf'\1\n\t\t\t(net {num} "{name}")',
                pad_body2,
                count=1,
            )
        new_block = new_block[: pm.start()] + pad_body2 + pm.group(2) + new_block[pm.end() :]
        print(f"  set {fp_name} pad {pad} -> {num} {name}")
    return src[: m.start()] + new_block + src[m.end() :]


print("Fixing U1...")
text = fix_fp_pads(text, "ESP32_Footprints:ESP32_30pin", U1_NETS)
print("Fixing J1...")
text = fix_fp_pads(text, "Connector_PinSocket_2.54mm:PinSocket_1x07_P2.54mm_Vertical", J1_NETS)
print("Fixing J2...")
text = fix_fp_pads(text, "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical", J2_NETS)

PCB.write_text(text, encoding="utf-8")

# Verify
text = PCB.read_text(encoding="utf-8")
for fp, expected in [
    ("ESP32_Footprints:ESP32_30pin", U1_NETS),
    ("Connector_PinSocket_2.54mm:PinSocket_1x07_P2.54mm_Vertical", J1_NETS),
    ("Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical", J2_NETS),
]:
    m = re.search(
        rf'\(footprint "{re.escape(fp)}".*?(?=\n\t\(footprint |\n\t\(segment |\n\t\(gr_rect )',
        text,
        re.S,
    )
    print("---", fp.split(":")[-1])
    for pad, (num, name) in expected.items():
        pm = re.search(rf'\(pad "{pad}".*?\(net ([^\n]+)\)', m.group(0), re.S)
        got = pm.group(1) if pm else "MISSING"
        ok = f'{num} "{name}"' in got or f'"{name}"' in got
        print(f"  pad {pad}: {got} {'OK' if ok else 'BAD'}")
print("segments:", text.count("(segment"))
