---
title: 0.24.0 - point a phone at the screen to get in
description: The round LCD shows the rescue hotspot as a QR code, the certificate finally names the address DHCP gave the device, and the reset button shows that it heard you.
tags: display, network, security, video
date: 2026-08-18
image: /assets/blog/0-24-0-point-a-phone-at-it/qr.webp
---

The rescue hotspot exists because the device cannot be reached any other way -
which also means nothing can hand you its password. Now the panel does: when the
hotspot is up, the round LCD gives its whole face to a QR code. Point a phone at
it and it joins. Small mono OLEDs sit this one out, because a code that size is
not something a phone can focus on.

**The certificate names the DHCP address.** Only a static address was ever put
in the certificate, so typing the IP of a device on DHCP landed on an untrusted
page. You could click through for the console, but not for the video: a browser
refuses a `wss://` stream to a mismatched certificate and gives you no way to
accept it. The address is recorded when it arrives and named from the next
restart.

**The button says it heard you.** Holding the board button to clear a forgotten
password used to be a gesture into the void - no light, no message, no way to
tell if the button was even wired. The panel now fills a ring around its rim as
you hold, empties it if you let go too early, and says what it cleared.

Two fixes underneath: the round LCD's framebuffer was not aligned the way the
SPI driver wants, so every frame was copied through internal memory - and this
chip has about half a megabyte of that, shared with TLS, USB, networking and the
video encoder. Turning on a display could take the video down. And when the
H.264 encoder cannot get its large contiguous block, the device now says so once,
with the actual memory figures, and carries on in MJPEG instead of retrying
thirty times a second forever.

[Release v.0.24.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.24.0)
