# Project Summary: Pixelling

Pixelling is a command-line image processing tool that converts images into
pixel-style outputs using deterministic image operations.

The tool supports two primary transformation modes:

1. Pixelation mode
   - Produces block-style pixelation while preserving the original image size
   - User controls visual pixel size via a block-size parameter
   - Implemented by downscaling then upscaling with nearest-neighbor resampling

2. Grid mode
   - Converts an image into a fixed low-resolution grid (e.g. 16x16, 32x32, 64x64)
   - Intended for sprite-style or icon-style pixel art
   - Optional upscale step for preview while preserving the true grid resolution

Pixelling is implemented in Python and uses the Pillow library for image
loading, resizing, color quantization, and output encoding.

The project is structured as a reusable library with a CLI front-end.
All image processing logic is isolated from CLI argument parsing to allow
future extensions such as batch processing, video support, or GUI wrappers.

The design goals are:
- Deterministic output 
- Clear and minimal CLI interface
- Testable image operations
- Clean separation between user interface and core logic
