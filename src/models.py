from pydantic import BaseModel
from typing import Optional


class PartOption(BaseModel):
    r: int
    g: int
    b: int


class Accessories(BaseModel):
    hat: Optional[str]
    outfit: Optional[str]
    equipment: Optional[str]


class DuckRequest(BaseModel):
    body: PartOption
    wing: PartOption
    eye: PartOption
    beak: PartOption
    eye_wing: PartOption
    accessories: Accessories
