import os
import random
from collections import namedtuple
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageChops
from fastapi import HTTPException

from .colors import DressColors, DuckyColors, make_man_duck_colors
from .ducky import ProceduralDucky
from .models import ManDuckRequest

ManDucky = namedtuple("ManDucky", "image")
Color = Tuple[int, int, int]

ASSETS_PATH = Path("duck-builder", "duck-person")
MAN_DUCKY_SIZE = (600, 1194)


class ManDuckGenerator:
    """Temporary class used to generate a ducky human."""

    VARIATIONS = (1, 2)
    HATS = {
        filename.stem: filename for filename in (ASSETS_PATH / "accessories/hats").iterdir()
    }
    OUTFITS = {
        "variation_1": {
            filename.stem: filename for filename in (ASSETS_PATH / "outfits/variation_1").iterdir()
        },
        "variation_2": {
            filename.stem: filename for filename in (ASSETS_PATH / "outfits/variation_2").iterdir()
        }
    }
    EQUIPMENTS = {
        "variation_1": {
            filename.stem: filename for filename in (ASSETS_PATH / "equipment/variation_1").iterdir()
        },
        "variation_2": {
            filename.stem: filename for filename in (ASSETS_PATH / "equipment/variation_2").iterdir()
        }
    }

    def __init__(self):
        self.output: Image.Image = Image.new("RGBA", MAN_DUCKY_SIZE, color=(0, 0, 0, 0))

    def generate_tempalte(
            self, ducky: ProceduralDucky, dress_colors: DressColors, variation_: int
    ) -> dict:
        """Generate a man duck structure from given configuration."""
        variation = f"variation_{variation_}"

        template = {
            "bill": (
                ASSETS_PATH / "templates/bill.png",
                ducky.colors.beak
            ),
            "head": (
                ASSETS_PATH / "templates/head.png",
                ducky.colors.body
            ),
            "eye": (
                ASSETS_PATH / "templates/eye.png",
                ducky.colors.eye
            ),
            "hands": (
                ASSETS_PATH / f"templates/{variation}/hands.png",
                ducky.colors.wing
            )
        }

        if variation_ == 1:
            template["dress"] = (
                ASSETS_PATH / "templates/variation_1/dress.png",
                dress_colors.shirt
            )
        else:
            template['shirt'] = (
                ASSETS_PATH / "templates/variation_2/shirt.png",
                dress_colors.shirt
            )
            template['pants'] = (
                ASSETS_PATH / "templates/variation_2/pants.png",
                dress_colors.pants
            )

        if ducky.hat:
            template["hat"] = (self.HATS[ducky.hat],)
        if ducky.outfit:
            template["outfit"] = (self.OUTFITS[variation][ducky.outfit],)
        if ducky.equipment:
            template["equipment"] = (self.EQUIPMENTS[variation][ducky.equipment],)
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
                ducky, make_man_duck_colors(ducky.colors.body), random.choice(self.VARIATIONS)
            )

        for item in template.values():
            self.apply_layer(*item)

        return ManDucky(self.output)

    def apply_layer(self, layer_path: str, recolor: Optional[Color] = None) -> None:
        """Add the given layer on top of the ducky. Can be recolored with the recolor argument."""
        try:
            layer = Image.open(layer_path)
        except FileNotFoundError:
            raise HTTPException(
                400,
                f"Invalid option provided: {os.path.basename(layer_path)} not found."
            )

        if recolor:
            if isinstance(recolor, dict):
                recolor = tuple(recolor.values())
            layer = ImageChops.multiply(layer, Image.new("RGBA", MAN_DUCKY_SIZE, color=recolor))
        self.output.alpha_composite(layer)
