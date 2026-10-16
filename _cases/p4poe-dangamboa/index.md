---
title: ESP32-P4 IP-KVM enclosure, enhanced
author: dangamboa
summary: jrowny's box for the Waveshare ESP32-P4-WIFI6-POE-ETH, with thicker walls, a microSD slot, an SMA antenna cutout, more vents and four holes for the power and reset wires.
boards: p4-poe
photo_credit: Photo by the author.
link.Model on MakerWorld: https://makerworld.com/en/models/3407493-esp32-p4-ip-kvm-enclosure-enhanced
link.Discussion #54: https://github.com/orgs/espkvm/discussions/54
photo: case.webp
photo_style: photo
---

A remix of [jrowny's enclosure](/cases/p4poe-jrowny/) by [@dangamboa](https://github.com/dangamboa), who runs ESP-KVM on this board ([#54](https://github.com/orgs/espkvm/discussions/54)). The walls are thicker, and there are cutouts for the microSD card and the Wi-Fi SMA connector.

The four holes on the front take wires to PC817 boards inside: power and reset buttons, the power LED and ground, labelled PWR, RST, PWL and GND. That is the [power control](/boards/#control) wiring, brought out of the box. About 45 g of PLA.

On PoE, cut the 5 V wire in the USB cable to the target. The [board's page](/boards/p4-poe/) says why.
