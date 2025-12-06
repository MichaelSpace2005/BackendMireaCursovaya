from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.interfaces.api.v1.routes import router as v1_router
from app.infra.database.session import init_models, dispose_models
from app.infra.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Evolution Tree Backend",
        version="1.0.0",
        description="Interactive evolution tree of game mechanics"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(v1_router)
    
    # Mount static files
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.on_event("startup")
    async def startup():
        """Initialize database on startup"""
        await init_models()
    
    @app.on_event("shutdown")
    async def shutdown():
        """Dispose engine on shutdown"""
        await dispose_models()
    
    @app.get("/")
    async def root():
        return {
            "message": "Evolution Tree API",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)