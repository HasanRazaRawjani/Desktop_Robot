# Desktop Robot — ESP32 Body

KiCad design for the body PCB of a small desktop robot. The board hosts a socketed **ESP32 DevKit V1**, a **1.3" ST7789 TFT**, and an **MPU6050** IMU so modules can be swapped without soldering them to the PCB.

## Hardware

| Ref | Part | Notes |
|-----|------|--------|
| **U1** | HiLetgo / DOIT ESP32 DevKit V1 (30-pin) | Whole DevKit plugs into female sockets — not a bare WROOM module |
| **J1** | 1.3" IPS ST7789 TFT (7-pin) | GND, VCC, SCL, SDA, RES, DC, BLK — **no CS pin** |
| **J2** | MPU6050 breakout (8-pin) | Only pins 1–4 wired (VCC, GND, SCL, SDA) |

All three use **female headers on the PCB** and **male headers on the modules**.

## Pin map

| Function | ESP32 GPIO |
|----------|------------|
| TFT SCK | 18 |
| TFT MOSI | 23 |
| TFT RST | 27 |
| TFT DC | 2 |
| MPU SDA | 21 |
| MPU SCL | 22 |

**TFT_eSPI notes:** set `TFT_CS` to `-1` (no chip select). `BLK` is tied to 3.3V on the PCB (`TFT_BL -1`).

Reserved for later: GPIO 4 (dock), 16/17 (UART), 32/33 (servos), 15 (touch), 0 (button).

## Board layout

- Flat single PCB, ~**37 × 60 mm**
- **J1 (TFT)** at the front, centered
- **U1 (ESP32)** set back, USB toward the rear
- **J2 (MPU)** beside the ESP32

Mount the board **upright** in the robot shell so the screen faces forward. Optional taller headers / standoffs on J1 push the display farther out.

CAD measurements: see `CAD-measurements.md`.

## Repo layout
