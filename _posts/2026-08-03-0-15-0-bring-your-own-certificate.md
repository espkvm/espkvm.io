---
title: 0.15.0 - bring your own certificate
description: Install a certificate from your own CA, or a real public one, so browsers trust the device with nothing to import.
tags: security
date: 2026-08-03
image:
---

Since 0.11.0 the device has been its own certificate authority. That works if
you are willing to import it once per machine. If you already run a CA, or the
device has a real name and a real public certificate, importing anything is the
wrong answer.

So install your own. Upload one PEM blob, the chain first and then the private
key, which is what `cat fullchain.pem privkey.pem` gives you. The console is
served with it. Delete it and the device goes back to the identity it makes
for itself.

Two things make it safe to try on a device you cannot walk to. The pair is
checked before it is stored: that it parses, and that the key belongs to the
certificate. And if the TLS stack still refuses it at start-up, the server falls
back to the self-signed certificate instead of not coming up at all.

[Release v.0.15.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.15.0)
