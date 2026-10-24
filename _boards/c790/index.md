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
spec.15-pin ribbon: yes, on the front (1.0 mm, the Pi 4 kind); cable in the box
spec.22-pin ribbon: yes, on the back (0.5 mm, the Pi 5 kind); cable in the box
spec.24-pin ribbon (M5Stack): no
spec.HDMI-CEC: yes, tried with a Steam Deck, a Nintendo Switch and an Android TV box
spec.HDMI out: no
spec.HDMI audio: yes, I2S on its own 5-pin connector; three wires and a ground to the P4
spec.Size: 45 x 30 mm
spec.Measured: 1080p50 H.264 at 25 fps on the Function EV, 1080p MJPEG at 20 fps on the P4-ETH; my own figures on this site are all with this board
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
- **HDMI-CEC works.** The board wires the CEC line through to the TC358743, so the console's remote can drive a source that speaks CEC. Tried with a Steam Deck in its dock, a Nintendo Switch and an Android TV box.
- The HDMI audio comes out as I2S on a separate 5-pin connector by the HDMI socket, not on the ribbon. Geekworm puts a cable in the box. Wire SCK, SD, WFS and GND to the P4 and pick the three pins in Settings -> Audio. Tried on the Function EV.
- The [C792](/boards/c792/) is the same bridge with a splitter in front, for a target that keeps its own monitor.
