from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models import TimeRequest
from app.services.time import time_service

router = APIRouter(prefix="/api/time", tags=["time"])

@router.post("/current")
async def get_current_time(time_request: TimeRequest):
    """Get current time for a timezone"""
    
    try:
        result = await time_service.get_current_time(time_request.timeZone)
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in time endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Sorry, something went wrong with your time request. Please try again.",
                "details": str(e)
            }
        )