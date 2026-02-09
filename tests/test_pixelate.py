import sys
import unittest
from pathlib import Path

from PIL import Image

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.ops.pixelate import pixelate_image_with_block_size


class PixelateOperationTests(unittest.TestCase):
    def test_pixelate_keeps_original_output_dimensions(self) -> None:
        input_image = Image.new("RGB", (12, 8), color=(120, 30, 220))

        output_image = pixelate_image_with_block_size(input_image, block_size=3)

        self.assertEqual(output_image.size, (12, 8))

    def test_pixelate_raises_error_when_block_size_is_not_positive(self) -> None:
        input_image = Image.new("RGB", (12, 8), color=(0, 0, 0))

        with self.assertRaises(ValueError):
            pixelate_image_with_block_size(input_image, block_size=0)


if __name__ == "__main__":
    unittest.main()
