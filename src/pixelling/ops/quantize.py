from PIL import Image

RGB_MODE = "RGB"
RGBA_MODE = "RGBA"
QUANTIZATION_METHOD = Image.Quantize.MEDIANCUT
DITHER_DISABLED = Image.Dither.NONE
DITHER_FLOYD_STEINBERG = Image.Dither.FLOYDSTEINBERG


def quantize_image_colors(image: Image.Image, color_count: int) -> Image.Image:
    """Return an image with colors reduced to the given count without dithering.

    Args:
        image: Input image to quantize.
        color_count: Number of colors to keep in the output image.

    Returns:
        A new image with a reduced color palette and preserved transparency.
    """
    return _quantize_image_colors(image, color_count, DITHER_DISABLED)


def quantize_image_colors_with_dithering(
    image: Image.Image,
    color_count: int,
) -> Image.Image:
    """Return an image with colors reduced using Floyd-Steinberg dithering.

    Args:
        image: Input image to quantize.
        color_count: Number of colors to keep in the output image.

    Returns:
        A new image with a reduced color palette and preserved transparency.
    """
    return _quantize_image_colors(image, color_count, DITHER_FLOYD_STEINBERG)


def apply_dithering_to_image(
    image: Image.Image,
    color_count: int,
) -> Image.Image:
    """Return an image with dithering applied during quantization.

    Args:
        image: Input image to dither and quantize.
        color_count: Number of colors to keep in the output image.

    Returns:
        A new image with a reduced color palette and preserved transparency.
    """
    return quantize_image_colors_with_dithering(image, color_count)


def _quantize_image_colors(
    image: Image.Image,
    color_count: int,
    dither_mode: Image.Dither,
) -> Image.Image:
    if color_count <= 0:
        raise ValueError("Color count must be a positive integer.")

    if "A" in image.getbands():
        rgba_image = image.convert(RGBA_MODE)
        red_channel, green_channel, blue_channel, alpha_channel = rgba_image.split()
        rgb_image = Image.merge(RGB_MODE, (red_channel, green_channel, blue_channel))
        quantized_image = rgb_image.quantize(
            colors=color_count,
            method=QUANTIZATION_METHOD,
            dither=dither_mode,
        )
        restored_image = quantized_image.convert(RGBA_MODE)
        restored_image.putalpha(alpha_channel)
        return restored_image

    rgb_image = image.convert(RGB_MODE)
    quantized_image = rgb_image.quantize(
        colors=color_count,
        method=QUANTIZATION_METHOD,
        dither=dither_mode,
    )
    return quantized_image.convert(RGB_MODE)
