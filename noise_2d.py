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
X_MAX = 20
Y_MAX = 20
PIXELS_PER_SQUARE = 10
BLACK = (0,0,0)

def main():
    # random.seed(2)
    CANVAS_SIZE = ((X_MAX-1)*PIXELS_PER_SQUARE, (Y_MAX-1)*PIXELS_PER_SQUARE)
    noise = perlin_noise(X_MAX, Y_MAX, PIXELS_PER_SQUARE)

    img = Image.new("RGB", CANVAS_SIZE)
    for i, j in itertools.product(range(CANVAS_SIZE[0]), range(CANVAS_SIZE[1])):
        value = noise[i, j]
        # The values seem to range from -0.7 to +0.7 at the extremes, so normalise within this range
        brightness = 128 + round((value / 0.7) * 128)
        img.putpixel((i, j), (brightness, brightness, brightness))

    img.save("noise.png")
    subprocess.run(["open", "noise.png"])

def perlin_noise(x_max, y_max, points_per_square):
    random.seed(time.time())

    const_vectors = {}
    for i, j in itertools.product(range(x_max), range(y_max)):
        x = rand_float(-1.0, 1.0)
        y = rand_float(-1.0, 1.0)
        gradient_vec = normalise((x, y))
        const_vectors[i, j] = gradient_vec

    # print(const_vectors)

    result = {}
    for i, j in itertools.product(range(x_max - 1), range(y_max - 1)):
        # print("square {}".format(i))
        for a, b in itertools.product(range(points_per_square), range(points_per_square)):
            displacement_top_left = (-a/points_per_square, -b/points_per_square)
            offset_dot_product_top_left = dot(const_vectors[i, j], displacement_top_left)

            displacement_top_right = ((points_per_square - a)/points_per_square, -b/points_per_square)
            offset_dot_product_top_right = dot(const_vectors[i+1, j], displacement_top_right)

            displacement_bottom_left = (-a/points_per_square, (points_per_square - b)/points_per_square)
            offset_dot_product_bottom_left = dot(const_vectors[i, j+1], displacement_bottom_left)

            displacement_bottom_right = ((points_per_square - a)/points_per_square, (points_per_square - b)/points_per_square)
            offset_dot_product_bottom_right = dot(const_vectors[i+1, j+1], displacement_bottom_right)

            interpleft = fade_lerp(b/points_per_square, offset_dot_product_top_left, offset_dot_product_bottom_left)
            interpright = fade_lerp(b/points_per_square, offset_dot_product_top_right, offset_dot_product_bottom_right)
            interp = fade_lerp(a/points_per_square, interpleft, interpright)

            x_val = points_per_square*i + a
            y_val = points_per_square*j + b
            result[x_val, y_val] = interp

    return result

def rand_float(start=0.0, end=1.0):
    """Return random float in range [start, end)."""
    return start + (end - start)*random.random()

def lerp(t, a1, a2):
    """Linear interpolation; get fraction t of the way between a1 and a2 (0 <= t <= 1)."""
    return a1 + t*(a2 - a1)

def fade(t):
    """Turn t into a smoother curve for linear interpolation."""
    return 6*(t**5) - 15*(t**4) + 10*(t**3)

def fade_lerp(t, a1, a2):
    return lerp(fade(t), a1, a2)

def normalise(vec):
    """Normalise the given vector so it has length 1."""
    scale = 1/math.sqrt((vec[0] * vec[0]) + (vec[1] * vec[1]))
    return (vec[0]*scale, vec[1]*scale)

def dot(vec_a, vec_b):
    """Return the dot product between the two vectors."""
    return vec_a[0]*vec_b[0] + vec_a[1]*vec_b[1]

if __name__ == "__main__":
    main()

