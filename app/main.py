"""FastAPI application entry point for the in-memory notes service."""

from fastapi import FastAPI

from app.config import settings
from app.routers import notes_create, notes_delete, notes_read

app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe, echoing the configured application name."""
    return {"status": "ok", "app_name": settings.app_name}


app.include_router(notes_create.router)
app.include_router(notes_read.router)
app.include_router(notes_delete.router)
