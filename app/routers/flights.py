from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.models import RetellResponse, FlightSearchRequest
from app.services.flight import flight_service
from app.services.retell import retell_service
import json

router = APIRouter(prefix="/api/flights", tags=["flights"])

@router.post("/search")
async def search_flights(flight_request: FlightSearchRequest):
    """Main endpoint for flight search from Retell AI"""

    try:
        print(f"Received request: {flight_request.model_dump()}")

        result = await flight_service.search_flights(flight_request)
        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JSONResponse(content={
        "error": "Sorry, something went wrong with your flight search. Please try again."
        })
