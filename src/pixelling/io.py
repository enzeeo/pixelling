import os

from PIL import Image

from .gif_io import save_animated_gif_frames_to_path

def load_image_from_path(input_image_path: str) -> Image.Image:
    """Load and return an image from a filesystem path.

    Args:
        input_image_path: Path to the input image file.

    Returns:
        Loaded Pillow image.
    """
    with Image.open(input_image_path) as image:
        return image.copy()


def save_image_to_path(
    image: Image.Image,
    output_image_path: str,
    allow_overwrite: bool,
) -> None:
    """Save an image to a filesystem path.

    Args:
        image: Image object to save.
        output_image_path: Destination image file path.
        allow_overwrite: Whether an existing file may be overwritten.
    """
    output_image_path = build_available_output_image_path(
        output_image_path=output_image_path,
        allow_overwrite=allow_overwrite,
    )
    image.save(output_image_path)


def save_animated_image_to_path(
    frames: list[Image.Image],
    output_image_path: str,
    allow_overwrite: bool,
    metadata: dict[str, object] | None = None,
) -> None:
    """Save an animated frame sequence to a filesystem path.

    Args:
        frames: Ordered list of image frames to save.
        output_image_path: Destination image file path.
        allow_overwrite: Whether an existing file may be overwritten.
        metadata: Optional animation metadata such as duration and loop.
    """
    output_image_path = build_available_output_image_path(
        output_image_path=output_image_path,
        allow_overwrite=allow_overwrite,
    )
    save_animated_gif_frames_to_path(
        frames=frames,
        output_image_path=output_image_path,
        metadata=metadata,
    )


def build_available_output_image_path(
    output_image_path: str,
    allow_overwrite: bool,
) -> str:
    """Return an output path that respects overwrite behavior.

    Args:
        output_image_path: Requested destination image file path.
        allow_overwrite: Whether an existing file may be overwritten.

    Returns:
        A path that is available for writing.
    """
    if allow_overwrite:
        return output_image_path

    copy_number = 1
    output_file_stem, output_file_extension = os.path.splitext(output_image_path)
    while os.path.exists(output_image_path):
        output_image_path = f"{output_file_stem}_{copy_number}{output_file_extension}"
        copy_number += 1

    return output_image_path


def build_default_output_image_path(input_image_path: str) -> str:
    """Build the default output path for a transformed image.

    Args:
        input_image_path: Source image file path.

    Returns:
        Output image file path based on the input path.
    """
    input_directory_path, input_file_name = os.path.split(input_image_path)
    input_file_stem, extension = os.path.splitext(input_file_name)

    if not input_file_stem:
        raise ValueError("Input image path must include a file name.")

    if not extension:
        extension = ".png"

    output_file_name = f"{input_file_stem}_pixelling{extension}"
    output_image_path = os.path.join(input_directory_path, output_file_name)
    return output_image_path
