import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.middleware.proxy import proxy_client
from app.routes.youtube import root_router, router as youtube_router
from app.utils.youtube_tools import YouTubeTools

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s on %s:%s", settings.PROJECT_NAME, settings.HOST, settings.PORT)
    logger.info("Proxy status: %s", YouTubeTools.get_runtime_status())
    yield
    await proxy_client.close()
    logger.info("Shut down %s", settings.PROJECT_NAME)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for extracting and processing YouTube video data",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(youtube_router)
app.include_router(root_router)

@app.get("/", tags=["root"])
async def root():
    """Root endpoint that provides API information"""
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        **YouTubeTools.get_runtime_status(),
    }

def start():
    """Function to start the server"""
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)

if __name__ == "__main__":
    start()
