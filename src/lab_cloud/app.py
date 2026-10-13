"""FastAPI application for the lab_cloud package."""

from fastapi import FastAPI

from lab_cloud import __version__

app = FastAPI(
    title="Lab Cloud API",
    version=__version__,
    description="Cloud Services Deployment Lab - Week 7",
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return the application status and version."""
    return {"status": "ok", "version": __version__}