"""Entry point for the lab_cloud package."""

import uvicorn


def main() -> None:  # pragma: no cover
    """Run the FastAPI application with uvicorn."""
    uvicorn.run(
        "lab_cloud.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":  # pragma: no cover
    main()
