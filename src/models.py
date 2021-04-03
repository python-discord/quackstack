from typing import Optional

from pydantic import BaseModel


class PartOption(BaseModel):
    """Valid options for a ducky component."""

    r: int
    g: int
    b: int


class Accessories(BaseModel):
    """Valid accessories for a duck."""

    hat: Optional[str]
    outfit: Optional[str]
    equipment: Optional[str]


class DuckRequest(BaseModel):
    """A request for a ducky generation."""

    body: PartOption
    wing: PartOption
    eye: PartOption
    beak: PartOption
    eye_wing: PartOption
    accessories: Accessories
