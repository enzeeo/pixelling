from PIL import Image
from .resize import resize_image_with_resampling


def resize_image_to_fixed_grid(
    image: Image.Image,
    grid_width: int,
    grid_height: int,
) -> Image.Image:
    """Return an image resized to a fixed grid width and height.

    Args:
        image: Input image to resize.
        grid_width: Target grid width in pixels.
        grid_height: Target grid height in pixels.

    Returns:
        A new image resized to the requested grid dimensions.
    """
    if grid_width <= 0 or grid_height <= 0:
        raise ValueError("Grid dimensions must be positive integers.")
    
    grid_image = resize_image_with_resampling(
        image=image,
        width=grid_width,
        height=grid_height,
        resampling_filter=Image.Resampling.NEAREST,
    )
    return grid_image
