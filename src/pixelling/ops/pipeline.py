from PIL import Image

from .quantize import quantize_image_colors
from .pixelate import pixelate_image_with_block_size
from .grid import resize_image_to_fixed_grid

def run_image_transformation_pipeline(
    image: Image.Image,
    transformation_mode: str,
    block_size: int | None = None,
    grid_width: int | None = None,
    grid_height: int | None = None,
    color_count: int | None = None,
) -> Image.Image:
    """Run the image transformation pipeline and return a transformed image.

    This function is intended to orchestrate the core image operations in order:
    1. Apply either pixel mode or grid mode.
    2. Optionally apply color quantization.

    Args:
        image: Input image to transform.
        transformation_mode: Transformation mode name, such as "pixel" or "grid".
        block_size: Pixel block size used for pixel mode.
        grid_width: Target grid width used for grid mode.
        grid_height: Target grid height used for grid mode.
        color_count: Optional number of colors for quantization.

    Returns:
        A transformed image after applying the selected operations.
    """
    if transformation_mode == "pixel":
        if block_size is None:
            raise ValueError("Block size must be provided for pixel mode.")
        transformed_image = pixelate_image_with_block_size(image, block_size)
    elif transformation_mode == "grid":
        if grid_width is None or grid_height is None:
            raise ValueError("Grid width and height must be provided for grid mode.")
        transformed_image = resize_image_to_fixed_grid(image, grid_width, grid_height)
    else:
        raise ValueError(f"Invalid transformation mode: '{transformation_mode}'. "
                         f"Valid options are: 'pixel' or 'grid'.")

    if color_count is not None:
        transformed_image = quantize_image_colors(transformed_image, color_count)

    return transformed_image
