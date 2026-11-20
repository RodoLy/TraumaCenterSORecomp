"""Make wide versions of the story backgrounds (files/sprite/bg/*.tpx).

Each background is a 1024x512 picture with a 256-colour palette. The room itself only fills the
middle (columns 180 to 843, of which a 4:3 screen shows 190 to 833); the columns on either side
hold a flat colour and are never shown.
This tool paints those unused sides as a continuation of the room, so a wide screen can show more
of it instead of black bars. The room keeps its proportions: nothing in it is moved or stretched,
only what lies past its edges is drawn.

The sides are painted by LaMa ("Resolution-robust Large Mask Inpainting with Fourier
Convolutions", Suvorov et al. 2021), a model that fills in missing parts of a picture from what
surrounds them: it continues the beams, walls and floor it sees at the edges. The painted columns
are then matched to the picture's own 256 colours, so the file keeps its size, its format and its
palette, and the columns a 4:3 screen shows are left exactly as they were.

The game files are not changed: the new files are written to another folder, and the port only
uses them with the wide picture on. Nothing taken from the disc goes into this repository.

Needs: numpy, pillow, torch, and the LaMa model as TorchScript (big-lama.pt), for example from
https://github.com/Sanster/models/releases/download/add_big_lama/big-lama.pt

Usage:
    python tools/wide_backgrounds.py <disc>/files/sprite/bg <output folder> --model big-lama.pt

For every bgXXX.tpx it writes:
    <output>/bgXXX.tpx            the wide background, for the port
    <output>/preview/bgXXX.png    what a 16:9 screen would show, to look at before using it
"""

from __future__ import annotations

import argparse
import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

# The TPL inside a .tpx file starts after the file's own header.
TPL_START = 0xA0
TPL_MAGIC = 0x0020AF30
FORMAT_C8 = 9  # 8-bit colour index, 8x4 pixel tiles

# Where the game shows the picture: the 4:3 screen is 644 columns wide and 491 rows tall in the
# texture (the quad runs a little past the screen on every side), centred on the texture.
SCREEN_COLUMNS = 644
SCREEN_ROWS = 491


@dataclass
class Background:
    raw: bytes
    width: int
    height: int
    palette: np.ndarray  # 256 x 4 (R, G, B, A)
    indices: np.ndarray  # height x width, one palette index per pixel
    pixel_offset: int    # where the tiled indices start in `raw`


def read_tpx(path: Path) -> Background:
    raw = path.read_bytes()
    magic, image_count, table = struct.unpack_from(">III", raw, TPL_START)
    if magic != TPL_MAGIC or image_count != 1:
        raise ValueError(f"{path.name}: not a single-image TPL")
    image_header, palette_header = struct.unpack_from(">II", raw, TPL_START + table)
    count, _, _, palette_format, palette_data = struct.unpack_from(">HBBII", raw, TPL_START + palette_header)
    height, width, image_format, image_data = struct.unpack_from(">HHII", raw, TPL_START + image_header)
    if image_format != FORMAT_C8 or count != 256:
        raise ValueError(f"{path.name}: expected an 8-bit indexed picture, got format {image_format}")

    # The palette is stored as two halves: first (green, red) pairs, then (alpha, blue) pairs.
    start = TPL_START + palette_data
    green_red = np.frombuffer(raw, np.uint8, count * 2, start).reshape(count, 2)
    alpha_blue = np.frombuffer(raw, np.uint8, count * 2, start + count * 2).reshape(count, 2)
    palette = np.stack([green_red[:, 1], green_red[:, 0], alpha_blue[:, 1], alpha_blue[:, 0]], axis=1)

    pixel_offset = TPL_START + image_data
    tiled = np.frombuffer(raw, np.uint8, width * height, pixel_offset)
    indices = untile(tiled, width, height)
    return Background(raw, width, height, palette, indices, pixel_offset)


def untile(tiled: np.ndarray, width: int, height: int) -> np.ndarray:
    """C8 pixels are stored in 8x4 tiles, row by row inside each tile."""
    tiles = tiled.reshape(height // 4, width // 8, 4, 8)
    return tiles.transpose(0, 2, 1, 3).reshape(height, width)


def tile(indices: np.ndarray) -> bytes:
    height, width = indices.shape
    tiles = indices.reshape(height // 4, 4, width // 8, 8).transpose(0, 2, 1, 3)
    return tiles.astype(np.uint8).tobytes()


# Every background keeps its room in the same columns; the sides are filled with a colour close
# to the room's edge (not always perfectly flat, so they are not worked out from the picture).
ROOM_COLUMNS = (180, 843)
# The columns a 4:3 screen shows. The room's outermost ten columns on each side are never on
# screen and some carry a thin border line, so they are painted over along with the sides.
SHOWN_COLUMNS = (190, 833)


def nearest_palette_index(rgb: np.ndarray, palette: np.ndarray) -> np.ndarray:
    colours = palette[:, :3].astype(np.int32)
    flat = rgb.reshape(-1, 3).astype(np.int32)
    best = np.empty(len(flat), np.uint8)
    for start in range(0, len(flat), 65536):
        chunk = flat[start:start + 65536]
        distance = ((chunk[:, None, :] - colours[None, :, :]) ** 2).sum(axis=2)
        best[start:start + 65536] = distance.argmin(axis=1)
    return best.reshape(rgb.shape[:2])


# The model is given a few of the room's own columns next to each side too, so its painting meets
# the room without a seam; those columns are kept from the original afterwards.
OVERLAP = 4


def paint_sides(background: Background, model) -> tuple[np.ndarray, np.ndarray]:
    """Returns the new indices and the new picture (RGBA)."""
    import torch

    rgba = background.palette[background.indices]
    picture = rgba[:, :, :3].astype(np.float32) / 255.0
    left, right = SHOWN_COLUMNS
    sides = np.zeros(background.indices.shape, np.float32)
    sides[:, :left + OVERLAP] = 1.0
    sides[:, right + 1 - OVERLAP:] = 1.0
    with torch.no_grad():
        image = torch.from_numpy(picture).permute(2, 0, 1)[None]
        mask = torch.from_numpy(sides)[None, None]
        painted = model(image, mask)[0].permute(1, 2, 0).numpy()

    indices = background.indices.copy()
    outside = np.zeros(background.width, bool)
    outside[:left] = True
    outside[right + 1:] = True
    colours = (painted[:, outside] * 255).round().clip(0, 255)
    indices[:, outside] = nearest_palette_index(colours, background.palette)
    return indices, background.palette[indices]


def screen_preview(rgba: np.ndarray, aspect: float) -> Image.Image:
    """What a screen of the given aspect shows of the picture, at 1080 rows."""
    height, width = rgba.shape[:2]
    centre = (ROOM_COLUMNS[0] + ROOM_COLUMNS[1] + 1) / 2
    texel_width = (SCREEN_ROWS * 4 / 3) / SCREEN_COLUMNS  # texels are a little wider than tall
    columns = min(width, SCREEN_ROWS * aspect / texel_width)
    top = (height - SCREEN_ROWS) / 2
    box = (round(centre - columns / 2), round(top), round(centre + columns / 2), round(top + SCREEN_ROWS))
    picture = Image.fromarray(rgba.astype(np.uint8), "RGBA").convert("RGB").crop(box)
    return picture.resize((round(1080 * aspect), 1080), Image.LANCZOS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path, help="folder with the disc's bgXXX.tpx files")
    parser.add_argument("output", type=Path, help="folder for the wide files and the previews")
    parser.add_argument("--model", type=Path, required=True, help="LaMa model as TorchScript (big-lama.pt)")
    parser.add_argument("--only", nargs="*", help="names to do (bg000 bg001 ...); all when left out")
    args = parser.parse_args()

    import torch

    model = torch.jit.load(str(args.model), map_location="cpu")
    model.eval()
    (args.output / "preview").mkdir(parents=True, exist_ok=True)
    names = args.only or sorted(path.stem for path in args.source.glob("*.tpx"))
    for name in names:
        background = read_tpx(args.source / f"{name}.tpx")
        indices, rgba = paint_sides(background, model)
        raw = bytearray(background.raw)
        raw[background.pixel_offset:background.pixel_offset + indices.size] = tile(indices)
        (args.output / f"{name}.tpx").write_bytes(bytes(raw))
        screen_preview(rgba, 16 / 9).save(args.output / "preview" / f"{name}.png")
        print(f"{name}: done")


if __name__ == "__main__":
    main()
