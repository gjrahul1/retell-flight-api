from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.services.retell import retell_service
from app.config import settings
import json
from typing import Dict, Any

router = APIRouter(prefix="/api/retell", tags=["retell"])

@router.post("/agent/{agent_id}")
async def retell_agent_endpoint(agent_id: str, request: Request):
    """
    Main endpoint for Retell voice agent interactions
    Handles webhook calls from Retell AI for the specified agent
    """
    try:
        # Get the request body
        body = await request.body()
        if not body:
            raise HTTPException(status_code=400, detail="Request body is required")
        
        try:
            post_data = json.loads(body.decode())
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in request body")
        
        # Verify Retell signature if enabled
        if not await retell_service.verify_signature(request, post_data):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Validate that this matches the expected agent_id
        expected_agent_id = "agent_bda99a1b4a3929766994d78bae"
        if agent_id != expected_agent_id:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        # Process the Retell request
        # This is where you would handle the actual agent logic
        # For now, returning a basic response structure
        
        response_data = {
            "response": f"Hello from Retell agent {agent_id}. I received your message.",
            "response_id": post_data.get("response_id", 1)
        }
        
        return JSONResponse(content=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in retell agent endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/agent/{agent_id}/health")
async def retell_agent_health(agent_id: str):
    """
    Health check endpoint for the Retell voice agent
    """
    expected_agent_id = "agent_bda99a1b4a3929766994d78bae"
    
    if agent_id != expected_agent_id:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    return {
        "agent_id": agent_id,
        "status": "healthy",
        "retell_configured": bool(settings.RETELL_API_KEY),
        "signature_verification": settings.VERIFY_RETELL_SIGNATURE
    }

@router.get("/config")
async def retell_config():
    """
    Get Retell configuration status
    """
    return {
        "retell_api_configured": bool(settings.RETELL_API_KEY),
        "signature_verification_enabled": settings.VERIFY_RETELL_SIGNATURE,
        "supported_agent": "agent_bda99a1b4a3929766994d78bae"
    }