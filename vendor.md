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
