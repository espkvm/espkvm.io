/*
 * "Check my board": ask an ESP32-P4 board on a USB serial port what it is - the
 * chip revision from eFuse, the flash size from the flash chip's ID, the USB
 * bridge's IDs - so the flasher and the tools page can suggest the image that
 * fits. Suggestions only: the pages never refuse a choice because of this.
 *
 * The reading itself is esptool-js (chipinfo.js, vendored - see docs/vendor.md),
 * loaded only when someone presses the button. It restarts the board when done.
 */

/* USB serial bridges seen on ESP32-P4 boards, by vendor:product. */
const BRIDGES = {
  "1a86:55d3": "WCH CH343",
  "1a86:55d4": "WCH CH9102",
  "1a86:7523": "WCH CH340",
  "10c4:ea60": "Silicon Labs CP210x",
  "303a:1001": "the chip's own USB Serial/JTAG",
  "0403:6001": "FTDI FT232R",
  "0403:6010": "FTDI FT2232",
  "0403:6014": "FTDI FT232H",
  "0403:6015": "FTDI FT231X",
};

const hex4 = (n) => n.toString(16).padStart(4, "0");

/*
 * PSRAM_CAP in eFuse (BLK1, 3 bits). Espressif does not publish what its values
 * mean for the P4, so this lists only what boards of a known size have read.
 * 2 is what three 32 MB boards read: an M5Stack Unit PoE-P4 (rev 1.3), an
 * ESP32-P4 Function EV Board (rev 3.2) and a Waveshare ESP32-P4-ETH (rev 1.3).
 */
const PSRAM_BY_CAP = { 2: 32 };

/* The JEDEC ID as manufacturer, type and capacity bytes. The register holds
   them low byte first, and sometimes junk above the third byte. */
function jedec(id) {
  const b = [id & 0xff, (id >> 8) & 0xff, (id >> 16) & 0xff];
  return b.map((x) => x.toString(16).padStart(2, "0")).join(" ");
}

/** Pick the port (needs the click that called it), read the board, restart it. */
export async function checkBoard(log = () => {}) {
  if (!("serial" in navigator)) throw new Error("this browser cannot talk to serial devices - use Chrome or Edge");
  const port = await navigator.serial.requestPort();
  const { identify } = await import("/assets/js/chipinfo.js");
  const r = await identify(port, log);
  const usb = r.usb || {};
  const key = usb.usbVendorId != null ? `${hex4(usb.usbVendorId)}:${hex4(usb.usbProductId)}` : "";
  return {
    chip: r.chip || "",
    isP4: r.chip === "ESP32-P4",
    revText: r.major !== undefined ? `v${r.major}.${r.minor}` : "",
    revFamily: r.major === undefined ? "" : r.major >= 3 ? "3" : "1",
    flashMB: r.flashMB || null,
    flashId: r.flashId != null ? jedec(r.flashId) : "",
    psramCap: r.psramCap,
    psramMB: r.psramCap !== undefined ? PSRAM_BY_CAP[r.psramCap] || null : null,
    mac: r.mac || "",
    bridge: BRIDGES[key] || (key ? `USB ${key}` : ""),
  };
}

/** One line for a person: what the board said. */
export function describe(d) {
  const parts = [d.chip + (d.revText ? ` rev ${d.revText}` : "")];
  parts.push(d.flashMB ? `${d.flashMB} MB flash` : "flash size not read");
  if (d.bridge) parts.push(`USB bridge: ${d.bridge}`);
  return parts.join(" · ");
}

/** What the analytics get from a reading: no MAC, nothing that names one board. */
export function trackParams(d) {
  return {
    chip: d.chip || "unknown",
    rev: d.revText || "",
    flash: d.flashMB || 0,
    psram: d.psramMB || 0,
    psram_cap: d.psramCap === undefined ? -1 : d.psramCap,
    bridge: d.bridge || "unknown",
  };
}

/** A failed reading, as a short reason for the analytics. */
export function errorReason(e) {
  const msg = e && e.message ? e.message : String(e);
  if (/No port selected|cancel/i.test(msg)) return "no_port";
  if (/cannot talk to serial/i.test(msg)) return "no_web_serial";
  if (/timed? ?out|timeout/i.test(msg)) return "timeout";
  return "read_failed";
}
