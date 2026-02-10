from PIL import Image, ImageSequence

DEFAULT_LOOP_COUNT = 0
DEFAULT_FRAME_DURATION_MILLISECONDS = 100


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
    if not is_animated_gif_file(input_image_path):
        raise ValueError("Input path must point to an animated GIF file.")

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
    metadata: dict[str, object] | None = None,
) -> None:
    """Save animated GIF frames to a file path.

    Args:
        frames: Ordered list of frames to save.
        output_image_path: Destination path for the GIF file.
        metadata: Optional GIF metadata such as duration and loop.
    """
    if len(frames) == 0:
        raise ValueError("At least one frame is required to save an animated GIF.")

    metadata_dictionary = metadata or {}
    loop_count = int(metadata_dictionary.get("loop", DEFAULT_LOOP_COUNT))
    default_frame_duration_milliseconds = int(
        metadata_dictionary.get("duration", DEFAULT_FRAME_DURATION_MILLISECONDS)
    )

    frame_duration_values = metadata_dictionary.get("frame_durations")
    valid_frame_duration_list = isinstance(frame_duration_values, list) and (
        len(frame_duration_values) == len(frames)
    )
    if valid_frame_duration_list:
        frame_durations: list[int] = []
        for frame_duration_value in frame_duration_values:
            normalized_frame_duration = max(1, int(frame_duration_value))
            frame_durations.append(normalized_frame_duration)
    else:
        frame_durations = []
        for _ in range(len(frames)):
            normalized_frame_duration = max(1, default_frame_duration_milliseconds)
            frame_durations.append(normalized_frame_duration)

    frames_converted_to_rgba: list[Image.Image] = []
    for frame in frames:
        frames_converted_to_rgba.append(frame.convert("RGBA"))

    first_frame = frames_converted_to_rgba[0]
    remaining_frames = frames_converted_to_rgba[1:]

    save_arguments: dict[str, object] = {
        "format": "GIF",
        "save_all": True,
        "append_images": remaining_frames,
        "loop": loop_count,
        "duration": frame_durations,
    }

    disposal_value = metadata_dictionary.get("disposal")
    if disposal_value is not None:
        save_arguments["disposal"] = disposal_value

    transparency_value = metadata_dictionary.get("transparency")
    if isinstance(transparency_value, int):
        save_arguments["transparency"] = transparency_value

    first_frame.save(output_image_path, **save_arguments)
