---
title: Wireless-Tag WT99P4C5-S1
family: Wireless-Tag
kind: device
status: candidate
verdict: candidate
checked: 2026-11
check.psram: y
check.camera: y
check.usb: y
check.network: y
chip: ?
ribbon: 22-pin, Pi order
order: 950
role: Not supported yet
summary: A large ESP32-P4 development board with Ethernet, an ESP32-C5 for Wi-Fi, RS-485 and audio.
spec.Chip: ESP32-P4 on the WT0132P4-A1 module, rev 1.x (N16R32) or rev 3.x (N16R32X)
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet (IP101GRI), dual-band Wi-Fi 6 (ESP32-C5 over SDIO)
spec.To the target: high-speed USB-C, or the high-speed USB-A socket (one of the two at a time)
spec.Capture connector: 22-pin 0.5 mm (J10), Raspberry Pi order
spec.microSD: yes
link.Wireless-Tag product page: https://shop.wireless-tag.com/products/new-esp32-p4-development-board-wt99p4c5-s1-based-on-espressif-esp32-p4-som-module-esp32-c5-wifi6-module-support-7inch-lcd-display
link.Wireless-Tag wiki: https://wiki.wireless-tag.com/docs/en/WT99P4C5-S1/board_features.html
link.Schematic: https://res.8ms.xyz/wiki_assets/WT99P4C5-S1/SCH_WT99P4C5-S1-1V1.pdf
photo: board.webp
photo_style: product
---

The WT99P4C5-S1 is a large development board built around the WT0132P4-A1 module. It has 100M Ethernet through an IP101GRI, an ESP32-C5 module on SDIO for dual-band Wi-Fi, RS-485, an ES8311 audio codec and a microSD slot.

The camera connector J10 is a 22-pin 0.5 mm one, and the schematic shows the Raspberry Pi 22-pin order: lanes, clock, CAM_IO0 and CAM_IO1 on pins 17 and 18, I2C on 20 and 21, 3.3 V on 22. So a 22-pin Pi camera ribbon from the capture board fits. The high-speed USB goes to a USB-C socket that can work as a device, and also to a USB-A socket. The guide says to use only one of the two at a time. A third USB-C socket is the full-speed port.

The module comes in two versions, N16R32 and N16R32X. Wireless-Tag's own example tells you to check the marking and pick the chip revision to match, so the board can have either a rev 1.x or a rev 3.x P4. The guide gives 360 MHz in one place and 400 MHz in another. ESP-KVM has separate images for the two revisions, so a port needs to know which one is on the board. It would also need the camera I2C and enable pins, the Ethernet PHY pins and the C5's SDIO pins.
