import httpx
from datetime import datetime, timedelta
from typing import Optional,Dict,Any
from app.config import settings
from app.models import AmadeusTokenResponse

class AmadeusService:
    def __init__(self):
        self._token_cache: Dict[str,Any] = {
            "token": None,
            "expires_at": None
        }

    async def get_access_token(self) -> str:
        """Get or Access Amadeus API Token"""

        if(self._token_cache["token"] and
           self._token_cache["expires_at"] and
           datetime.now() < self._token_cache["expires_at"]):

           return self._token_cache["token"]

    
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.AMADEUS_TOKEN_URL,
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "client_credentials",
                    "client_id": settings.AMADEUS_API_KEY,
                    "client_secret": settings.AMADEUS_API_SECRET
                },
                timeout=settings.REQUEST_TIMEOUT
            )

            if response.status_code != 200:
                raise Exception(f"Token request failed: {response.status_code}")

            token_data = response.json()

            token = token_data["access_token"]
            expires_in = token_data.get("expires_in", settings.AMADEUS_TOKEN_CACHE_TIME)

            #Cache Token
            self._token_cache["token"] = token
            self._token_cache["expires_at"] = datetime.now() + timedelta(seconds = expires_in - 60)

            return token

    async def search_flights(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Search flights using Amadeus API"""

        token = await self.get_access_token()

        params = {
            "originLocationCode": search_params.get("origin",""),
            "destinationLocationCode": search_params.get("destination",""),
            "departureDate": search_params.get("departure_date",""),
            "adults": search_params.get("adults",1),
            "max": settings.MAX_FLIGHT_RESULTS,
            "currencyCode": settings.DEFAULT_CURRENCY
        }

        if search_params.get("return_date"):
            params["returnDate"] = search_params["return_date"]

        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.AMADEUS_FLIGHT_URL,
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                params = params,
                timeout = settings.REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                raise ValueError(f"Invalid request: {error_data}")
            else:
                raise Exception(f"Flight search failed: {response.status_code}")

amadeus_service = AmadeusService()