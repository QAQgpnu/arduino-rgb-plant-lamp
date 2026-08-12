# Electrical safety and validation boundary

## Verified in this repository

- Source-level bounds checks prevent writing past the serial buffer.
- PWM commands are clamped to `0..255`; malformed values are ignored.
- The offline simulator and repository tests run without hardware or cloud services.

## Not verified here

- A specific LED strip, power supply, MOSFET board, Bluetooth module, or enclosure.
- Mains-voltage switching, thermal behavior, EMC, waterproofing, plant-growth
  performance, or measured energy savings.
- The accuracy of the example power estimate for any real circuit.

Use only an isolated low-voltage supply while prototyping. Add fusing,
current limiting, reverse-polarity protection, appropriate wire gauges and
thermal checks for the actual load. Mains wiring should be designed and
reviewed by a qualified person; it is outside this project.
