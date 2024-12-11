import fastapi_pagination
from fastapi import FastAPI

from app import settings
from app.routers import entitlements

tags_metadata = [
    {
        "name": "Entitlements",
        "description": "Operations with entitlements",
    },
]


app = FastAPI(
    title="Optscale Operations API",
    description="API to be used by Operators to manage Optscale",
    openapi_tags=tags_metadata,
    root_path="/v1",
    debug=settings.debug,
)

fastapi_pagination.add_pagination(app)


# TODO: Add healthcheck

app.include_router(entitlements.router, prefix="/entitlements", tags=["Entitlements"])
