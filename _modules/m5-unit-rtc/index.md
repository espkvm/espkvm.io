---
title: M5Stack Unit RTC
family: M5Stack
kind: clock
status: tested
order: 40
role: Clock (optional)
chip: RTC8563
summary: An RTC8563 (a PCF8563 twin) with its battery inside and a Grove connector.
boards: m5-poe-p4
spec.Chip: RTC8563, at 0x51
spec.Connector: Grove (HY2.0-4P), cable in the box
spec.Power: 5V; its own 3.3 V regulator, and the I2C pull-ups go to that
spec.Battery: built in
spec.Setting: found by itself, also on the display's Grove bus
spec.Firmware: 0.61.0 or newer to be found by itself
link.M5Stack docs: https://docs.m5stack.com/en/unit/Unit_RTC
photo: module.jpg
photo_style: product
---

On the M5Stack Unit PoE-P4 it goes on the Grove port next to a status display
(through a Grove hub) and is found by itself: "Auto" looks on the display's
bus too. On other boards it is four wires: 5V, GND, SDA and SCL. Its pull-ups
go to its own 3.3 V, so 5V on VCC is safe for the ESP32-P4.

Run on the Unit PoE-P4 beside a Unit OLED. Two things kept it from being found
before 0.61.0, both fixed: its BM8563 reads one bit of the timer register
differently from the NXP PCF8563, and a new one holds no valid time until the
device first sets it. On older firmware, pick "PCF8563" under Settings →
System → Clock, choose "own pins" and name the display's two pins.
