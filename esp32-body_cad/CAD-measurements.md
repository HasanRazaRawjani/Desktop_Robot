# ESP32 Body PCB — CAD measurements

Saved from KiCad `Edge.Cuts` + footprint positions (2026-07-08).

## Board outline (`Edge.Cuts`)

| Property | Value |
|----------|-------|
| Shape | Rectangle |
| Start X | **154.000** mm |
| Start Y | **38.981** mm |
| End X | **190.960** mm |
| End Y | **99.307** mm |
| Width | **36.960** mm |
| Height | **60.327** mm |
| Corner radius | 0 mm |
| Line width | 0.05 mm |

**CAD tip:** Treat board as **36.96 × 60.33 mm**. Put local origin at the **front-left** corner of the outline (KiCad Start).

```
KiCad absolute → local CAD (mm):
  local_x = kicad_x - 154.000
  local_y = kicad_y - 38.981
```

Orientation in KiCad (top view):
- **+Y down** in screen coords, but for CAD use the numbers as absolute distances from Start
- **Front** = small Y (TFT / J1 side)
- **Back** = large Y (USB side)

---

## Footprint origins (KiCad absolute → local)

| Ref | Part | KiCad (X, Y) mm | Rotation | Local (X, Y) mm |
|-----|------|-----------------|----------|-----------------|
| **J1** | ST7789 1×7 socket | 177.040, 43.000 | −90° | **23.040, 4.019** |
| **U1** | ESP32 DevKit V1 | 168.928, 72.540 | 0° | **14.928, 33.559** |
| **J2** | MPU6050 1×8 socket | 187.500, 63.220 | 0° | **33.500, 24.239** |

Local = relative to board Start (154, 38.981).

---

## Module / header sizes (for shell clearance)

### Headers on PCB (female sockets)

| Ref | Type | Pin pitch | Pin count | Pin-span (first→last) | Typical plastic body |
|-----|------|-----------|-----------|------------------------|----------------------|
| J1 | 1×7 vertical | 2.54 mm | 7 | **15.24** mm | ~2.5 × 17.8 × 8.5 mm |
| J2 | 1×8 vertical | 2.54 mm | 8 | **17.78** mm | ~2.5 × 20.3 × 8.5 mm |

### Plugged-in modules (approximate — measure your real parts)

| Module | Approx outline | Notes |
|--------|----------------|-------|
| ESP32 DevKit V1 (30-pin) | ~**28 × 52** mm (+ USB overhang) | Fills whole U1 footprint when plugged in |
| 1.3" ST7789 TFT | ~**27 × 40** mm (varies by vendor) | Glass faces away from PCB with straight headers |
| MPU6050 8-pin breakout | ~**15 × 25** mm (varies) | Only pins 1–4 wired |

### Stack height (Z) — useful for “pop out”

| Stack | Typical height |
|-------|----------------|
| PCB thickness | **1.6** mm (confirm with fab) |
| Female socket | ~**8.5** mm |
| Male header on module | ~**11** mm pins / ~2.5 mm plastic |
| Extra standoffs (optional) | **10–15** mm if you want more pop-out |
| TFT above PCB (straight headers, no extra standoffs) | ~**12–15** mm to glass |

---

## Other useful measurements to take (physical)

Measure these on your **real parts** with calipers — CAD accuracy depends on them more than KiCad:

1. **TFT module** — L × W × thickness; pin-1 location relative to glass; glass active area
2. **ESP32 DevKit** — L × W; USB connector overhang past PCB; antenna keepout
3. **MPU6050 board** — L × W; which end is pin 1 (VCC)
4. **Header mating height** — PCB top → module bottom when fully seated
5. **Mounting holes** — if the shell uses screws: hole diameter + positions (ESP footprint has 4 corner holes)
6. **USB access** — cutout size/position at the **back** edge for the cable
7. **Face opening** — window size for the TFT glass in the robot shell
8. **Board thickness** — order **1.6 mm** unless you change fab options

---

## Quick CAD sketch (local mm, front at top)

```
(0,0) ──────────────────── (36.96, 0)     FRONT (TFT)
  │         J1 ~ (23.0, 4.0)              │
  │                                       │
  │              U1 ~ (14.9, 33.6)        │
  │         J2 ~ (33.5, 24.2)             │
  │                                       │
(0, 60.33) ────────────── (36.96, 60.33)  BACK (USB)
```

**Note:** Footprint origins are KiCad anchor points (not always geometric center). For the shell, model the **module outlines** from physical measurements, then align to these socket positions.
