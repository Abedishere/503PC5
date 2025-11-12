"""
Geocoding Server - MCP-compliant server for address/coordinate conversion
Following OpenAI Agents SDK patterns with function tools
"""

import asyncio
import os
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field
import httpx


class GeocodingResult(BaseModel):
    """Result from a geocoding operation"""
    address: str
    latitude: float
    longitude: float
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1")
    place_type: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


class GeocodingServer:
    """
    MCP-compliant Geocoding Server
    Provides forward and reverse geocoding capabilities
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the Geocoding Server

        Args:
            api_key: API key for geocoding service (optional for OSM Nominatim)
            base_url: Base URL for geocoding API (defaults to OSM Nominatim)
        """
        self.api_key = api_key or os.getenv("OPENSTREETMAP_API_KEY", "")
        self.base_url = base_url or "https://nominatim.openstreetmap.org"
        self.session = None

    async def _get_session(self) -> httpx.AsyncClient:
        """Get or create HTTP session"""
        if self.session is None:
            self.session = httpx.AsyncClient(timeout=30.0)
        return self.session

    async def forward_geocode(
        self,
        address: str,
        limit: int = 5
    ) -> List[GeocodingResult]:
        """
        Convert an address to geographic coordinates (forward geocoding)

        Args:
            address: The address to geocode (e.g., "1600 Amphitheatre Parkway, Mountain View, CA")
            limit: Maximum number of results to return (default: 5)

        Returns:
            List of geocoding results with coordinates and metadata

        Example:
            >>> results = await server.forward_geocode("Empire State Building, New York")
            >>> print(f"Location: {results[0].latitude}, {results[0].longitude}")
        """
        # PLACEHOLDER: Replace with actual API call
        # This simulates the API call structure for OSM Nominatim
        session = await self._get_session()

        params = {
            "q": address,
            "format": "json",
            "limit": limit,
            "addressdetails": 1
        }

        headers = {
            "User-Agent": "MCP-MapServers/1.0"
        }

        # Simulated response - replace with actual API call:
        # response = await session.get(f"{self.base_url}/search", params=params, headers=headers)
        # data = response.json()

        # MOCK DATA for demonstration
        mock_data = [
            {
                "lat": "40.7484",
                "lon": "-73.9857",
                "display_name": f"{address} (simulated)",
                "importance": 0.9,
                "type": "building",
                "address": {
                    "country": "United States",
                    "city": "New York"
                }
            }
        ]

        results = []
        for item in mock_data:
            result = GeocodingResult(
                address=item.get("display_name", address),
                latitude=float(item["lat"]),
                longitude=float(item["lon"]),
                confidence=float(item.get("importance", 0.5)),
                place_type=item.get("type"),
                country=item.get("address", {}).get("country"),
                city=item.get("address", {}).get("city")
            )
            results.append(result)

        return results

    async def reverse_geocode(
        self,
        latitude: float,
        longitude: float
    ) -> GeocodingResult:
        """
        Convert geographic coordinates to an address (reverse geocoding)

        Args:
            latitude: Latitude coordinate (-90 to 90)
            longitude: Longitude coordinate (-180 to 180)

        Returns:
            Geocoding result with address information

        Example:
            >>> result = await server.reverse_geocode(40.7484, -73.9857)
            >>> print(f"Address: {result.address}")
        """
        # Validate coordinates
        if not (-90 <= latitude <= 90):
            raise ValueError(f"Invalid latitude: {latitude}. Must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError(f"Invalid longitude: {longitude}. Must be between -180 and 180")

        # PLACEHOLDER: Replace with actual API call
        session = await self._get_session()

        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json",
            "addressdetails": 1
        }

        headers = {
            "User-Agent": "MCP-MapServers/1.0"
        }

        # Simulated response - replace with actual API call:
        # response = await session.get(f"{self.base_url}/reverse", params=params, headers=headers)
        # data = response.json()

        # MOCK DATA for demonstration
        mock_data = {
            "lat": str(latitude),
            "lon": str(longitude),
            "display_name": f"Simulated address near {latitude}, {longitude}",
            "importance": 0.8,
            "type": "building",
            "address": {
                "country": "United States",
                "city": "New York"
            }
        }

        result = GeocodingResult(
            address=mock_data.get("display_name", f"{latitude}, {longitude}"),
            latitude=latitude,
            longitude=longitude,
            confidence=float(mock_data.get("importance", 0.5)),
            place_type=mock_data.get("type"),
            country=mock_data.get("address", {}).get("country"),
            city=mock_data.get("address", {}).get("city")
        )

        return result

    async def batch_geocode(
        self,
        addresses: List[str]
    ) -> List[List[GeocodingResult]]:
        """
        Geocode multiple addresses in batch

        Args:
            addresses: List of addresses to geocode

        Returns:
            List of geocoding results for each address

        Example:
            >>> addresses = ["Times Square, NYC", "Central Park, NYC"]
            >>> results = await server.batch_geocode(addresses)
        """
        # Process in parallel with rate limiting
        tasks = [self.forward_geocode(addr, limit=1) for addr in addresses]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error geocoding address '{addresses[i]}': {result}")
                processed_results.append([])
            else:
                processed_results.append(result)

        return processed_results

    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.aclose()
            self.session = None


# Function tools for OpenAI Agents SDK
async def geocode_address(address: str, limit: int = 5) -> str:
    """
    Convert an address to coordinates (OpenAI Agents SDK tool)

    Args:
        address: Address to geocode
        limit: Max results to return

    Returns:
        JSON string with geocoding results
    """
    server = GeocodingServer()
    results = await server.forward_geocode(address, limit)
    await server.close()

    # Format for agent consumption
    formatted = []
    for r in results:
        formatted.append({
            "address": r.address,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "confidence": r.confidence
        })

    return str(formatted)


async def reverse_geocode_coordinates(latitude: float, longitude: float) -> str:
    """
    Convert coordinates to an address (OpenAI Agents SDK tool)

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate

    Returns:
        JSON string with address information
    """
    server = GeocodingServer()
    result = await server.reverse_geocode(latitude, longitude)
    await server.close()

    return str({
        "address": result.address,
        "city": result.city,
        "country": result.country,
        "confidence": result.confidence
    })
