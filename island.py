#!/usr/bin/env python3

import itertools
import random
import subprocess
import time

import numpy as np
from PIL import Image

import noise_2d

levels = {
    (0, 101): (30, 70, 220),      # Deep Blue sea
    (101, 127): (30, 150, 180),   # Shallow sea
    (128, 160): (239, 221, 111),  # Golden sand
    (161, 190): (52, 140, 49),    # Green grass
    (191, 220): (145, 142, 133),  # Grey stone mountain
    (220, 256): (255, 255, 255),  # White snow
}

def main():
    # random.seed(0)
    random.seed(time.time())
    height = 400
    width = 400
    noise = noise_2d.noisy_image(width, height, [(5, 1.0), (10, 0.2), (20, 0.05)])

    img = Image.new("RGB", (height, width))
    for i, j in itertools.product(range(width), range(height)):
        val = noise[i, j]
        for level, colour in levels.items():
            if val >= level[0] and val <= level[1]:
                img.putpixel((i, j), colour)
                break
        else:
            img.putpixel((i, j), (0, 0, 0))
    img.save("island.png")
    subprocess.run(["open", "island.png"])

if __name__ == "__main__":
    main()
