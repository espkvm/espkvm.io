---
title: Wireless-Tag WTDKP4C5-S1
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
summary: A small ESP32-P4 development board on the WT01P4C5-S1 module, which has an ESP32-C5 for dual-band Wi-Fi.
spec.Chip: ESP32-P4 on the WT01P4C5-S1 module, rev 1.x (N16R32) or rev 3.x (N16R32X)
spec.Memory: 32 MB PSRAM in the N16R32 module (an N16R16 module with 16 MB also exists), 16 MB flash
spec.Network: dual-band Wi-Fi 6 (ESP32-C5 over SDIO), Ethernet only with an external PHY on the header
spec.To the target: high-speed USB-C (J1)
spec.Capture connector: 22-pin 0.5 mm (J4), Raspberry Pi order
spec.microSD: no
link.Wireless-Tag product page: https://shop.wireless-tag.com/products/small-size-esp32-p4-esp32-c5-dual-chips-development-board-wtdkp4c5-s1-based-on-esp32p4c5-core-board-wi-fi6-wifi-ble-module-support-7inch-lcd-screen
link.Wireless-Tag wiki: https://wiki.wireless-tag.com/docs/en/WTDKP4C5-S1/board_features.html
link.Schematic: https://res.8ms.xyz/wiki_assets/WTDKP4C5-S1/WTDKP4C5-S1-1V3_SCH_V1.1.pdf
photo: board.webp
photo_style: product
---

The WTDKP4C5-S1 is a small board around the WT01P4C5-S1 module. The module holds both the ESP32-P4 and an ESP32-C5, linked over SDIO, so Wi-Fi works on 2.4 and 5 GHz. It takes power from USB-C or a 12 V jack.

The camera connector J4 is a 22-pin 0.5 mm one, and the schematic shows the Raspberry Pi 22-pin order. The high-speed USB goes to USB-C J1, which the guide says can work as a USB device. Both fit ESP-KVM.

The module is made with 16 or 32 MB of PSRAM, and ESP-KVM needs the 32 MB one. Wireless-Tag's example also names two versions, N16R32 and N16R32X, so the P4 can be rev 1.x or rev 3.x, and the marking tells which. There is no microSD slot, so virtual media and recordings would have nowhere to go. There is no Ethernet on the board. The header brings out the P4's EMAC pins for an external PHY. A port would need the camera I2C and enable pins and the C5's SDIO pins.
