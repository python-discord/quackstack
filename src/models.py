from pydantic import BaseModel
from typing import Optional


class PartOption(BaseModel):
    colour: int
    lightness: float
    dark: bool
    hue: float


class Accessories(BaseModel):
    hat: str
    outfit: str
    equipment: str


class DuckRequest(BaseModel):
    body: PartOption
    wing: PartOption
    eye: PartOption
    beak: PartOption
    accessories: Accessories
