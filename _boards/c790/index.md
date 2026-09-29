---
title: Geekworm C790
kind: capture
status: tested
order: 10
role: The capture - the one this project is built on
summary: A TC358743 HDMI to camera bridge with both camera connectors, 15-pin and 22-pin, and a ribbon for each. Fits every TC358743 board here.
bridge: TC358743
spec.Bridge: Toshiba TC358743
spec.Input: HDMI
spec.Connector: 15-pin 1.0 mm on the front, 22-pin 0.5 mm on the back; both ribbons in the box
link.Geekworm wiki page: https://wiki.geekworm.com/C790
photo: board.webp
photo_style: product
---

Turns the target's HDMI into a camera stream the ESP32-P4 can read. Any other
TC358743 capture board should do just as well - the firmware talks to that
chip, not to the board around it.

## Good to know

- **Two connectors.** The wide 15-pin one on the front is the Raspberry Pi 4 kind; the narrow 22-pin one on the back is the Pi 5 / Zero kind. Use the one that matches the board: the P4-ETH takes the 22-pin ribbon, most other boards here the 15-pin one.

- **No 1080p60.** Two CSI lanes carrying RGB cannot take more than about 81 megapixels a second, so the EDID offers 1080p at 30 Hz or lower, never a mode that would give a black screen.
- The HDMI audio comes out as I2S on a separate 5-pin connector by the HDMI socket, not on the ribbon. The firmware does not capture it yet.
- The [C792](https://wiki.geekworm.com/C792) is the same bridge with a splitter in front and should work too, though nobody here has run one. Use its 15-pin connector.
