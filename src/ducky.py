from collections import namedtuple
from pathlib import Path
from random import choice, randint
from typing import Dict, Optional, Tuple

from PIL import Image, ImageChops
from fastapi import HTTPException

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

    @staticmethod
    def validate_rgb(name: str, data: dict) -> Tuple[int, int, int]:
        """Validate that the provided data dictionary has compliant RGB values (0-255)."""
        if not all(0 <= value <= 255 for value in data.values()):
            raise HTTPException(400, f"Invalid RGB values given for {name}")
        return data["r"], data["g"], data["b"]

    @staticmethod
    def random_rgb() -> Dict[str, int]:
        """Generate a random RGB colour."""
        # TODO: refactor this to use colorsys for nicer colours.

        return {
            "r": randint(0, 255),
            "g": randint(0, 255),
            "b": randint(0, 255),
        }

    @classmethod
    def make_random(cls):
        """Generate a random RGB duck structure."""
        return {
            "body": cls.random_rgb(),
            "wing": cls.random_rgb(),
            "eye": cls.random_rgb(),
            "beak": cls.random_rgb(),
            "eye_wing": cls.random_rgb(),
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

        output: Image.Image = Image.new("RGBA", DUCK_SIZE, color=(0, 0, 0, 0))

        body = cls.validate_rgb("body", options["body"])
        wing = cls.validate_rgb("wing", options["wing"])
        eye = cls.validate_rgb("eye", options["eye"])
        beak = cls.validate_rgb("beak", options["beak"])
        eye_wing = cls.validate_rgb("eye_wing", options["eye_wing"])
        colors = DuckyColors(eye, eye_wing, wing, body, beak)

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
