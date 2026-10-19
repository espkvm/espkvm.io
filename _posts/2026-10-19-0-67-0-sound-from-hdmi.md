---
title: 0.67.0 - Sound from HDMI
description: The console plays the target's sound, and recordings and dashcam clips keep it. Three wires and a ground from the C790 to the board. Plus an Fn keyboard with media keys, pinch zoom on a phone, and a fix for WebRTC on a slow link.
tags: audio, console, recording, input
date: 2026-10-19 21:00
image: /assets/blog/0-67-0-sound-from-hdmi/hero.webp
---

Until now ESP-KVM gave you the picture only. You could not hear the Windows error chime, or tell whether a video on the target played with sound. In 0.67.0 the console plays the target's sound.

The HDMI signal carries the sound, and the TC358743 on the C790 takes it out and sends it as I2S on a small connector of its own, next to the HDMI socket. Geekworm puts a cable for it in the box. Three wires (SCK, SD, WFS) and a ground go to free pins on the P4 board, and you pick the pins in Settings -> Audio. The bridge drives the clocks, so the device takes whatever rate the source plays. On the Function EV the C790's cable lands on the Raspberry Pi header: GPIO 22, 27 and 53. The M5Stack PoE-P4 and its Display In module have no sound: M5Stack left the LT6911D's audio pins unconnected.

The work started from Zachary Leahan's audio code in his fork. I kept his idea and rewrote the parts that fixed the pins and the rate at build time.

## In the console

The speaker button under the picture turns the sound on. Over WebRTC it goes in the same connection as the picture. With the picture on the WebSocket it comes on a socket of its own, and the browser decodes it with WebCodecs. The device encodes nothing while nobody listens.

The encoder runs below the video, so the frame rate stays the same with the sound on.

## In recordings

A recording gets the sound as mono AAC next to the picture, in the .ts and in a dashcam clip's MP4. When the source plays nothing, the track holds silence, so picture and sound stay in step to the end. The dashcam keeps the last two minutes of sound in memory, about 1.3 MB of PSRAM, so the part of a clip from before the event has sound too.

## Also in 0.67.0

- An Fn layout on the on-screen keyboard: F1-F12, Esc, Enter and the arrows, for a BIOS, plus the media keys. Media keys on your own keyboard go to the target too, when your OS lets them through. Brightness works on a laptop's own screen, not on a monitor on HDMI.
- Pinch to zoom the picture on a phone or tablet. Two fingers move the zoomed picture.
- Over WebRTC on a slow link the picture kept freezing for a moment. A frame that took long to send let the encoder get ahead, the skipped frame asked for a keyframe, and the keyframe took even longer to send. Now the encoder waits for the send.
- Tailscale gives back 28 KB of the P4's internal RAM: three of its tasks keep their stacks in PSRAM.

[Release 0.67.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.67.0)
