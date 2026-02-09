import sys
import unittest
from pathlib import Path

from PIL import Image

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.ops.quantize import quantize_image_colors


class QuantizeOperationTests(unittest.TestCase):
    def test_quantize_preserves_size_for_rgb_image(self) -> None:
        input_image = Image.new("RGB", (8, 8))
        for x_coordinate in range(8):
            for y_coordinate in range(8):
                input_image.putpixel(
                    (x_coordinate, y_coordinate),
                    (x_coordinate * 10, y_coordinate * 10, (x_coordinate + y_coordinate) * 10),
                )

        output_image = quantize_image_colors(input_image, color_count=4)

        self.assertEqual(output_image.mode, "RGB")
        self.assertEqual(output_image.size, input_image.size)

    def test_quantize_preserves_alpha_channel_values_for_rgba_image(self) -> None:
        input_image = Image.new("RGBA", (2, 2))
        input_image.putdata(
            [
                (255, 0, 0, 0),
                (0, 255, 0, 64),
                (0, 0, 255, 128),
                (255, 255, 0, 255),
            ]
        )

        output_image = quantize_image_colors(input_image, color_count=2)

        self.assertEqual(output_image.mode, "RGBA")
        self.assertEqual(output_image.size, input_image.size)
        self.assertEqual(list(output_image.getchannel("A").getdata()), [0, 64, 128, 255])

    def test_quantize_raises_error_for_non_positive_color_count(self) -> None:
        input_image = Image.new("RGB", (4, 4), color=(10, 20, 30))

        with self.assertRaises(ValueError):
            quantize_image_colors(input_image, color_count=0)


if __name__ == "__main__":
    unittest.main()
