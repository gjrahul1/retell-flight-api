import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    #API KEYS
    RETELL_API_KEY: Optional[str] = None
    AMADEUS_API_KEY: Optional[str] = None
    AMADEUS_API_SECRET: Optional[str] = None
    OPENWEATHER_API_KEY: Optional[str] = None
    OPENTRIPMAP_API_KEY: Optional[str] = None

    #APP Settings
    PORT: int = 8000
    DEBUG: bool = False
    VERIFY_RETELL_SIGNATURE: bool = True

    #Amadeus API Settings
    AMADEUS_TOKEN_URL: str = "https://test.api.amadeus.com/v1/security/oauth2/token"
    AMADEUS_FLIGHT_URL: str = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    AMADEUS_TOKEN_CACHE_TIME: int = 1800

    #Flight Search Settings
    MAX_FLIGHT_RESULTS: int = 10
    VOICE_FLIGHT_RESULTS: int = 3
    DEFAULT_CURRENCY:str = "USD"
    REQUEST_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()

