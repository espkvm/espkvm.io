---
title: M5Stack Unit RTC
kind: clock
status: untested
order: 40
role: Clock (optional)
chip: RTC8563
summary: An RTC8563 (a PCF8563 twin) with its battery inside and a Grove connector.
boards: m5-poe-p4
spec.Chip: RTC8563, at 0x51
spec.Connector: Grove (HY2.0-4P), cable in the box
spec.Power: 5V; its own 3.3 V regulator, and the I2C pull-ups go to that
spec.Battery: built in
spec.Setting: found by itself; Settings → System → Clock
link.M5Stack docs: https://docs.m5stack.com/en/unit/Unit_RTC
photo: module.jpg
photo_style: product
---

On the M5Stack Unit PoE-P4 it goes into the Grove port: under Settings ->
System → Clock pick "own pins" and name the same two pins as the display. On
other boards it is four wires: 5V, GND, SDA and SCL. Its pull-ups go to its own
3.3 V, so 5V on VCC is safe for the ESP32-P4.

The driver is written from the PCF8563 datasheet. Nobody has run this unit
with ESP-KVM yet.
