from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from typing import Sequence

from .ops.pipeline import run_image_transformation_pipeline
from .io import (
    build_default_output_image_path,
    load_image_from_path,
    save_animated_image_to_path,
    save_image_to_path,
)
from .gif_io import is_animated_gif_file, load_animated_gif_frames_from_path
from .ops.animated_pipeline import run_animated_image_transformation_pipeline

import sys

def create_command_line_argument_parser() -> ArgumentParser:
    """Create and return the command-line argument parser for pixelling.

    Returns:
        An argument parser configured with pixelling commands and options.
    """
    argument_parser = ArgumentParser(
        prog="pixelling",
        description=(
            "Convert images into pixel-style outputs.\n"
            "Use pixel mode to keep original size, or grid mode to resize to a fixed grid."
        ),
        epilog=(
            "Examples:\n"
            "  pixelling input.png --mode pixel --block-size 8\n"
            "  pixelling input.png --mode grid --grid-width 32 --grid-height 32\n"
            "  pixelling input.png --mode pixel --block-size 6 --color-count 16 -o out.png"
        ),
        formatter_class=RawTextHelpFormatter,
    )

    argument_parser.add_argument(
        "input_image_path",
        type=str,
        help="Path to the input image file to transform.",
    )
    argument_parser.add_argument(
        "-o",
        "--output-image-path",
        type=str,
        default=None,
        help=(
            "Path to the output image file.\n"
            "If omitted, defaults to output.png."
        ),
    )
    argument_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    argument_parser.add_argument(
        "--mode",
        choices=["pixel", "grid"],
        required=True,
        help=(
            "Transformation mode.\n"
            "'pixel' keeps original image size.\n"
            "'grid' resizes to fixed width and height."
        ),
    )
    argument_parser.add_argument(
        "--block-size",
        type=int,
        default=None,
        help="Required for pixel mode. Size of each pixel block. Must be greater than 0.",
    )
    argument_parser.add_argument(
        "--grid-width",
        type=int,
        default=None,
        help="Required for grid mode. Target output width in pixels. Must be greater than 0.",
    )
    argument_parser.add_argument(
        "--grid-height",
        type=int,
        default=None,
        help="Required for grid mode. Target output height in pixels. Must be greater than 0.",
    )
    argument_parser.add_argument(
        "--color-count",
        type=int,
        default=None,
        help="Optional number of colors for quantization. Must be greater than 0.",
    )

    return argument_parser


def parse_command_line_arguments(
    command_line_arguments: Sequence[str] | None = None,
) -> Namespace:
    """Parse command-line arguments and return a namespace of values.

    Args:
        command_line_arguments: Optional command-line arguments to parse.

    Returns:
        Parsed command-line arguments.
    """
    argument_parser = create_command_line_argument_parser()
    parsed_arguments = argument_parser.parse_args(command_line_arguments)
    return parsed_arguments


def validate_command_line_arguments(parsed_arguments: Namespace) -> None:
    """Validate parsed command-line arguments and raise on invalid combinations.

    Args:
        parsed_arguments: Parsed command-line arguments to validate.
    """
    if parsed_arguments.mode == "pixel":
        if parsed_arguments.block_size is None:
            raise ValueError("Block size must be provided for pixel mode.")
        if parsed_arguments.grid_width is not None or parsed_arguments.grid_height is not None:
            raise ValueError("Grid width and height should not be provided for pixel mode.")
        
    elif parsed_arguments.mode == "grid":
        if parsed_arguments.grid_width is None or parsed_arguments.grid_height is None:
            raise ValueError("Grid width and height must be provided for grid mode.")
        if parsed_arguments.block_size is not None:
            raise ValueError("Block size should not be provided for grid mode.")


def run_command_line_interface(
    command_line_arguments: Sequence[str] | None = None,
) -> int:
    """Run the pixelling command-line interface.

    Args:
        command_line_arguments: Optional command-line arguments to process.

    Returns:
        Process exit status code.
    """
    parsed_arguments = parse_command_line_arguments(command_line_arguments)
    validate_command_line_arguments(parsed_arguments)

    if parsed_arguments.output_image_path is None:
        parsed_arguments.output_image_path = build_default_output_image_path(
            parsed_arguments.input_image_path
        )

    if is_animated_gif_file(parsed_arguments.input_image_path):
        frames, metadata = load_animated_gif_frames_from_path(parsed_arguments.input_image_path)
        transformed_frames = run_animated_image_transformation_pipeline(
            frames=frames,
            transformation_mode=parsed_arguments.mode,
            block_size=parsed_arguments.block_size,
            grid_width=parsed_arguments.grid_width,
            grid_height=parsed_arguments.grid_height,
            color_count=parsed_arguments.color_count,
        )
        save_animated_image_to_path(
            frames=transformed_frames,
            output_image_path=parsed_arguments.output_image_path,
            allow_overwrite=parsed_arguments.overwrite,
            metadata=metadata,
        )
        return 0
    
    else: 
        image = load_image_from_path(parsed_arguments.input_image_path)

        output_image = run_image_transformation_pipeline(
                                  image=image,
                                  transformation_mode=parsed_arguments.mode,
                                  block_size=parsed_arguments.block_size,
                                  grid_width=parsed_arguments.grid_width,
                                  grid_height=parsed_arguments.grid_height,
                                  color_count=parsed_arguments.color_count,
                              )

        save_image_to_path(
            image=output_image,
            output_image_path=parsed_arguments.output_image_path,
            allow_overwrite=parsed_arguments.overwrite,
        )

        return 0
    

def main() -> None:
    """Run the pixelling command-line entry point."""
    exit_status = run_command_line_interface()
    sys.exit(exit_status)
