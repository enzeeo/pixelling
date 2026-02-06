from PIL import Image

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
    pixelate_image = image.resize(size = (pixelate_width, pixelate_height), resample = Image.Resampling.NEAREST)
    upscaled_image = pixelate_image.resize(size = (width, height), resample = Image.Resampling.NEAREST)

    return upscaled_image

