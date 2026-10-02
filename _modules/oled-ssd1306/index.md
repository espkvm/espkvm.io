---
title: I2C OLED - SSD1306 / SH1106 / SSD1315
tile_maker: I2C OLED
tile_model: SSD1306 / SH1106 / SSD1315
kind: display
status: tested
order: 10
role: Status display (optional)
chip: I2C OLED
summary: A mono OLED on four wires, from 0.96" 128x64 down to 0.49" 64x32. It sits on the capture chip's I2C bus and needs no pins of its own.
spec.Controller: SSD1306, SH1106, SSD1315
spec.Sizes: SSD1306 128x64, 128x32, 96x16, 72x40, 64x48, 64x32; SH1106 128x64, 128x32, 96x16, 64x48; SSD1315 128x64, 72x40
spec.Wiring: VCC to 3V3, GND, SDA and SCL to the capture board's I2C bus
spec.Setting: Settings → Display
photo: module.jpg
photo_style: product
---

The device draws its address, link, capture status and health across a few
pages. A shorter panel shows fewer lines, and the address is the line it keeps.
A line that does not fit steps along a character at a time.

## Good to know

- These controllers cannot tell how big the glass is, so Settings → Display picks the panel by controller and size in one list.
- In hotspot mode it shows the network and its password as a QR code, in turn with the same as text. Panels too short for a readable code show only the text.
- It can be turned upside down in the settings, for a panel mounted that way. The switch applies at once.
- It can also go on two pins of its own instead of the capture bus: name them as OLED SDA and OLED SCL.
