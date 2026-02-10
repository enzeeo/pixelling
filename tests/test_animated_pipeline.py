import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from pixelling.ops.animated_pipeline import run_animated_image_transformation_pipeline


class AnimatedPipelineOperationTests(unittest.TestCase):
    def test_animated_pipeline_rejects_empty_frame_sequence(self) -> None:
        with self.assertRaises(ValueError):
            run_animated_image_transformation_pipeline(
                frames=[],
                transformation_mode="pixel",
                block_size=2,
            )

    def test_animated_pipeline_transforms_each_frame_in_order(self) -> None:
        first_input_frame = Image.new("RGB", (8, 8), color=(10, 20, 30))
        second_input_frame = Image.new("RGB", (8, 8), color=(30, 20, 10))
        first_output_frame = Image.new("RGB", (8, 8), color=(100, 110, 120))
        second_output_frame = Image.new("RGB", (8, 8), color=(120, 110, 100))

        with patch(
            "pixelling.ops.animated_pipeline.run_image_transformation_pipeline",
            side_effect=[first_output_frame, second_output_frame],
        ) as pipeline_mock:
            transformed_frames = run_animated_image_transformation_pipeline(
                frames=[first_input_frame, second_input_frame],
                transformation_mode="pixel",
                block_size=2,
            )

        self.assertEqual(transformed_frames, [first_output_frame, second_output_frame])
        self.assertEqual(pipeline_mock.call_count, 2)
        pipeline_mock.assert_any_call(
            image=first_input_frame,
            transformation_mode="pixel",
            block_size=2,
            grid_width=None,
            grid_height=None,
            color_count=None,
        )
        pipeline_mock.assert_any_call(
            image=second_input_frame,
            transformation_mode="pixel",
            block_size=2,
            grid_width=None,
            grid_height=None,
            color_count=None,
        )


if __name__ == "__main__":
    unittest.main()
