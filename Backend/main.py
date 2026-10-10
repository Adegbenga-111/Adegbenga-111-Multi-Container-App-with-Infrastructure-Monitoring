from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database.connection import (
    check_database_connection,
    close_database_connection,
)
from routes.task import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_database_connection()


app = FastAPI(
    title="Kubernetes Task Manager API",
    description="Task management API built with FastAPI and MongoDB",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the local React development server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

# Register API routes.
app.include_router(task_router)


@app.get("/")
def root():
    return {
        "message": "Kubernetes Task Manager API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    if not check_database_connection():
        raise HTTPException(
            status_code=503,
            detail="MongoDB is unavailable",
        )

    return {
        "status": "healthy",
        "database": "connected",
    }


@app.get("/health/live")
def liveness_check():
    return {"status": "alive"}
