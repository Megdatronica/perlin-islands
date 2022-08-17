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

WIDTH = 1920
HEIGHT = 1080
SUPPRESSION_AMPLITUDE = 250
BORDER_START = 100

SL = 127  # Sea Level

levels = {
    (0, SL*0.75): (30, 70, 220),      # Deep Blue sea
    (SL*0.75, SL): (30, 150, 180),   # Shallow sea
    (SL, SL*1.1): (239, 221, 111),  # Golden sand
    (SL*1.1, SL*1.26): (52, 140, 49),    # Green grass
    (SL*1.26, SL*1.57): (38, 106, 46),     # Dark Green jungle
    (SL*1.57, SL*1.77): (145, 142, 133),  # Grey stone mountain
    (SL*1.77, 256): (255, 255, 255),  # White snow
}

def main():
    if len(sys.argv) >= 2:
        seed = sys.argv[1]
    else:
        seed = round(time.time())
    print("Seed: {}".format(seed))
    random.seed(int(seed))

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
    draw_curve = True

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

        if j == int(curve_val) and draw_curve:
            img.putpixel((i, j), (255, 0, 0))
            continue

        horizontal_edge_dist = min(abs(i - WIDTH), abs(i))
        vertical_edge_dist = min(abs(j - HEIGHT), abs(j))
        edge_dist = min(horizontal_edge_dist, vertical_edge_dist)
        t = min(1.0, 1.0 - edge_dist/BORDER_START)
        p = min(1.0, noise_2d.lerp(t, 1.0, 0.0))
        val = val * p

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
