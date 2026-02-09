import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.io import (
    build_default_output_image_path,
    load_image_from_path,
    save_image_to_path,
)


class InputOutputOperationTests(unittest.TestCase):
    def test_build_default_output_image_path_appends_suffix(self) -> None:
        output_image_path = build_default_output_image_path("images/photo.png")

        self.assertEqual(output_image_path, "images/photo_pixelling.png")

    def test_build_default_output_image_path_uses_png_when_missing_extension(self) -> None:
        output_image_path = build_default_output_image_path("images/photo")

        self.assertEqual(output_image_path, "images/photo_pixelling.png")

    def test_load_image_from_path_returns_loaded_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory_path:
            input_image_path = Path(temporary_directory_path) / "input.png"
            Image.new("RGB", (5, 5), color=(30, 60, 90)).save(input_image_path)

            loaded_image = load_image_from_path(str(input_image_path))

            self.assertEqual(loaded_image.size, (5, 5))
            self.assertEqual(loaded_image.mode, "RGB")

    def test_save_image_to_path_creates_numbered_file_when_overwrite_is_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory_path:
            output_image_path = Path(temporary_directory_path) / "result.png"
            Image.new("RGB", (5, 5), color=(0, 0, 0)).save(output_image_path)

            image_to_save = Image.new("RGB", (5, 5), color=(255, 255, 255))
            save_image_to_path(
                image=image_to_save,
                output_image_path=str(output_image_path),
                allow_overwrite=False,
            )

            numbered_output_image_path = Path(temporary_directory_path) / "result_1.png"
            self.assertTrue(numbered_output_image_path.exists())


if __name__ == "__main__":
    unittest.main()
