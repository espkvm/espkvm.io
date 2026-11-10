---
title: Osprey OspreyPi-P4C5-Module
family: Osprey
kind: device
status: candidate
verdict: candidate
checked: 2026-11
check.psram: y
check.camera: y
check.usb: y
check.network: y
chip: ?
ribbon: 15-pin 1.0 mm, Pi pinout (per the maker)
order: 950
role: Not supported yet
summary: An ESP32-P4 core board with a dual-band ESP32-C5, a Raspberry Pi style camera connector and high-speed USB on a Type-C or Type-A socket.
spec.Chip: ESP32-P4 with 32 MB PSRAM in the package, rev not known
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: dual-band Wi-Fi 6 (ESP32-C5). No Ethernet PHY, RMII pins only on the headers
spec.To the target: USB 2.0 high-speed, switched between a USB-C and a USB-A socket (TS3USB221)
spec.Capture connector: 15-pin 1.0 mm MIPI-CSI on the back, Raspberry Pi pinout, plus a 24-pin 0.5 mm CSI connector on the front
spec.Size: 72 x 52 mm
link.Osprey datasheet (PDF): https://ae-pic-a1.aliexpress-media.com/kf/Sd6c810d0f5e04b86bc41f68714910c3fX.pdf?file=Sd6c810d0f5e04b86bc41f68714910c3fX.pdf
photo: board.webp
photo_style: product
---

Osprey Optoelectronics (brand osptek) makes this base board for two plug-in core boards: one with an ESP32-C6 and one with a dual-band ESP32-C5. Board revision 1.3 takes either. The ESP32-P4 has 32 MB of PSRAM in the package, with 16 MB of flash next to it. The photo shows the C6 version, the base board is the same. It is also sold as the Maker Go ESP32P4C5 core board.

What fits ESP-KVM: the maker's datasheet says the 15-pin 1.0 mm camera connector on the back is compatible with the Raspberry Pi interface, so the capture board's ribbon should fit. The high-speed USB goes through a TS3USB221 switch to either the USB-C socket or the USB-A socket. The USB-C socket would be the lead to the target, as long as the switch is set to it. The second USB-C socket is a CH343 serial port for flashing.

What is not known: the chip revision of the C5 core board (the C6 core board in the datasheet photo is marked NRW32, rev 1.x), how the C5 is wired to the P4 (SDIO is the usual way, but the datasheet does not say), and which GPIO drives the USB switch. The datasheet names a schematic but the copy I found does not include it. A port needs those pins first.
