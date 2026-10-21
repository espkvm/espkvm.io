---
title: Waveshare ESP32-P4-WIFI6-POE-ETH
family: Waveshare
kind: device
status: tested
order: 50
role: The device - community-tested, PoE
summary: The first supported board that takes PoE: one cable to a KVM in a rack. 1080p H.264 at 23 fps.
flasher: p4-poe
capture: c790, c792, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x or rev 3.x (an image for each)
spec.Memory: 32 MB PSRAM, 32 MB flash
spec.Size: 68 x 55 mm
spec.Network: 100M Ethernet with PoE, Wi-Fi 6 (ESP32-C6)
spec.To the target: USB-A
spec.Capture connector: 15-pin Raspberry Pi camera connector
spec.microSD: yes
spec.Measured: 1080p H.264 at 23 fps (rev 3.x)
link.Waveshare product page: https://www.waveshare.com/esp32-p4-wifi6-poe-eth.htm
photo: board.jpg
photo_style: product
---

One cable to a KVM in a rack instead of two. The same IP101 Ethernet, microSD
wiring and ESP32-C6 as the other Waveshare boards, and a full-size USB-A port
for the target.

Confirmed by [@deltorek112](https://github.com/deltorek112) on rev 3.x silicon
with the `p4-poe-rev3` image, through Waveshare's HDMI to CSI adapter: 1080p over
H.264 at 23 fps ([#51](https://github.com/espkvm/espkvm/issues/51)).

[@dangamboa](https://github.com/dangamboa) runs one too, with the same image and adapter ([#54](https://github.com/orgs/espkvm/discussions/54)). The browser flasher could not connect to that board, and espconnect flashed it.

**PoE and the USB-A port do not mix as they are.** On PoE, the USB cable to the target must have its 5 V wire cut, or the target's port and the board's PoE supply both drive the same 5 V line. Waveshare's support confirmed it (#54). Without PoE, a normal cable is fine.

Waveshare's wiki names the rev 1.x chip and the product page the rev 3.x one,
and the one tested was rev 3.x. **Check the boot log before flashing**: it prints `chip revision:`. The
pre-3.0 image has not been run on this board yet.

Its 40-pin header has the Raspberry Pi layout, with the capture chip's I2C bus on pins 3 and 5, so a "DS3231 for Pi" clock module should plug straight onto pins 1-9 (read from the vendor pinout, not tried on this board).
