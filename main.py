from fastapi import FastAPI
from typing import Optional
from hashlib import sha1
from pathlib import Path
from json import dumps
from time import time
from os import getenv

from fastapi.staticfiles import StaticFiles

from src.models import DuckRequest
from src.generator import DuckBuilder


CACHE = Path(getenv("LOCATION", "./static"))

CACHE.mkdir(exist_ok=True)

app = FastAPI(docs_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

def dicthash(data: dict):
    return sha1(dumps(data).encode()).hexdigest()

@app.get("/duck")
async def get_duck(duck: Optional[DuckRequest] = None):
    """Create a new duck."""

    if duck:
        dh = dicthash(duck.dict())
        file = CACHE / f"{dh}.png"

        if not file.exists():
            DuckBuilder.generate(duck).save(file)
    else:
        dh = sha1(str(time).encode()).hexdigest()
        file = CACHE / f"{dh}.png"

        DuckBuilder.generate().save(file)

    return {"file": f"/static/{dh}.png"}

@app.get("/details")
async def get_details():
    """Get details about accessories which can be used to build ducks."""

    return {
        "hats": list(DuckBuilder.hats.keys()),
        "outfits": list(DuckBuilder.outfits.keys()),
        "equipments": list(DuckBuilder.equipments.keys()),
    }
