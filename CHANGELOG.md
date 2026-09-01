# Changelog

All notable changes to this project are documented here.

## 0.3.0 - 2026-09-01

- Put the sketch in an Arduino CLI-compatible directory and compile it for Arduino Uno in CI.
- Drop an entire overlong serial frame instead of accepting its trailing bytes as a new command.
- Accept actual tab characters as command separators.
- Add an evidence-bounded project progress and publication-scope matrix.

## 0.2.0 - 2026-08-12

- Add `OFF` and `STATUS` serial commands and reject malformed numeric values.
- Add a zero-dependency offline simulator with configurable power estimation.
- Add architecture, wiring, safety, and validation-boundary documentation.
- Expand automated protocol and repository-quality tests.

## 0.1.0 - 2026-08-12

- Initial public-safe Arduino RGB plant-lamp example.
- Add serial/Bluetooth UART commands, documentation, tests, CI, and MIT license.
