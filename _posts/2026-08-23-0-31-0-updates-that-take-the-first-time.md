---
title: 0.31.0 - updates that take on the first try
description: A chip fault during its own restart made updates look like they reverted themselves. Fixed, along with uploads that died part-way over HTTPS.
tags: update, network
date: 2026-08-23
image:
---

Some people updated, watched the device come back, and found the old version
running. It looked like the new firmware had been rejected and rolled back. It
had not.

The chip could fault part-way through its own restart. The boot that followed
read the new firmware wrong and got nowhere; a few seconds later the watchdog
reset the board properly, the old version came up, and from outside that is
indistinguishable from a rollback. The fault is in ESP-IDF's restart path on
chips with external RAM - it never needed an update to happen, a plain restart
could do it - and it is gone in ESP-IDF 6.1, which the releases are built with
now.

Updating to this version is enough, and no cable is needed. But the restart that
installs it is still done by the old firmware, so if the device comes back on
the old version, run the update once more. From this version on it stops
happening. Found from a serial log by
[@petrn](https://github.com/petrn) in
[#22](https://github.com/orgs/espkvm/discussions/22).

**Uploads that died at a few percent.** Over HTTPS a quiet moment on the socket
arrives as a raw "nothing yet" from the TLS library, not the timeout the code
was watching for, so it was read as a broken connection and the whole upload was
thrown away. Live video can starve a socket for half a minute, so updating with
the console open could fail every time. A silence is now treated as a silence.

The rescue hotspot also learned to show a join code on the mono OLED, at whatever
size the glass can hold.

[Release v.0.31.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.31.0)
