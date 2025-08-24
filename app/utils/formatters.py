from datetime import datetime
from locale import currency
from typing import Dict, Any
from app.config import settings

class FlightFormatter:

    def format_for_voice(self, flights_data: Dict[str, Any], origin: str, destination: str) -> str:
        """Format Flight Data for Voice Response"""

        if not flights_data.get("data") or len(flights_data["data"]) == 0:
            return f"Sorry, I couldn't find any flights from {origin} to {destination}. Please try different dates or destinations."

        flights = flights_data["data"][:settings.VOICE_FLIGHT_RESULTS]
        result = f"Great! I found {len(flights)} flight options from {origin} to {destination}:\n\n"

        for i, flight in enumerate(flights, start=1):
            try:
                flight_info = self._extract_flight_info(flight)
                result += self._format_single_flight(i, flight_info)

            except Exception as e:
                print(f"Error formatting flight {i}: {e}")
                result += f"Option {i}: Flight available\n\n"

        result += "Would you like me to search for different dates or provide more details?"
        return result

    def _extract_flight_info(self, flight: Dict[str, Any]) -> Dict[str, Any]:
        """Extract Flight Information"""

        price = flight["price"]["total"]
        currency = flight["price"]["currency"]

        itinerary = flight["itineraries"][0]
        segments = itinerary["segments"]

        first_segment = segments[0]
        last_segment = segments[-1]

        return {
            "price": price,
            "currency": currency,
            "departure_code": first_segment["departure"]["iataCode"],
            "departure_time": first_segment["departure"]["at"],
            "arrival_code": last_segment["arrival"]["iataCode"],
            "arrival_time": last_segment["arrival"]["at"],
           "airline_code": first_segment["carrierCode"],
           "flight_number": f"{first_segment['carrierCode']}{first_segment['number']}",
            "duration": itinerary.get("duration", "").replace("PT", "").replace("H", "h ").replace("M", "m"),
            "stops": len(segments) - 1
        }

    def _format_single_flight(self, index: int, flight_info: Dict[str, Any]) -> str:
        """Format a single flight for voice output"""

        try:
            dep_dt =  datetime.fromisoformat(flight_info["departure_time"]).replace("Z","+00:00")
            arr_dt = datetime.fromisoformat(flight_info["arrival_time"]).replace("Z","+00:00")
            dep_time = dep_dt.strftime("%I:%M %p").lstrip("0")
            arr_time = arr_dt.strftime("%I:%M %p").lstrip("0")

        except:
            dep_time = flight_info["departure_time"].lstrip("T")[1][:5]
            arr_time = flight_info["arrival_time"].lstrip("0")[1][:5]

        # Format stops
        stops = flight_info["stops"]
        stop_text = f", {stops} stop{'s' if stops != 1 else ''}" if stops > 0 else ", non-stop"
        
        return (f"Option {index}: {flight_info['flight_number']} for "
                f"{flight_info['price']} {flight_info['currency']}\n"
                f"Departs {flight_info['departure_code']} at {dep_time}, "
                f"arrives {flight_info['arrival_code']} at {arr_time}\n"
                f"Duration: {flight_info['duration']}{stop_text}\n\n")