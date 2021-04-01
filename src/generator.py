from fastapi import HTTPException
from pathlib import Path
from typing import Union, Tuple, Optional
from random import choice, randint
from PIL import Image, ImageChops

from .models import DuckRequest


ASSETS_PATH = Path("branding/quackstack")
DUCK_SIZE = (499, 600)


class DuckBuilder:
    """A class used to build new ducks."""

    templates = {
        int(filename.name[0]): Image.open(filename) for filename in (ASSETS_PATH / "silverduck_templates").iterdir()
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
    def validate_rgb(name: str, data: dict) -> bool:
        if not all(0 <= value <= 255 for value in data.values()):
            raise HTTPException(400, f"Invalid RGB values given for {name}")
        return (data["r"], data["g"], data["b"])

    @classmethod
    def make_random(cls):
        def randrgb():
            return {
                "r": randint(0, 255),
                "g": randint(0, 255),
                "b": randint(0, 255),
            }

        return {
            "body": randrgb(),
            "wing": randrgb(),
            "eye": randrgb(),
            "beak": randrgb(),
            "eye_wing": randrgb(),
            "accessories": {
                "hat": choice([*list(cls.hats), None]),
                "outfit": choice([*list(cls.outfits), None]),
                "equipment": choice([*list(cls.equipments), None]),
            }
        }

    def generate(cls, options: Union[DuckRequest, None] = None):
        options = options.dict() if options else cls.make_random()

        output: Image.Image = Image.new("RGBA", DUCK_SIZE, color=(0, 0, 0, 0))

        body = cls.validate_rgb("body", options["body"])
        wing = cls.validate_rgb("wing", options["wing"])
        eye = cls.validate_rgb("eye", options["eye"])
        beak = cls.validate_rgb("beak", options["beak"])
        eye_wing = cls.validate_rgb("eye_wing", options["eye_wing"])

        accessories = options["accessories"]
        equipment = accessories["equipment"]
        outfit = accessories["outfit"]
        hat = accessories["hat"]

        if equipment and not equipment in cls.equipments:
            raise HTTPException(400, "Invalid equipment provided.")

        if outfit and not outfit in cls.outfits:
            raise HTTPException(400, "Invalid outfit provided.")

        if hat and not hat in cls.hats:
            raise HTTPException(400, "Invalid hat provided.")

        def apply_layer(layer: Image.Image, recolor: Optional[Tuple[int, int, int]] = None):
            if recolor:
                layer = ImageChops.multiply(layer, Image.new("RGBA", DUCK_SIZE, color=recolor))
            output.alpha_composite(layer)

        apply_layer(cls.templates[5], beak)
        apply_layer(cls.templates[4], body)

        if equipment:
            equipment_type = cls.equipments[equipment]
            apply_layer(equipment_type)

        apply_layer(cls.templates[3], wing)
        apply_layer(cls.templates[2], eye_wing)
        apply_layer(cls.templates[1], eye)

        if outfit:
            outfit_type = cls.outfits[outfit]
            apply_layer(outfit_type)

        if hat:
            hat_type = cls.hats[hat]
            apply_layer(hat_type)

        return output
