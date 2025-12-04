import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.interfaces.api.v1.routes import router as v1_router
from app.infra.database.session import init_models, get_engine

def create_app() -> FastAPI:
    app = FastAPI(title="Evolution Tree Backend", version="1.0.0")
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(v1_router, prefix="/api/v1")
    
    # Mount static files
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
    except Exception:
        pass
    
    return app

app = create_app()

@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    engine = get_engine()
    await init_models(engine)

@app.on_event("shutdown")
async def shutdown():
    """Dispose engine on shutdown"""
    engine = get_engine()
    await engine.dispose()

@app.get("/")
async def root():
    return {"message": "Evolution Tree API", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)