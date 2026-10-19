---
title: Geekworm C792
kind: capture
status: tested
order: 11
role: The capture, with an HDMI pass-through for a local monitor
summary: The same TC358743 bridge as the C790, with a GSV2001 splitter in front of it. A second HDMI port passes the picture on to a monitor at the target.
bridge: TC358743
spec.Bridge: Toshiba TC358743, behind a GSV2001 splitter
spec.Input: HDMI, up to 4K60; 4K is scaled down to 1080p at the same refresh rate
spec.HDMI out: pass-through (VIDEO-OUT), the same picture as the input; not tried yet
spec.HDMI audio: I2S on its own connector, as on the C790; not tried on this board
spec.15-pin ribbon: yes, on the front (1.0 mm, the Pi 4 kind); cable in the box
spec.22-pin ribbon: yes, on the back (0.5 mm, the Pi 5 kind); cable in the box
spec.24-pin ribbon (M5Stack): no
spec.Power: its own 5 V input, cable in the box
spec.Size: 56 x 56 mm
spec.Measured: 1080p30 picture on the ESP32-P4-WIFI6-DB, with no monitor on VIDEO-OUT
link.Geekworm wiki page: https://wiki.geekworm.com/C792
photo: board.webp
photo_style: product
---

For a target that should keep its own monitor. The splitter sends the HDMI picture to the TC358743 and to the VIDEO-OUT port at the same time, so the screen on the desk shows the same thing the console does. The firmware talks to the TC358743, so it needs nothing new for this board.

## Good to know

- **The monitor changes the EDID.** I have not tried this part yet; it is what the splitter's design says. With a monitor on VIDEO-OUT, the source reads that monitor's EDID instead of the one ESP-KVM offers, and may pick 1080p60. Two CSI lanes cannot carry that: there is no picture, and the console says the mode is too fast. Set the source to 1080p30 or 720p60, or unplug the monitor and let the source read the EDID from ESP-KVM.
- **4K becomes 1080p, not slower.** A 4K60 source arrives as 1080p60, which is again too fast. 4K30 arrives as 1080p30 and works.
- **Power it from its own 5 V input.** Geekworm asks for it for stable operation.
- **Use the connector that fits the board,** as with the C790: the 22-pin ribbon for the P4-ETH, the 15-pin one for most other boards.
- The I2S audio comes out on its own connector, as on the C790. Wired the same way it should work; not tried on this board yet.
