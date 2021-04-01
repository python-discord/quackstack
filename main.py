from fastapi import FastAPI
from typing import Optional

from src.models import DuckRequest


app = FastAPI(docs_url=None)

@app.get("/duck")
async def get_duck(duck: Optional[DuckRequest]):
    """Create a new duck."""
    pass  # TODO: Implement this endpoint.

@app.get("/details")
async def get_details():
    """Get details about accessories which can be used to build ducks."""
    pass  # TODO: Implement this endpoint.
