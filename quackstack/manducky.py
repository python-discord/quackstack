from pathlib import Path
from random import Random
from typing import NamedTuple

from PIL import Image, ImageChops
from frozendict import frozendict

from quackstack import __file__ as qs_file

from .colors import DressColors, DuckyColors, make_man_duck_colors
from .ducky import ProceduralDucky


class ManDucky(NamedTuple):
    """Holds a reference to the ManDucky's source image."""

    image: Image.Image


Color = tuple[int, int, int]

ASSETS_PATH = Path(qs_file).parent / Path("assets", "manduck")
MAN_DUCKY_SIZE = (600, 1194)


class ManDuckBuilder:
    """Temporary class used to generate a ducky human."""

    VARIATIONS = (1, 2)
    HATS = frozendict({
        filename.stem: filename for filename in (ASSETS_PATH / "accessories/hats").iterdir()
    })
    OUTFITS = frozendict({
        "variation_1": {
            filename.stem: filename for filename in (ASSETS_PATH / "accessories/outfits/variation_1").iterdir()
        },
        "variation_2": {
            filename.stem: filename for filename in (ASSETS_PATH / "accessories/outfits/variation_2").iterdir()
        },
    })
    EQUIPMENTS = frozendict({
        "variation_1": {
            filename.stem: filename for filename in (ASSETS_PATH / "accessories/equipment/variation_1").iterdir()
        },
        "variation_2": {
            filename.stem: filename for filename in (ASSETS_PATH / "accessories/equipment/variation_2").iterdir()
        },
    })

    def __init__(self, seed: int | None = None) -> None:
        self.random = Random(seed)
        self.output: Image.Image = Image.new("RGBA", MAN_DUCKY_SIZE, color=(0, 0, 0, 0))

    def generate_template(
        self, ducky: ProceduralDucky, dress_colors: DressColors, variation_: int,
    ) -> dict:
        """Generate a man duck structure from given configuration."""
        variation = f"variation_{variation_}"

        template = {
            "bill": (
                ASSETS_PATH / "templates/bill.png",
                ducky.colors.beak,
            ),
            "head": (
                ASSETS_PATH / "templates/head.png",
                ducky.colors.body,
            ),
            "eye": (
                ASSETS_PATH / "templates/eye.png",
                ducky.colors.eye,
            ),
            "hands": (
                ASSETS_PATH / f"templates/{variation}/hands.png",
                ducky.colors.wing,
            ),
        }

        if variation_ == 1:
            template["dress"] = (
                ASSETS_PATH / "templates/variation_1/dress.png",
                dress_colors.shirt,
            )
        else:
            template["shirt"] = (
                ASSETS_PATH / "templates/variation_2/shirt.png",
                dress_colors.shirt,
            )
            template["pants"] = (
                ASSETS_PATH / "templates/variation_2/pants.png",
                dress_colors.pants,
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

        return self.generate_template(
            ducky=ProceduralDucky(None, colors, **accessories),
            dress_colors=DressColors(**options["dress_colors"]),
            variation_=options["variation"],
        )

    def generate(
        self,
        *,
        options: dict | None = None,
        ducky: ProceduralDucky | None = None,
    ) -> ManDucky:
        """Actually generate the man ducky from the provided request, else generate a random one.."""
        if options:
            template = self.generate_from_options(options)
        else:
            template = self.generate_template(
                ducky, make_man_duck_colors(ducky.colors.body), self.random.choice(self.VARIATIONS),
            )

        for item in template.values():
            self.apply_layer(*item)

        return ManDucky(self.output)

    def apply_layer(self, layer_path: str, recolor: Color | None = None) -> None:
        """Add the given layer on top of the ducky. Can be recolored with the recolor argument."""
        try:
            layer = Image.open(layer_path)
        except FileNotFoundError as e:
            raise ValueError(f"Invalid option provided: {Path.name(layer_path)} not found.") from e

        if recolor:
            if isinstance(recolor, dict):
                recolor = tuple(recolor.values())
            layer = ImageChops.multiply(layer, Image.new("RGBA", MAN_DUCKY_SIZE, color=recolor))
        self.output.alpha_composite(layer)
