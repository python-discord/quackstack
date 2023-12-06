from colorsys import hls_to_rgb, rgb_to_hls
from itertools import starmap
from random import Random
from typing import NamedTuple


class DuckyColors(NamedTuple):
    """RGB tuples of colours for each part of the Ducky."""

    eye: tuple[int, int, int]
    eye_wing: tuple[int, int, int]
    wing: tuple[int, int, int]
    body: tuple[int, int, int]
    beak: tuple[int, int, int]


class DressColors(NamedTuple):
    """RGB tuples of colours for each part of the Ducky's dress."""

    shirt: tuple[int, int, int]
    pants: tuple[int, int, int]


def make_color(random: Random, hue: float, *, dark_variant: bool) -> tuple[float, float, float]:
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


def make_duck_colors(random: Random) -> DuckyColors:
    """Create a matching DuckyColors object."""
    hue = random.random()
    dark_variant = random.choice([True, False])
    eye, wing, body, beak = (make_color(random, hue, dark_variant=dark_variant) for _ in range(4))

    # Lower the eye light
    eye_main = (eye[0], max(.1, eye[1] - .7), eye[2])
    eye_wing = (eye[0], min(.9, eye[1] + .4), eye[2])
    # Shift the hue of the beck
    beak = (beak[0] + .1 % 1, beak[1], beak[2])

    scalar_colors = list(starmap(hls_to_rgb, (eye_main, eye_wing, wing, body, beak)))
    colors = (tuple(int(color * 256) for color in color_pair) for color_pair in scalar_colors)

    return DuckyColors(*colors)


def make_man_duck_colors(ducky: tuple) -> DressColors:
    """Create a matching DuckyColors object."""
    hls_ = tuple(rgb_to_hls(ducky[0] / 255, ducky[1] / 255, ducky[2] / 255))

    # Find the first triadic hls color
    first_variant = [((hls_[0] * 360 + 120) % 360) / 360, hls_[1], hls_[2]]

    # Find the second triadic hls color
    second_variant = [((hls_[0] * 360 + 240) % 360) / 360, hls_[1], hls_[2]]

    first = tuple(
        round(x * 255) for x in hls_to_rgb(first_variant[0], first_variant[1], first_variant[2])
    )
    second = tuple(
        round(x * 255) for x in hls_to_rgb(second_variant[0], second_variant[1], second_variant[2])
    )

    return DressColors(first, second)
