---
name: Tailscale
title: ESP-KVM on your tailnet
page_title: Tailscale IP-KVM, built into the firmware - ESP-KVM
description: ESP-KVM has a Tailscale client in its firmware. The KVM joins your tailnet by itself and answers at its 100.x address or MagicDNS name from anywhere, with no port forward, no gateway and no VPS.
tip: Tailscale, built in
summary: Joins your tailnet from the firmware. No port forward, no gateway.
mark: mark.svg
order: 2
link.Setup guide: https://github.com/espkvm/espkvm/blob/main/docs/SETUP.md#reaching-it-from-outside-tailscale-or-wireguard
link.The client, microlink: https://github.com/espkvm/microlink
---

There is no Linux on this KVM to install Tailscale on, so the client is part of the firmware. The device joins your tailnet like any other node, and the console opens at its tailnet address from a laptop or a phone anywhere. Nothing on your router changes. Tailscale is off by default.

## Setting it up

1. In the console open Settings, VPN, and turn on Enable Tailscale. Leave the auth key empty.
2. The VPN tab shows Sign in to Tailscale. The link opens Tailscale's page: approve the device with your account.
3. A few seconds later the device is on the tailnet, at a 100.x address and its MagicDNS name.

An auth key still works, for a device set up without a browser. Log out of the tailnet makes the device forget its keys, and the next start asks again.

## What it does with the tailnet

- **A trusted certificate.** With MagicDNS and HTTPS certificates on in the Tailscale admin console, Trusted certificate (Let's Encrypt) gets a certificate for the device's tailnet name, such as `espkvm.tailnet.ts.net`. Any browser on the tailnet trusts it with nothing to import. It renews by itself, and no domain or open port is needed.
- **Sign in by who you are.** Sign in these tailnet users and Let these tailnet users watch take Tailscale logins. A browser on one of their devices is signed in as the owner or as a viewer, with no password. It works once a password of your own is set.
- **Console only over Tailscale.** The console then answers only to tailnet addresses. The setup hotspot still works, and when Tailscale is down the console answers on the LAN again, so a broken tailnet does not lock you out.
- **The tailnet's access rules.** The device follows the ACLs set in the admin console.
- **Peers.** The VPN tab lists the other devices on the tailnet, whose they are, whether traffic goes straight or through a relay, and the round trip. A slow console over Tailscale is usually a relay.
- **The key's expiry.** The VPN tab shows when the node key runs out, and a notification comes 14 days before, or as many as you set.
- **Headscale.** Control server takes a self-hosted control plane, such as Headscale or Ionscale, in place of Tailscale's own.

## Good to know

- Tailscale and WireGuard are both built in, and one of them runs at a time.
- The client is microlink, a Tailscale client written in C for microcontrollers. ESP-KVM uses its own fork of it.
