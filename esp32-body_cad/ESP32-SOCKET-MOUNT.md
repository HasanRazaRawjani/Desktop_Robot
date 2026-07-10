# ESP32 plug-in socket mount (no direct solder)

Your PCB already uses **PinSocket** footprints for TFT (J1) and MPU6050 (J2).
Do the same for the ESP32: **solder sockets on the PCB, plug the dev board in.**

## What changed

- Removed **4 mounting holes** (Edge.Cuts circles) from `ESP32_30pin` on the PCB.
- **30 pin holes** stay — those are where you solder **female headers**.

## Physical build

```
PCB                           Your hands
───                           ──────────
2× 15-pin female socket  ←──  solder into U1 holes
ESP32 dev board          ←──  plug in (remove anytime)
```

Buy: **2× 1×15 female pin header** (2.54 mm pitch), or one **2×15 socket strip** cut to fit.

## KiCad — finish in Footprint Editor (recommended)

1. Open **`esp32-body.kicad_pcb`**
2. Click **U1** → **E** → **Edit Footprint**
3. Select all **30 pads** → set **Drill = 1.0 mm** (matches J1/J2 sockets)
4. **File → Save Footprint** (save to project if prompted)
5. **3D Viewer** → remove or hide ESP32 board 3D on footprint (optional):
   - Footprint properties → 3D Models → delete `ESP32-30pin.step` from PCB footprint
   - ESP32 3D stays in Fusion only

## Schematic note

- **U1** stays on schematic for **wiring/GPIO names**
- On PCB only **holes + sockets** are installed
- ESP32 board is **not** a PCB part — it's a plug-in module (like TFT)

## Optional: mark ESP32 not assembled on PCB

1. Schematic → click **U1**
2. Properties → **Exclude from BOM** or add note: "Module — not soldered to PCB"
3. Footprint on PCB can rename reference to **J3** / **ESP32_SOCKET** if you prefer

## Fusion 3D

After KiCad changes:
1. Re-export **esp32-body.step**
2. Re-import in Fusion
3. Lift ESP32 model **~8 mm** on Z (socket height) above PCB

## Parts (Amazon search)

- `2.54mm 1x15 female header socket`
- `2.54mm 2x15 pin socket strip`
