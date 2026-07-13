# Voxia

**Voxia** is a small desktop study companion robot. It sits on your desk with an animated face, can sense motion, move with servo “legs,” and — once the Pi build is fully wired — talk, listen, play music, and help you stay focused while you study.

## Why it exists

Voxia is meant to make studying less lonely and a bit more accountable. The long-term idea is a robot that:

- Keeps you company at the desk with a face on a small TFT
- Lets you **talk to it** (mic in, speaker out)
- **Plays music** while you work
- Uses a **USB camera** for simple awareness at the desk
- Helps **track where your phone is** — and if it detects the phone is in your hand when you should be studying, it can **start beeping** to nudge you to put it down
- Can **move** a little (servos) so it feels present, not like a static gadget

None of that is fully finished yet. The goal is a Pi-powered desk robot that can grow into those features over time.

## Current approach: Raspberry Pi 4 + breadboard

Early on, this project included a custom **ESP32 body PCB** in KiCad (socketed DevKit, ST7789 face display, MPU6050). That work was useful for learning PCB design, but the plan changed.

**Why the switch:** getting a full custom board fabbed and revised for every new idea (camera, mic, speaker, phone nudges, movement) was going to slow everything down. Wiring on a **Raspberry Pi 4** with **breadboards** makes it faster to try sensors, audio, and camera ideas before committing to another PCB.

So for now:

- **Brain:** Raspberry Pi 4  
- **Prototyping:** breadboards + jumper wires  
- **Display / IMU / servos / audio / camera:** added as modules as the build grows  

## Earlier PCB work (still in the repo)

The KiCad files are kept as a record of that first design pass:

| Path | Contents |
|------|----------|
| `esp32-body_PCBcad/` | KiCad project, footprints, and CAD helpers |
| `esp32-body_PCBcad/pcb and schematic/` | `esp32-body.kicad_pro` / `.kicad_sch` / `.kicad_pcb` |
| `esp32-body_PCBcad/pcb and schematic screenshots/` | Layout screenshots from the PCB sessions |

That board targeted an ESP32 DevKit V1, ST7789 TFT (face), and MPU6050 on female headers. It is **not** the active build path anymore, but it stays here for reference.

## Planned Pi peripherals

| Piece | Role |
|-------|------|
| TFT (ST7789) | Animated face / status UI |
| MPU6050 | Motion / orientation sensing |
| Servos | Small “leg” or body movement |
| USB camera | Desk awareness / study context |
| Mic | Voice input — talk to Voxia |
| Speaker | Voice replies, music, phone-nudge beeps |

## Journal

Build notes live in [`JOURNAL.md`](JOURNAL.md).
