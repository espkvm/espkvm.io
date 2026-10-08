---
title: M5Stack Unit Glass2
family: M5Stack
tile_maker: M5Stack
tile_model: Unit Glass2
kind: display
status: untested
order: 22
role: Status display (optional)
chip: Grove OLED
summary: A 1.51" transparent 128x64 OLED (SSD1309) with two Grove ports. Pick "SSD1309 128x64" in Settings.
spec.Controller: SSD1309, 128x64, I2C at 0x3C (0x3D by a solder pad)
spec.Connector: two Grove (HY2.0-4P), linked, so the bus passes on
spec.Setting: Settings → Display → "SSD1309 128x64"
spec.Firmware: 0.61.0 or newer
link.M5Stack docs: https://docs.m5stack.com/en/unit/Glass2%20Unit
photo: module.webp
photo_style: product
---

A see-through panel in blue. The SSD1309 takes the same commands as the
SSD1306, so it runs on the same code.

Its glass shows 128x56 of the 128x64 the controller drives, so the top or
bottom row of the status pages may sit just outside the transparent part.

On the M5Stack Unit PoE-P4 it plugs into the Grove port. On another board,
wire it to the capture board's I2C bus, or name two pins as OLED SDA and OLED
SCL under Settings → Display.

This is the Glass2. The first Unit Glass has a small microcontroller in
front of its panel that speaks its own protocol, and is not supported.

Not tried on one yet.
