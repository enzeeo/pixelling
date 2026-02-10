import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.gif_io import save_animated_gif_frames_to_path


class GifInputOutputOperationTests(unittest.TestCase):
    def test_save_animated_gif_frames_to_path_rejects_empty_frame_list(self) -> None:
        with self.assertRaises(ValueError):
            save_animated_gif_frames_to_path(
                frames=[],
                output_image_path="output.gif",
                metadata=None,
            )

    def test_save_animated_gif_frames_to_path_writes_animated_gif_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory_path:
            output_image_path = Path(temporary_directory_path) / "animated.gif"
            first_frame = Image.new("RGBA", (6, 6), color=(255, 0, 0, 255))
            second_frame = Image.new("RGBA", (6, 6), color=(0, 255, 0, 255))

            save_animated_gif_frames_to_path(
                frames=[first_frame, second_frame],
                output_image_path=str(output_image_path),
                metadata={"loop": 0, "duration": 50},
            )

            self.assertTrue(output_image_path.exists())
            with Image.open(output_image_path) as saved_image:
                self.assertEqual(saved_image.format, "GIF")
                self.assertTrue(bool(getattr(saved_image, "is_animated", False)))
                self.assertEqual(saved_image.n_frames, 2)


if __name__ == "__main__":
    unittest.main()
