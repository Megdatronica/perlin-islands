#!/usr/bin/env python3

import itertools
import math
import random
import statistics
import subprocess
import sys
import time

import numpy as np
from PIL import Image

# X_MAX = 3
# Y_MAX = 3
# PIXELS_PER_SQUARE = 5
X_MAX = 20
Y_MAX = 20
PIXELS_PER_SQUARE = 10

BLACK = (0,0,0)

def main():
    # random.seed(time.time())
    random.seed(2)

    px_max = 1000
    py_max = 1000

    noise1 = perlin_noise(9, 9, 125)
    noise2 = perlin_noise(21, 21, 50)
    noise3 = perlin_noise(101, 101, 10)

    img1 = image_from_noises([noise1], px_max, py_max)
    img2 = image_from_noises([noise2], px_max, py_max)
    # img3 = image_from_noises([smooth(noise3, 2, px_max, py_max)], px_max, py_max)
    img3 = image_from_noises([noise3], px_max, py_max)

    # img1 = image_from_noises([noise3], px_max, py_max)
    # img1.save("rough.png")
    # img3 = image_from_noises([smooth(noise3, 5, px_max, py_max)], px_max, py_max)
    # img3.save("smooth.png")

    img = image_from_noises([noise1, noise2, noise3], px_max, py_max, amplitudes=[1.0, 0.3, 0.05])
    img.save("noise.png")
    subprocess.run(["open", "noise.png"])

def noisy_image(width, height, octaves):
    """Generate a full 2d array of perlin noise.

    Args:
        - width: Width of image to generate
        - height: Height of image to generate
        - octaves: Array of (scale, amplitude) tuples, where:
            - scale is the number of noise squares per image
              (smaller = larger noise that varies more gradually)
            - amplitude is the size (between 0.0 and 1.0) of the peaks/troughs of the noise

    The noise takes values between 0 and 255, 127 being the average.

    """
    # result = {}
    # for i, j in itertools.product(range(width), range(height)):
    #     result[i,j] = 127
    result = np.full((width, height), 127)
    for freq, amplitude in octaves:
        points_per_square = width // (freq - 1)
        noise = perlin_noise(freq, freq, points_per_square)
        for i, j in itertools.product(range(width), range(height)):
            # The values seem to range from -0.7 to +0.7 at the extremes, so normalise in this range
            result[i,j] += noise[i,j]*amplitude*127 / 0.7
    return result

def image_from_noises(noises, px_max, py_max, amplitudes=[1.0]):
    img = Image.new("RGB", (px_max, py_max))
    for i, j in itertools.product(range(px_max), range(py_max)):
        # The values seem to range from -0.7 to +0.7 at the extremes, so normalise within this range
        value = 0
        for noise, amplitude in zip(noises, amplitudes):
            value += noise[i, j]*amplitude / 0.7

        brightness = 128 + round(value * 128)
        img.putpixel((i, j), (round(brightness/2), brightness//3, brightness))
    return img

def perlin_noise(x_max, y_max, points_per_square):
    const_vectors = {}
    for i, j in itertools.product(range(x_max+1), range(y_max+1)):
        x = rand_float(-1.0, 1.0)
        y = rand_float(-1.0, 1.0)
        gradient_vec = normalise((x, y))
        const_vectors[i, j] = gradient_vec

    # print(const_vectors)

    result = {}
    for i, j in itertools.product(range(x_max), range(y_max)):
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

def smooth(noise, d, px_max, py_max):
    """Smooth the noise out by setting each point to the average of all points within d."""
    smoothed = {}
    for key in noise.keys():
        i, j = key
        points_to_avg = points_within((i, j), d, px_max, py_max)
        smoothed[key] = statistics.mean([noise[p] for p in points_to_avg])
    return smoothed

def points_within(p, d, px_max, py_max):
    """Return all valid points with distance dof p."""
    x_range = range(max(0, p[0] - d), min(p[0] + d + 1, px_max))
    y_range = range(max(0, p[1] - d), min(p[1] + d + 1, py_max))

    points = []
    for point in itertools.product(x_range, y_range):
        if dist(p, point) <= d:
            points.append(point)
    return points

def dist(a, b):
    return math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 )

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

