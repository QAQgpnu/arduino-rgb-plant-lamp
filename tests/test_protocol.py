import json
import pathlib
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from demo.lamp_simulator import estimate_power_w, parse_line  # noqa: E402


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.off = {"R": 0, "G": 0, "B": 0}

    def test_multiple_channels_are_applied(self):
        self.assertEqual(parse_line("R180,G80 B20", self.off), {"R": 180, "G": 80, "B": 20})

    def test_values_are_clamped(self):
        self.assertEqual(parse_line("R999 G-2 B255", self.off), {"R": 255, "G": 0, "B": 255})

    def test_malformed_and_unknown_tokens_are_ignored(self):
        self.assertEqual(parse_line("Rabc X20 G", {"R": 4, "G": 5, "B": 6}), {"R": 4, "G": 5, "B": 6})

    def test_off_clears_all_channels(self):
        self.assertEqual(parse_line("OFF", {"R": 4, "G": 5, "B": 6}), self.off)

    def test_status_does_not_change_state(self):
        state = {"R": 4, "G": 5, "B": 6}
        self.assertEqual(parse_line("STATUS", state), state)

    def test_power_estimate_uses_configured_values(self):
        config = json.loads((ROOT / "config" / "hardware.example.json").read_text(encoding="utf-8"))
        self.assertAlmostEqual(estimate_power_w({"R": 255, "G": 255, "B": 255}, config), 0.3)

    def test_demo_runs_without_dependencies(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "demo" / "lamp_simulator.py"), "R255", "OFF"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("R=255", result.stdout)
        self.assertIn("estimated=0.000 W", result.stdout)


class RepositoryTests(unittest.TestCase):
    def test_required_public_files_exist(self):
        required = [
            "README.md",
            "LICENSE",
            "SECURITY.md",
            "CONTRIBUTING.md",
            "CHANGELOG.md",
            "docs/architecture.svg",
            "docs/wiring.md",
            "docs/safety.md",
            "firmware/rgb_plant_lamp/rgb_plant_lamp.ino",
        ]
        for relative_path in required:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_examples_do_not_request_credentials(self):
        text = (ROOT / "examples" / "commands.txt").read_text(encoding="utf-8").lower()
        for forbidden in ("api_key", "password", "passwd", "pswd", "token", "ssid"):
            self.assertNotIn(forbidden, text)

    def test_sketch_has_bounds_numeric_validation_and_status(self):
        text = (ROOT / "firmware" / "rgb_plant_lamp" / "rgb_plant_lamp.ino").read_text(encoding="utf-8")
        self.assertIn("inputLength < kBufferSize - 1", text)
        self.assertIn("discardingInput = true", text)
        self.assertIn("!discardingInput && inputLength > 0", text)
        self.assertIn("end == token + 1", text)
        self.assertIn('equalsIgnoreCase(token, "OFF")', text)
        self.assertIn('equalsIgnoreCase(token, "STATUS")', text)


if __name__ == "__main__":
    unittest.main()
