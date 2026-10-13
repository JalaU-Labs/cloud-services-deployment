"""FastAPI application for the lab_cloud package."""

from fastapi import FastAPI

from lab_cloud import __version__
from lab_cloud.routes.contacts import router as contacts_router

app = FastAPI(
    title="Lab Cloud API",
    version=__version__,
    description="Cloud Services Deployment Lab - Week 7",
)

app.include_router(contacts_router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return the application status and version."""
    return {"status": "ok", "version": __version__}
