#!/usr/bin/env python3

import itertools
from functools import partial
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

    fun = generate_curve(WIDTH, HEIGHT)

    img = Image.new("RGB", (WIDTH, HEIGHT))
    for i in range(WIDTH):
        y = round(fun(i))
        y = min(y, HEIGHT - 1)
        y = max(y, 0)
        img.putpixel((i, y), (255, 0, 0))
    img.save("parabola.png")
    subprocess.run(["open", "parabola.png"])

def generate_curve(width, height):
    """Return a function x -> y that will produce a nice curve."""
    coefficient = random.choice([1.0, -1.0])*random.uniform(math.sqrt(height)/2, math.sqrt(height)*2) / (width*100)
    y_offset = random.randint(height//4, round(3*height/4))
    # x_offset = random.randint(width//4, round(3*width/4))
    x_offset = 0
    print("{}*(x + {}) + {}".format(coefficient, x_offset, y_offset))

    def fun(coefficient, x_offset, y_offset, x):
        return coefficient*(x_offset + x)*(x_offset + x) + y_offset

    while fun(coefficient, x_offset, y_offset, width) < 0 or fun(coefficient, x_offset, y_offset, width) >= height:
        x_offset -= 1

    # Put the function roughly in the centre of the image in terms of its height
    output_values = [fun(coefficient, x_offset, y_offset, x) for x in range(WIDTH)]
    output_range = max(output_values) - min(output_values)
    height_adjustment = (HEIGHT//2 - output_range//2) - min(output_values)
    y_offset += height_adjustment

    return partial(fun, coefficient, x_offset, y_offset)

if __name__ == "__main__":
    main()
