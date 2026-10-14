---
title: 0.65.0 - video over Tailscale that keeps up
description: Frame acks, so a slow link shows the newest frame instead of a queue of old ones, and a run of Tailscale fixes that took video between two ESP32-P4 devices from 1-3 fps to 11-14.
tags: video, network, tailscale
date: 2026-10-14 21:00
---

Over a slow link the device used to send frames faster than they could arrive. They queued up, and what you saw was seconds old. Now a viewer can ack each frame, and the device keeps at most two on the way to it. A slow link shows fewer frames, but always the newest one. The console acks from this release on.

The device says on the video socket that it takes acks, and a viewer only acks after that. Older firmware would read the ack as a request for a keyframe, so an old device and a new console still work together.

## Tailscale

Most of this release is the Tailscale client. Video between two ESP32-P4 devices on my Wi-Fi went from 1-3 fps to 11-14 fps at 720p. What was wrong:

- The tunnel delivers everything to one UDP socket, and it held only 6 packets. A burst of video is about 45. It holds 64 now.
- A send that timed out wrote half a WebSocket frame, and the viewer lost track of the frames. A frame now goes whole, or the socket closes.
- Every small message, a pong or an input echo, waited 200-450 ms for the ACK of the one before it. Nagle is off now.
- After one side restarted, the two could not meet again: a second handshake replaced the first before its reply came back. Now the first one is left to finish.
- The tunnel started a new handshake every 15-40 s for nothing: when it moved between the direct path and the relay, and when an idle peer did not answer its keepalives. Now a session just moves to the other path.

## Also in 0.65.0

- A viewer could be dropped when several connections came at once, for example a page load on another computer. Open video and control sockets now stay connected.
- Each connection has its own send lock, so one slow viewer no longer holds up the others.
- Settings -> Input -> Several screens draws where the captured screen sits on the whole desktop.
- Two settings bugs: a number could land in the wrong field, or be lost when typed right after another one.

Most of these fixes came out of a side project, [ESP-KVM terminal on an M5Stack Tab5](/blog/esp-kvm-terminal-on-an-m5stack-tab5/), which talks to the device over Tailscale all day.

[Release 0.65.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.65.0)
