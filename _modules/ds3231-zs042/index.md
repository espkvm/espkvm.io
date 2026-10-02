---
title: DS3231 module - ZS-042
tile_maker: DS3231
tile_model: ZS-042
kind: clock
status: tested
order: 20
role: Clock (optional)
chip: DS3231
summary: The common blue board with a CR2032 holder on the back. Four wires to the capture board's I2C bus.
spec.Chip: DS3231SN at 0x68, plus a 24C32 memory chip at 0x57
spec.Wiring: VCC to 3V3, GND, SDA and SCL to the capture board's I2C bus
spec.Battery: CR2032 or LIR2032
spec.Setting: found by itself; Settings → System → Clock
photo: module.jpg
photo_style: product
---

The 24C32 memory chip sits at another address and is left alone. The pins on
the far side pass the bus on, so a status OLED can hang off the same wires.

## Good to know

- **Power it from 3V3, not 5V.** Its pull-ups go to its own VCC, so 5V there puts 5V on the ESP32-P4's pins.
- **The battery.** Most of these boards charge the cell through a diode and a resistor. With a plain CR2032 in it, take that diode off, or fit a rechargeable LIR2032.
- The DS3231 chip is the one I run; this exact board I have not.
