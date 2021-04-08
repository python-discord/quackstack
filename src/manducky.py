import random
from collections import namedtuple
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageChops

from .colors import make_man_duck_colors

ManDucky = namedtuple("ManDucky", "image hat equipment outfit")
ProceduralDucky = namedtuple("ProceduralDucky", "image colors hat equipment outfit")
Color = Tuple[int, int, int]

ASSETS_PATH = Path("duck-builder", "duck-person")
MAN_DUCKY_SIZE = (600, 1194)


class ManDuckGenerator:
    """Temporary class used to generate a ducky human."""

    def __init__(self, ducky: ProceduralDucky) -> None:
        self.output: Image.Image = Image.new("RGBA", MAN_DUCKY_SIZE, color=(0, 0, 0, 0))
        self.colors = ducky.colors

        self.variation = random.choice((1, 2))

        self.templates = {
            "head": Image.open(ASSETS_PATH / "templates/head.png"),
            "eye": Image.open(ASSETS_PATH / "templates/eye.png"),
            "bill": Image.open(ASSETS_PATH / "templates/bill.png"),
            "hands": Image.open(ASSETS_PATH / f"templates/variation_{self.variation}/hands.png"),
        }

        if self.variation == 1:
            self.templates["dress"] = Image.open(ASSETS_PATH / "templates/variation_1/dress.png")
        if self.variation == 2:
            self.templates["shirt"] = Image.open(ASSETS_PATH / "templates/variation_2/shirt.png")
            self.templates["pants"] = Image.open(ASSETS_PATH / "templates/variation_2/pants.png")

        if ducky.hat:
            self.templates["hat"] = Image.open(ASSETS_PATH / f"accessories/hats/{ducky.hat}.png")
        if ducky.outfit:
            self.templates["outfit"] = Image.open(
                ASSETS_PATH / f"outfits/variation_{self.variation}/{ducky.outfit}.png"
            )
        if ducky.equipment:
            self.templates["equipment"] = Image.open(
                ASSETS_PATH / f"equipment/variation_{self.variation}/{ducky.equipment}.png"
            )

        self.hat = ducky.hat
        self.equipment = ducky.equipment
        self.outfit = ducky.outfit

    def generate(self) -> ManDucky:
        """Actually generate the ducky."""
        dress_colors = make_man_duck_colors()

        if self.variation == 2:
            self.apply_layer(self.templates["pants"], dress_colors.pants)

        self.apply_layer(self.templates["bill"], self.colors.beak)
        self.apply_layer(self.templates["head"], self.colors.body)
        self.apply_layer(self.templates["eye"], self.colors.eye)

        if self.variation == 2:
            self.apply_layer(self.templates["shirt"], dress_colors.shirt)

        elif self.variation == 1:
            self.apply_layer(self.templates["dress"], dress_colors.shirt)

        if self.outfit and self.outfit != "bread":
            self.apply_layer(self.templates["outfit"])

        if self.equipment:
            self.apply_layer(self.templates["equipment"])

        self.apply_layer(self.templates["hands"], self.colors.wing)

        if self.outfit and self.outfit == "beard":
            self.apply_layer(self.templates["outfit"])

        if self.hat:
            self.apply_layer(self.templates["hat"])

        return ManDucky(self.output, self.hat, self.equipment, self.outfit)

    def apply_layer(self, layer: Image.Image, recolor: Optional[Color] = None) -> None:
        """Add the given layer on top of the ducky. Can be recolored with the recolor argument."""
        if recolor:
            layer = ImageChops.multiply(layer, Image.new("RGBA", MAN_DUCKY_SIZE, color=recolor))
        self.output.alpha_composite(layer)
