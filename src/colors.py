import random
from collections import namedtuple
from colorsys import hls_to_rgb
from typing import Tuple

DuckyColors = namedtuple("DuckyColors", "eye eye_wing wing body beak")
DressColors = namedtuple("DressColors", "shirt pants")


def make_color(hue: float, dark_variant: bool) -> Tuple[float, float, float]:
    """Make a nice hls color to use in a duck."""
    saturation = 1
    lightness = random.uniform(.7, .85)

    # green and blue do not like high lightness, so we adjust this depending on how far from blue-green we are
    # hue_fix is the square of the distance between the hue and cyan (0.5 hue)
    hue_fix = (1 - abs(hue - 0.5)) ** 2
    # magic fudge factors
    lightness -= hue_fix * 0.15
    if dark_variant:
        lightness -= hue_fix * 0.25
    saturation -= hue_fix * 0.1

    return hue, lightness, saturation


def make_duck_colors() -> DuckyColors:
    """Create a matching DuckyColors object."""
    hue = random.random()
    dark_variant = random.choice([True, False])
    eye, wing, body, beak = (make_color(hue, dark_variant) for _ in range(4))

    # Lower the eye light
    eye_main = (eye[0], max(.1, eye[1] - .7), eye[2])
    eye_wing = (eye[0], min(.9, eye[1] + .4), eye[2])
    # Shift the hue of the beck
    beak = (beak[0] + .1 % 1, beak[1], beak[2])

    scalar_colors = [hls_to_rgb(*color_pair) for color_pair in (eye_main, eye_wing, wing, body, beak)]
    colors = (tuple(int(color * 256) for color in color_pair) for color_pair in scalar_colors)

    return DuckyColors(*colors)


def make_man_duck_colors() -> DressColors:
    """Create a matching DuckyColors object."""
    hue = random.random()
    dark_variant = random.choice([True, False])
    shirt, pants = (make_color(hue, dark_variant) for _ in range(2))

    scalar_colors = [hls_to_rgb(*color_pair) for color_pair in (shirt, pants)]
    colors = (tuple(int(color * 256) for color in color_pair) for color_pair in scalar_colors)

    return DressColors(*colors)
