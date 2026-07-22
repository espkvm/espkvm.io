# espkvm.io

The project page for [ESP-KVM](https://github.com/espkvm/espkvm) - an IP-KVM
built from an ESP32-P4 and a TC358743 HDMI bridge.

Two pages: what the project is, and a flasher that installs the firmware onto a
board over USB straight from the browser.

## How it is built

It is not. No build step, no framework, no dependencies: the styles are inline,
the diagram is inline SVG, and nothing is fetched from a third party at runtime.
A project whose point is working on a network with no way out should not
describe itself through a CDN.

`flash.js` is the one piece of code that came from elsewhere, and it is
vendored rather than linked - see [vendor.md](vendor.md) for what it is and how
to rebuild it.

The firmware images the flasher writes are not stored here. They are published
by the firmware repository's CI to `espkvm.github.io/espkvm/flash/` and fetched
from there, so this site cannot go stale.

## Preview

```sh
python3 -m http.server 8000
```

Serial access needs a secure page, so `Install` works over `localhost` or
HTTPS and refuses anything else. That is the browser's rule, not ours.
