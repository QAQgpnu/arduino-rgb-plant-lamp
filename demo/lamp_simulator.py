"""Zero-dependency command simulator for the RGB plant-lamp protocol."""

from __future__ import annotations

import argparse
import json
import pathlib


CHANNELS = ("R", "G", "B")


def parse_line(line: str, state: dict[str, int]) -> dict[str, int]:
    """Apply one protocol line and return a new state."""
    updated = dict(state)
    for raw_token in line.replace(",", " ").split():
        token = raw_token.upper()
        if token == "OFF":
            updated = {channel: 0 for channel in CHANNELS}
            continue
        if token == "STATUS":
            continue
        if token[:1] not in CHANNELS or len(token) == 1:
            continue
        try:
            value = int(token[1:], 10)
        except ValueError:
            continue
        updated[token[0]] = max(0, min(255, value))
    return updated


def estimate_power_w(state: dict[str, int], config: dict) -> float:
    """Estimate LED electrical input from example per-channel current values."""
    voltage = float(config["supply_voltage_v"])
    currents = config["channel_max_current_ma"]
    current_ma = sum(float(currents[channel]) * state[channel] / 255 for channel in CHANNELS)
    return voltage * current_ma / 1000


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate RGB plant-lamp serial commands")
    parser.add_argument("commands", nargs="*", help="commands such as R255,G80,B20 or OFF")
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1] / "config" / "hardware.example.json",
        help="hardware estimate JSON",
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    state = {channel: 0 for channel in CHANNELS}
    commands = args.commands or ["R180,G80,B20", "STATUS", "OFF"]
    for command in commands:
        state = parse_line(command, state)
        power = estimate_power_w(state, config)
        print(f"> {command}")
        print(f"  R={state['R']:3d} G={state['G']:3d} B={state['B']:3d} estimated={power:.3f} W")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
