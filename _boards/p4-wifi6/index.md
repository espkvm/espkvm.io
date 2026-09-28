---
title: Waveshare ESP32-P4-WIFI6
kind: device
status: tested
order: 60
role: The device - wireless only
summary: The PoE board without the wired port. Capture and USB confirmed; Wi-Fi is the only way in.
flasher: p4-wifi6
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x or rev 3.x (an image for each)
spec.Memory: 32 MB PSRAM, 32 MB flash
spec.Network: Wi-Fi 6 (ESP32-C6) only
spec.Capture: 15-pin Raspberry Pi camera connector
spec.microSD: yes
link.Waveshare product page: https://www.waveshare.com/esp32-p4-wifi6.htm
spec.To the target: USB OTG on an MX1.25 4-pin header
photo: board.webp
photo_style: product
---

Contributed by [@nwomn](https://github.com/nwomn), who has one: capture through
the C790 and the USB keyboard and mouse both work, and the expansion header is
checked against the board.

## Wiring

- USB OTG is on an **MX1.25 4-pin header**, so the target needs an MX1.25 to USB-A cable.

## Wi-Fi

Wi-Fi is the only link it has, and it used to stall: the board pulls its SDIO
lines up through 51k where Espressif ask for 10k, which lost the co-processor's
data-ready interrupt. Since 0.41.1 the chip's own pull-ups are on for this board,
and it holds. That is one board and one tester -
[#27](https://github.com/espkvm/espkvm/issues/27) if yours differs.
