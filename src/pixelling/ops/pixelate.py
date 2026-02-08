from PIL import Image
from .resize import resize_image_with_resampling


def pixelate_image_with_block_size(image: Image.Image, block_size: int) -> Image.Image:
    """Return a pixelated copy of the image using a fixed block size.

    Args:
        image: Input image to pixelate.
        block_size: Size of each pixel block in pixels.

    Returns:
        A new image with block-style pixelation applied.
    """
    width, height = image.size
    if block_size <= 0:
        raise ValueError("Block size must be a positive integer.")
    if block_size > min(width, height):
        raise ValueError("Block size must not exceed the smaller image dimension.")
    
    pixelate_width = width // block_size
    pixelate_height = height // block_size

    pixelate_image = resize_image_with_resampling(
        image=image,
        width=pixelate_width,
        height=pixelate_height,
        resampling_filter=Image.Resampling.NEAREST,
    )
    
    upscaled_image = resize_image_with_resampling(
        image=pixelate_image,
        width=width,
        height=height,
        resampling_filter=Image.Resampling.NEAREST,
    )

    return upscaled_image
