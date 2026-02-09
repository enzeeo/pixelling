from PIL import Image, ImageSequence


def is_animated_gif_file(input_image_path: str) -> bool:
    """Return whether the input path points to an animated GIF file.

    Args:
        input_image_path: Path to an input image file.

    Returns:
        True when the file is an animated GIF; otherwise False.
    """
    with Image.open(input_image_path) as image:
        if image.format == "GIF":
            is_gif = True
        else:
            is_gif = False
        is_animated = bool(getattr(image, "is_animated", False))

    return is_gif and is_animated 


def load_animated_gif_frames_from_path(
    input_image_path: str,
) -> tuple[list[Image.Image], dict[str, object]]:
    """Load animated GIF frames and metadata from a file path.

    Args:
        input_image_path: Path to an animated GIF file.

    Returns:
        A tuple containing:
        - A list of image frames.
        - A metadata dictionary for fields like duration and loop.
    """
    if is_animated_gif_file(input_image_path):
        with Image.open(input_image_path) as image:
            
            gif_metadata: dict[str, object] = {
                "loop": image.info.get("loop", 0),
                "duration": image.info.get("duration", 0),
                "disposal": image.info.get("disposal"),
                "transparency": image.info.get("transparency"),
            }

            frame_images: list[Image.Image] = []
            frame_durations: list[int] = []

            for frame in ImageSequence.Iterator(image):
                frame_images.append(frame.convert("RGBA").copy())
                frame_durations.append(int(frame.info.get("duration", gif_metadata["duration"])))

            gif_metadata["frame_durations"] = frame_durations
            return frame_images, gif_metadata


def save_animated_gif_frames_to_path(
    frames: list[Image.Image],
    output_image_path: str,
    allow_overwrite: bool,
    metadata: dict[str, object] | None = None,
) -> None:
    """Save animated GIF frames to a file path.

    Args:
        frames: Ordered list of frames to save.
        output_image_path: Destination path for the GIF file.
        allow_overwrite: Whether an existing file may be overwritten.
        metadata: Optional GIF metadata such as duration and loop.
    """
    raise NotImplementedError("Animated GIF frame saving is not implemented yet.")
