#!/usr/bin/env python3

import itertools
import random
import subprocess

import numpy as np
from PIL import Image

import noise_2d

def main():
    random.seed(0)
    height = 400
    width = 400
    # noise = noise_2d.noisy_image(400, 400, [(5, 1.0), (9, 0.3), (41, 0.05)])
    noise = noise_2d.noisy_image(400, 400, [(5, 1.0), (10, 0.2), (20, 0.05)])
    # noise = noise_2d.noisy_image(width, height, [(5, 1.0)])

    img = Image.new("RGB", (height, width))
    for i, j in itertools.product(range(width), range(height)):
        img.putpixel((i,j), (noise[i, j], noise[i, j], noise[i, j]))
    img.save("island.png")
    subprocess.run(["open", "island.png"])

if __name__ == "__main__":
    main()
