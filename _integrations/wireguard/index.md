---
name: WireGuard
title: ESP-KVM over WireGuard
page_title: WireGuard IP-KVM, with the client in the firmware - ESP-KVM
description: ESP-KVM has a WireGuard client in its firmware. It connects to a WireGuard server of yours and answers at its tunnel address, while the console stays open on the local network too.
tip: WireGuard client, to a hub of your own
summary: A split tunnel to a WireGuard hub of your own.
mark: mark.svg
order: 3
link.Setup guide: https://github.com/espkvm/espkvm/blob/main/docs/SETUP.md#reaching-it-from-outside-tailscale-or-wireguard
link.Try the console: https://demo.espkvm.io/
---

There is no Linux on this KVM, so the WireGuard client is part of the firmware. The device connects to one WireGuard server, your hub, and from any machine on that VPN the console opens at the device's tunnel address. If you have no WireGuard server and do not want one, [Tailscale](/integrations/tailscale/) is built in too. Only one of the two runs at a time. WireGuard is off by default.

## What you need

- A WireGuard server the device can reach: a router with WireGuard, a VPS, a home server with a port forwarded to it.
- A free address on the tunnel network for the device, such as `10.9.0.2`.

## Setting up the device

1. In the console open Settings, VPN, and find WireGuard.
2. Fill in Tunnel address, Peer public key (the server's public key) and Peer endpoint, such as `vpn.example.com:51820`.
3. Leave Private key empty. The device makes its own key and shows the public half below the fields.
4. Turn on Enable WireGuard and save.

## Setting up the server

Add the device as a peer, with the public key the console shows:

```
[Peer]
PublicKey = <the device's public key>
AllowedIPs = 10.9.0.2/32
```

Reload WireGuard on the server. The device keeps the connection open with a keepalive every 25 seconds, so a router on its side does not forget the mapping.

## How the traffic goes

It is a split tunnel. Only the tunnel network, taken as a /24 around the tunnel address, goes through WireGuard. Everything else, the local network and the console on it, stays as it was, so turning WireGuard on cannot lock you out of the device on the LAN.

The video works through the tunnel on both codecs. WebRTC sends H.264 in packets small enough to fit in it.

## Good to know

- WireGuard handshakes carry a timestamp, and the server refuses one older than the last it saw. A board with no clock starts from zero after a restart. Turn on Sync time over SNTP if the device can reach an NTP server, or use a board with a real-time clock.
- The private key stays on the device and is never sent back to the console.
