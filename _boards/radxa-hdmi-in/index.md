---
title: Radxa 4K HDMI IN to MIPI CSI-2 Adapter
family: Radxa
kind: capture
status: untested
order: 41
role: The capture - RK628H, not tested yet
summary: Radxa's adapter with a Rockchip RK628H and a 15-pin two-lane camera connector. The driver is written but has never run on one.
bridge: RK628H
spec.Bridge: Rockchip RK628H
spec.Input: HDMI
spec.15-pin ribbon: yes (1.0 mm, the Pi 4 kind), two lanes
spec.22-pin ribbon: no; a 15-to-22-pin ribbon for a board with the narrow connector
spec.24-pin ribbon (M5Stack): no
spec.ESP32-P4: rev 3.x only; the chip sends YUV422 and rev 1.x images capture RGB888
spec.HDMI audio: I2S, wired to the P4 like the C790's; never tried
spec.HDMI-CEC: through the chip's own controller, if the board wires the pin; never tried
spec.Size: 30 x 65 mm
link.Radxa product page: https://radxa.com/products/accessories/4k-hdmi-to-mipi-csi/
link.Radxa docs: https://docs.radxa.com/en/accessories/display/hdmi-in-to-mipi-csi2
photo: board.webp
photo_style: product
---

**Not tested on hardware. It may not work.** I do not have this board. The driver is written from what Rockchip's own Linux driver does, and every image from 0.91.0 on carries it: plug the adapter in and the firmware looks for it by itself. To make it work I need the log lines tagged `rk628`, from start-up to plugging a source in.

The adapter also has a wide 31-pin four-lane connector for 4K30. The ESP32-P4 has two lanes, so it is the 15-pin one that fits.


## Good to know

- **The reset line.** The adapter takes the chip's reset from pin 5 of the 15-pin connector, the camera's GPIO line. A board that holds that pin low keeps the chip in reset, and then the log says nothing answered on the capture bus. The board's schematic shows what that pin does.
- **A rev 3.x ESP32-P4.** The RK628 sends only YUV422, and the images for rev 1.x boards capture RGB888.
- **Two lanes, 1080p.** A 4K source is scaled down to 1080p on the chip.
