---
title: The demo is a whole fake computer now
description: The interactive demo moved to its own address and stopped being a screenshot: it is the real console, driving a machine that boots, crashes and lets you update its firmware.
tags: demo, console
date: 2026-08-27
image: /assets/blog/the-demo-is-a-whole-fake-computer/sheep.webp
---

There is a demo of ESP-KVM at [demo.espkvm.io](https://demo.espkvm.io/). No
hardware, no sign-up, no install. One page, about 300 KB, and you are looking at
the console.

What is real and what is not: the console is the real one, the same code the
firmware serves, built from the same repository. The device underneath it is
faked. The page intercepts the calls the console makes and answers them itself,
out of data captured off a live board.

Behind those answers sits a machine. Not a video of one. A little state machine
with stages, a clock, and an 80x25 character screen laid out with the same
geometry the firmware reports for a real UEFI console.

So the story runs like a call-out. The page opens on a machine mid-POST, not on
a dark screen, and it lands on "No boot device found". The screen tells you to
pick an image under Media. Choosing one writes the same setting that mounts a
disc on a real device. Reset boots it. The prompt takes the keys you type. Do
nothing for fifteen seconds and the demo loads an image itself, and the first
thing you do stops that for good.

There are four things to boot, and each falls over in its own dialect:

- **HalfOS Life** - a shell. Type `startx` and the pointer constellation comes up. Type something unwise at the prompt and you get a kernel panic with a call trace.
- **Sheeps XP** - flat hills, walking sheep and a taskbar, which is the picture above. The flock gathers round the pointer once you have taken control, and grazes when you leave it alone. Click the black sheep and the machine stops with `BLACK_SHEEP_NOT_RESPONDING`, wool.sys, "contact your shepherd".
- **Pear OS** - a smiling computer, then a progress bar that sticks at nine tenths, then a desktop with a dock. One tile in that dock tells you to restart your pear.
- **memtest** - a memory test that never finishes, with a pass counter climbing until it finds a one-bit failure.

Every crash screen is text on purpose. Select and Copy light up on them and
really work, because there are characters there to read.

The firmware update runs end to end too. The demo serves its own manifest,
offers a newer version, streams an image of the right size in chunks so both
progress bars move, then fails every call for seven seconds while the "device"
restarts, and comes back on the new version.

Building this found two bugs in code that ships. A refused image left the
console stuck behind its own full-screen overlay, with only a reload out. And
the console read every keyboard report as a fresh press, so two overlapping keys
repeated a letter, which is what fast typing looks like. A fake device walks
paths a real one rarely reaches.
