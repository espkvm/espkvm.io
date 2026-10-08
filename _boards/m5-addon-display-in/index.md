---
title: M5Stack Add-on Display In
family: M5Stack
kind: capture
status: tested
order: 30
role: The capture - M5Stack units only
summary: A Lontium LT6911D and a microSD slot, on a 24-pin flat cable. Fits the Unit PoE-P4 and nothing else.
bridge: LT6911D
spec.Bridge: Lontium LT6911D
spec.Input: HDMI
spec.Connector: 24-pin flat cable (M5Stack's own)
spec.microSD: yes
spec.HDMI-CEC: no; the line is wired to the chip, but its CEC is undocumented
spec.HDMI audio: no; the chip's audio pins are not connected
spec.Measured: 720p MJPEG at 23 fps
link.M5Stack shop page: https://shop.m5stack.com/products/add-on-display-in-for-poe-p4-lt6911d
photo: board.webp
photo_style: product
---

Not a TC358743. It plugs onto the 24-pin flat cable on M5Stack's Unit PoE-P4
and PoE-P4X - not the 15-pin camera cable every other board here uses, so it
fits none of them and none of them drives it.

The LT6911D cannot tell whether the source is switched on, so after a long "No
signal" the console offers a Reconnect HDMI button with a countdown.

No HDMI audio, either, and it cannot be switched on. M5Stack's
[schematic](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1265/SCH_UnitPoEP4_display_in_V0.3_SCH_PDF_20260326_2026_03_26_16_04_18.pdf)
marks every audio pin of the LT6911D as not connected, and a probe of every line
the add-on reaches the board on found them all still with a laptop playing a
video into the HDMI input.
