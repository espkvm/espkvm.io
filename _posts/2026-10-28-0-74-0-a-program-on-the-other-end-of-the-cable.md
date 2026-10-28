---
title: 0.74.0 - A program on the other end of the cable
description: A serial port on the USB cable to the target, for the serial console or for espkvm-agent, a small program on the target. The agent gives the machine's name and addresses, the clipboard both ways and a clean shutdown. Also about 9% more MJPEG frames and fixes for slow viewers.
tags: input, console, video
date: 2026-10-28 22:00
image: /assets/blog/0-74-0-a-program-on-the-other-end-of-the-cable/hero.webp
---

Text could already go into the target: paste it in the console and the device types it. The other way there was nothing. An error message or a long path on the target's screen I retyped by hand.

## A serial port on the same cable

The target already has a USB cable to the device for the keyboard and mouse. Now it can carry a serial port as well, switched on in Settings under "Serial port over USB". Linux sees /dev/ttyACM0, Windows a COM port, macOS /dev/cu.usbmodem-something. All three have the driver built in. It is off by default and takes a restart. It can't be on together with the gamepad, the two need more USB endpoints than the P4 has.

Set it to "console" and the serial console uses this port instead of two wires to the UART. On Linux one command gives you a login there: `systemctl enable --now serial-getty@ttyACM0`.

## espkvm-agent

Set it to "agent" and the port goes to espkvm-agent, a small program for the target on Linux, Windows or macOS. A new Agent button in the console opens a window with the machine's name, OS and addresses. Send puts text on its clipboard, Get reads the clipboard back. Restart and Shut down go through the OS.

![The Agent window: the machine's name, OS and address, a clipboard box with Get and Send, Restart and Shut down.](/assets/blog/0-74-0-a-program-on-the-other-end-of-the-cable/agent-window.webp)

Reading the clipboard and power stay off until a flag on the machine itself turns them on, and the clipboard is not read while the screen is locked. Install commands, the flags and what to do when it does not connect are on [the agent's page](/agent/).

## Video

In MJPEG the encoder used to make 50 frames a second even when a viewer took 10. Now a frame is made only when some viewer is about to be ready for it. A viewer gets about 9% more frames, and the chip runs cooler.

A viewer on a slow link (a VPN, weak Wi-Fi) could restart the device. The send kept retrying a full socket without a pause until the watchdog fired. The same viewer held up everyone else too, because frames went out to viewers one by one. Now each viewer has its own sender.

Several viewers at once over Wi-Fi could also trip the watchdog, in the encryption or in the Wi-Fi driver. TLS writes now go one at a time, and the driver's short waits sleep instead of spinning.

[Release 0.74.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.74.0)
