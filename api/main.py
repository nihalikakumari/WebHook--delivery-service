from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.core.config import settings
from app.routers import webhooks, auth, users, items, subscriptions
from app.db.base import Base
from app.db.session import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A robust webhook delivery service with reliable delivery, retries, and comprehensive logging.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Render deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhooks.router, prefix=settings.API_PREFIX, tags=["webhooks"])
app.include_router(auth.router, prefix=settings.API_PREFIX, tags=["auth"])
app.include_router(users.router, prefix=settings.API_PREFIX, tags=["users"])
app.include_router(items.router, prefix=settings.API_PREFIX, tags=["items"])
app.include_router(subscriptions.router, prefix=settings.API_PREFIX, tags=["subscriptions"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)