import httpx
from fastapi import HTTPException
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class ExchangeRateService:
    def __init__(self):
        self.base_url = "https://v6.exchangerate-api.com/v6"
        
    async def convert_currency(self, from_currency: str, to_currency: str, amount: float) -> dict:
        """Convert currency using ExchangeRate API"""
        
        if not settings.EXCHANGERATE_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="ExchangeRate API key not configured"
            )
        
        # Build URL with API key and parameters
        url = f"{self.base_url}/{settings.EXCHANGERATE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.get(url)
                
                if response.status_code == 404:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Currency pair {from_currency}/{to_currency} not found"
                    )
                
                if response.status_code != 200:
                    logger.error(f"ExchangeRate API error: {response.status_code}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Exchange rate service unavailable"
                    )
                
                data = response.json()
                
                # Check if API returned an error
                if data.get("result") != "success":
                    error_type = data.get("error-type", "unknown")
                    raise HTTPException(
                        status_code=400,
                        detail=f"Exchange rate API error: {error_type}"
                    )
                
                return self._format_exchange_response(data, from_currency, to_currency, amount)
                    
        except httpx.TimeoutException:
            logger.error("Timeout when calling ExchangeRate API")
            raise HTTPException(
                status_code=408,
                detail="Exchange rate service timeout"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error when calling ExchangeRate API: {e}")
            raise HTTPException(
                status_code=503,
                detail="Exchange rate service unavailable"
            )
    
    def _format_exchange_response(self, data: dict, from_currency: str, to_currency: str, amount: float) -> dict:
        """Format the exchange rate API response"""
        try:
            return {
                "conversion": {
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "original_amount": amount,
                    "converted_amount": data.get("conversion_result"),
                    "conversion_rate": data.get("conversion_rate")
                },
                "api_info": {
                    "base_code": data.get("base_code"),
                    "target_code": data.get("target_code"),
                    "result": data.get("result"),
                    "time_last_update": data.get("time_last_update_utc"),
                    "time_next_update": data.get("time_next_update_utc")
                }
            }
        except Exception as e:
            logger.error(f"Error formatting exchange rate response: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error processing exchange rate data"
            )

exchange_rate_service = ExchangeRateService()