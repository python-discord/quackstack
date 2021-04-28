from hashlib import sha1
from json import dumps
from os import getenv
from pathlib import Path
from time import time
from typing import Any, Dict, Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.ducky import DuckBuilder
from src.manducky import ManDuckGenerator
from src.models import DuckRequest, ManDuckRequest

CACHE = Path(getenv("LOCATION", "./static"))

CACHE.mkdir(exist_ok=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory=CACHE), name="static")


def dicthash(data: dict) -> str:
    """Take a dictionary and convert it to a SHA-1 hash."""
    return sha1(dumps(data).encode()).hexdigest()


@app.get("/duck")
async def get_duck(duck: Optional[DuckRequest] = None) -> Dict[str, Any]:
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

    return {"file": f"/static/{dh}.png"}


@app.get("/manduck")
async def get_man_duck(manduck: Optional[ManDuckRequest] = None) -> Dict[str, Any]:
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

    return {"file": f"/static/{dh}.png"}


@app.get("/details")
async def get_details() -> Dict[str, Any]:
    """Get details about accessories which can be used to build ducks."""
    return {
        "hats": list(DuckBuilder.hats.keys()),
        "outfits": list(DuckBuilder.outfits.keys()),
        "equipments": list(DuckBuilder.equipments.keys()),
    }
