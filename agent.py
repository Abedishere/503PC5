"""
Map Services Agent - OpenAI Agents SDK Integration
Integrates geocoding, routing, and POI servers following MCP conventions
Compatible with OpenAI and DeepSeek APIs
"""

import os
import asyncio
from typing import List, Optional
from dotenv import load_dotenv

# Note: This is a conceptual implementation showing the structure
# For actual OpenAI Agents SDK, you would use:
# from openai_agents import Agent, Tool, Session

# Load environment variables
load_dotenv()


class MapServicesAgent:
    """
    Agent that integrates all map services using OpenAI Agents SDK patterns
    Compatible with OpenAI and DeepSeek LLM providers
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize the Map Services Agent

        Args:
            api_key: API key for LLM provider (OpenAI or DeepSeek)
            base_url: Base URL for API (OpenAI or DeepSeek)
            model: Model to use (e.g., gpt-4, deepseek-chat)
        """
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("LLM_MODEL", "gpt-4")

        # Import map servers
        from map_servers.geocoding_server import (
            geocode_address,
            reverse_geocode_coordinates
        )
        from map_servers.routing_server import (
            calculate_route_between_points,
            get_distance_matrix
        )
        from map_servers.poi_server import (
            find_nearby_places,
            search_places_by_text,
            get_place_info
        )

        # Store function tools
        self.tools = {
            "geocode_address": geocode_address,
            "reverse_geocode_coordinates": reverse_geocode_coordinates,
            "calculate_route_between_points": calculate_route_between_points,
            "get_distance_matrix": get_distance_matrix,
            "find_nearby_places": find_nearby_places,
            "search_places_by_text": search_places_by_text,
            "get_place_info": get_place_info
        }

        print(f"🗺️  Map Services Agent initialized")
        print(f"   LLM Provider: {self.base_url}")
        print(f"   Model: {self.model}")
        print(f"   Available tools: {len(self.tools)}")

    def get_system_prompt(self) -> str:
        """Get the system prompt for the agent"""
        return """You are a helpful map services assistant with access to geocoding, routing, and points of interest tools.

You can help users with:
1. Converting addresses to coordinates and vice versa (geocoding)
2. Calculating routes between locations with distance and duration
3. Finding nearby places like restaurants, hotels, museums, etc.
4. Searching for specific places and getting detailed information

When users ask about locations, routes, or places:
- Use the geocoding tools to convert addresses to coordinates
- Use routing tools to calculate travel information
- Use POI tools to find and recommend places
- Provide clear, helpful responses with relevant details

Available tools:
- geocode_address(address, limit): Convert address to coordinates
- reverse_geocode_coordinates(latitude, longitude): Convert coordinates to address
- calculate_route_between_points(origin_lat, origin_lon, dest_lat, dest_lon, mode): Calculate route
- get_distance_matrix(origins, destinations, mode): Calculate distances between multiple points
- find_nearby_places(latitude, longitude, category, radius_meters, limit): Find nearby POIs
- search_places_by_text(query, latitude, longitude, limit): Search places by text query
- get_place_info(place_name): Get detailed place information

Be helpful, accurate, and conversational!"""

    async def process_query(self, user_query: str) -> str:
        """
        Process a user query using the agent's tools

        Args:
            user_query: The user's natural language query

        Returns:
            Agent's response

        Note: This is a simplified implementation. In production, you would use:
            - OpenAI Agents SDK's Agent class
            - Proper function calling with the LLM
            - Session management for conversation history
        """
        print(f"\n🤔 Processing query: {user_query}")

        # PLACEHOLDER: In production, this would use OpenAI Agents SDK
        # Example with actual SDK:
        #
        # from openai_agents import Agent, Session
        #
        # agent = Agent(
        #     name="map_services",
        #     instructions=self.get_system_prompt(),
        #     tools=list(self.tools.values()),
        #     model=self.model,
        #     api_key=self.api_key,
        #     base_url=self.base_url
        # )
        #
        # session = Session()
        # response = await agent.run(user_query, session)
        # return response.messages[-1].content

        # Simplified demonstration logic
        response = await self._simulate_agent_response(user_query)
        return response

    async def _simulate_agent_response(self, query: str) -> str:
        """
        Simulate agent response for demonstration
        In production, this would be handled by the LLM with function calling
        """
        query_lower = query.lower()

        # Simulate intelligent routing to appropriate tools
        if "geocode" in query_lower or "coordinates" in query_lower or "address" in query_lower:
            if any(word in query_lower for word in ["40.", "41.", "-73", "-74"]):  # Looks like coordinates
                result = await self.tools["reverse_geocode_coordinates"](40.7484, -73.9857)
                return f"Based on those coordinates, here's what I found:\n{result}"
            else:
                result = await self.tools["geocode_address"]("Empire State Building", 1)
                return f"Here are the coordinates I found:\n{result}"

        elif "route" in query_lower or "direction" in query_lower or "distance" in query_lower:
            result = await self.tools["calculate_route_between_points"](
                40.7484, -73.9857,  # Empire State Building
                40.7829, -73.9654,  # Central Park
                "driving"
            )
            return f"Here's the route information:\n{result}"

        elif any(word in query_lower for word in ["find", "nearby", "restaurant", "cafe", "hotel", "museum"]):
            category = None
            if "restaurant" in query_lower:
                category = "restaurant"
            elif "cafe" in query_lower or "coffee" in query_lower:
                category = "cafe"
            elif "museum" in query_lower:
                category = "museum"
            elif "park" in query_lower:
                category = "park"

            result = await self.tools["find_nearby_places"](
                40.7484, -73.9857,  # Empire State Building area
                category, 2000, 5
            )
            return f"Here are nearby places I found:\n{result}"

        elif "search" in query_lower or "place" in query_lower:
            result = await self.tools["search_places_by_text"](
                query, 40.7484, -73.9857, 5
            )
            return f"Here's what I found:\n{result}"

        else:
            return """I can help you with:
1. Geocoding - convert addresses to coordinates and vice versa
2. Routing - calculate routes and distances between locations
3. Places - find nearby restaurants, hotels, museums, and more

What would you like to know?"""

    async def interactive_session(self):
        """Run an interactive session with the agent"""
        print("\n" + "="*60)
        print("🗺️  Map Services Agent - Interactive Session")
        print("="*60)
        print("\nI can help you with locations, routes, and places!")
        print("Type 'exit' or 'quit' to end the session.\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\n👋 Goodbye! Have a great day!")
                    break

                if not user_input:
                    continue

                response = await self.process_query(user_input)
                print(f"\n🗺️  Agent: {response}\n")

            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


async def main():
    """Main entry point for the agent"""
    # Initialize agent (works with OpenAI or DeepSeek)
    agent = MapServicesAgent()

    # Example queries
    print("\n" + "="*60)
    print("🧪 Running Example Queries")
    print("="*60)

    examples = [
        "What are the coordinates of the Empire State Building?",
        "Find restaurants near Times Square",
        "Calculate the route from Empire State Building to Central Park",
        "Tell me about Central Park"
    ]

    for i, query in enumerate(examples, 1):
        print(f"\n📝 Example {i}: {query}")
        response = await agent.process_query(query)
        print(f"💬 Response: {response}")
        await asyncio.sleep(1)  # Brief pause between queries

    # Uncomment to run interactive session:
    # await agent.interactive_session()


if __name__ == "__main__":
    asyncio.run(main())
