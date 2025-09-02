from typing import Dict, Any
from app.services.amadeus import amadeus_service
from app.models import FlightSearchRequest

class FlightService:
    def __init__(self):
        pass

    def validate_search_request(self, request: FlightSearchRequest) -> tuple[bool,str]:
        """Validate Flight Search Request"""

        if not request.origin or not request.destination or not request.departure_date:
            return False, "Origin, destination, and departure date are required"

        if len(request.origin) < 2 or len(request.destination) < 2:
            return False, "Airport codes must be at least 2 characters"

        try:
            from datetime import datetime
            datetime.strptime(request.departure_date, "%Y-%m-%d")
            if request.return_date:
                datetime.strptime(request.return_date, "%Y-%m-%d")
        except Exception as e:
            return False, "Invalid date format"

        return True, ""


    async def search_flights(self, request: FlightSearchRequest) -> Dict[str, Any]:
        """Search Flights and return raw data"""

        is_valid, error_msg = self.validate_search_request(request)
        if not is_valid:
            return {"error": f"I need valid flight information: {error_msg}"}

        try:
            # Prepare search parameters
            search_params = {
                "origin": request.origin.upper(),
                "destination": request.destination.upper(),
                "departure_date": request.departure_date,
                "adults": request.adults
            }

            if request.return_date:
                search_params["return_date"] = request.return_date

            flights_data = await amadeus_service.search_flights(search_params)
            return flights_data
            
        except ValueError as e:
            return {"error": f"Invalid search parameters: {str(e)}"}
        except Exception as e:
            print(f"Flight search error: {e}")
            return {"error": "I'm having trouble searching for flights right now. Please try again."}

# Singleton instance
flight_service = FlightService()