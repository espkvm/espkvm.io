---
title: Wireless-Tag WT9932P4C61-TINY
family: Wireless-Tag
kind: device
status: candidate
verdict: maybe
checked: 2026-11
check.psram: y
check.camera: y
check.usb: y
check.network: ?
chip: 3.x
ribbon: 15-pin, Pi order
order: 950
role: Not supported yet
summary: A narrow 33 x 69 mm ESP32-P4 board with an ESP32-C61 for Wi-Fi, made to sit in a breadboard.
spec.Chip: ESP32-P4, rev 3.x (WT01P461-S1 module)
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 2.4 GHz Wi-Fi 6 (ESP32-C61 over SPI), no Ethernet
spec.To the target: high-speed USB-C (J10)
spec.Capture connector: 15-pin 1.0 mm (J2), Raspberry Pi order
spec.microSD: yes
spec.Size: 33 x 69 mm
link.Wireless-Tag product page: https://shop.wireless-tag.com/products/wireless-tag-wt9932p4c61-tiny-esp32-p4-esp32-c61-tiny-size-esp32-development-board-based-on-esp32-p4-c61-wi-fi6-module-iot-development-board-series
link.Wireless-Tag wiki: https://wiki.wireless-tag.com/docs/en/WT9932P4C61-TINY/board_features.html
link.Schematic: https://res.8ms.xyz/wiki_assets/WT9932P4C61-TINY/WT9932P4C61-TINY_SCH_V1.0.pdf
photo: board.webp
photo_style: product
---

The WT9932P4C61-TINY is a narrow board for a breadboard, built on the WT01P461-S1 module. The module has an ESP32-P4 rev 3.x with 32 MB of PSRAM and an ESP32-C61 for 2.4 GHz Wi-Fi.

The capture side fits. The camera connector J2 is a 15-pin 1.0 mm one, and Wireless-Tag says it uses the Raspberry Pi pin order. The high-speed USB has its own USB-C socket, J10, with the 5.1k CC resistors of a device port. The other USB-C socket, J9, is the full-speed port on GPIO 24 and 25. There is a microSD slot.

The network is the problem. There is no Ethernet, and the C61 talks to the P4 over SPI. ESP-KVM only runs Wi-Fi chips over SDIO today, so this board needs SPI support for the co-processor first.
