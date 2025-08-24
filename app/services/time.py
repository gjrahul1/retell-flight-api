import httpx
from fastapi import HTTPException
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class TimeService:
    def __init__(self):
        self.base_url = "https://timeapi.io/api/Time/current/zone"
        
    async def get_current_time(self, timezone: str) -> dict:
        """Get current time for a timezone using TimeAPI"""
        
        # Build URL with timezone parameter
        url = f"{self.base_url}?timeZone={timezone}"
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.get(url)
                
                if response.status_code == 404:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Timezone '{timezone}' not found"
                    )
                
                if response.status_code == 400:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid timezone format: '{timezone}'"
                    )
                
                if response.status_code != 200:
                    logger.error(f"TimeAPI error: {response.status_code}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Time service unavailable"
                    )
                
                data = response.json()
                return self._format_time_response(data, timezone)
                    
        except httpx.TimeoutException:
            logger.error("Timeout when calling TimeAPI")
            raise HTTPException(
                status_code=408,
                detail="Time service timeout"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error when calling TimeAPI: {e}")
            raise HTTPException(
                status_code=503,
                detail="Time service unavailable"
            )
    
    def _format_time_response(self, data: dict, requested_timezone: str) -> dict:
        """Format the time API response"""
        try:
            return {
                "time_info": {
                    "requested_timezone": requested_timezone,
                    "current_time": data.get("dateTime"),
                    "date": data.get("date"),
                    "time": data.get("time"),
                    "timezone": data.get("timeZone"),
                    "day_of_week": data.get("dayOfWeek"),
                    "day_of_year": data.get("dayOfYear"),
                    "week_of_year": data.get("weekOfYear")
                },
                "raw_data": data
            }
        except Exception as e:
            logger.error(f"Error formatting time response: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error processing time data"
            )

time_service = TimeService()