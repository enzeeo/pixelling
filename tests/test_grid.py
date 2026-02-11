import sys
import unittest
from pathlib import Path

from PIL import Image

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.ops.grid import resize_image_to_fixed_grid


class GridOperationTests(unittest.TestCase):
    def test_grid_resize_returns_requested_dimensions(self) -> None:
        input_image = Image.new("RGB", (16, 12), color=(10, 20, 30))

        output_image = resize_image_to_fixed_grid(
            image=input_image,
            grid_width=4,
            grid_height=3,
        )

        self.assertEqual(output_image.size, (4, 3))

    def test_grid_resize_matches_box_resampling_reference(self) -> None:
        input_image = Image.new("RGB", (4, 4))
        input_image.putdata(
            [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
                (255, 0, 255),
                (0, 255, 255),
                (64, 64, 64),
                (128, 128, 128),
                (200, 0, 0),
                (0, 200, 0),
                (0, 0, 200),
                (200, 200, 0),
                (10, 10, 10),
                (20, 20, 20),
                (30, 30, 30),
                (40, 40, 40),
            ]
        )

        expected_output_image = input_image.resize((2, 2), resample=Image.Resampling.BOX)
        actual_output_image = resize_image_to_fixed_grid(
            image=input_image,
            grid_width=2,
            grid_height=2,
        )

        self.assertEqual(list(actual_output_image.getdata()), list(expected_output_image.getdata()))

    def test_grid_resize_center_crops_before_resizing_to_target_aspect_ratio(self) -> None:
        input_image = Image.new("RGB", (8, 4))
        for x in range(8):
            for y in range(4):
                if x < 2:
                    input_image.putpixel((x, y), (255, 0, 0))
                elif x >= 6:
                    input_image.putpixel((x, y), (0, 0, 255))
                else:
                    input_image.putpixel((x, y), (0, 255, 0))

        expected_cropped_image = input_image.crop((2, 0, 6, 4))
        expected_output_image = expected_cropped_image.resize(
            (2, 2),
            resample=Image.Resampling.BOX,
        )
        actual_output_image = resize_image_to_fixed_grid(
            image=input_image,
            grid_width=2,
            grid_height=2,
        )

        self.assertEqual(list(actual_output_image.getdata()), list(expected_output_image.getdata()))


if __name__ == "__main__":
    unittest.main()
