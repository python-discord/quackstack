from pydantic import BaseModel
from typing import Optional


class PartOption(BaseModel):
    colour: Optional[int]
    lightness: Optional[float]
    dark: Optional[bool]
    hue: Optional[float]


class Accessories(BaseModel):
    hat: Optional[str]
    outfit: Optional[str]
    equipment: Optional[str]


class DuckRequest(BaseModel):
    body: Optional[PartOption]
    wing: Optional[PartOption]
    eye: Optional[PartOption]
    beak: Optional[PartOption]
    accessories: Optional[Accessories]