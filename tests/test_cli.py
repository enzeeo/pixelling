import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.cli import (
    parse_command_line_arguments,
    run_command_line_interface,
    validate_command_line_arguments,
)


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

    def test_run_command_line_interface_routes_animated_input_through_animated_pipeline(self) -> None:
        first_frame = Image.new("RGBA", (8, 8), color=(10, 20, 30, 255))
        second_frame = Image.new("RGBA", (8, 8), color=(30, 20, 10, 255))
        transformed_frames = [
            Image.new("RGBA", (8, 8), color=(100, 110, 120, 255)),
            Image.new("RGBA", (8, 8), color=(120, 110, 100, 255)),
        ]
        metadata = {"loop": 1, "duration": 30}

        with patch("pixelling.cli.is_animated_gif_file", return_value=True), patch(
            "pixelling.cli.load_animated_gif_frames_from_path",
            return_value=([first_frame, second_frame], metadata),
        ), patch(
            "pixelling.cli.run_animated_image_transformation_pipeline",
            return_value=transformed_frames,
        ) as animated_pipeline_mock, patch(
            "pixelling.cli.save_animated_image_to_path"
        ) as save_animated_image_mock, patch(
            "pixelling.cli.save_image_to_path"
        ) as save_single_image_mock:
            exit_status = run_command_line_interface(
                ["input.gif", "--mode", "pixel", "--block-size", "4"]
            )

        self.assertEqual(exit_status, 0)
        animated_pipeline_mock.assert_called_once_with(
            frames=[first_frame, second_frame],
            transformation_mode="pixel",
            block_size=4,
            grid_width=None,
            grid_height=None,
            color_count=None,
        )
        save_animated_image_mock.assert_called_once_with(
            frames=transformed_frames,
            output_image_path="input_pixelling.gif",
            allow_overwrite=False,
            metadata=metadata,
        )
        save_single_image_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
