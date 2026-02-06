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
    raise NotImplementedError("Resize helper has not been implemented yet.")


def select_resampling_filter(resampling_name: str) -> Image.Resampling:
    """Return the Pillow resampling filter for a given user-facing name.

    Args:
        resampling_name: Human-readable resampling filter name.

    Returns:
        The Pillow resampling enum value for the provided name.
    """
    raise NotImplementedError("Resampling selection has not been implemented yet.")
