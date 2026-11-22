---
title: Waveshare HDMI to CSI Adapter (B)
family: Waveshare
kind: capture
status: untested
order: 40
role: The capture - RK628H, not tested yet
summary: Waveshare's adapter with a Rockchip RK628H. The driver is written but has never run on one.
bridge: RK628H
spec.Bridge: Rockchip RK628H
spec.Input: HDMI
spec.15-pin ribbon: no; a 22-to-15-pin ribbon for a board with the wide connector
spec.22-pin ribbon: yes (0.5 mm, the Pi 5 kind)
spec.24-pin ribbon (M5Stack): no
spec.ESP32-P4: rev 3.x only; the chip sends YUV422 and rev 1.x images capture RGB888
spec.HDMI audio: I2S, wired to the P4 like the C790's; never tried
spec.HDMI-CEC: through the chip's own controller, if the board wires the pin; never tried
link.Waveshare product page: https://www.waveshare.com/hdmi-to-csi-adapter-b.htm
photo: board.webp
photo_style: product
---

**Not tested on hardware. It may not work.** I do not have this board. The driver is written from what Rockchip's own Linux driver does, and every image from 0.91.0 on carries it: plug the adapter in and the firmware looks for it by itself, after the TC358743 and the LT6911D. To make it work I need the log lines tagged `rk628`, from start-up to plugging a source in.


## Good to know

- **A rev 3.x ESP32-P4.** The RK628 sends only YUV422, and the images for rev 1.x boards capture RGB888. On a rev 1.x board the log says so and the picture stays off.
- **Two lanes, 1080p.** The chip sends at 1296 Mbit/s on two lanes, which carries 1080p60. A faster source, 4K say, is scaled down to 1080p on the chip.
- **The same chip as the Radxa adapter and the WarpKVM boards**, so one driver covers all three.
