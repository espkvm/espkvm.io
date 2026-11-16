---
name: VNC
title: ESP-KVM with a VNC client
page_title: VNC for an ESP32-P4 IP-KVM, TigerVNC over TLS in H.264 - ESP-KVM
description: Turn on the VNC server and TigerVNC shows the target's screen and drives its keyboard and mouse over TLS, with the same H.264 stream as the browser.
tip: VNC, with TigerVNC in H.264
summary: TigerVNC over TLS, with the browser's H.264 stream.
mark: mark.svg
order: 11
link.VNC in the API docs: https://github.com/espkvm/espkvm/blob/main/docs/API.md#vnc
link.VNC in H.264, the post: /blog/0-86-0-vnc-as-fast-as-the-browser/
---

The device has a VNC server, written by Jan Heil. A VNC client shows the target's screen and sends it the keyboard and the mouse, next to the browser console or instead of it. It is off by default.

## Setting it up

1. In the console open Settings, Video, VNC server.
2. Set a password of up to 8 characters. That is a limit of VNC's own sign-in, so use all 8.
3. Turn on VNC server. The port is 5900.
4. Point the client at the device's address.

A script can ask `POST /api/v1/vnc/session` for a password that works once, within 60 seconds.

## Clients

TigerVNC gets the same H.264 stream as the browser: 26 fps at 1080p on a JetKVM Mini. It needs a build with H.264, version 1.13 or newer (the Windows builds have it, on Linux it needs FFmpeg), and H.264 as the stream codec on the device: Settings, Video, Picture. Other clients get JPEG, about 20 fps at 1080p on the same Mini.

A client needs Tight encoding for JPEG, and VeNCrypt for TLS. These have both:

| Client | Runs on | Picture | Get it |
|---|---|---|---|
| TigerVNC | Windows, Linux, macOS | H.264 or JPEG | [tigervnc.org](https://tigervnc.org/) |
| TurboVNC | Windows, Linux, macOS | JPEG | [turbovnc.org](https://turbovnc.org/) |
| Remmina | Linux | JPEG | [remmina.org](https://remmina.org/) |
| AVNC | Android | JPEG | [F-Droid](https://f-droid.org/packages/com.gaurav.avnc/), [Google Play](https://play.google.com/store/apps/details?id=com.gaurav.avnc) |
| bVNC | Android | JPEG | [Google Play](https://play.google.com/store/apps/details?id=com.iiordanov.freebVNC), [source](https://github.com/iiordanov/remote-desktop-clients) |
| MultiVNC | Android | JPEG | [F-Droid](https://f-droid.org/packages/com.coboltforge.dontmind.multivnc/), [Google Play](https://play.google.com/store/apps/details?id=com.coboltforge.dontmind.multivnc) |

RealVNC Viewer and the screen sharing app on a Mac have no Tight encoding, so they cannot connect.

## From outside

VNC is plain TCP on port 5900. It does not find its way through NAT like the browser's WebRTC does. Reach it over Tailscale or WireGuard, both built into the firmware, and keep plain VNC without TLS on your own network.

## One client at a time

A new client that signs in takes over from the one before it, and a wrong password does not end the session. The console lists the VNC client with the other viewers. Clients that come over the device's own hotspot are turned away unless VNC over the hotspot is on.
