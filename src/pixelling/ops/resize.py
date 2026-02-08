"""Resize helpers and resampling choices."""

from PIL import Image


def resize_image_with_resampling(
    image: Image.Image,
    width: int,
    height: int,
    resampling_filter: Image.Resampling,
) -> Image.Image:
    """Return an image resized to the target width and height.

    Args:
        image: Input image to resize.
        width: Target width in pixels.
        height: Target height in pixels.
        resampling_filter: Pillow resampling filter to use.

    Returns:
        A new image resized with the requested resampling filter.
    """
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")
    
    resized_image = image.resize( (width, height), resample=resampling_filter)
    return resized_image


def select_resampling_filter(resampling_name: str) -> Image.Resampling:
    """Return the Pillow resampling filter for a given user-facing name.

    Args:
        resampling_name: Human-readable resampling filter name.

    Returns:
        The Pillow resampling enum value for the provided name.
    """
    resampling_names = {
        "nearest": Image.Resampling.NEAREST,
        "bilinear": Image.Resampling.BILINEAR,
        "bicubic": Image.Resampling.BICUBIC,
        "lanczos": Image.Resampling.LANCZOS,
    }

    normalized_resampling_name = resampling_name.strip().lower()
    if normalized_resampling_name not in resampling_names:
        raise ValueError(
            f"Invalid resampling filter name: '{resampling_name}'. "
            f"Valid options are: {', '.join(resampling_names.keys())}."
        )
    
    return resampling_names[normalized_resampling_name]
