from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import flights
from app.config import settings
import uvicorn
import socket

# Initialize FastAPI app
app = FastAPI(
    title="Retell AI - Amadeus Flight API",
    description="Flight search integration for Retell AI voice agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(flights.router)

@app.get("/")
async def root():
    return {"message": "Retell AI - Amadeus Flight API is running!", "status": "healthy"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "amadeus_configured": bool(settings.AMADEUS_API_KEY and settings.AMADEUS_API_SECRET),
        "retell_configured": bool(settings.RETELL_API_KEY)
    }

def find_free_port():
    """Find a free port to use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

if __name__ == "__main__":
    # Use configured port or find a free one
    port = settings.PORT if hasattr(settings, 'PORT') and settings.PORT else find_free_port()
    print(f"Starting server on localhost:{port}")
    
    uvicorn.run(
        "main:app", 
        host="127.0.0.1",  # localhost instead of 0.0.0.0
        port=port, 
        reload=settings.DEBUG
    )
