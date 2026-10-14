---
title: 0.65.0 - video over Tailscale that keeps up
description: Frame acks, so a slow link shows the newest frame instead of a queue of old ones, and a run of Tailscale fixes that took video between two ESP32-P4 devices from 1-3 fps to 11-14.
tags: video, network, tailscale
date: 2026-10-14 21:00
---

Over a slow link the device sent frames faster than they could arrive, they queued up, and what you saw was a few seconds old. In 0.65.0 a viewer acks each frame and the device keeps at most two on the way to it. On my Wi-Fi a client that showed about 3 fps went to 8-9. The console acks from this release on.

The device says on the video socket that it takes acks, and a viewer only acks after that. Older firmware would read the ack as a request for a keyframe, so an old device and a new console still work together.

## Tailscale

Most of this release is the Tailscale client. Video between two ESP32-P4 devices on my Wi-Fi went from 1-3 fps to 11-14 fps at 720p. What was wrong:

- The tunnel delivers everything to one UDP socket, and that socket held 6 packets. A burst of video is about 45, so most of it was dropped. The queue is 64 long.
- A send that hit its timeout wrote half a WebSocket frame and gave up, and the viewer lost track of where frames start. Each frame goes out whole, or the socket closes.
- Nagle's algorithm held every small message, a pong or an input echo, until the one before it was acked: 200-450 ms each. Turning it off was the biggest single win. The ping went from 440 ms to 15.
- After one side restarted, the two could not meet again. A second handshake replaced the first before its reply came back, so every reply was for a handshake that no longer existed.
- And the tunnel started a fresh handshake every 15-40 s for no reason, each time it moved between the direct path and the relay, or when an idle peer did not answer a keepalive. Session keys do not depend on the path, so it just moves the session.

## Also in 0.65.0

- A viewer could be dropped when several connections came at once, for example a page load on another computer. Open video and control sockets now stay connected.
- Each connection has its own send lock, so one slow viewer no longer holds up the others.
- Settings -> Input -> Several screens draws where the captured screen sits on the whole desktop.
- Two settings bugs: a number could land in the wrong field, or be lost when typed right after another one.

Most of these fixes came out of a side project, [ESP-KVM terminal on an M5Stack Tab5](/blog/esp-kvm-terminal-on-an-m5stack-tab5/), which talks to the device over Tailscale all day.

[Release 0.65.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.65.0)
