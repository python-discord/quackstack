from hashlib import sha1
from json import dumps
from os import getenv
from pathlib import Path
from time import time
from typing import Optional, Union

from fastapi import FastAPI, Response, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.datastructures import URL

from api.models import DuckRequest, DuckResponse, DuckyDetails, ManDuckDetails, ManDuckRequest, ManDuckVariations
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


def make_file_path(dh: str, request_url: URL) -> str:
    """Build a file path from dict_hash and a URL."""
    fqdn = str(request_url).removesuffix(request_url.path)
    return f"{fqdn}/static/{dh}.png"


@app.get("/duck", response_model=DuckResponse, status_code=201)
async def get_duck(request: Request, response: Response, seed: Optional[int] = None) -> DuckResponse:
    """Create a new random duck, with an optional seed."""
    dh = sha1(str(time()).encode()).hexdigest()
    file = CACHE / f"{dh}.png"

    DuckBuilder(seed).generate().image.save(file)

    file_path = make_file_path(dh, request.url)
    response.headers["Location"] = file_path
    return DuckResponse(file=file_path)


@app.post("/duck", response_model=DuckResponse, status_code=201)
async def post_duck(request: Request, response: Response, duck: DuckRequest = None) -> DuckResponse:
    """Create a new duck with a given set of options."""
    dh = dicthash(duck.dict())
    file = CACHE / f"{dh}.png"

    if not file.exists():
        try:
            DuckBuilder().generate(options=duck.dict()).image.save(file)
        except ValueError as e:
            raise HTTPException(400, e.args[0])
        except KeyError as e:
            raise HTTPException(400, f"Invalid configuration option provided: '{e.args[0]}'")

    file_path = make_file_path(dh, request.url)
    response.headers["Location"] = file_path
    return DuckResponse(file=file_path)


@app.get("/manduck", response_model=DuckResponse, status_code=201)
async def get_man_duck(request: Request, response: Response, seed: Optional[int] = None) -> DuckResponse:
    """Create a new man_duck, with an optional seed."""
    dh = sha1(str(time()).encode()).hexdigest()

    ducky = DuckBuilder(seed).generate()
    ducky = ManDuckBuilder(seed).generate(ducky=ducky)
    ducky.image.save(CACHE / f"{dh}.png")

    file_path = make_file_path(dh, request.url)
    response.headers["Location"] = file_path
    return DuckResponse(file=file_path)


@app.post("/manduck", response_model=DuckResponse, status_code=201)
async def post_man_duck(request: Request, response: Response, manduck: ManDuckRequest) -> DuckResponse:
    """Create a new man_duck with a given set of options."""
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

    file_path = make_file_path(dh, request.url)
    response.headers["Location"] = file_path
    return DuckResponse(file=file_path)


@app.get("/details/{type}", response_model=Union[ManDuckDetails, DuckyDetails])
async def get_details(type: str) -> Union[ManDuckDetails, DuckyDetails]:
    """Get details about accessories which can be used to build ducks/man-ducks."""
    details = {
        "ducky": DuckyDetails(
            hats=list(DuckBuilder.hats),
            outfits=list(DuckBuilder.outfits),
            equipments=list(DuckBuilder.equipments),
        ),
        "manduck": ManDuckDetails(
            hats=list(ManDuckBuilder.HATS),
            outfits=ManDuckVariations(
                variation_1=list(ManDuckBuilder.OUTFITS["variation_1"]),
                variation_2=list(ManDuckBuilder.OUTFITS["variation_2"]),
            ),
            equipments=ManDuckVariations(
                variation_1=list(ManDuckBuilder.EQUIPMENTS["variation_1"]),
                variation_2=list(ManDuckBuilder.EQUIPMENTS["variation_2"]),
            ),
            variations=list(ManDuckBuilder.VARIATIONS),
        )
    }

    return details.get(type, Response("Requested type is not available", 400))
