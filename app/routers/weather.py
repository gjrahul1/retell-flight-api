from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from app.services.weather import weather_service

router = APIRouter(prefix="/api/weather", tags=["weather"])

@router.get("/current")
async def get_weather(q: str = Query(..., description="City name or location query")):
    """Get current weather for a location"""
    
    try:
        result = await weather_service.get_current_weather(q)
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in weather endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Sorry, something went wrong with your weather request. Please try again.",
                "details": str(e)
            }
        )