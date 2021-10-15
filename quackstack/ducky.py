import os
from collections import namedtuple
from pathlib import Path
from random import Random
from typing import Optional, Tuple

from PIL import Image, ImageChops

from quackstack import __file__ as qs_file

from .colors import DuckyColors, make_duck_colors

ASSETS_PATH = Path(qs_file).parent / Path("assets", "ducky")
DUCK_SIZE = (499, 600)

ProceduralDucky = namedtuple("ProceduralDucky", "image colors hat equipment outfit")


class DuckBuilder:
    """A class used to build new ducks."""

    templates = {
        int(filename.name[0]): filename for filename in (ASSETS_PATH / "templates").iterdir()
    }
    hats = {
        filename.stem: filename for filename in (ASSETS_PATH / "accessories/hats").iterdir()
    }
    equipments = {
        filename.stem: filename for filename in (ASSETS_PATH / "accessories/equipment").iterdir()
    }
    outfits = {
        filename.stem: filename for filename in (ASSETS_PATH / "accessories/outfits").iterdir()
    }

    def __init__(self, seed: Optional[int] = None):
        self.random = Random(seed)
        self.output: Image.Image = Image.new("RGBA", DUCK_SIZE, color=(0, 0, 0, 0))

    def generate_template(
            self, colors: DuckyColors, hat: str, outfit: str, equipment: str
    ) -> Tuple[dict, DuckyColors, str, str, str]:
        """Generate a duck structure from given configuration."""
        template = {
            "beak": (self.templates[5], colors.beak),
            "body": (self.templates[4], colors.body),
            "wing": (self.templates[3], colors.wing),
            "eye": (self.templates[1], colors.eye),
            "eye_wing": (self.templates[2], colors.eye_wing),
        }

        if hat:
            template["hat"] = (self.hats[hat],)
        if outfit:
            template["outfit"] = (self.outfits[outfit],)
        if equipment:
            template["equipment"] = (self.equipments[equipment],)

        return template, colors, hat, outfit, equipment

    def generate_from_options(self, options: dict) -> Tuple[dict, DuckyColors, str, str, str]:
        """Generate a duck from the provided request."""
        return self.generate_template(
            colors=DuckyColors(**options["colors"]),
            **options["accessories"]
        )

    def generate(self, *, options: Optional[dict] = None) -> ProceduralDucky:
        """Actually generate the ducky from the provided request, else generate a random one."""
        if options:
            template, colors, hat, outfit, equipment = self.generate_from_options(options)
        else:
            template, colors, hat, outfit, equipment = self.generate_template(
                make_duck_colors(self.random),
                self.random.choice([*list(self.hats), None]),
                self.random.choice([*list(self.outfits), None]),
                self.random.choice([*list(self.equipments), None])
            )

        for key in ["beak", "body", "eye", "equipment", "wing", "eye_wing", "hat", "outfit"]:
            if item := template.get(key):
                self.apply_layer(*item)

        return ProceduralDucky(self.output, colors, hat, equipment, outfit)

    def apply_layer(self, layer_path: str, recolor: Optional[Tuple[int, int, int]] = None) -> None:
        """Add the given layer on top of the ducky. Can be recolored with the recolor argument."""
        try:
            layer = Image.open(layer_path)
        except FileNotFoundError:
            raise ValueError(f"Invalid option provided: {os.path.basename(layer_path)} not found.")

        if recolor:
            if isinstance(recolor, dict):
                recolor = tuple(recolor.values())
            layer = ImageChops.multiply(layer, Image.new("RGBA", DUCK_SIZE, color=recolor))
        self.output.alpha_composite(layer)
