---
title: WarpKVM rk628-22p
family: WarpKVM
kind: capture
status: untested
order: 42
role: The capture - open hardware, RK628H, not tested yet
summary: An open-hardware RK628H board with a 22-pin connector, schematics and gerbers published. The driver is written but has never run on one.
bridge: RK628H
spec.Bridge: Rockchip RK628H
spec.Input: HDMI
spec.15-pin ribbon: no; a 22-to-15-pin ribbon for a board with the wide connector
spec.22-pin ribbon: yes (0.5 mm), wired for four lanes; ESP-KVM uses two
spec.24-pin ribbon (M5Stack): no
spec.ESP32-P4: rev 3.x only; the chip sends YUV422 and rev 1.x images capture RGB888
spec.HDMI audio: I2S header, wired to the P4 like the C790's; never tried
spec.HDMI-CEC: through the chip's own controller, if the board wires the pin; never tried
spec.Size: 45 x 30 mm
link.Design files on GitHub: https://github.com/WarpKVM/rk628-bridge-boards
photo: board.webp
photo_style: product
---

**Not tested on hardware. It may not work.** I do not have this board. The driver is written from what Rockchip's own Linux driver does, and every image from 0.91.0 on carries it. To make it work I need the log lines tagged `rk628`, from start-up to plugging a source in.

The WarpKVM team published three RK628 boards as open hardware, under CERN-OHL-S. The 22-pin one is the one an ESP32-P4 board takes. The 30-pin one fits no ESP32-P4 board I know, and the two-link one is for 4K60, which two lanes cannot carry.


## Good to know

- **RK628H, not RK628D.** The design takes either chip. This driver knows only the F/H generation: an RK628D is found, named in the log and left alone.
- **A rev 3.x ESP32-P4.** The RK628 sends only YUV422, and the images for rev 1.x boards capture RGB888.

The photo is WarpKVM's, from their repository (CERN-OHL-S-2.0).
