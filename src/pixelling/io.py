from PIL import Image
import os

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
    if not allow_overwrite:
        i = 1
        base, extension = os.path.splitext(output_image_path)
        while os.path.exists(output_image_path):
            output_image_path = f"{base}_{i}{extension}"  
            i += 1
        
    image.save(output_image_path)


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
