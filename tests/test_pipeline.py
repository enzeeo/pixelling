import sys
import unittest
from pathlib import Path

from PIL import Image

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.ops.pipeline import run_image_transformation_pipeline


class PipelineOperationTests(unittest.TestCase):
    def test_pipeline_pixel_mode_returns_image_with_original_dimensions(self) -> None:
        input_image = Image.new("RGB", (12, 8), color=(120, 40, 220))

        output_image = run_image_transformation_pipeline(
            image=input_image,
            transformation_mode="pixel",
            block_size=3,
        )

        self.assertEqual(output_image.size, (12, 8))

    def test_pipeline_grid_mode_returns_requested_dimensions(self) -> None:
        input_image = Image.new("RGB", (12, 8), color=(120, 40, 220))

        output_image = run_image_transformation_pipeline(
            image=input_image,
            transformation_mode="grid",
            grid_width=4,
            grid_height=2,
        )

        self.assertEqual(output_image.size, (4, 2))

    def test_pipeline_rejects_missing_pixel_argument(self) -> None:
        input_image = Image.new("RGB", (12, 8), color=(120, 40, 220))

        with self.assertRaises(ValueError):
            run_image_transformation_pipeline(
                image=input_image,
                transformation_mode="pixel",
                block_size=None,
            )

    def test_pipeline_rejects_invalid_mode(self) -> None:
        input_image = Image.new("RGB", (12, 8), color=(120, 40, 220))

        with self.assertRaises(ValueError):
            run_image_transformation_pipeline(
                image=input_image,
                transformation_mode="unknown",
            )


if __name__ == "__main__":
    unittest.main()
