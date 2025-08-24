from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models import ExchangeRateRequest
from app.services.exchange import exchange_rate_service

router = APIRouter(prefix="/api/exchange", tags=["exchange"])

@router.post("/convert")
async def convert_currency(exchange_request: ExchangeRateRequest):
    """Convert currency using exchange rates"""
    
    try:
        result = await exchange_rate_service.convert_currency(
            exchange_request.from_currency, 
            exchange_request.to_currency, 
            exchange_request.amount
        )
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in exchange rate endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Sorry, something went wrong with your currency conversion. Please try again.",
                "details": str(e)
            }
        )