from PIL import Image

RED_GREEN_BLUE_MODE = "RGB"
RED_GREEN_BLUE_ALPHA_MODE = "RGBA"
QUANTIZATION_METHOD = Image.Quantize.MEDIANCUT


def quantize_image_colors(image: Image.Image, color_count: int) -> Image.Image:
    """Return an image with colors reduced to the given count.

    Args:
        image: Input image to quantize.
        color_count: Number of colors to keep in the output image.

    Returns:
        A new image with a reduced color palette and preserved transparency.
    """
    if color_count <= 0:
        raise ValueError("Color count must be a positive integer.")

    if "A" in image.getbands():
        image_with_alpha = image.convert(RED_GREEN_BLUE_ALPHA_MODE)
        red_channel, green_channel, blue_channel, alpha_channel = image_with_alpha.split()
        image_without_alpha = Image.merge(
            RED_GREEN_BLUE_MODE,
            (red_channel, green_channel, blue_channel),
        )
        quantized_image = image_without_alpha.quantize(
            colors=color_count,
            method=QUANTIZATION_METHOD,
        )
        restored_image = quantized_image.convert(RED_GREEN_BLUE_ALPHA_MODE)
        restored_image.putalpha(alpha_channel)
        return restored_image

    image_without_alpha = image.convert(RED_GREEN_BLUE_MODE)
    quantized_image = image_without_alpha.quantize(
        colors=color_count,
        method=QUANTIZATION_METHOD,
    )
    return quantized_image.convert(RED_GREEN_BLUE_MODE)
