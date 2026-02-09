import sys
import unittest
from pathlib import Path

from PIL import Image

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.ops.resize import resize_image_with_resampling, select_resampling_filter


class ResizeOperationTests(unittest.TestCase):
    def test_resize_returns_requested_dimensions(self) -> None:
        input_image = Image.new("RGB", (10, 6), color=(1, 2, 3))

        output_image = resize_image_with_resampling(
            image=input_image,
            width=5,
            height=3,
            resampling_filter=Image.Resampling.NEAREST,
        )

        self.assertEqual(output_image.size, (5, 3))

    def test_resize_raises_error_for_non_positive_dimension(self) -> None:
        input_image = Image.new("RGB", (10, 6), color=(1, 2, 3))

        with self.assertRaises(ValueError):
            resize_image_with_resampling(
                image=input_image,
                width=0,
                height=3,
                resampling_filter=Image.Resampling.NEAREST,
            )

    def test_select_resampling_filter_accepts_trimmed_case_insensitive_name(self) -> None:
        selected_filter = select_resampling_filter("  Lanczos  ")

        self.assertEqual(selected_filter, Image.Resampling.LANCZOS)

    def test_select_resampling_filter_raises_error_for_unknown_name(self) -> None:
        with self.assertRaises(ValueError):
            select_resampling_filter("unknown")


if __name__ == "__main__":
    unittest.main()
