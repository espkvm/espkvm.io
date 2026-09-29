---
title: Waveshare ESP32-P4-WIFI6-DB
kind: device
status: untested
order: 135
role: Not tested on hardware
summary: The ESP32-P4-WIFI6 with a dual-band ESP32-C5 and a rev 3.x chip. Wi-Fi only.
flasher: p4-wifi6-db
capture: c790, waveshare-19137
spec.Chip: ESP32-P4NRW32X, rev 3.x
spec.Memory: 32 MB PSRAM, 32 MB flash
spec.Network: dual-band Wi-Fi 6 (ESP32-C5) only
spec.To the target: USB OTG on a 4-pin header
spec.Capture: 2-lane camera connector
spec.microSD: yes
link.Waveshare product page: https://www.waveshare.com/esp32-p4-wifi6-db.htm
link.Waveshare docs: https://docs.waveshare.com/ESP32-P4-WIFI6-DB
photo: board.webp
photo_style: product
---

The ESP32-P4-WIFI6 with an ESP32-C5 in place of the C6. Waveshare's pin table
matches the WIFI6 apart from the co-processor, so the image is the WIFI6's with
the C5 and the chip revision changed.

## Wiring

- USB OTG is on a **4-pin header**, like on the WIFI6, so the target needs a cable from that header to USB-A.
- The Type-C is power, flashing and the log, through a CH343P.

It has no Ethernet: Wi-Fi is the only way in, and the first boot opens the setup
hotspot. Built from Waveshare's documentation, not yet run on one.
