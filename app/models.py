from locale import currency
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class FlightSearchRequest(BaseModel):
    origin: str = Field(..., description="Origin airport code")
    destination: str = Field(..., description="Destination airport code") 
    departure_date: str = Field(..., description="Departure date YYYY-MM-DD")
    return_date: Optional[str] = Field(None, description="Return date YYYY-MM-DD")
    adults: Optional[int] = Field(1, description="Number of adult passengers")

class RetellRequest(BaseModel):
    args: FlightSearchRequest

class RetellResponse(BaseModel):
    result: str

class AmadeusTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str

class FlightSegment(BaseModel):
    departure_code: str
    arrival_code: str
    departure_code: str
    arrival_time: str
    airline_code: str
    flight_number: str
    duration: str

class FlightOffer(BaseModel):
    price: str
    currency:str
    segments: List[FlightSegment]
    stops: int
    total_duration: str

class FlightSearchResponse(BaseModel):
    flights: List[FlightOffer]
    total_results: int
    origin: str
    destination: str

class WeatherRequest(BaseModel):
    q: str = Field(..., description="Location query (city name, country, etc.)")