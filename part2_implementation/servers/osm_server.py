"""
OpenStreetMap Server for geocoding and POI searches.
Handles geocoding, reverse geocoding, and point-of-interest searches using Nominatim.
"""

import os
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OSMServer:
    """OpenStreetMap server for geocoding and POI operations."""

    def __init__(self):
        """Initialize the OSM server."""
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {
            "User-Agent": "MapAgent/1.0"  # Required by Nominatim
        }
        self.country_codes = os.getenv("OSM_COUNTRY_CODES", "lb")

    def geocode(self, place: str) -> Dict[str, Any]:
        """
        Convert a place name to geographic coordinates.

        Args:
            place: Place name (e.g., "Tripoli, Lebanon")

        Returns:
            Dictionary with coordinates and place information
        """
        url = f"{self.base_url}/search"

        params = {
            "q": place,
            "format": "json",
            "limit": 1,
            "countrycodes": self.country_codes
        }

        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if data and len(data) > 0:
                result = data[0]
                return {
                    "place": result.get("display_name", "Unknown"),
                    "latitude": float(result.get("lat", 0)),
                    "longitude": float(result.get("lon", 0)),
                    "type": result.get("type", "Unknown"),
                    "importance": result.get("importance", 0),
                    "bbox": result.get("boundingbox", [])
                }
            else:
                return {"error": f"Could not find location: {place}"}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def reverse(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Convert coordinates to a human-readable address.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dictionary with address information
        """
        url = f"{self.base_url}/reverse"

        params = {
            "lat": lat,
            "lon": lon,
            "format": "json"
        }

        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if "address" in data:
                address = data.get("address", {})
                return {
                    "display_name": data.get("display_name", "Unknown"),
                    "address": {
                        "road": address.get("road", ""),
                        "suburb": address.get("suburb", ""),
                        "city": address.get("city", address.get("town", address.get("village", ""))),
                        "state": address.get("state", ""),
                        "country": address.get("country", ""),
                        "postcode": address.get("postcode", "")
                    },
                    "latitude": lat,
                    "longitude": lon,
                    "type": data.get("type", "Unknown")
                }
            else:
                return {"error": "Could not reverse geocode coordinates"}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def search_poi(self, query: str, city: str = None) -> Dict[str, Any]:
        """
        Find points of interest based on a keyword and optional city.

        Args:
            query: Search keyword (e.g., "restaurant")
            city: Optional city name to limit search

        Returns:
            Dictionary with POI results
        """
        url = f"{self.base_url}/search"

        # Build search query
        search_query = query
        if city:
            search_query = f"{query} in {city}"

        params = {
            "q": search_query,
            "format": "json",
            "limit": 10,
            "countrycodes": self.country_codes
        }

        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            pois = []
            for result in data:
                pois.append({
                    "name": result.get("display_name", "Unknown"),
                    "latitude": float(result.get("lat", 0)),
                    "longitude": float(result.get("lon", 0)),
                    "type": result.get("type", "Unknown"),
                    "class": result.get("class", "Unknown"),
                    "importance": result.get("importance", 0)
                })

            return {
                "query": search_query,
                "count": len(pois),
                "pois": pois
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
