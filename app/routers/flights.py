from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.models import RetellRequest, RetellResponse, FlightSearchRequest
from app.services.flight import flight_service
from app.services.retell import retell_service
import json

router = APIRouter(prefix="/api/flights", tags=["flights"])

@router.post("/search", response_model=RetellResponse)
async def search_flights(retell_request: RetellRequest):
    """Main endpoint for flight search from Retell AI"""

    try:
        print(f"Received request: {retell_request.model_dump()}")
        search_request = retell_request.args

        result = await flight_service.search_flights(search_request)
        return JSONResponse(content={"result": result})

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JSONResponse(content={
            "result": "Sorry, something went wrong with your flight search. Please try again."
        })
