from hashlib import sha1
from json import dumps
from os import getenv
from pathlib import Path
from time import time
from typing import Optional, Union

from api.models import DuckRequest, DuckResponse, DuckyDetails, ManDuckRequest, ManduckDetails, ManduckVariations
from fastapi import FastAPI, Response
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from quackstack import DuckBuilder, ManDuckBuilder


CACHE = Path(getenv("LOCATION", "./static"))

CACHE.mkdir(exist_ok=True)

app = FastAPI(docs_url="/swagger_docs", redoc_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=CACHE), name="static")


def dicthash(data: dict) -> str:
    """Take a dictionary and convert it to a SHA-1 hash."""
    return sha1(dumps(data).encode()).hexdigest()


@app.get("/duck", response_model=DuckResponse)
async def get_duck(duck: Optional[DuckRequest] = None, seed: Optional[int] = None) -> DuckResponse:
    """Create a new duck."""
    if duck:
        dh = dicthash(duck.dict())
        file = CACHE / f"{dh}.png"

        if not file.exists():
            try:
                DuckBuilder().generate(options=duck.dict()).image.save(file)
            except ValueError as e:
                raise HTTPException(400, e.args[0])
            except KeyError as e:
                raise HTTPException(400, f"Invalid configuration option provided: '{e.args[0]}'")
    else:
        dh = sha1(str(time()).encode()).hexdigest()
        file = CACHE / f"{dh}.png"

        DuckBuilder(seed).generate().image.save(file)

    return DuckResponse(file=f"/static/{dh}.png")


@app.get("/manduck", response_model=DuckResponse)
async def get_man_duck(manduck: Optional[ManDuckRequest] = None, seed: Optional[int] = None) -> DuckResponse:
    """Create a new man_duck."""
    if manduck:
        dh = dicthash(manduck.dict())
        file = CACHE / f"{dh}.png"

        if not file.exists():
            try:
                ducky = ManDuckBuilder().generate(options=manduck.dict())
            except ValueError as e:
                raise HTTPException(400, e.args[0])
            except KeyError as e:
                raise HTTPException(400, f"Invalid configuration option provided: '{e.args[0]}'")
            ducky.image.save(CACHE / f"{dh}.png")

    else:
        dh = sha1(str(time()).encode()).hexdigest()

        ducky = DuckBuilder(seed).generate()
        ducky = ManDuckBuilder(seed).generate(ducky=ducky)
        ducky.image.save(CACHE / f"{dh}.png")

    return DuckResponse(file=f"/static/{dh}.png")


@app.get("/details/{type}", response_model=Union[ManduckDetails, DuckyDetails])
async def get_details(type: str) -> Union[ManduckDetails, DuckyDetails]:
    """Get details about accessories which can be used to build ducks/man-ducks."""
    details = {
        "ducky": DuckyDetails(
            hats=list(DuckBuilder.hats),
            outfits=list(DuckBuilder.outfits),
            equipments=list(DuckBuilder.equipments),
        ),
        "manduck": ManduckDetails(
            hats=list(ManDuckBuilder.HATS),
            outfits=ManduckVariations(
                variation_1=list(ManDuckBuilder.OUTFITS["variation_1"]),
                variation_2=list(ManDuckBuilder.OUTFITS["variation_2"]),
            ),
            equipments=ManduckVariations(
                variation_1=list(ManDuckBuilder.EQUIPMENTS["variation_1"]),
                variation_2=list(ManDuckBuilder.EQUIPMENTS["variation_2"]),
            ),
            variations=list(ManDuckBuilder.VARIATIONS),
        )
    }

    return details.get(type, Response("Requested type is not available", 400))
