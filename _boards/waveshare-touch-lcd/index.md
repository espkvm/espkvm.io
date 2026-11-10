---
title: Waveshare ESP32-P4-WIFI6-Touch-LCD-7B
family: Waveshare
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
summary: A 7" MIPI-DSI touch display board with an ESP32-C6, a Raspberry Pi camera connector and a USB-A socket on the P4's high-speed USB.
spec.Chip: ESP32-P4NRW32X, rev 3.x
spec.Memory: 32 MB PSRAM, 32 MB flash
spec.Network: Wi-Fi 6 (ESP32-C6 over SDIO), no Ethernet
spec.To the target: USB-A (A-to-A cable, 5 V wire cut)
spec.Capture connector: 15-pin 1.0 mm camera connector, Raspberry Pi order
spec.microSD: yes
spec.Size: 164 x 97 mm
link.Waveshare product page: https://www.waveshare.com/esp32-p4-wifi6-touch-lcd-7b.htm
link.Waveshare docs: https://docs.waveshare.com/ESP32-P4-WIFI6-Touch-LCD-7B
link.Schematic: https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-7B/ESP32-P4-WIFI6-Touch-LCD-7B.pdf
photo: board.webp
photo_style: product
---

A 7" 1024x600 touch display board in Waveshare's ESP32-P4-WIFI6-Touch-LCD line. It carries Waveshare's ESP32-P4-Core module (an ESP32-P4NRW32X, so rev 3.x, with 32 MB of flash), an ESP32-C6-MINI-1 on SDIO and a microSD slot. The 7B-C is the same board sold with an OV5647 camera.

On paper it has everything ESP-KVM needs. The camera connector is a 15-pin 1.0 mm one, and in the schematic its pins follow the Raspberry Pi order: ground, data lane 0, data lane 1, clock, two GPIOs, I2C and 3.3 V. So the capture board's ribbon should plug straight in. The P4's high-speed USB goes to a USB-A socket marked USB-OTG. That socket gets 5 V through a load switch, so until the switch is checked, the lead to the target should be an A-to-A cable with the 5 V wire cut, as on the NANO.

There is no Ethernet, so the network is Wi-Fi through the C6 only. A port needs the board's pins: the C6's SDIO and reset lines, the camera I2C (shared with the touch panel and the audio codec on GPIO7 and GPIO8) and the microSD pins. They are all in the published schematic.

The other boards in the line differ. The 4.3" and 5" ones have a 15-pin 0.5 mm camera connector, which needs a 0.5 mm to 1.0 mm ribbon. The 3.5" one has a 15-pin 0.5 mm connector too. The 4B (a 4" 720x720 screen) has a 15-pin 1.0 mm camera connector, the high-speed USB on USB-C and an IP101 Ethernet PHY whose lines go only to a header, but it uses a rev 1.x ESP32-P4NRW32.
