from ast import Return
import json
from retell import Retell
from fastapi import Request
from app.config import settings

class RetellService:
    def __init__(self):
        self.retell = None

        if settings.RETELL_API_KEY:
            self.retell = Retell(api_key = settings.RETELL_API_KEY)

    async def verify_signature(self, request: Request, post_data: dict) -> bool:
        """Verify Retell Signature"""

        if not self.retell or not settings.VERIFY_RETELL_SIGNATURE:
            return True

        try:
            signature = request.headers.get("X-Retell-Signature","")
            body = json.dumps(post_data, separators=(",",":"), ensure_ascii = False)

            return self.retell.verify(
                 body,
                api_key=settings.RETELL_API_KEY,
                signature=signature
            )

        except Exception as e:
            print(f"Error verifying Retell signature: {e}")
            return False

retell_service = RetellService()