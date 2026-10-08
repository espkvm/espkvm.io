---
title: M5Stack Unit OLED
family: M5Stack
tile_maker: M5Stack
tile_model: Unit OLED (U119)
kind: display
status: tested
order: 21
role: Status display (optional)
chip: Grove OLED
summary: A 1.3" 128x64 SH1107 panel with a Grove cable. On the M5Stack Unit PoE-P4 it plugs into the Grove port; pick "SH1107 128x64" in Settings and it shows.
boards: m5-poe-p4
spec.Controller: SH1107, 128x64, I2C at 0x3C
spec.Connector: Grove (HY2.0-4P), cable in the box
spec.Setting: Settings → Display → "SH1107 128x64"
link.M5Stack docs: https://docs.m5stack.com/en/unit/oled
photo: module.webp
photo_style: product
---

The bigger sibling of the Mini OLED: the same Grove plug, a 1.3" panel with
nearly three times the pixels, so the status pages show whole lines instead of
stepping along them. It needs firmware 0.61.0 or newer.

The SH1107 drives this glass on its side - it thinks the panel is 64 pixels
wide and 128 tall - so the firmware turns the picture as it sends it. Nothing
to set for that; if your enclosure has it the other way up, turn on
"Upside down".

On the M5Stack Unit PoE-P4 the Grove port is an I2C bus of its own and the
firmware already knows its pins. On another board, wire it to the capture
board's I2C bus, or name two pins as OLED SDA and OLED SCL under Settings →
Display.

Run on the M5Stack Unit PoE-P4.
