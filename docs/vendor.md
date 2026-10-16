# Vendored code

`flash.js` is [esp-web-tools](https://github.com/esphome/esp-web-tools) 10.4.0
bundled with esbuild, Apache-2.0, copyright Nabu Casa. It carries esptool-js
inside it, also Apache-2.0, copyright Espressif Systems.

The esptool-js in it is **0.7.0**, not the 0.6 that esp-web-tools 10.4.0 ships
with. 0.6 could not talk to a Waveshare ESP32-P4-WIFI6-DB (rev 3.2, through
its CH343 bridge): it synced and then failed reading the chip type with
"Serial data stream stopped". 0.7.0 identifies the chip by GET_SECURITY_INFO
first and flashed it (2026-10-16). Bundling the *unbundled* entry
(`dist/install-button.js`) is what lets the override reach the code;
`dist/web/install-button.js` already has 0.6 baked in. @material/web is held
at 2.2.0, the last version that still has the style files esp-web-tools
imports.

It is committed here rather than loaded from a CDN so the page has no
third-party runtime dependencies. Rebuild it with:

```sh
cat > package.json <<'JSON'
{ "private": true, "overrides": { "esptool-js": "0.7.0", "@material/web": "2.2.0" } }
JSON
npm i esp-web-tools@10.4.0 esbuild@0.24.0
echo 'import "esp-web-tools/dist/install-button.js";' > entry.js
npx esbuild entry.js --bundle --format=esm --minify --target=es2020 --outfile=flash.js
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

