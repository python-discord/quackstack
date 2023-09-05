from collections import namedtuple
from colorsys import hls_to_rgb, rgb_to_hls
from random import Random

DuckyColors = namedtuple("DuckyColors", "eye eye_wing wing body beak")
DressColors = namedtuple("DressColors", "shirt pants")


def make_color(random: Random, hue: float, dark_variant: bool) -> tuple[float, float, float]:
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
    eye, wing, body, beak = (make_color(random, hue, dark_variant) for _ in range(4))

    # Lower the eye light
    eye_main = (eye[0], max(.1, eye[1] - .7), eye[2])
    eye_wing = (eye[0], min(.9, eye[1] + .4), eye[2])
    # Shift the hue of the beck
    beak = (beak[0] + .1 % 1, beak[1], beak[2])

    scalar_colors = [hls_to_rgb(*color_pair) for color_pair in (eye_main, eye_wing, wing, body, beak)]
    colors = (tuple(int(color * 256) for color in color_pair) for color_pair in scalar_colors)

    return DuckyColors(*colors)


def make_man_duck_colors(ducky: tuple) -> DressColors:
    """Create a matching DuckyColors object."""
    hls_ = tuple(rgb_to_hls(ducky[0] / 255, ducky[1] / 255, ducky[2] / 255))

    # Find the first triadic hls color
    first_varient = [((hls_[0] * 360 + 120) % 360) / 360, hls_[1], hls_[2]]

    # Find the second triadic hls color
    second_varient = [((hls_[0] * 360 + 240) % 360) / 360, hls_[1], hls_[2]]

    first = tuple(
        round(x * 255) for x in hls_to_rgb(first_varient[0], first_varient[1], first_varient[2])
    )
    second = tuple(
        round(x * 255) for x in hls_to_rgb(second_varient[0], second_varient[1], second_varient[2])
    )

    return DressColors(first, second)
