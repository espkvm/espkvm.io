---
title: 0.84.0 - A safety net for network changes
description: A network change that cuts the device off now goes back by itself after 10 minutes, and a device with no network restarts on a schedule. The target can see plain USB and monitor names instead of ESP-KVM, or your own.
tags: network, security, input
date: 2026-11-14 23:00
---

A device on Wi-Fi in another building has one way back from a bad network setting: someone walks over and presses the button. Now it can come back by itself.

## A network change goes on trial

Change the Wi-Fi password, the address, the connection mode, Tailscale or WireGuard, and the device checks for the next 10 minutes that it is still on the network. The gateway has to answer. If the change touched a VPN, or was made over one, that VPN has to come up too. Opening the console in that time also keeps the change.

If none of that happens, the device puts the old settings back and restarts. I tried it with a wrong Wi-Fi password, a static address on the wrong subnet and a bad Tailscale server, and each time the device came back on its own. A change made over Tailscale or WireGuard is kept only by a sign-in over a VPN, so a console open on the local network does not keep a VPN change that broke remote access.

It is on by default: Settings, Network, Safety net.

## A network watchdog

With no working network for 30 minutes, the device restarts. If that does not help, it tries again after 1, 2 and 4 hours, then every 6 hours. If the Wi-Fi chip did not start at all, the first restarts come after 2 and 5 minutes. It does not restart during a recording or an update, or when the Ethernet cable is just unplugged.

## No logout over Tailscale

Logging out of Tailscale over Tailscale is now refused. A logout forgets the keys, and joining again needs a login link that nobody can reach over the tailnet the device has just left. Log out from the local network instead.

## What the target sees

Settings, System, "Seen by the target" has two new choices.

USB name: ESP-KVM, a plain Generic USB Device (with a USB Disk and a USB Speaker), or Custom, with your own manufacturer, product, serial number and USB IDs. ESP-KVM Tools finds the device by its USB IDs, so with other IDs it does not see it.

Monitor name: ESP-KVM, Plain (a monitor named HDMI), or Custom, with your own name, maker code, product code and serial number. This one is for boards with a TC358743. The others keep their bridge's own EDID.

## A serial number of its own

The device had the USB serial number "0", the same on every device, so two of them on one computer looked like one device to Windows. Now the serial number comes from the device's MAC address. After the update Windows finds the device once as new, and its serial port may get another COM number.

## What the target is, on the status display

The status display now shows what is plugged in: Windows, macOS, Linux, Android, a Nintendo Switch or a Steam Deck. Its mark and name are on the video page, in colour on a colour screen. A Switch and a Steam Deck name themselves over HDMI-CEC. The rest is the guess from how the target enumerated USB, the same one the console's OS button shows. On a square screen, such as the JetKVM Mini's, the mark also takes the place of ON in the USB corner.

## The TV remote with CEC off

The TV remote is in the command palette even when HDMI-CEC is off, with a button to turn it on.

## Full screen on a phone

With the bars hidden in full screen, the picture went under the camera cutout and lost its top corners. Now it starts below the cutout. With the phone on its side, the touch buttons stand in a column at the right of the picture, and the on-screen keyboard is lower, so the picture keeps more of the screen.

The full list is in the [changelog](https://github.com/espkvm/espkvm/blob/main/CHANGELOG.md).
