from collections import namedtuple
from pathlib import Path
from random import choice
from typing import Optional, Tuple

from PIL import Image, ImageChops
from fastapi import HTTPException

from .colors import make_duck_colors
from .models import DuckRequest

ASSETS_PATH = Path("duck-builder", "ducky")
DUCK_SIZE = (499, 600)

ProceduralDucky = namedtuple("ProceduralDucky", "image colors hat equipment outfit")
DuckyColors = namedtuple("DuckyColors", "eye eye_wing wing body beak")


class DuckBuilder:
    """A class used to build new ducks."""

    templates = {
        int(filename.name[0]): Image.open(filename) for filename in (ASSETS_PATH / "templates").iterdir()
    }
    hats = {
        filename.stem: Image.open(filename) for filename in (ASSETS_PATH / "accessories/hats").iterdir()
    }
    equipments = {
        filename.stem: Image.open(filename) for filename in (ASSETS_PATH / "accessories/equipment").iterdir()
    }
    outfits = {
        filename.stem: Image.open(filename) for filename in (ASSETS_PATH / "accessories/outfits").iterdir()
    }

    @classmethod
    def make_random(cls):
        """Generate a random RGB duck structure."""
        colors = make_duck_colors()
        return {
            "colors": {
                "body": colors.body,
                "wing": colors.wing,
                "eye": colors.eye,
                "beak": colors.beak,
                "eye_wing": colors.eye_wing
            },
            "accessories": {
                "hat": choice([*list(cls.hats), None]),
                "outfit": choice([*list(cls.outfits), None]),
                "equipment": choice([*list(cls.equipments), None]),
            }
        }

    @classmethod
    def generate(cls, options: Optional[DuckRequest] = None):
        """Generate a duck from the provided request, else generate a random one."""
        options = options.dict() if options else cls.make_random()

        # Create `colors` namedtuple
        colors = DuckyColors(**options["colors"])

        output: Image.Image = Image.new("RGBA", DUCK_SIZE, color=(0, 0, 0, 0))

        accessories = options["accessories"]
        equipment = accessories["equipment"]
        outfit = accessories["outfit"]
        hat = accessories["hat"]

        if equipment and equipment not in cls.equipments:
            raise HTTPException(400, "Invalid equipment provided.")

        if outfit and outfit not in cls.outfits:
            raise HTTPException(400, "Invalid outfit provided.")

        if hat and hat not in cls.hats:
            raise HTTPException(400, "Invalid hat provided.")

        # TODO: move this function outside of this method body.
        def apply_layer(layer: Image.Image, recolor: Optional[Tuple[int, int, int]] = None) -> None:
            if recolor:
                layer = ImageChops.multiply(layer, Image.new("RGBA", DUCK_SIZE, color=recolor))
            output.alpha_composite(layer)

        apply_layer(cls.templates[5], colors.beak)
        apply_layer(cls.templates[4], colors.body)
        apply_layer(cls.templates[1], colors.eye)

        if outfit:
            apply_layer(cls.outfits[outfit])

        if equipment:
            apply_layer(cls.equipments[equipment])

        apply_layer(cls.templates[3], colors.wing)
        apply_layer(cls.templates[2], colors.eye_wing)

        if hat:
            apply_layer(cls.hats[hat])

        return ProceduralDucky(
            output,
            colors,
            hat,
            equipment,
            outfit
        )
