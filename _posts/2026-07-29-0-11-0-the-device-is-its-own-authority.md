---
title: 0.11.0 - the device becomes its own certificate authority
description: Import one small certificate once and the browser trusts the device for good - which is also what unlocks H.264 and the keyboard channel.
tags: security, video
date: 2026-07-29
image:
---

A self-signed certificate gets you a warning page you can click through. That is
enough for a settings page and no use for the rest: a browser will not open a
WebSocket or hand video to a hardware decoder over a connection it does not
trust. Clicking through cost you H.264 and, in some browsers, the keyboard.

The device now generates a small certificate authority of its own, once, and
keeps it. That authority signs the certificate the console is served with. You
can download the authority from Settings, or from `/cert.pem`, and import it
into your machine's trust store - and from then on the device is genuinely
trusted, warning gone, H.264 and the control channel working.

When the hostname or a static address changes, the device re-issues its
certificate under the same authority, so the import you did once still holds.

The same release fixes something broken since 0.9.0. The web server's routing
table had one slot too few, and the two WebSocket routes were registered last,
so those were the ones that vanished. Every ordinary page still answered, which
is why it looked like a browser problem. H.264, keyboard and mouse are back.

[Release v.0.11.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.11.0)
