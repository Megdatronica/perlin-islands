#!/usr/bin/env python3

import itertools
import math
import random
import subprocess
import sys
import time

import numpy as np
from PIL import Image

import noise_2d

WIDTH = 1000
HEIGHT = 500

def main():
    if len(sys.argv) >= 2:
        seed = sys.argv[1]
    else:
        seed = round(time.time())
    print("Seed: {}".format(seed))
    random.seed(seed)

    img = Image.new("RGB", (WIDTH, HEIGHT))
    coefficient = random.choice([1.0, -1.0])*random.uniform(math.sqrt(HEIGHT)/2, math.sqrt(HEIGHT)*2) / (WIDTH*100)
    y_offset = random.randint(HEIGHT//4, round(3*HEIGHT/4))
    # x_offset = random.randint(WIDTH//4, round(3*WIDTH/4))
    x_offset = 0
    print("{}*(x + {}) + {}".format(coefficient, x_offset, y_offset))

    while coefficient*(x_offset + WIDTH)*(x_offset + WIDTH) + y_offset <= 0 or coefficient*(x_offset + WIDTH)*(x_offset + WIDTH) + y_offset > HEIGHT:
        x_offset -= 1

    def fun(x):
        return coefficient*(x_offset + x)*(x_offset + x) + y_offset

    for i in range(WIDTH):
        y = round(fun(i))
        y = min(y, HEIGHT - 1)
        y = max(y, 0)
        img.putpixel((i, y), (255, 0, 0))
    img.save("parabola.png")
    subprocess.run(["open", "parabola.png"])

if __name__ == "__main__":
    main()
