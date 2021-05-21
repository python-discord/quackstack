from hashlib import sha1
from json import dumps
from os import getenv
from pathlib import Path
from time import time
from typing import Optional, Union

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

from src.ducky import DuckBuilder
from src.manducky import ManDuckGenerator
from src.models import DuckRequest, ManDuckRequest, DuckResponse, DuckyDetails, ManduckDetails, ManduckVariations

CACHE = Path(getenv("LOCATION", "./static"))

CACHE.mkdir(exist_ok=True)

app = FastAPI(docs_url="/swagger_docs", redoc_url="/docs")

app.mount("/static", StaticFiles(directory=CACHE), name="static")


def dicthash(data: dict) -> str:
    """Take a dictionary and convert it to a SHA-1 hash."""
    return sha1(dumps(data).encode()).hexdigest()


@app.get("/duck", response_model=DuckResponse)
async def get_duck(duck: Optional[DuckRequest] = None) -> DuckResponse:
    """Create a new duck."""
    if duck:
        dh = dicthash(duck.dict())
        file = CACHE / f"{dh}.png"

        if not file.exists():
            DuckBuilder().generate(options=duck).image.save(file)
    else:
        dh = sha1(str(time()).encode()).hexdigest()
        file = CACHE / f"{dh}.png"

        DuckBuilder().generate().image.save(file)

    return DuckResponse(file=f"/static/{dh}.png")


@app.get("/manduck", response_model=DuckResponse)
async def get_man_duck(manduck: Optional[ManDuckRequest] = None) -> DuckResponse:
    """Create a new man_duck."""
    if manduck:
        dh = dicthash(manduck.dict())
        file = CACHE / f"{dh}.png"

        if not file.exists():
            ducky = ManDuckGenerator().generate(options=manduck)
            ducky.image.save(CACHE / f"{dh}.png")

    else:
        dh = sha1(str(time()).encode()).hexdigest()

        ducky = DuckBuilder().generate()
        ducky = ManDuckGenerator().generate(ducky=ducky)
        ducky.image.save(CACHE / f"{dh}.png")

    return DuckResponse(file=f"/static/{dh}.png")


@app.get("/details/{type}", response_model=Union[ManduckDetails, DuckyDetails])
async def get_details(type: str = None) -> Union[ManduckDetails, DuckyDetails]:
    """Get details about accessories which can be used to build ducks/man-ducks."""

    details = {
        "ducky": DuckyDetails(
            hats=list(DuckBuilder.hats),
            outfits=list(DuckBuilder.outfits),
            equipments=list(DuckBuilder.equipments),
        ),
        "manduck": ManduckDetails(
            hats=list(ManDuckGenerator.HATS),
            outfits=ManduckVariations(
                variation_1=list(ManDuckGenerator.OUTFITS["variation_1"]),
                variation_2=list(ManDuckGenerator.OUTFITS["variation_2"]),
            ),
            equipments=ManduckVariations(
                variation_1=list(ManDuckGenerator.EQUIPMENTS["variation_1"]),
                variation_2=list(ManDuckGenerator.EQUIPMENTS["variation_2"]),
            ),
            variations=list(ManDuckGenerator.VARIATIONS),
        )
    }

    return details.get(type, Response("Requested type is not available", 400))
