from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import flights, weather, itinerary, exchange, time, retell
from app.config import settings
import uvicorn
import socket
import logging
import json
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Custom middleware to log requests
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request details
        logger.info(f"=== INCOMING REQUEST ===")
        logger.info(f"Method: {request.method}")
        logger.info(f"URL: {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        # Log request body for POST requests
        if request.method == "POST":
            body = await request.body()
            if body:
                try:
                    body_json = json.loads(body.decode())
                    logger.info(f"Request Body: {json.dumps(body_json, indent=2)}")
                except:
                    logger.info(f"Request Body (raw): {body.decode()}")
            else:
                logger.info("Request Body: Empty")
        
        # Process the request
        response = await call_next(request)
        
        # Log response status
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"=== END REQUEST ===\n")
        
        return response

# Initialize FastAPI app
app = FastAPI(
    title="Retell AI - Amadeus Flight API",
    description="Flight search integration for Retell AI voice agents",
    version="1.0.0"
)

# Add request logging middleware (add this FIRST)
app.add_middleware(RequestLoggingMiddleware)

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
app.include_router(weather.router)
app.include_router(itinerary.router)
app.include_router(exchange.router)
app.include_router(time.router)
app.include_router(retell.router)

@app.get("/")
async def root():
    return {"message": "Retell AI - Amadeus Flight API is running!", "status": "healthy"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "amadeus_configured": bool(settings.AMADEUS_API_KEY and settings.AMADEUS_API_SECRET),
        "retell_configured": bool(settings.RETELL_API_KEY),
        "openweather_configured": bool(settings.OPENWEATHER_API_KEY),
        "opentripmap_configured": bool(settings.OPENTRIPMAP_API_KEY),
        "exchangerate_configured": bool(settings.EXCHANGERATE_API_KEY),
        "timeapi_configured": True
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
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG
    )
