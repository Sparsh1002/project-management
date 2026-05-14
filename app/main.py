
from unittest.mock import Base

from fastapi import FastAPI
from sqlalchemy import engine
from app.api.routes import (
    auth,
    issue,
    projects,
    sprints,
    comments,
    search,
    watchers,
    notifications
)
from app.websocket.manager import websocket_router
from app.middleware.auth_middleware import (
    auth_middleware
)
from seed import seed_data

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Management Platform",
    version="1.0.0"
)

app.middleware("http")(auth_middleware)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(issue.router)
app.include_router(sprints.router)
app.include_router(comments.router)
app.include_router(search.router)
app.include_router(watchers.router)
app.include_router(notifications.router)
app.include_router(websocket_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():

    seed_data()
