// Read what an ESP32-P4 board says about itself over its USB serial port:
// chip and revision from eFuse, the flash chip's ID (and so its size), the
// raw PSRAM capacity field, and the USB bridge's IDs. Restarts the board after.
import { ESPLoader, Transport } from "esptool-js";

export async function identify(port, log = () => {}) {
  const terminal = { clean() {}, writeLine: (s) => log(s), write: (s) => log(s) };
  const transport = new Transport(port, false);
  const loader = new ESPLoader({ transport, baudrate: 115200, terminal, debugLogging: false });
  const out = { usb: port.getInfo ? port.getInfo() : {} };
  try {
    await loader.detectChip("default_reset");
    const chip = loader.chip;
    out.chip = chip.CHIP_NAME;
    out.description = await chip.getChipDescription(loader);
    if (chip.getChipRevision) out.revision = await chip.getChipRevision(loader);
    try {
      out.mac = await chip.readMac(loader);
    } catch {}
    if (chip.CHIP_NAME === "ESP32-P4") {
      const word2 = await loader.readReg(chip.EFUSE_BLOCK1_ADDR + 8);
      out.major = (((word2 >>> 23) & 1) << 2) | ((word2 >>> 4) & 3);
      out.minor = word2 & 0x0f;
      out.psramCap = (word2 >>> 13) & 7;
    }
    try {
      await loader.flashSpiAttach(0);
      const id = await loader.readFlashId();
      out.flashId = id;
      const sizeCode = (id >>> 16) & 0xff;
      if (sizeCode >= 0x12 && sizeCode <= 0x1a) out.flashMB = 2 ** (sizeCode - 20);
    } catch (e) {
      out.flashError = String(e && e.message ? e.message : e);
    }
  } finally {
    try {
      await loader.after("hard_reset");
    } catch {}
    try {
      await transport.disconnect();
    } catch {}
  }
  return out;
}
