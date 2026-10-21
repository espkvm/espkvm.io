---
title: Waveshare ESP32-P4-NANO-WIFI6-DB
family: Waveshare
kind: device
status: tested
order: 130
role: The device - community-tested
summary: The NANO with a dual-band ESP32-C5, so it can join a 5 GHz network.
flasher: p4-nano-wifi6-db
capture: c790, c792, waveshare-19137
spec.Chip: ESP32-P4, rev 3.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Size: 52 x 50 mm
spec.Network: 100M Ethernet, PoE with the add-on PoE module (in kits B, C and D), dual-band Wi-Fi 6 (ESP32-C5)
spec.microSD: yes
spec.To the target: USB-A (A-to-A cable, 5 V wire cut)
spec.Capture connector: 15-pin Raspberry Pi camera connector
link.Waveshare product page: https://www.waveshare.com/esp32-p4-nano-wifi6-db.htm
photo: board.webp
photo_style: product
---

The first supported board that can join a 5 GHz network. It carries an
ESP32-P4NRW32**X**, which is rev 3.x silicon, so it has one image and no pre-3.0
twin.

Its right-hand header also brings out the high-speed USB pair, so the target
can be wired there instead of the Type-A socket.

## Wiring

- The Type-A socket for the target always carries 5 V, as on the NANO.
- So the lead to the target is an **A-to-A cable with the 5 V wire cut**. A plain A-to-A cable joins two 5 V supplies.

Run by a user with a C790 from AliExpress, with no problems. Wi-Fi has not been tried on it yet.
