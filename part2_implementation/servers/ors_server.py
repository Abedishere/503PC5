"""
OpenRouteService Server for routing and distance calculations.
Handles routing, distance calculations, and finding nearby points of interest.
"""

import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ORSServer:
    """OpenRouteService server for routing and POI operations."""

    def __init__(self):
        """Initialize the ORS server with API key."""
        self.api_key = os.getenv("ORS_API_KEY")
        if not self.api_key or self.api_key == "YOUR_ORS_KEY_HERE":
            raise ValueError("ORS_API_KEY not set in .env file")

        self.base_url = "https://api.openrouteservice.org/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def route(self, origin: List[float], destination: List[float], profile: str = "driving-car") -> Dict[str, Any]:
        """
        Get driving directions between two points.

        Args:
            origin: [longitude, latitude] of starting point
            destination: [longitude, latitude] of ending point
            profile: Travel profile (default: "driving-car")

        Returns:
            Dictionary with route information including distance, duration, and steps
        """
        url = f"{self.base_url}/directions/{profile}"

        # Convert protobuf RepeatedComposite to list if needed
        origin = list(origin) if not isinstance(origin, list) else origin
        destination = list(destination) if not isinstance(destination, list) else destination

        payload = {
            "coordinates": [origin, destination]
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            # Extract route information
            if "routes" in data and len(data["routes"]) > 0:
                route = data["routes"][0]
                summary = route.get("summary", {})

                return {
                    "distance_km": round(summary.get("distance", 0) / 1000, 2),
                    "duration_minutes": round(summary.get("duration", 0) / 60, 2),
                    "geometry": route.get("geometry", {}),
                    "segments": route.get("segments", []),
                    "bbox": route.get("bbox", [])
                }
            else:
                return {"error": "No route found"}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def distance(self, origin: List[float], destination: List[float]) -> Dict[str, Any]:
        """
        Calculate distance between two points.

        Args:
            origin: [longitude, latitude] of starting point
            destination: [longitude, latitude] of ending point

        Returns:
            Dictionary with distance in kilometers
        """
        url = f"{self.base_url}/directions/driving-car"

        # Convert protobuf RepeatedComposite to list if needed
        origin = list(origin) if not isinstance(origin, list) else origin
        destination = list(destination) if not isinstance(destination, list) else destination

        payload = {
            "coordinates": [origin, destination]
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if "routes" in data and len(data["routes"]) > 0:
                route = data["routes"][0]
                summary = route.get("summary", {})
                distance_km = round(summary.get("distance", 0) / 1000, 2)

                return {
                    "distance_km": distance_km,
                    "origin": origin,
                    "destination": destination
                }
            else:
                return {"error": "Could not calculate distance"}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def nearby(self, coordinates: List[float], category: str = None) -> Dict[str, Any]:
        """
        Find nearby points of interest.

        Args:
            coordinates: [longitude, latitude] of the point
            category: Optional category filter (e.g., "restaurant", "hospital")

        Returns:
            Dictionary with nearby POIs
        """
        url = f"{self.base_url}/pois"

        # Convert protobuf RepeatedComposite to list if needed
        coordinates = list(coordinates) if not isinstance(coordinates, list) else coordinates

        # Build request payload
        payload = {
            "request": "pois",
            "geometry": {
                "bbox": [
                    [coordinates[0] - 0.01, coordinates[1] - 0.01],
                    [coordinates[0] + 0.01, coordinates[1] + 0.01]
                ],
                "geojson": {
                    "type": "Point",
                    "coordinates": coordinates
                },
                "buffer": 1000  # 1km radius
            }
        }

        if category:
            payload["filters"] = {
                "category_ids": [category]
            }

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            # Extract POI information
            pois = []
            if "features" in data:
                for feature in data["features"][:10]:  # Limit to 10 results
                    properties = feature.get("properties", {})
                    geometry = feature.get("geometry", {})

                    pois.append({
                        "name": properties.get("osm_tags", {}).get("name", "Unknown"),
                        "category": properties.get("category_ids", {}).get("category_name", "Unknown"),
                        "coordinates": geometry.get("coordinates", []),
                        "distance": properties.get("distance", 0)
                    })

            return {
                "center": coordinates,
                "pois": pois,
                "count": len(pois)
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
