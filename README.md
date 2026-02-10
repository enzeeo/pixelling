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

| Original |  | Pixelated |
|---|---|---|
| <img src="contents/original.png" alt="Original image" width="320" /> |  | <img src="contents/pixelated.png" alt="Pixelated image" width="320" /> |

- Running the pixel mode with a block size of 10
- `pixelling content/rain.jpg --mode pixel --block-size 10`