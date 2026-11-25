---
title: 0.92.0 - JetKVM's OS Services, and Redfish
description: ESP-KVM takes the target's screen over USB from JetKVM's open-source OS Services, a contribution by Ruben Jongejan. Also Redfish for server tools, and a click anywhere on the picture to take control.
tags: video, power, console
date: 2026-11-25 21:00
image: /assets/blog/0-92-0-jetkvm-os-services-and-redfish/hero.webp
---

In September JetKVM published [OS Services](https://github.com/jetkvm/os-services): a small program for the target computer that captures its screen, encodes it and sends it to the KVM over the USB cable. It is MIT-licensed, and its protocol is meant to be vendor-neutral, so any KVM can take it. Ruben Jongejan made ESP-KVM one of them ([#103](https://github.com/espkvm/espkvm/pull/103)).

## What it gives

The picture comes from the target itself, not through HDMI. No HDMI cable is needed, and the screen stays sharp, because the target encodes its own desktop. When the program stops, the console goes back to HDMI.

OS Services runs on Windows 11, on macOS with Apple silicon and on Linux. It does more than video: a clipboard, a terminal and file transfer. ESP-KVM takes the video only for now. The clipboard both ways and a clean shutdown already come from [ESP-KVM Tools](/espkvm-tools/), and both work over the same USB cable at the same time.

## How to use it

It is built in on the wired JetKVM Mini. Other boards can turn it on at build time, with `CONFIG_KVM_ENABLE_USB_VIDEO`.

1. Install OS Services on the target. JetKVM's installers for Windows, macOS and Linux are on [jetkvm.com/os-services/install](https://jetkvm.com/os-services/install). Or let ESP-KVM hand it over as a disc: in the Media panel, choose an image at a URL and give it `https://os-services.jetkvm.com/jetkvm-os-services.iso`. The target sees a CD with all three installers, read from JetKVM's server as it goes, with nothing copied to the card.
2. In the console: Settings, Video, USB screen sharing, "Allow USB video". The target's USB reconnects once, and the target may ask you to allow the new device.
3. Pair it. The console shows a fingerprint, so compare it before you approve the device on the computer. On Linux the question needs zenity or kdialog. Without them it never shows up, and `--approve-kvm <fingerprint>` approves the device from the command line.

The device takes up to 1920x1200 at 30 fps. It is off again after every restart, and it takes no memory while off. While it runs, screen text, screen areas, MJPEG and screenshots are off, since they need the HDMI picture.

Ruben tested the picture on his JetKVM Mini with a Mac. I tested the rest on a P4-ETH: the USB interface comes and goes with the switch, and the memory comes back when it is off. On my Linux laptop it paired but sent no picture: KDE Plasma 6.6 on Wayland gives a 10-bit screen, and OS Services cannot encode it yet.

## Redfish

If you do not know why you would want Redfish, you do not need it. The console does everything it does.

Servers have a BMC, such as iDRAC on a Dell or iLO on an HP. Tools that set up machines in bulk talk to it over Redfish: MAAS, OpenStack Ironic, Metal3, Ansible. They switch a machine on, put an installer in its virtual drive and reboot it. A desktop has no BMC. With Redfish on, an ESP-KVM next to it answers those calls.

- **Power.** With the ATX wiring it presses the power and reset buttons. Without it, only "On", through Wake-on-LAN and the USB wake signal.
- **Virtual media.** `InsertMedia` takes an image URL, and the target boots it straight from the web server.

```
curl -k -u admin:PASSWORD -H 'Content-Type: application/json' \
  -d '{"Image":"https://example.com/debian.iso"}' \
  https://espkvm.local/redfish/v1/Managers/1/VirtualMedia/Cd/Actions/VirtualMedia.InsertMedia
```

It has a password of its own, which opens power and virtual media and nothing else. It is off by default: Settings, Security, Redfish. I checked it with curl, redfishtool and sushy, the client OpenStack Ironic uses. A 3 MB ISO inserted from sushy reached the target as a CD of exactly that size. The power buttons over Redfish have not pressed anything real yet, since I have no ATX wiring on the bench. The calls are in [docs/API.md](https://github.com/espkvm/espkvm/blob/main/docs/API.md#redfish).

## Click anywhere

Settings, Input, Pointer, "Start controlling on" now has "Click anywhere": any click on the picture takes control, with no button over the picture. The first click only moves the pointer there, so nothing on the target gets clicked by accident.

The release: [v.0.92.0](https://github.com/espkvm/espkvm/releases/tag/v.0.92.0).
