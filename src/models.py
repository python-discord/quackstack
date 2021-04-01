from pydantic import BaseModel
from typing import Optional


class PartOption(BaseModel):
    r: int
    g: int
    b: int


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
