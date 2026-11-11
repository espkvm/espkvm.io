---
title: JetKVM Mini
h1: JetKVM Mini custom firmware
page_title: JetKVM Mini custom firmware for the Mini and Mini W - ESP-KVM
description: Open-source custom firmware for the JetKVM Mini and Mini W, which are built on the ESP32-P4X. ESP-KVM has a first version for each.
kind: device
status: untested
order: 900
role: First version, testing in progress
summary: A small ready-made KVM on the ESP32-P4X, the chip ESP-KVM runs on, with Ethernet. ESP-KVM has a first version for it, still being tested.
spec.Chip: ESP32-P4X, rev 3.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Capture: HDMI in, built in (TC358743)
spec.Network: 100M Ethernet
spec.To the target: USB-C
spec.Screen: 240x240 colour (ST7789)
spec.microSD: yes
spec.Power: 5 V, 500 mA, from either USB-C port
spec.HDMI audio: no, the capture chip's audio lines are not wired to the P4
spec.Size: 42 x 42 x 23 mm
link.JetKVM product page: https://jetkvm.com/products/jetkvm-mini
flasher: jetkvm-mini
photo: board.webp
photo_style: product
---

The JetKVM Mini is a small ready-made KVM. Inside is the ESP32-P4X, the chip ESP-KVM runs on, with the same 32 MB of PSRAM and a TC358743 for the HDMI input. The box, the screen and the USB port are already there, so it makes a very nice home for ESP-KVM. Thank you, JetKVM, for building it and for publishing its firmware.

> **The first version for this device.** ESP-KVM on the Mini is new and has not been through enough testing yet. In theory nothing can break: at worst the image does not start, and you flash it again over USB. Still, a first version is at your own risk, so make the backup from the steps below first. Once it has been tested properly, I will say so here, and from then on it can be installed without any worry.

ESP-KVM has a first version for the Mini and one for the Mini W, made from the pins in JetKVM's open firmware. If you try one, tell me how it went.

## What the image uses

- The HDMI input, through the TC358743.
- Ethernet on the Mini, the ESP32-C5 for Wi-Fi on the Mini W.
- The microSD slot, for virtual media and recordings.
- The 240x240 screen, switched on from the first boot for the address and the status.
- The SW2 button on the side, for the password reset.
- The SW3 button: a press shows the next page on the screen, holding it turns the screen off or on. In Settings, Buttons it can do something else, such as press the target's power button.

## Before you flash

JetKVM's firmware only takes updates signed by JetKVM, so ESP-KVM goes on over USB:

1. In JetKVM's web interface, open Settings, Advanced and turn on USB Debugging, then restart the Mini. Without it JetKVM's firmware turns the flashing port off about two seconds after start.
2. Unplug the Mini from the target. Connect its EXT port (Power EXT, not Computer) to your computer with a USB-C cable that carries data. The Mini takes its power from that port too.
3. Check the eFuses with `espefuse.py summary`. If Secure Boot or flash encryption is on, stop: the device will not run anything unsigned.
4. Back up the whole flash: press Back up the flash on the [flasher](/flash/), or run `esptool.py read_flash 0 0x1000000 jetkvm-mini.bin`. Keep that file: it has your device's own settings and data.
5. Flash ESP-KVM from the [flasher](/flash/). Pick JetKVM Mini or JetKVM Mini W. Then plug the Computer port into the target.

## Back to JetKVM's firmware

Connect the EXT port as above and write your backup back with `esptool.py write_flash 0 jetkvm-mini.bin`. Without a backup, JetKVM has a recovery image for each model on its [recovery page](https://jetkvm.com/docs/advanced-usage/factory-reset-mini).

## Questions

### Can I put custom firmware on a JetKVM Mini?

Yes, over USB. JetKVM's firmware is open source, and its build turns on neither Secure Boot nor flash encryption. The steps above check that on your own unit before anything is written.

### Does ESP-KVM run on the original JetKVM?

No. The original JetKVM is a Linux computer on a Rockchip RV1106, and ESP-KVM is firmware for the ESP32-P4. JetKVM's own software for it is open source at [github.com/jetkvm/kvm](https://github.com/jetkvm/kvm).

### What does ESP-KVM add on the Mini?

The same firmware as on the other boards: recordings and screenshots on the microSD card, runbooks, alerts to Telegram and other places, Tailscale and WireGuard, Home Assistant. ATX power control and a serial console on pins need wires, and the Mini has no free pins for them. On the Mini all of this is a first version, as the note above says.

### Can I go back to JetKVM's firmware?

Yes. Write your backup back, or JetKVM's recovery image, as described above.

## Mini and Mini W

The two differ in the network. The Mini has 100M Ethernet. The [Mini W](/boards/jetkvm-mini-w/) has an ESP32-C5 for Wi-Fi 6 on 2.4 and 5 GHz in its place.

How ESP-KVM and the JetKVM Mini compare today is on the [comparison page](/compare/).

ESP-KVM is a separate open-source project. It is not made, sold or supported by JetKVM.
