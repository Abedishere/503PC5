"""
Agent SDK Application for Map Assistant.
Registers map servers as tools and creates the main agent assistant.
"""

from .servers.ors_server import ORSServer
from .servers.osm_server import OSMServer


# Initialize servers
ors_server = ORSServer()
osm_server = OSMServer()


# Create list of all available tools
TOOLS = [
    # OSM Server tools
    osm_server.geocode,
    osm_server.reverse,
    osm_server.search_poi,
    # ORS Server tools
    ors_server.route,
    ors_server.distance,
    ors_server.nearby
]


class AgentsSDKMapAssistant:
    """
    Map Assistant that dispatches tool calls to appropriate servers.
    """

    def __init__(self):
        """Initialize the map assistant with server instances."""
        self.ors_server = ors_server
        self.osm_server = osm_server

    def geocode(self, place: str):
        """Geocode a place name to coordinates."""
        return self.osm_server.geocode(place)

    def reverse(self, lat: float, lon: float):
        """Reverse geocode coordinates to address."""
        return self.osm_server.reverse(lat, lon)

    def search_poi(self, query: str, city: str = None):
        """Search for points of interest."""
        return self.osm_server.search_poi(query, city)

    def route(self, origin: list, destination: list, profile: str = "driving-car"):
        """Get route between two points."""
        return self.ors_server.route(origin, destination, profile)

    def distance(self, origin: list, destination: list):
        """Calculate distance between two points."""
        return self.ors_server.distance(origin, destination)

    def nearby(self, coordinates: list, category: str = None):
        """Find nearby points of interest."""
        return self.ors_server.nearby(coordinates, category)


# Create global agent instance
agent = AgentsSDKMapAssistant()
