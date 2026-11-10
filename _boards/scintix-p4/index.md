---
title: RELOC SCINTIX P4
family: RELOC
kind: device
status: candidate
verdict: candidate
checked: 2026-11
check.psram: y
check.camera: y
check.usb: y
check.network: y
chip: 3.x
ribbon: on the carrier board (its CSI1 / CAM1 connector)
order: 950
role: Not supported yet
summary: An ESP32-P4 compute module in the Raspberry Pi CM4/CM5 form factor, with Ethernet and an ESP32-C6, that plugs into CM4 and CM5 carrier boards.
spec.Chip: ESP32-P4NRW32X, rev 3.x
spec.Memory: 32 MB PSRAM, 32 MB flash
spec.Network: 10/100 Ethernet (KSZ8091 PHY on the module), Wi-Fi 6 (ESP32-C6 over SDIO)
spec.To the target: the carrier's USB port, on the P4's high-speed controller
spec.Capture connector: MIPI-CSI, 2-lane, on the carrier's CSI1 connector
spec.Size: 55 x 40 x 5 mm
link.RELOC product page: https://www.reloc.it/products/rm-cmp4/
link.RELOC wiki: https://wiki.reloc.it/scintix-p4/
link.Carrier board guide: https://github.com/relocsrl/scintix-p4/blob/main/docs/carrier-boards.md
photo: board.webp
photo_style: product
---

The SCINTIX P4 is a module with the same connectors and pin assignment as the Raspberry Pi CM4 and CM5. It has the ESP32-P4NRW32X (rev 3.x) with 32 MB of PSRAM, an Ethernet PHY on the module and an ESP32-C6 on SDIO. The camera socket and the USB ports come from whatever carrier board it sits on.

RELOC's carrier guide answers most of what ESP-KVM needs. The module has one camera interface, CSI1, with 2 lanes, so the carrier's CAM1 connector is the one to use. CAM0 is not supported. On the Waveshare CM4 to Pi 4B adapter the camera was tested by RELOC, and its USB-C port works as a device port on the high-speed controller. That is the setup a port would start from. On the CM4 IO Board the main USB port goes to a hub, so it is a host port there.

A port would need a board definition for the module: the CSI pins, the PHY pins, the SDIO pins to the C6 and the USB routing (the J6 jumper on the module changes it). The carrier also matters: the capture board's ribbon has to fit its CAM1 socket, and its GPIO voltage has to be set to 3.3 V. I have not found a published schematic for the module.
