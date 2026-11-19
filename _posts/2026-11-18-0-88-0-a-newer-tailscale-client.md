---
title: 0.88.0 - A newer Tailscale client, and signed releases
description: The Tailscale client moves onto current upstream microlink. Classic WireGuard now answers through its tunnel, and every release is signed.
tags: vpn, tailscale, security, update
date: 2026-11-18 23:00
image: /assets/blog/0-88-0-a-newer-tailscale-client/hero.webp
---

ESP-KVM's Tailscale client, microlink, moves from my old fork onto current upstream, with my changes on top. Classic WireGuard now answers through its tunnel. And release files are signed.

## A newer Tailscale client

Upstream fixed several security bugs in the WireGuard and Noise code: endpoint takeover by another peer, nonce reuse, a buffer overflow on a malformed Noise reply. On top go 25 small commits of mine: the sign-in link, peer owners and paths on the VPN tab, the tailnet HTTPS certificate, Headscale support, DERP retries, TOS 0 for Wi-Fi through the ESP32-C6. I plan to send the general ones upstream.

| Board | Over the tailnet | For comparison |
| --- | --- | --- |
| JetKVM Mini, Ethernet | 23.2 fps, H.264 1080p | 23.4 fps, old client |
| P4-ETH rev 1.3, Ethernet | 5.5 fps, MJPEG 1080p | 4.6 fps, old client |
| Function EV, Wi-Fi | 22.6 fps, H.264 1080p | 25.2 fps on the LAN |

Through a DERP relay only, with UDP blocked on the other side, the console opened in 0.6 s and files came at 300-370 KB/s.

Headscale auth keys are 89 characters long and did not fit the 63-character field. It now takes 127.

## WireGuard through the tunnel

The tunnel was never added to lwIP's list of interfaces, so replies to the hub left through the normal network port and were lost. Now it is in the list. On a P4-ETH rev 1.3 at 1080p, H.264 gets 7.2 fps through the tunnel, the same as on the LAN.

WireGuard also sent nothing if Tailscale had run since the last restart: a flag set by the Tailscale client stayed on. Now switching between the two in Settings works without a restart.

## Signed releases

`sha256sums.txt` now lists every file of a release, and `sha256sums.txt.minisig` signs it. CI holds the private key. The public key is in `minisign.pub`:

```
RWT4vgu3y5NjVA5BZXZvWztNO983re08arr7Q+YZKb7G+xeXpm3m1fcg
```

Check a download offline:

```
minisign -Vm sha256sums.txt -P RWT4vgu3y5NjVA5BZXZvWztNO983re08arr7Q+YZKb7G+xeXpm3m1fcg
sha256sum -c --ignore-missing sha256sums.txt
```

This was asked [in Discussions](https://github.com/orgs/espkvm/discussions/101), together with Secure Boot. Secure Boot stays off in release images: it burns eFuses for good, and I want the board to stay a normal ESP32-P4 you can flash with anything later. Build from source to turn it on with your own key.

## Also

- [docs/TROUBLESHOOTING.md](https://github.com/espkvm/espkvm/blob/main/docs/TROUBLESHOOTING.md#a-vga-dvi-or-displayport-target) explains DisplayPort adapters: passive ones need a DP++ port, USB-C ones are always active.
- The JetKVM Mini and Mini W are in the README board list.
