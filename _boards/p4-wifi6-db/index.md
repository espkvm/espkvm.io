---
title: Waveshare ESP32-P4-WIFI6-DB
family: Waveshare
kind: device
status: tested
order: 135
role: The Wi-Fi-only device with a 5 GHz radio
summary: The ESP32-P4-WIFI6 with a dual-band ESP32-C5 and a rev 3.x chip. Wi-Fi only.
flasher: p4-wifi6-db
capture: c790, c792, waveshare-19137
spec.Chip: ESP32-P4NRW32X, rev 3.x
spec.Memory: 32 MB PSRAM, 32 MB flash
spec.Size: 70 x 21 mm, 76 mm with the PCB antenna
spec.Antenna: two versions, a PCB antenna on the board or an external FPC one on a cable; tested with the FPC one
spec.Network: dual-band Wi-Fi 6 (ESP32-C5) only
spec.To the target: USB OTG on a 4-pin header
spec.Capture connector: 22-pin 0.5 mm camera connector (Pi 5 kind)
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
- The camera connector is the 22-pin 0.5 mm kind, not the WIFI6's 15-pin. The C790 and C792 have a 22-pin connector on the back and the cable for it in the box.

It has no Ethernet: Wi-Fi is the only way in, and the first boot opens the setup
hotspot. Tested on one: flashed from the browser, Wi-Fi through the C5, a 1080p30 picture from a C792, keyboard and mouse on the target. Mine is the version with the external FPC antenna.
