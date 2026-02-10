from PIL import Image

from .pipeline import run_image_transformation_pipeline

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
    if len(frames) == 0:
        raise ValueError("At least one frame is required for animated processing.")

    transformed_frames: list[Image.Image] = []
    for frame in frames:
        transformed_frame = run_image_transformation_pipeline(
            image=frame,
            transformation_mode=transformation_mode,
            block_size=block_size,
            grid_width=grid_width,
            grid_height=grid_height,
            color_count=color_count,
        )
        transformed_frames.append(transformed_frame)
    return transformed_frames
