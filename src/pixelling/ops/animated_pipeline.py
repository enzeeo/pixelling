"""Pipeline helpers for animated image processing."""

from PIL import Image


def run_animated_image_transformation_pipeline(
    frames: list[Image.Image],
    transformation_mode: str,
    block_size: int | None = None,
    grid_width: int | None = None,
    grid_height: int | None = None,
    color_count: int | None = None,
) -> list[Image.Image]:
    """Run the transformation pipeline across an ordered frame sequence.

    Args:
        frames: Input frame sequence to transform.
        transformation_mode: Transformation mode such as "pixel" or "grid".
        block_size: Pixel block size used for pixel mode.
        grid_width: Target grid width used for grid mode.
        grid_height: Target grid height used for grid mode.
        color_count: Optional number of colors for quantization.

    Returns:
        Transformed frame sequence in the same order as the input frames.
    """
    raise NotImplementedError("Animated transformation pipeline is not implemented yet.")
