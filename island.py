#!/usr/bin/env python3
"""
https://medium.com/@yvanscher/playing-with-perlin-noise-generating-realistic-archipelagos-b59f004d8401
"""

import itertools
import random
import subprocess
import sys
import time

import numpy as np
from PIL import Image

import noise_2d
from curve import generate_curve

levels = {
    (0, 100): (30, 70, 220),      # Deep Blue sea
    (100, 127): (30, 150, 180),   # Shallow sea
    (127, 140): (239, 221, 111),  # Golden sand
    (140, 160): (52, 140, 49),    # Green grass
    (160, 200): (38, 106, 46),     # Dark Green jungle
    (200, 225): (145, 142, 133),  # Grey stone mountain
    (225, 256): (255, 255, 255),  # White snow
}

WIDTH = 1000
HEIGHT = 500
SUPPRESSION_AMPLITUDE = 500

def main():
    if len(sys.argv) >= 2:
        seed = sys.argv[1]
    else:
        seed = round(time.time())
    print("Seed: {}".format(seed))
    random.seed(seed)

    # noise = noise_2d.noisy_image(WIDTH, HEIGHT, [(5, 1.0), (10, 0.2), (20, 0.05)])
    # noise = noise_2d.noisy_image(WIDTH, HEIGHT, [(10, 1.0), (20, 0.02), (40, 0.05)])
    # noise = noise_2d.noisy_image(WIDTH, HEIGHT, [(60, 1.0), (30, 0.02), (15, 0.05)])

    octaves = [
        (HEIGHT//5, 1.0),
        (HEIGHT//10, 0.2),
        (HEIGHT//20, 0.5),
    ]
    noise = noise_2d.noisy_image(WIDTH, HEIGHT, octaves)

    # shape = numpy.full((WIDTH, HEIGHT), 127)

    # midpoint = (WIDTH//2, HEIGHT//2)
    curve = generate_curve(WIDTH, HEIGHT)
    img = Image.new("RGB", (WIDTH, HEIGHT))
    for i, j in itertools.product(range(WIDTH), range(HEIGHT)):
        # img.putpixel((i, j), (int(noise[i, j]), int(noise[i, j]), int(noise[i, j])))
        val = noise[i, j]

        # dist = abs(j - HEIGHT//2)
        curve_val = curve(i)
        dist = abs(j - curve_val)
        dist_fraction = min(dist / (HEIGHT // 2), 1)
        p = noise_2d.fade_lerp(dist_fraction, 0, SUPPRESSION_AMPLITUDE)
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
