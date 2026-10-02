---
title: ChronoDot v2
tile_maker: Macetech
tile_model: ChronoDot v2
kind: clock
status: tested
order: 30
role: Clock (optional)
chip: DS3231SN
summary: Macetech's round DS3231SN board, with a CR1632 holder and no charging circuit, so a plain cell is fine.
spec.Chip: DS3231SN, at 0x68
spec.Wiring: VCC to 3V3, GND, SDA and SCL to the capture board's I2C bus
spec.Battery: CR1632
spec.Setting: found by itself; Settings → System → Clock
photo: module.jpg
photo_style: product
---

Its pull-up pads (R1, R2) can stay empty, since the capture board's bus
already has them.

The DS3231 chip is the one I run; this exact board I have not.
