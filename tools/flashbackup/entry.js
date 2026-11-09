// Copy the whole flash of an ESP32-P4 device to a file, before anything is
// written to it: the only way back to a vendor's signed firmware (the JetKVM
// Mini's, for one) is the image that was on it. Runs esptool-js's own flasher
// stub, which is what can read flash fast; the ROM loader cannot.
import { ESPLoader, Transport } from "esptool-js";

export async function backupFlash(port, { log = () => {}, progress = () => {} } = {}) {
  const terminal = { clean() {}, writeLine: (s) => log(s), write: (s) => log(s) };
  const transport = new Transport(port, false);
  const loader = new ESPLoader({ transport, baudrate: 921600, terminal, debugLogging: false });
  try {
    await loader.main("default_reset");
    if (loader.secureDownloadMode) {
      throw new Error("this chip is in Secure Download Mode: Secure Boot is on, and it will not run unsigned firmware");
    }
    const mac = await loader.chip.readMac(loader);
    const id = await loader.readFlashId();
    const code = (id >>> 16) & 0xff;
    const size = code >= 0x12 && code <= 0x1a ? 2 ** code : 16 * 1024 * 1024;
    const chunk = 1024 * 1024;
    const out = new Uint8Array(size);
    for (let at = 0; at < size; at += chunk) {
      const part = await loader.readFlash(at, Math.min(chunk, size - at), (_p, got) => progress((at + got) / size));
      out.set(part, at);
    }
    progress(1);
    return { data: out, mac, size };
  } finally {
    try {
      await loader.after("hard_reset");
    } catch {}
    try {
      await transport.disconnect();
    } catch {}
  }
}
