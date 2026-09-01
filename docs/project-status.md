# Project status and public boundary

Status checked on 2026-09-01.

## Progress matrix

| Area | Status | Evidence or boundary |
|---|---|---|
| Serial RGB protocol | Confirmed in repository tests | `R/G/B`, multi-channel input, `OFF`, `STATUS`, clamping, and malformed-token handling |
| Offline simulator | Confirmed in repository tests | Runs with Python standard library only; theoretical power is not a measurement |
| Firmware syntax/build | Confirmed by CI when the `firmware-build` job passes | Arduino CLI compiles the sketch for `arduino:avr:uno` |
| Documentation | Confirmed in repository tests | Architecture, protocol, wiring, and electrical-safety boundaries are present |
| Real Arduino upload and lamp operation | Not verified | Requires the selected board, driver stage, lamp, and power supply |
| Electrical and optical measurements | Not verified | No measured power, temperature, brightness, EMC, waterproofing, or plant-growth result is claimed |

## Included in the public repository

- Reimplemented generic Arduino firmware for serial or transparent Bluetooth-UART control.
- A local simulator, example configuration, command samples, automated tests, and CI.
- General architecture, wiring, protocol, and safety documentation.
- MIT-licensed repository content created for this reproducible public example.

## Deliberately excluded

- API keys, passwords, Wi-Fi credentials, account identifiers, and private device data.
- Vendor SDKs, private protocols, copied third-party repositories, and build artifacts.
- Team application, patent, customer, company, or personal materials whose public rights are unclear.
- Claims about measured energy savings or hardware behavior that have not been tested.

## Next evidence needed

1. Compile and upload to the exact physical board used in the build.
2. Record the driver circuit, supply rating, and load current before powering a lamp.
3. Capture a short hardware demonstration and measured power/temperature table.
4. Update this file with board revision, test conditions, and reproducible measurements.
