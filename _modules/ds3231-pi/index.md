---
title: DS3231 module for the Raspberry Pi
tile_maker: DS3231
tile_model: Raspberry Pi module
kind: clock
status: tested
order: 10
role: Clock (optional)
chip: DS3231
summary: The small one with a soldered-on coin cell and a five-pin socket. On a board with a Raspberry Pi header it plugs straight onto pins 1-9.
boards: funcev, p4-poe, p4-module-devkit, viewe-p4-pi
spec.Chip: DS3231, at 0x68
spec.Socket: five pins marked + D C NC -, Pi header pins 1, 3, 5, 7, 9
spec.Wiring: on other boards 3V3, GND and the capture board's SDA and SCL
spec.Battery: soldered-on coin cell
spec.Setting: found by itself; Settings → System → Clock
photo: module.jpg
photo_style: product
---

This is the one I run on my Function EV. It sits on the capture chip's I2C bus,
so it needs no pins of its own. The device finds it at start-up and sets its
clock from it, and writes the time back when it learns it from NTP or a
browser. I pulled the power cable several times, and each time the clock came
back within a second.

Diagnostics also shows the chip's thermometer, as the temperature by the board.
Home Assistant gets it as a "Board temperature" sensor.
