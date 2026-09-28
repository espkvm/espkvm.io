---
title: 0.55.0 - a DVD drive that acts like one, and images over 4 GB
description: The virtual drive now answers the commands only an optical drive has, and an exFAT card takes a full DVD installer. Recordings over 2 GB show the right size and seek again.
tags: storage
date: 2026-09-28 12:00
---

## A drive that acts like a drive

An `.iso` was already served as a CD-ROM: the right device type, 2048-byte
blocks. But every command that only an optical drive has was refused - the
table of contents, the drive's profile, "a disc was inserted". UEFI and Linux
booted anyway. Windows, macOS and some firmware ask those questions first.

Now the drive answers them. An image above 900 MB shows up as a DVD, a
smaller one as a CD. A Linux target sees a DVD drive with a disc in it. I
have not tried Windows or a BIOS boot yet.

## Images over 4 GB

A full DVD installer is 5 to 8 GB. exFAT allows such a file, and the part of
the device that reads it for the target was 64-bit already. The upload was
not: the web server reads a body's length as 32 bits. So the console now
sends a big file in 2 GB parts, and the device adds each one to the end of
the file. A 4.5 GB image went up in three parts and read back on the target
with the same md5.

## Recordings over 2 GB

Looking for other 32-bit places turned up one in the file system's seek. It
counted in a signed 32-bit number, so past 2 GB the position went negative.
For a recording, which can grow to 3.9 GB, that meant a negative size in the
list and no seeking in the player. For appending an upload it would have
been worse: the file system took the negative number as a huge offset and
tried to grow the file to it. Files and sizes are read in 64 bits now.

[Release notes on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.55.0)
