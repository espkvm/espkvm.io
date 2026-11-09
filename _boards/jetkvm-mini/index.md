---
title: JetKVM Mini
page_title: JetKVM Mini custom firmware - open-source ESP-KVM for the Mini and Mini W
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
spec.HDMI audio: no, the capture chip's audio lines are not wired to the P4
spec.Size: 42 x 42 x 23 mm
link.JetKVM product page: https://jetkvm.com/products/jetkvm-mini
flasher: jetkvm-mini
photo: board.webp
photo_style: product
---

The JetKVM Mini is a small ready-made KVM. Inside is the ESP32-P4X, the chip ESP-KVM runs on, with the same 32 MB of PSRAM and a TC358743 for the HDMI input. The box, the screen and the USB port are already there, so it makes a very nice home for ESP-KVM. Thank you, JetKVM, for building it and for publishing its firmware.

> **The first version for this device.** ESP-KVM on the Mini is new and has not been through enough testing yet. In theory nothing can break: at worst the image does not start, and you flash it again over USB. Still, a first version is at your own risk, so keep the backup from the steps below: it is the only way back to the stock firmware. Once it has been tested properly, I will say so here, and from then on it can be installed without any worry.

ESP-KVM has a first version for the Mini and one for the Mini W, made from the pins in JetKVM's open firmware. If you try one, tell me how it went.

## What the image uses

- The HDMI input, through the TC358743.
- Ethernet on the Mini, the ESP32-C5 for Wi-Fi on the Mini W.
- The microSD slot, for virtual media and recordings.
- The 240x240 screen, switched on from the first boot for the address and the status.
- The SW2 button on the side, for the password reset.
- The SW3 button: a press shows the next page on the screen, holding it turns the screen off or on. In Settings, Buttons it can do something else, such as press the target's power button.

## Before you flash

The stock firmware only takes updates signed by JetKVM, so ESP-KVM goes on over USB:

1. Check the eFuses with `espefuse.py summary`. If Secure Boot or flash encryption is on, stop: the device will not run anything unsigned.
2. Turn on "USB debugging" in JetKVM's settings. Without it the stock firmware switches the USB Serial/JTAG port off at start.
3. Back up the whole flash: press Back up the flash on the [flasher](/flash/), or run `esptool.py read_flash 0 0x1000000 jetkvm-mini.bin`. Keep that file: it is the only way back to the stock firmware.
4. Flash ESP-KVM from the [flasher](/flash/). Pick JetKVM Mini or JetKVM Mini W.

## Mini and Mini W

The two differ in the network. The Mini has 100M Ethernet. The [Mini W](/boards/jetkvm-mini-w/) has an ESP32-C5 for Wi-Fi 6 on 2.4 and 5 GHz in its place.

How ESP-KVM and the JetKVM Mini compare today is on the [comparison page](/compare/).

ESP-KVM is a separate open-source project. It is not made, sold or supported by JetKVM.
