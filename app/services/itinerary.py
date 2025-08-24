import httpx
from fastapi import HTTPException
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class ItineraryService:
    def __init__(self):
        self.base_url = "https://api.opentripmap.com/0.1/en/places/geoname"
        
    async def get_itineraries(self, name: str) -> dict:
        """Get itineraries for a given place from OpenTripMap API"""
        
        if not settings.OPENTRIPMAP_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenTripMap API key not configured"
            )
        
        params = {
            "name": name,
            "apikey": settings.OPENTRIPMAP_API_KEY
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.get(self.base_url, params=params)
                
                if response.status_code == 404:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Place '{name}' not found"
                    )
                
                if response.status_code != 200:
                    logger.error(f"OpenTripMap API error: {response.status_code}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Itinerary service unavailable"
                    )
                
                data = response.json()
                return self._format_itinerary_response(data, name)
                    
        except httpx.TimeoutException:
            logger.error("Timeout when calling OpenTripMap API")
            raise HTTPException(
                status_code=408,
                detail="Itinerary service timeout"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error when calling OpenTripMap API: {e}")
            raise HTTPException(
                status_code=503,
                detail="Itinerary service unavailable"
            )
    
    def _format_itinerary_response(self, data: dict, original_name: str) -> dict:
        """Format the OpenTripMap API response"""
        try:
            return {
                "query": {
                    "original_name": original_name,
                    "status": "success"
                },
                "place_info": {
                    "name": data.get("name"),
                    "country": data.get("country"),
                    "timezone": data.get("timezone"),
                    "population": data.get("population"),
                    "location": {
                        "lat": data.get("lat"),
                        "lon": data.get("lon")
                    }
                },
                "raw_data": data
            }
        except Exception as e:
            logger.error(f"Error formatting itinerary response: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error processing itinerary data"
            )

itinerary_service = ItineraryService()