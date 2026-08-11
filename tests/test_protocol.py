import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_sketch_and_docs_exist(self):
        self.assertTrue((ROOT / "src" / "rgb_plant_lamp.ino").is_file())
        self.assertTrue((ROOT / "docs" / "protocol.md").is_file())

    def test_protocol_examples_are_safe(self):
        text = (ROOT / "examples" / "commands.txt").read_text(encoding="utf-8")
        self.assertIn("R255", text)
        self.assertNotIn("api_key", text.lower())
        self.assertNotIn("password", text.lower())

    def test_sketch_has_bounds_and_line_termination(self):
        text = (ROOT / "src" / "rgb_plant_lamp.ino").read_text(encoding="utf-8")
        self.assertIn("kBufferSize", text)
        self.assertIn("inputLength < kBufferSize - 1", text)
        self.assertIn("ch == '\\n'", text)


if __name__ == "__main__":
    unittest.main()

