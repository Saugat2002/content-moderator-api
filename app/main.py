from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.routes import router
from app.core.config import get_settings
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("app.log")],
)

# Create logger
logger = logging.getLogger(__name__)
logger.info("Starting Content Moderator API")

settings = get_settings()

app = FastAPI(
    title="Content Moderator API",
    description="AI-powered content moderation service",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root(request: Request):
    logger.info("Serving root endpoint")
    return templates.TemplateResponse(request, "index.html")
