---
title: 0.14.0 - WireGuard, and an API simple enough for a script
description: Reach the KVM over a WireGuard tunnel without opening a port, and drive the target with plain HTTP calls instead of a binary protocol.
tags: vpn, api, network
date: 2026-07-31
image:
---

**WireGuard.** The device can join a WireGuard peer over its existing network
connection, off by default. It is a split tunnel: only the device's own tunnel
address goes through WireGuard, so the console stays reachable on the local
network at the same time. The device generates its own key the first time and
shows you the public half to paste into your peer; you give it the peer key,
the endpoint and a tunnel address. Bring-up runs on its own task, so a peer that
is slow or unreachable never holds up boot or the web server.

**An API a script can use.** The console drives the target over a binary
WebSocket protocol, which is efficient and awful to write against. So there are
now plain HTTP endpoints for the same things: fetch one JPEG of the screen, move
the pointer, click, press a key, type a string. That is enough for a monitoring
script, or for an AI agent that needs to look at a machine and press something.

Because those endpoints hand out the same control the console has, they are
behind a setting that is off by default, and each call still needs a session and
a target attached.

[Release v.0.14.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.14.0)
