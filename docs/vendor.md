# Vendored code

`flash.js` is [esp-web-tools](https://github.com/esphome/esp-web-tools) 10.4.0
bundled with esbuild, Apache-2.0, copyright Nabu Casa. It carries esptool-js
inside it, also Apache-2.0, copyright Espressif Systems.

It is committed here rather than loaded from a CDN so the page has no
third-party runtime dependencies. Rebuild it with:

```sh
npm init -y && npm i esp-web-tools@10.4.0
echo 'import "esp-web-tools/dist/web/install-button.js";' > entry.js
esbuild entry.js --bundle --format=esm --minify --target=es2020 --outfile=flash.js
```

`assets/js/chipinfo.js` is [esptool-js](https://github.com/espressif/esptool-js)
0.7.0, Apache-2.0, copyright Espressif Systems, bundled with one small entry of
ours that reads the chip revision, the flash ID and a few eFuse fields
(`identify(port)`). The flasher stubs are left out: reading needs only the ROM
loader, and without them the file is 160 KB instead of 300. It is loaded only
when someone presses "Check my board" on the flasher or "Read the board" on the
tools page; `assets/js/board-check.js` (ours) wraps it. Rebuild it with:

```sh
npm init -y && npm i esptool-js@0.7.0 esbuild
# entry.js and build.mjs are in tools/chipinfo/
node build.mjs   # esbuild with a plugin that swaps stub_flasher/*.json for {}
```

