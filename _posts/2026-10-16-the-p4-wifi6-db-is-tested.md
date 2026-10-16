---
title: The ESP32-P4-WIFI6-DB runs ESP-KVM, and the browser flasher talks to it now
description: The Waveshare ESP32-P4-WIFI6-DB is tested on hardware - Wi-Fi through its ESP32-C5, a 1080p30 picture, keyboard and mouse. On the way the browser flasher had to be fixed for boards with a CH343 USB bridge.
tags: hardware
date: 2026-10-16 20:00
image: /boards/p4-wifi6-db/board.webp
image_alt: The Waveshare ESP32-P4-WIFI6-DB in its PCB antenna version, a narrow board with the ESP32-C5 module at one end.
---

The [Waveshare ESP32-P4-WIFI6-DB](/boards/p4-wifi6-db/) has been in the catalog since September as "untested": I built its image from the schematic. Today it ran on a real board, and it works.

What I checked:

- flashed from [the site](/flash/), first boot opens the setup hotspot;
- joins a home network through the ESP32-C5, which also does 5 GHz (mine has the external FPC antenna; Waveshare also sells it with a PCB antenna);
- a 1080p30 picture from a C792 on the board's 22-pin camera connector;
- keyboard and mouse on the target, through the 4-pin USB header.

The C5 on this board comes with esp-hosted 2.12.9 and the firmware speaks 3.0.9. They agree on a compatible mode by themselves. The log still prints "major version mismatch" at boot, you can ignore it.

Power: from a laptop's USB port the board and the capture board together were too much, and the USB link dropped in the middle of flashing. Flash it without the capture board, or give it a proper 5 V supply.

## The flasher fix

The first try from the browser did not get far. The flasher synced with the chip and then stopped with "Serial data stream stopped: Possible serial noise or corruption". Python esptool on the same cable worked fine.

The flasher is esp-web-tools 10.4.0, and it carries esptool-js 0.6 inside. That version reads the chip type from a register, and over this board's CH343 USB bridge that read broke. esptool-js 0.7.0 asks the chip with a GET_SECURITY_INFO command first. I rebuilt the flasher with 0.7.0 inside, and it flashed the board on the first try. The Function EV, with the P4's own USB-JTAG, flashes with it as before.

If the browser flasher gave you that error on a board with a CH343 or a similar USB-serial chip, try it again.
