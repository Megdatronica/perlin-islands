#!/usr/bin/env python3

import itertools
import random
import subprocess
import time

import numpy as np
from PIL import Image

import noise_2d

levels = {
    (0, 100): (30, 70, 220),      # Deep Blue sea
    (100, 127): (30, 150, 180),   # Shallow sea
    (127, 160): (239, 221, 111),  # Golden sand
    (160, 190): (52, 140, 49),    # Green grass
    (190, 220): (145, 142, 133),  # Grey stone mountain
    (220, 256): (255, 255, 255),  # White snow
}

def main():
    # random.seed(0)
    random.seed(time.time())
    height = 600
    width = 600
    # noise = noise_2d.noisy_image(width, height, [(5, 1.0), (10, 0.2), (20, 0.05)])
    noise = noise_2d.noisy_image(width, height, [(10, 1.0), (20, 0.02), (40, 0.05)])

    # shape = numpy.full((width, height), 127)

    midpoint = (height//2, width//2)
    img = Image.new("RGB", (height, width))
    for i, j in itertools.product(range(width), range(height)):
        val = noise[i, j]

        dist = noise_2d.dist((i, j), midpoint)
        # dist_fraction = 1 - max(dist / (height//2), 1.0)
        # print(i, j, dist_fraction)
        # val -= dist_fraction * 127
        dist_fraction = min(dist / (height/1.5), 1)
        # val = max(0, val - dist_fraction*127)
        p = noise_2d.fade_lerp(dist_fraction, 0, 150)
        val = max(0, val - p)

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
