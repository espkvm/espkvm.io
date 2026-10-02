---
title: M5Stack Mini OLED Unit
kind: display
status: tested
order: 20
role: Status display (optional)
chip: Grove OLED
summary: A 0.42" 72x40 SSD1315 panel with a Grove cable. On the M5Stack Unit PoE-P4 it plugs in with nothing to solder and nothing to set.
boards: m5-poe-p4
spec.Controller: SSD1315, 72x40
spec.Connector: Grove (HY2.0-4P), cable in the box
spec.Setting: Settings → Display
photo: module.webp
photo_style: product
---

The Grove port on the M5Stack Unit PoE-P4 is an I2C bus of its own, and the
firmware for that board already knows its pins. Any other board can use it the
same way: name the two pins as OLED SDA and OLED SCL under Settings → Display.

Twelve characters to a line and four lines under the heading, so it shows the
address, the link, the picture's size and the health figures, one screen at a
time.
