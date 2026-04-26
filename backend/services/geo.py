import requests
from typing import Dict, Any

class GeolocationService:
    """
    Resolves attacker IP addresses to physical locations using public APIs.
    """
    def __init__(self):
        self.api_url = "http://ip-api.com/json/"

    def get_location(self, ip: str) -> Dict[str, Any]:
        """
        Fetches city, country, and coordinates for a given IP.
        Note: Will return internal/private data for localhost/private IPs.
        """
        if ip in ["127.0.0.1", "localhost", "::1"]:
            return {
                "city": "Internal Network",
                "country": "Localhost",
                "lat": 19.0760, # Default to Mumbai for demo if local
                "lon": 72.8777
            }
            
        try:
            response = requests.get(f"{self.api_url}{ip}", timeout=5)
            data = response.json()
            
            if data.get("status") == "success":
                return {
                    "city": data.get("city"),
                    "country": data.get("country"),
                    "lat": data.get("lat"),
                    "lon": data.get("lon")
                }
        except Exception as e:
            print(f"Geolocation error: {e}")
            
        return {
            "city": "Unknown",
            "country": "Unknown",
            "lat": 0.0,
            "lon": 0.0
        }
