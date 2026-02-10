# Pixelling
Pixelling is a command-line tool that converts images and animated GIFs 
into pixel-art style outputs using either pixelation or fixed-grid resizing.

## Features
Two modes:
- `pixel` mode keeps the original image size but makes it look blocky.
- `grid` mode resizes the image to a small fixed size like 32x32.

Optional color reduction with `--color-count` to create a limited-palette look.

Works with animated GIFs by processing each frame of the animation.

File saving:
- Creates a default output filename automatically.
- Avoids replacing existing files unless you use `--overwrite`.

## Examples 

<p align="center">
  <img src="contents/rain.jpg" alt="Original image" width="320" />
  <img src="contents/rain_pixelling.jpg" alt="Pixelated image" width="320" />
</p>
<p align="center"><em>Left: original | Right: pixelated</em></p>

Running the pixel mode with a block size of 10

`pixelling content/rain.jpg --mode pixel --block-size 10`