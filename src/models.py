from typing import List, Optional

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

    hats: List[str]
    outfits: List[str]
    equipments: List[str]


class ManduckVariations(BaseModel):
    """Details of available manduck variations."""

    variation_1: List[str]
    variation_2: List[str]


class ManduckDetails(BaseModel):
    """Details of available manduck creation assets."""

    hats: List[str]
    outfits: ManduckVariations
    equipments: ManduckVariations
    variations: List[int]
