from typing import Optional

from pydantic import BaseModel


class PartOption(BaseModel):
    """Valid options for a ducky component."""

    r: int
    g: int
    b: int


class Colors(BaseModel):
    """Valid options for a ducky colors."""

    body: PartOption
    wing: PartOption
    eye: PartOption
    beak: PartOption
    eye_wing: PartOption


class DressColors(BaseModel):
    """Valid options for a man ducky dress colors."""

    shirt: PartOption
    pants: Optional[PartOption]


class Accessories(BaseModel):
    """Valid accessories for a duck."""

    hat: Optional[str]
    outfit: Optional[str]
    equipment: Optional[str]


class DuckRequest(BaseModel):
    """A request for a ducky generation."""

    colors: Colors
    accessories: Accessories


class ManDuckRequest(BaseModel):
    """A request for a man ducky generation."""

    variation: int
    colors: Colors
    dress_colors: DressColors
    accessories: Accessories


class DuckResponse(BaseModel):
    """The generated ducky file location."""

    file: str


class DuckyDetails(BaseModel):
    """Details of available ducky creation assets."""

    hats: list[str]
    outfits: list[str]
    equipments: list[str]


class ManDuckVariations(BaseModel):
    """Details of available manduck variations."""

    variation_1: list[str]
    variation_2: list[str]


class ManDuckDetails(BaseModel):
    """Details of available manduck creation assets."""

    hats: list[str]
    outfits: ManDuckVariations
    equipments: ManDuckVariations
    variations: list[int]
