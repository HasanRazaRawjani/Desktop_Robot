"""Add 2x SG90 servo male headers (J3, J4) to schematic + PCB and route them."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

SCH = Path(
    r"c:\Users\rawja\OneDrive\Desktop\Desktop_Robot\esp32-body_cad\pcb and schematic\esp32-body.kicad_sch"
)
PCB = Path(
    r"c:\Users\rawja\OneDrive\Desktop\Desktop_Robot\esp32-body_cad\pcb and schematic\esp32-body.kicad_pcb"
)


def uid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Schematic updates
# ---------------------------------------------------------------------------

CONN_01X03 = r'''		(symbol "Connector_Generic:Conn_01x03"
			(pin_names
				(offset 1.016)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(in_pos_files yes)
			(duplicate_pin_numbers_are_jumpers no)
			(property "Reference" "J"
				(at 0 5.08 0)
				(show_name no)
				(do_not_autoplace no)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "Conn_01x03"
				(at 0 -5.08 0)
				(show_name no)
				(do_not_autoplace no)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Description" "Generic connector, single row, 01x03"
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "ki_keywords" "connector"
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "ki_fp_filters" "Connector*:*_1x??_*"
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "Conn_01x03_1_1"
				(rectangle
					(start -1.27 3.81)
					(end 1.27 -3.81)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
				(rectangle
					(start -1.27 2.667)
					(end 0 2.413)
					(stroke
						(width 0.1524)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(rectangle
					(start -1.27 0.127)
					(end 0 -0.127)
					(stroke
						(width 0.1524)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(rectangle
					(start -1.27 -2.413)
					(end 0 -2.667)
					(stroke
						(width 0.1524)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(pin passive line
					(at -5.08 2.54 0)
					(length 3.81)
					(name "Pin_1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at -5.08 0 0)
					(length 3.81)
					(name "Pin_2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at -5.08 -2.54 0)
					(length 3.81)
					(name "Pin_3"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "3"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)
'''

PWR_5V = r'''		(symbol "power:+5V"
			(power global)
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(in_pos_files yes)
			(duplicate_pin_numbers_are_jumpers no)
			(property "Reference" "#PWR"
				(at 0 -3.81 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "+5V"
				(at 0 3.556 0)
				(show_name no)
				(do_not_autoplace no)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Description" "Power symbol creates a global label with name \"+5V\""
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "ki_keywords" "global power"
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "+5V_0_1"
				(polyline
					(pts
						(xy -0.762 1.27) (xy 0 2.54)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0 0) (xy 0 2.54)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0 2.54) (xy 0.762 1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "+5V_1_1"
				(pin power_in line
					(at 0 0 90)
					(length 0)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)
'''


def make_conn(ref: str, value: str, x: float, y: float, uuid_sym: str) -> str:
    pins = "\n".join(
        f'''		(pin "{n}"
			(uuid "{uid()}")
		)'''
        for n in ("1", "2", "3")
    )
    return f'''	(symbol
		(lib_id "Connector_Generic:Conn_01x03")
		(at {x} {y} 0)
		(unit 1)
		(body_style 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(in_pos_files yes)
		(dnp no)
		(uuid "{uuid_sym}")
		(property "Reference" "{ref}"
			(at {x} {y - 5.08} 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "{value}"
			(at {x} {y + 5.08} 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"
			(at {x} {y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at {x} {y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "SG90 servo male header GND/5V/SIG"
			(at {x} {y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
{pins}
		(instances
			(project "esp32-body"
				(path "/e1af0617-b6fc-4c67-8b6b-2b3efc40d505"
					(reference "{ref}")
					(unit 1)
				)
			)
		)
	)
'''


def make_pwr(lib: str, value: str, ref: str, x: float, y: float, rot: int = 0) -> str:
    return f'''	(symbol
		(lib_id "{lib}")
		(at {x} {y} {rot})
		(unit 1)
		(body_style 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(in_pos_files yes)
		(dnp no)
		(uuid "{uid()}")
		(property "Reference" "{ref}"
			(at {x} {y - 2.54} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "{value}"
			(at {x} {y + 3.81} 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at {x} {y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at {x} {y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" ""
			(at {x} {y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "1"
			(uuid "{uid()}")
		)
		(instances
			(project "esp32-body"
				(path "/e1af0617-b6fc-4c67-8b6b-2b3efc40d505"
					(reference "{ref}")
					(unit 1)
				)
			)
		)
	)
'''


def make_wire(x1, y1, x2, y2) -> str:
    return f'''	(wire
		(pts
			(xy {x1} {y1}) (xy {x2} {y2})
		)
		(stroke
			(width 0)
			(type default)
		)
		(uuid "{uid()}")
	)
'''


def make_label(name: str, x: float, y: float) -> str:
    return f'''	(label "{name}"
		(at {x} {y} 0)
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify left bottom)
		)
		(uuid "{uid()}")
	)
'''


def update_schematic() -> None:
    text = SCH.read_text(encoding="utf-8")

    # Insert lib symbols before closing of lib_symbols if missing
    if "Connector_Generic:Conn_01x03" not in text:
        text = text.replace(
            '\t\t(symbol "Connector_Generic:Conn_01x07"',
            CONN_01X03 + '\t\t(symbol "Connector_Generic:Conn_01x07"',
            1,
        )
    if 'symbol "power:+5V"' not in text:
        text = text.replace(
            '\t\t(symbol "power:+3.3V"',
            PWR_5V + '\t\t(symbol "power:+3.3V"',
            1,
        )

    # Remove no_connects on GPIO32 (133.35 91.44), GPIO33 (133.35 93.98), VIN (133.35 114.3)
    for xy in ("133.35 91.44", "133.35 93.98", "133.35 114.3"):
        text = re.sub(
            rf"\t\(no_connect\n\t\t\(at {re.escape(xy)}\)\n\t\t\(uuid \"[^\"]+\"\)\n\t\)\n",
            "",
            text,
        )

    # Avoid duplicating if re-run
    if 'Reference" "J3"' in text or 'Reference" "J3"\n' in text:
        # crude check
        if "(property \"Reference\" \"J3\"" in text:
            print("Schematic already has J3 — skipping schematic instance insert")
            SCH.write_text(text, encoding="utf-8")
            return

    # Place connectors left of ESP32
    # J3 SERVO1: pins at x-5.08 = connection. Place body at (100, 91.44) so pin1 at (94.92, 93.98)? 
    # Conn pins: pin1 at local (-5.08, 2.54), pin2 (-5.08, 0), pin3 (-5.08, -2.54)
    # Put J3 at (100, 88.9) => pin connections at x=94.92
    # Better: put connectors at (90, 91.44) and (90, 106.68)

    j3_uuid = uid()
    j4_uuid = uid()
    instances = (
        make_conn("J3", "SERVO1_SG90", 95.25, 91.44, j3_uuid)
        + make_conn("J4", "SERVO2_SG90", 95.25, 106.68, j4_uuid)
        # Power symbols on servo headers
        + make_pwr("power:GND", "GND", "#PWR020", 90.17, 93.98)  # near J3 pin1 (GND) — adjust
        + make_pwr("power:+5V", "+5V", "#PWR021", 90.17, 91.44)
        + make_pwr("power:GND", "GND", "#PWR022", 90.17, 109.22)
        + make_pwr("power:+5V", "+5V", "#PWR023", 90.17, 106.68)
        + make_pwr("power:+5V", "+5V", "#PWR024", 128.27, 114.3)  # VIN -> +5V
        + make_pwr("power:PWR_FLAG", "PWR_FLAG", "#FLG02", 125.73, 114.3)
    )

    # Wires / labels
    # U1 GPIO32 @ 133.35,91.44 -> label SERVO1
    # U1 GPIO33 @ 133.35,93.98 -> label SERVO2
    # J3 pin3 (signal) at body(95.25,91.44)+(-5.08,-2.54)=(90.17,88.9)
    # J3 pin2 (5V) = (90.17, 91.44)
    # J3 pin1 (GND) = (90.17, 93.98)
    # J4 pin3 = (90.17, 104.14), pin2=(90.17,106.68), pin1=(90.17,109.22)

    wiring = (
        make_wire(133.35, 91.44, 120.65, 91.44)
        + make_label("SERVO1", 120.65, 91.44)
        + make_wire(133.35, 93.98, 120.65, 93.98)
        + make_label("SERVO2", 120.65, 93.98)
        # J3 signal pin3
        + make_wire(90.17, 88.9, 85.09, 88.9)
        + make_label("SERVO1", 85.09, 88.9)
        # J4 signal pin3
        + make_wire(90.17, 104.14, 85.09, 104.14)
        + make_label("SERVO2", 85.09, 104.14)
        # VIN to +5V
        + make_wire(133.35, 114.3, 128.27, 114.3)
        + make_wire(128.27, 114.3, 125.73, 114.3)
        # Power to J3 pins
        + make_wire(90.17, 93.98, 90.17, 93.98)  # placeholder removed below
    )

    # Clean zero wires from template mistake
    wiring = re.sub(
        r"\t\(wire\n\t\t\(pts\n\t\t\t\(xy 90\.17 93\.98\) \(xy 90\.17 93\.98\)\n\t\t\)\n\t\t\(stroke\n\t\t\t\(width 0\)\n\t\t\t\(type default\)\n\t\t\)\n\t\t\(uuid \"[^\"]+\"\)\n\t\)\n",
        "",
        wiring,
    )

    # Insert before end of file (before final paren)
    if not text.rstrip().endswith(")"):
        raise SystemExit("schematic format unexpected")
    # Insert before last closing paren
    text = text.rstrip()
    if text.endswith(")"):
        text = text[:-1] + wiring + instances + ")\n"

    SCH.write_text(text, encoding="utf-8")
    print("Schematic updated with J3/J4 servo headers + +5V")


# ---------------------------------------------------------------------------
# PCB updates
# ---------------------------------------------------------------------------

def header_fp(ref: str, value: str, x: float, y: float, rot: float, nets: list[tuple[int, str]]) -> str:
    """nets: list of (net_num, net_name) for pads 1..3"""
    pads = []
    shapes = ["rect", "oval", "oval"]
    for i, ((nnum, nname), shape) in enumerate(zip(nets, shapes), start=1):
        py = (i - 1) * 2.54
        pads.append(
            f'''\t\t(pad "{i}" thru_hole {shape}
\t\t\t(at 0 {py} {int(rot) % 360})
\t\t\t(size 1.7 1.7)
\t\t\t(drill 1)
\t\t\t(layers "*.Cu" "*.Mask")
\t\t\t(remove_unused_layers no)
\t\t\t(net {nnum} "{nname}")
\t\t\t(pintype "passive")
\t\t\t(uuid "{uid()}")
\t\t)'''
        )
    pads_txt = "\n".join(pads)
    return f'''\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"
\t\t(layer "F.Cu")
\t\t(uuid "{uid()}")
\t\t(at {x} {y} {rot})
\t\t(descr "Through hole straight pin header, 1x03, 2.54mm pitch, single row")
\t\t(tags "Through hole pin header THT 1x03 2.54mm single row")
\t\t(property "Reference" "{ref}"
\t\t\t(at 0 -2.33 {0 if rot % 180 == 0 else 90})
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
\t\t\t(at 0 7.41 {0 if rot % 180 == 0 else 90})
\t\t\t(layer "F.Fab")
\t\t\t(uuid "{uid()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1 1)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Datasheet" ""
\t\t\t(at 0 0 0)
\t\t\t(layer "F.Fab")
\t\t\t(hide yes)
\t\t\t(uuid "{uid()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Description" "SG90 servo male header"
\t\t\t(at 0 0 0)
\t\t\t(layer "F.Fab")
\t\t\t(hide yes)
\t\t\t(uuid "{uid()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(attr through_hole)
\t\t(fp_line
\t\t\t(start -1.33 1.27)
\t\t\t(end -1.33 6.41)
\t\t\t(stroke
\t\t\t\t(width 0.12)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start -1.33 1.27)
\t\t\t(end 1.33 1.27)
\t\t\t(stroke
\t\t\t\t(width 0.12)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start -1.33 6.41)
\t\t\t(end 1.33 6.41)
\t\t\t(stroke
\t\t\t\t(width 0.12)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start 1.33 1.27)
\t\t\t(end 1.33 6.41)
\t\t\t(stroke
\t\t\t\t(width 0.12)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start -1.33 0)
\t\t\t(end -1.33 -1.33)
\t\t\t(stroke
\t\t\t\t(width 0.12)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_line
\t\t\t(start -1.33 -1.33)
\t\t\t(end 0 -1.33)
\t\t\t(stroke
\t\t\t\t(width 0.12)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(fp_rect
\t\t\t(start -1.8 -1.8)
\t\t\t(end 1.8 6.85)
\t\t\t(stroke
\t\t\t\t(width 0.05)
\t\t\t\t(type default)
\t\t\t)
\t\t\t(fill no)
\t\t\t(layer "F.CrtYd")
\t\t\t(uuid "{uid()}")
\t\t)
{pads_txt}
\t\t(embedded_fonts no)
\t\t(model "${{KICAD10_3DMODEL_DIR}}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x03_P2.54mm_Vertical.step"
\t\t\t(offset
\t\t\t\t(xyz 0 0 0)
\t\t\t\t)
\t\t\t(scale
\t\t\t\t(xyz 1 1 1)
\t\t\t\t)
\t\t\t(rotate
\t\t\t\t(xyz 0 0 0)
\t\t\t\t)
\t\t)
\t)
'''


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


def path(net: int, pts, w: float, layer: str) -> list[str]:
    out = []
    for a, b in zip(pts, pts[1:]):
        if a != b:
            out.append(seg(net, a, b, w, layer))
    return out


def update_pcb() -> None:
    text = PCB.read_text(encoding="utf-8")

    if "PinHeader_1x03" in text and 'Reference" "J3"' in text:
        print("PCB already has J3 — will still ensure nets/routes")

    # Add nets 9,10,11 if missing
    if '(net 9 "/SERVO1")' not in text:
        text = text.replace(
            '(net 8 "/I2C_SDA")\n',
            '(net 8 "/I2C_SDA")\n'
            '(net 9 "/SERVO1")\n'
            '(net 10 "/SERVO2")\n'
            '(net 11 "+5V")\n',
            1,
        )

    # Assign U1 pads: GPIO32=pad10 -> SERVO1, GPIO33=pad9 -> SERVO2, VIN=pad1 -> +5V
    def set_u1_pad(src: str, pad: str, net_num: int, net_name: str, pinfunction: str) -> str:
        # Match pad block and replace/insert net
        pat = re.compile(
            rf'(\(pad "{pad}" thru_hole oval\n'
            rf'\t\t\t\(at [^\n]+\)\n'
            rf'\t\t\t\(size [^\n]+\)\n'
            rf'\t\t\t\(drill [^\n]+\)\n'
            rf'\t\t\t\(layers [^\n]+\)\n'
            rf'(?:\t\t\t\(remove_unused_layers [^\n]+\)\n)?'
            rf')(?:\t\t\t\(net [^\n]+\)\n)?'
            rf'(\t\t\t\(pinfunction "{re.escape(pinfunction)}"\)\n)',
            re.M,
        )

        def repl(m):
            return m.group(1) + f'\t\t\t(net {net_num} "{net_name}")\n' + m.group(2)

        new, n = pat.subn(repl, src, count=1)
        print(f"  U1 pad {pad} -> {net_name}: {n}")
        return new

    text = set_u1_pad(text, "10", 9, "/SERVO1", "GPIO32_10")
    text = set_u1_pad(text, "9", 10, "/SERVO2", "GPIO33_9")
    text = set_u1_pad(text, "1", 11, "+5V", "VIN_1")

    # Place headers along bottom edge (board 154..191 x, 39..99 y)
    # J3 at (158.5, 93.5) rot 0 — vertical, fits under left side
    # J4 at (164.5, 93.5) rot 0
    # Check collision with U1 which extends to y~89.5 bottom USB area... U1 at y=72.5, pads from ~54 to 89.5
    # Bottom free band ~90.5 to 98.5
    J3 = (158.5, 92.5, 0.0)
    J4 = (165.0, 92.5, 0.0)

    # Absolute pad positions
    j3_pads = {
        1: (J3[0], J3[1]),  # GND
        2: (J3[0], J3[1] + 2.54),  # +5V
        3: (J3[0], J3[1] + 5.08),  # SERVO1
    }
    j4_pads = {
        1: (J4[0], J4[1]),
        2: (J4[0], J4[1] + 2.54),
        3: (J4[0], J4[1] + 5.08),
    }
    # U1 pads
    U1 = (168.92754, 72.540187)
    u1_10 = (U1[0] - 11.92754, U1[1] - 5.840187)  # GPIO32
    u1_9 = (U1[0] - 11.92754, U1[1] - 3.300187)  # GPIO33
    u1_1 = (U1[0] - 11.92754, U1[1] + 17.019813)  # VIN
    u1_2 = (U1[0] - 11.92754, U1[1] + 14.479813)  # GND

    print("J3 pads", j3_pads)
    print("J4 pads", j4_pads)
    print("U1 GPIO32/33/VIN", u1_10, u1_9, u1_1)

    # Remove old J3/J4 footprints if present
    text = re.sub(
        r'\t\(footprint "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"[\s\S]*?\n\t\)\n',
        "",
        text,
    )

    fps = header_fp(
        "J3",
        "SERVO1",
        J3[0],
        J3[1],
        J3[2],
        [(1, "GND"), (11, "+5V"), (9, "/SERVO1")],
    ) + header_fp(
        "J4",
        "SERVO2",
        J4[0],
        J4[1],
        J4[2],
        [(1, "GND"), (11, "+5V"), (10, "/SERVO2")],
    )

    # Insert footprints before first segment or gr_rect
    insert_at = text.find("\t(segment\n")
    if insert_at < 0:
        insert_at = text.find("\t(gr_rect\n")
    text = text[:insert_at] + fps + text[insert_at:]

    # Remove previous servo routes if any (nets 9,10,11 segments only — careful)
    # We'll append new routes; strip segments that reference net 9/10/11 first
    def strip_net_segs(src: str, net: int) -> str:
        return re.sub(
            rf"\t\(segment\n"
            rf"\t\t\(start [^\n]+\)\n"
            rf"\t\t\(end [^\n]+\)\n"
            rf"\t\t\(width [^\n]+\)\n"
            rf"\t\t\(layer \"[^\"]+\"\)\n"
            rf"\t\t\(net {net}\)\n"
            rf"\t\t\(uuid \"[^\"]+\"\)\n"
            rf"\t\)\n?",
            "",
            src,
        )

    for n in (9, 10, 11):
        text = strip_net_segs(text, n)

    items: list[str] = []
    SIG, PWR = 0.25, 0.5

    # SERVO1: U1.10 -> J3.3
    items += path(
        9,
        [
            (round(u1_10[0], 4), round(u1_10[1], 4)),
            (156.5, round(u1_10[1], 4)),
            (156.5, j3_pads[3][1]),
            (j3_pads[3][0], j3_pads[3][1]),
        ],
        SIG,
        "F.Cu",
    )
    # SERVO2: U1.9 -> J4.3
    items += path(
        10,
        [
            (round(u1_9[0], 4), round(u1_9[1], 4)),
            (155.8, round(u1_9[1], 4)),
            (155.8, 98.0),
            (j4_pads[3][0], 98.0),
            (j4_pads[3][0], j4_pads[3][1]),
        ],
        SIG,
        "B.Cu",
    )
    # GND: J3.1 and J4.1 to U1.2
    items += path(
        1,
        [
            (j3_pads[1][0], j3_pads[1][1]),
            (j3_pads[1][0], round(u1_2[1], 4)),
            (round(u1_2[0], 4), round(u1_2[1], 4)),
        ],
        PWR,
        "F.Cu",
    )
    items += path(
        1,
        [
            (j4_pads[1][0], j4_pads[1][1]),
            (j3_pads[1][0], j4_pads[1][1]),
            (j3_pads[1][0], j3_pads[1][1]),
        ],
        PWR,
        "F.Cu",
    )
    # +5V: U1.1 (VIN) -> J3.2 and J4.2
    items += path(
        11,
        [
            (round(u1_1[0], 4), round(u1_1[1], 4)),
            (156.5, round(u1_1[1], 4)),
            (156.5, j3_pads[2][1]),
            (j3_pads[2][0], j3_pads[2][1]),
        ],
        PWR,
        "B.Cu",
    )
    items += path(
        11,
        [
            (j3_pads[2][0], j3_pads[2][1]),
            (j4_pads[2][0], j3_pads[2][1]),
            (j4_pads[2][0], j4_pads[2][1]),
        ],
        PWR,
        "F.Cu",
    )

    edge = "\t(gr_rect\n\t\t(start 154 38.980514)"
    if edge not in text:
        raise SystemExit("edge cuts missing")
    text = text.replace(edge, "\n".join(items) + "\n" + edge, 1)

    PCB.write_text(text, encoding="utf-8")
    print(f"PCB updated: J3/J4 placed, {len(items)} new segments")


if __name__ == "__main__":
    update_schematic()
    update_pcb()
    print("DONE")
