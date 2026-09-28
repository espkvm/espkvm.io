---
title: Waveshare HDMI to CSI Adapter
kind: capture
status: tested
order: 20
role: The capture - community-tested
summary: The same TC358743 bridge on Waveshare's board, with a full-size HDMI input.
bridge: TC358743
spec.Bridge: Toshiba TC358743
spec.Input: full-size HDMI
spec.Connector: 15-pin Raspberry Pi camera ribbon (also powers it)
spec.Measured: 1080p H.264 at 23 fps on the WIFI6-POE-ETH
link.Waveshare wiki page: https://www.waveshare.com/wiki/HDMI_to_CSI_Adapter
photo: board.webp
photo_style: product
---

Waveshare's product 19137. The firmware treats it exactly like the C790. A user
confirmed it on the ESP32-P4-WIFI6-POE-ETH: 1080p over H.264 at 23 fps.
