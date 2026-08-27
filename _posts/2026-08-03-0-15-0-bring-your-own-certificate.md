---
title: 0.15.0 - bring your own certificate
description: Install a certificate from your own CA, or a real public one, so browsers trust the device with nothing to import.
tags: security
date: 2026-08-03
image:
---

Since 0.11.0 the device has been its own certificate authority, which works well
if you are willing to import that authority once per machine. In an organisation
that already runs its own CA, or on a device that has a real name and a real
public certificate, importing anything is the wrong answer.

So you can now install your own. Upload one PEM blob - the certificate chain
first, then the private key, which is exactly what `cat fullchain.pem
privkey.pem` gives you - and the device serves the console with it. Delete it
and the device goes back to the identity it makes for itself.

Two things make this safe to try on a device you cannot walk to: the pair is
checked before it is stored, both that it parses and that the key really belongs
to the certificate; and if the TLS stack still refuses it at start-up, the
server falls back to the self-signed certificate instead of not coming up.

[Release v.0.15.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.15.0)
