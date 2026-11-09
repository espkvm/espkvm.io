import { build } from "esbuild";
// Only the ESP32-P4 stubs: every other chip's is swapped for nothing.
const p4Only = {
  name: "p4-only",
  setup(b) {
    b.onResolve({ filter: /stub_flasher\/.*\.json$/ }, (a) =>
      /esp32p4(-rev1)?\.json$/.test(a.path) ? undefined : { path: a.path, namespace: "nostub" });
    b.onLoad({ filter: /.*/, namespace: "nostub" }, () => ({ contents: "{}", loader: "json" }));
  },
};
await build({ entryPoints: ["entry.js"], bundle: true, format: "esm", minify: true, target: "es2020", outfile: "flashbackup.js", plugins: [p4Only] });
