---
title: Wireless-Tag WT99P461-S1
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
summary: A large ESP32-P4 development board with Ethernet, an ESP32-C61 for Wi-Fi, RS-485 and CAN.
spec.Chip: ESP32-P4, rev 3.2 (WT01P461-S1 module)
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet (IP101), 2.4 GHz Wi-Fi 6 (ESP32-C61 over SPI)
spec.To the target: high-speed USB-A (J4, A-to-A cable, 5 V wire cut)
spec.Capture connector: 15-pin 1.0 mm (J15), Raspberry Pi order
spec.microSD: yes
link.Wireless-Tag product page: https://shop.wireless-tag.com/products/wt99p461-s1-esp32-p4-c61-dual-chips-development-board-based-on-wt01p461-s1-som-module-400mhz-dual-core-risc-v-more-interfaces
link.Wireless-Tag wiki: https://wiki.wireless-tag.com/docs/en/WT99P461-S1/board_features.html
link.Schematic: https://res.8ms.xyz/wiki_assets/WT99P461-S1/WT99P461-S1-SCH_V1.0.pdf
photo: board.webp
photo_style: product
---

The WT99P461-S1 is a large development board built on the WT01P461-S1 module, an ESP32-P4 rev 3.2 with 32 MB of PSRAM and an ESP32-C61. It has 100M Ethernet through an IP101, RS-485, CAN, audio and a microSD slot.

The camera connector J15 is a 15-pin 1.0 mm one, and the schematic shows the Raspberry Pi order: lanes and clock on pins 2 to 9, CAM_IO0 and CAM_IO1 on 11 and 12, I2C on 13 and 14, 3.3 V on 15. Ethernet gives the network, so the C61 is not needed. It talks SPI, which ESP-KVM does not support yet.

The high-speed USB goes to the USB-A socket J4. A load switch always drives 5 V onto its VBUS, as on the Waveshare NANO. So the lead to the target would be an A-to-A cable with the 5 V wire cut. The USB-C socket J3 is only full speed, and J1 is a USB-UART bridge for flashing. The microSD slot sits on SDMMC slot 1 behind an analog switch on GPIO 33. A port would need the Ethernet PHY pins, the camera I2C pins and that switch.
