#!/usr/bin/env python3

import itertools
import math
import random
import subprocess
import sys
import time

from PIL import Image

# X_MAX = 3
# Y_MAX = 3
# PIXELS_PER_SQUARE = 5
X_MAX = 8
Y_MAX = 8
PIXELS_PER_SQUARE = 8

CANVAS_SIZE = ((X_MAX-1)*PIXELS_PER_SQUARE, (Y_MAX-1)*PIXELS_PER_SQUARE)
BLACK = (0,0,0)


def main():
    # random.seed(2)
    random.seed(time.time())

    const_vectors = {}
    for i, j in itertools.product(range(X_MAX), range(Y_MAX)):
        x = rand_float(-1.0, 1.0)
        y = rand_float(-1.0, 1.0)
        gradient_vec = normalise((x, y))
        const_vectors[i, j] = gradient_vec

    print(const_vectors)

    img = Image.new("RGB", CANVAS_SIZE)

    for i, j in itertools.product(range(X_MAX - 1), range(Y_MAX - 1)):
        # print("square {}".format(i))
        for a, b in itertools.product(range(PIXELS_PER_SQUARE), range(PIXELS_PER_SQUARE)):
            displacement_top_left = (-a/PIXELS_PER_SQUARE, -b/PIXELS_PER_SQUARE)
            offset_dot_product_top_left = dot(const_vectors[i, j], displacement_top_left)

            displacement_top_right = ((PIXELS_PER_SQUARE - a)/PIXELS_PER_SQUARE, -b/PIXELS_PER_SQUARE)
            offset_dot_product_top_right = dot(const_vectors[i+1, j], displacement_top_right)

            displacement_bottom_left = (-a/PIXELS_PER_SQUARE, (PIXELS_PER_SQUARE - b)/PIXELS_PER_SQUARE)
            offset_dot_product_bottom_left = dot(const_vectors[i, j+1], displacement_bottom_left)

            displacement_bottom_right = ((PIXELS_PER_SQUARE - a)/PIXELS_PER_SQUARE, (PIXELS_PER_SQUARE - b)/PIXELS_PER_SQUARE)
            offset_dot_product_bottom_right = dot(const_vectors[i+1, j+1], displacement_bottom_right)

            interpleft = lerp(b/PIXELS_PER_SQUARE, offset_dot_product_top_left, offset_dot_product_bottom_left)
            interpright = lerp(b/PIXELS_PER_SQUARE, offset_dot_product_top_right, offset_dot_product_bottom_right)
            interp = lerp(a/PIXELS_PER_SQUARE, interpleft, interpright)

            x_val = PIXELS_PER_SQUARE*i + a
            y_val = PIXELS_PER_SQUARE*j + b
            color = 128 + round(interp * 256)
            print(i, j, a, b, interp, color)

            # if ((i, j, a, b) == (0, 1, 4, 2)):
            #     print("Top left:", const_vectors[i,j], displacement_top_left)
            #     print("Top right:", const_vectors[i+1,j], displacement_top_right)
            #     print("Bottom left:", const_vectors[i,j+1], displacement_bottom_left)
            #     print("Bottom right:", const_vectors[i+1,j+1], displacement_bottom_right)
            # if ((i, j, a, b) == (1, 1, 0, 2)):
            #     print("Top left:", const_vectors[i,j], displacement_top_left)
            #     print("Top right:", const_vectors[i+1,j], displacement_top_right)
            #     print("Bottom left:", const_vectors[i,j+1], displacement_bottom_left)
            #     print("Bottom right:", const_vectors[i+1,j+1], displacement_bottom_right)
            # print(x_val, y_val)
            img.putpixel((x_val, y_val), (color, color, color))

    img.save("noise.png")
    subprocess.run(["open", "noise.png"])

def rand_float(start=0.0, end=1.0):
    """Return random float in range [start, end)."""
    return start + (end - start)*random.random()

def lerp(t, a1, a2):
    """Get t of the way between a1 and a2 (0 <= t <= 1)."""
    return a1 + t*(a2 - a1)

def normalise(vec):
    """Normalise the given vector so it has length 1."""
    scale = 1/math.sqrt((vec[0] * vec[0]) + (vec[1] * vec[1]))
    return (vec[0]*scale, vec[1]*scale)

def dot(vec_a, vec_b):
    """Return the dot product between the two vectors."""
    return vec_a[0]*vec_b[0] + vec_a[1]*vec_b[1]

if __name__ == "__main__":
    main()

