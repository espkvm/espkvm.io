import { build } from "esbuild";
// The flasher stubs (one JSON per chip) are only needed to write flash; reading
// eFuse and the flash ID works with the ROM loader alone. Swap them for nothing.
const noStubs = {
  name: "no-stubs",
  setup(b) {
    b.onResolve({ filter: /stub_flasher\/.*\.json$/ }, (a) => ({ path: a.path, namespace: "nostub" }));
    b.onLoad({ filter: /.*/, namespace: "nostub" }, () => ({ contents: "{}", loader: "json" }));
  },
};
await build({ entryPoints: ["entry.js"], bundle: true, format: "esm", minify: true, target: "es2020", outfile: "chipinfo.js", plugins: [noStubs] });
