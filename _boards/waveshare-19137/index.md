---
title: Waveshare HDMI to CSI Adapter
family: Waveshare
kind: capture
status: tested
order: 20
role: The capture - community-tested
summary: The same TC358743 bridge on Waveshare's board, with a full-size HDMI input.
bridge: TC358743
spec.Bridge: Toshiba TC358743
spec.Input: full-size HDMI
spec.Connector: 15-pin Raspberry Pi camera ribbon only (also powers it)
spec.HDMI-CEC: same chip as the C790; not tried on this board
spec.Measured: 1080p H.264 at 23 fps on the WIFI6-POE-ETH
link.Waveshare wiki page: https://www.waveshare.com/wiki/HDMI_to_CSI_Adapter
photo: board.webp
photo_style: product
---

Waveshare's product 19137. The firmware treats it exactly like the C790.

It has only the wide 15-pin connector. On a board with the narrow 22-pin one -
the [ESP32-P4-ETH](/boards/p4-eth/) - it needs a 15-to-22-pin ribbon, the kind
sold as a Raspberry Pi 5 camera cable. A user
confirmed it on the ESP32-P4-WIFI6-POE-ETH: 1080p over H.264 at 23 fps.
