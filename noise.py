#!/usr/bin/env python3

import math
import random
import subprocess
import sys
import time

from PIL import Image

X_MAX = 10
# PIXELS_PER_SQUARE = 100
PIXELS_PER_SQUARE = 100
CANVAS_SIZE = X_MAX*PIXELS_PER_SQUARE
BLACK = (0,0,0)

def main():
    # random.seed(0)
    random.seed(time.time())
    const_vectors = [(float(i), rand_float(-1.0, 1.0)) for i in range(X_MAX + 1)]
    # print(const_vectors)

    img = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), color="white")

    for i in range(X_MAX):
        # print("square {}".format(i))
        for j in range(PIXELS_PER_SQUARE):
            offset_dot_product_left = const_vectors[i][1] * j/PIXELS_PER_SQUARE
            offset_dot_product_right = const_vectors[i+1][1] * -(PIXELS_PER_SQUARE-j)/PIXELS_PER_SQUARE
            final = lerp(j/PIXELS_PER_SQUARE, offset_dot_product_left, offset_dot_product_right)

            x_val = PIXELS_PER_SQUARE*i + j
            y_val = math.floor(CANVAS_SIZE//2 + final*CANVAS_SIZE/2)
            # print(x_val, y_val)
            img.putpixel((x_val, y_val), BLACK)
            # print(offset_dot_product_left, offset_dot_product_right, final)

    img.save("noise.png")
    subprocess.run(["open", "noise.png"])

def rand_float(start=0.0, end=1.0):
    """Return random float in range [start, end)."""
    return start + (end - start)*random.random()

def lerp(t, a1, a2):
    return a1 + t*(a2 - a1)

if __name__ == "__main__":
    main()
