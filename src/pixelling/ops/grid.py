from PIL import Image
from .resize import resize_image_with_resampling

GRID_DOWNSCALE_RESAMPLING_FILTER = Image.Resampling.BOX


def crop_image_to_target_aspect_ratio(
    image: Image.Image,
    target_width: int,
    target_height: int,
) -> Image.Image:
    """Return a center-cropped image that matches the target aspect ratio.

    Args:
        image: Source image to crop.
        target_width: Target output width in pixels.
        target_height: Target output height in pixels.

    Returns:
        A cropped image with the same aspect ratio as the target dimensions.
    """
    source_width, source_height = image.size
    source_aspect_ratio = source_width / source_height
    target_aspect_ratio = target_width / target_height

    if source_aspect_ratio > target_aspect_ratio:
        cropped_width = int(round(source_height * target_aspect_ratio))
        left_crop = (source_width - cropped_width) // 2
        right_crop = left_crop + cropped_width
        return image.crop((left_crop, 0, right_crop, source_height))

    if source_aspect_ratio < target_aspect_ratio:
        cropped_height = int(round(source_width / target_aspect_ratio))
        top_crop = (source_height - cropped_height) // 2
        bottom_crop = top_crop + cropped_height
        return image.crop((0, top_crop, source_width, bottom_crop))

    return image


def resize_image_to_fixed_grid(
    image: Image.Image,
    grid_width: int,
    grid_height: int,
) -> Image.Image:
    """Return an image resized to a fixed grid width and height.

    The operation center-crops to match the target aspect ratio, then
    downsamples with a box filter for cleaner low-resolution pixel-art output.

    Args:
        image: Input image to resize.
        grid_width: Target grid width in pixels.
        grid_height: Target grid height in pixels.

    Returns:
        A new image resized to the requested grid dimensions.
    """
    if grid_width <= 0 or grid_height <= 0:
        raise ValueError("Grid dimensions must be positive integers.")

    cropped_image = crop_image_to_target_aspect_ratio(
        image=image,
        target_width=grid_width,
        target_height=grid_height,
    )
    
    grid_image = resize_image_with_resampling(
        image=cropped_image,
        width=grid_width,
        height=grid_height,
        resampling_filter=GRID_DOWNSCALE_RESAMPLING_FILTER,
    )
    return grid_image
