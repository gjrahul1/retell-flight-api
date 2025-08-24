from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models import ItineraryRequest
from app.services.itinerary import itinerary_service

router = APIRouter(prefix="/api/itinerary", tags=["itinerary"])

@router.post("/places")
async def get_itineraries(itinerary_request: ItineraryRequest):
    """Get itineraries for a given place"""
    
    try:
        result = await itinerary_service.get_itineraries(itinerary_request.name)
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in itinerary endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Sorry, something went wrong with your itinerary request. Please try again.",
                "details": str(e)
            }
        )