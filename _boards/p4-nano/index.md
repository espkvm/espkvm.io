---
title: Waveshare ESP32-P4-NANO
family: Waveshare
kind: device
status: tested
order: 30
role: The device - community-tested
summary: Small, with Ethernet and an ESP32-C6. Capture, USB and Ethernet confirmed on both chip revisions.
flasher: p4-nano
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x or rev 3.x (an image for each)
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet, Wi-Fi 6 (ESP32-C6)
spec.To the target: USB-A (A-to-A cable, 5 V wire cut)
spec.Capture: 15-pin Raspberry Pi camera connector
link.Waveshare product page: https://www.waveshare.com/esp32-p4-nano.htm
photo: board.jpg
photo_style: product
---

The same IP101 Ethernet and onboard ESP32-C6 as the bigger Waveshare boards.
Contributors confirmed capture, USB and Ethernet on both silicon revisions, and
Wi-Fi on rev 3.1.

## Wiring

- The OTG port is a USB-A socket that drives its own 5 V.
- So the lead to the target is an **A-to-A cable with the 5 V wire cut**. A plain A-to-A cable joins two 5 V supplies.

It ships as either chip revision under one product code; check `chip revision:` in
the boot log and pick the image to match.
