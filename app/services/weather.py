import httpx
from fastapi import HTTPException
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
    async def get_current_weather(self, q: str) -> dict:
        """Get current weather for a location"""
        
        if not settings.OPENWEATHER_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenWeather API key not configured"
            )
        
        params = {
            "q": q,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.get(self.base_url, params=params)
                
                if response.status_code == 404:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Location '{q}' not found"
                    )
                
                if response.status_code != 200:
                    logger.error(f"OpenWeather API error: {response.status_code}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Weather service unavailable"
                    )
                
                data = response.json()
                return self._format_weather_response(data)
                    
        except httpx.TimeoutException:
            logger.error("Timeout when calling OpenWeather API")
            raise HTTPException(
                status_code=408,
                detail="Weather service timeout"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error when calling OpenWeather API: {e}")
            raise HTTPException(
                status_code=503,
                detail="Weather service unavailable"
            )
    
    def _format_weather_response(self, data: dict) -> dict:
        """Format the weather API response"""
        try:
            return {
                "location": {
                    "name": data.get("name"),
                    "country": data.get("sys", {}).get("country"),
                    "coordinates": {
                        "lat": data.get("coord", {}).get("lat"),
                        "lon": data.get("coord", {}).get("lon")
                    }
                },
                "weather": {
                    "main": data.get("weather", [{}])[0].get("main"),
                    "description": data.get("weather", [{}])[0].get("description"),
                    "temperature": {
                        "current": data.get("main", {}).get("temp"),
                        "feels_like": data.get("main", {}).get("feels_like"),
                        "min": data.get("main", {}).get("temp_min"),
                        "max": data.get("main", {}).get("temp_max")
                    },
                    "humidity": data.get("main", {}).get("humidity"),
                    "pressure": data.get("main", {}).get("pressure"),
                    "visibility": data.get("visibility"),
                    "wind": {
                        "speed": data.get("wind", {}).get("speed"),
                        "direction": data.get("wind", {}).get("deg")
                    }
                },
                "timestamp": data.get("dt"),
                "timezone": data.get("timezone")
            }
        except Exception as e:
            logger.error(f"Error formatting weather response: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error processing weather data"
            )

weather_service = WeatherService()