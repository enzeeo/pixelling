import sys
import unittest
from pathlib import Path

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.cli import parse_command_line_arguments, validate_command_line_arguments


class CommandLineArgumentTests(unittest.TestCase):
    def test_parse_pixel_mode_arguments(self) -> None:
        parsed_arguments = parse_command_line_arguments(
            [
                "input.png",
                "--mode",
                "pixel",
                "--block-size",
                "6",
                "--color-count",
                "12",
            ]
        )

        self.assertEqual(parsed_arguments.input_image_path, "input.png")
        self.assertEqual(parsed_arguments.mode, "pixel")
        self.assertEqual(parsed_arguments.block_size, 6)
        self.assertEqual(parsed_arguments.color_count, 12)
        self.assertIsNone(parsed_arguments.grid_width)
        self.assertIsNone(parsed_arguments.grid_height)

    def test_parse_grid_mode_arguments(self) -> None:
        parsed_arguments = parse_command_line_arguments(
            [
                "input.png",
                "--mode",
                "grid",
                "--grid-width",
                "32",
                "--grid-height",
                "24",
            ]
        )

        self.assertEqual(parsed_arguments.mode, "grid")
        self.assertEqual(parsed_arguments.grid_width, 32)
        self.assertEqual(parsed_arguments.grid_height, 24)
        self.assertIsNone(parsed_arguments.block_size)

    def test_validation_rejects_grid_arguments_in_pixel_mode(self) -> None:
        parsed_arguments = parse_command_line_arguments(
            [
                "input.png",
                "--mode",
                "pixel",
                "--block-size",
                "6",
                "--grid-width",
                "16",
            ]
        )

        with self.assertRaises(ValueError):
            validate_command_line_arguments(parsed_arguments)

    def test_validation_rejects_pixel_argument_in_grid_mode(self) -> None:
        parsed_arguments = parse_command_line_arguments(
            [
                "input.png",
                "--mode",
                "grid",
                "--grid-width",
                "16",
                "--grid-height",
                "16",
                "--block-size",
                "3",
            ]
        )

        with self.assertRaises(ValueError):
            validate_command_line_arguments(parsed_arguments)


if __name__ == "__main__":
    unittest.main()
