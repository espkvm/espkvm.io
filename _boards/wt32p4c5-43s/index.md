---
title: Wireless-Tag WT32P4C5-43S
family: Wireless-Tag
kind: device
status: candidate
verdict: candidate
checked: 2026-11
check.psram: y
check.camera: y
check.usb: y
check.network: y
chip: 3.x
ribbon: 15-pin, Pi order
order: 950
role: Not supported yet
summary: A 4.3" touch screen in a case, with an ESP32-P4 and an ESP32-C5 for Wi-Fi on the board behind it.
spec.Chip: ESP32-P4, rev 3.x (WT0132P4-A1-N16R32X module)
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: dual-band Wi-Fi 6 (ESP32-C5 over SDIO), no Ethernet
spec.To the target: high-speed USB-C (J5)
spec.Capture connector: 15-pin 1.0 mm (J2), Raspberry Pi order
spec.microSD: yes
spec.Screen: 4.3" 800x480 RGB, touch
link.Wireless-Tag product page: https://shop.wireless-tag.com/products/4-3-inch-dual-chip-esp32-p4-and-esp-32-c5-wi-fi6-touch-lcd-screen-wt32p4c5-43s-800x480-resolution-dual-band-esp32-display
link.Schematic: https://github.com/smartpanle/ZX4D30CE40S_V13/blob/master/doc/ZX4D30CE40S-V13.pdf
photo: board.webp
photo_style: product
---

The WT32P4C5-43S is a 4.3" touch screen in a plastic case. The board behind the screen is the ZX4D30CE40S-V13. It carries the WT0132P4-A1-N16R32X module, which is an ESP32-P4 rev 3.x with 32 MB of PSRAM, and an ESP32-C5 module for dual-band Wi-Fi.

What ESP-KVM needs is there. The camera connector J2 is a 15-pin 1.0 mm one in Raspberry Pi order. The high-speed USB goes to its own USB-C socket J5, which has the 5.1k CC resistors of a USB device port. The second USB-C socket, J10, is the full-speed port on GPIO 24 and 25. There is a microSD slot.

A port would need the Wi-Fi pins and the camera pins. The C5 talks SDIO on GPIO 28 to 34, with its enable on GPIO 28. The camera's I2C is shared with the touch panel on GPIO 14 (SDA) and GPIO 15 (SCL). The camera enable line has a 10k pull-up, and the schematic does not show it on a GPIO. ESP-KVM would not use the screen at first. There is no Ethernet.
