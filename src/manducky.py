import random
from collections import namedtuple
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageChops

from .colors import DressColors, DuckyColors, make_man_duck_colors
from .ducky import ProceduralDucky
from .models import ManDuckRequest

ManDucky = namedtuple("ManDucky", "image")
Color = Tuple[int, int, int]

ASSETS_PATH = Path("duck-builder", "duck-person")
MAN_DUCKY_SIZE = (600, 1194)


class ManDuckGenerator:
    """Temporary class used to generate a ducky human."""

    def __init__(self):
        self.output: Image.Image = Image.new("RGBA", MAN_DUCKY_SIZE, color=(0, 0, 0, 0))

    @staticmethod
    def generate_tempalte(
            ducky: ProceduralDucky, dress_colors: DressColors, variation_: int
    ) -> dict:
        """Generate a man duck structure from given configuration."""
        variation = f"variation_{variation_}"

        template = {
            "head": (
                Image.open(ASSETS_PATH / "templates/head.png"),
                ducky.colors.body
            ),
            "eye": (
                Image.open(ASSETS_PATH / "templates/eye.png"),
                ducky.colors.eye
            ),
            "bill": (
                Image.open(ASSETS_PATH / "templates/bill.png"),
                ducky.colors.beak
            ),
            "hands": (
                Image.open(ASSETS_PATH / f"templates/{variation}/hands.png"),
                ducky.colors.wing
            )
        }

        if variation_ == 1:
            template["dress"] = (
                Image.open(ASSETS_PATH / "templates/variation_1/dress.png"),
                dress_colors.shirt
            )
        else:
            template['shirt'] = (
                Image.open(ASSETS_PATH / "templates/variation_2/shirt.png"),
                dress_colors.shirt
            )
            template['pants'] = (
                Image.open(ASSETS_PATH / "templates/variation_2/pants.png"),
                dress_colors.pants
            )

        if ducky.hat:
            template["hat"] = (
                Image.open(ASSETS_PATH / f"accessories/hats/{ducky.hat}.png"),
            )
        if ducky.outfit:
            template["outfit"] = (
                Image.open(ASSETS_PATH / f"outfits/{variation}/{ducky.outfit}.png"),
            )
        if ducky.equipment:
            template["equipment"] = (
                Image.open(ASSETS_PATH / f"equipment/{variation}/{ducky.equipment}.png"),
            )

        return template

    def generate_from_options(self, options: dict) -> dict:
        """Generate a man duck from the provided request."""
        colors = DuckyColors(**options["colors"])
        accessories = options["accessories"]

        return self.generate_tempalte(
            ducky=ProceduralDucky(None, colors, **accessories),
            dress_colors=DressColors(**options["dress_colors"]),
            variation_=options['variation']
        )

    def generate(
            self,
            *,
            options: Optional[ManDuckRequest] = None,
            ducky: Optional[ProceduralDucky] = None
    ) -> ManDucky:
        """Actually generate the man ducky from the provided request, else generate a random one.."""
        if options:
            template = self.generate_from_options(options.dict())
        else:
            template = self.generate_tempalte(
                ducky, make_man_duck_colors(), random.choice((1, 2))
            )

        for item in template.values():
            self.apply_layer(*item)

        return ManDucky(self.output)

    def apply_layer(self, layer: Image.Image, recolor: Optional[Color] = None) -> None:
        """Add the given layer on top of the ducky. Can be recolored with the recolor argument."""
        if recolor:
            if isinstance(recolor, dict):
                recolor = tuple(recolor.values())
            layer = ImageChops.multiply(layer, Image.new("RGBA", MAN_DUCKY_SIZE, color=recolor))
        self.output.alpha_composite(layer)
