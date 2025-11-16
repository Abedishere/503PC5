# Map Agent Project Summary

## Overview
This project implements a Map Agent using custom map servers (OpenRouteService and OpenStreetMap) integrated with the Gemini LLM through the OpenAI Agents SDK.

## Architecture

### Components

1. **Map Servers (Tools)**
   - **OpenStreetMap Server (OSMServer)**: Handles geocoding, reverse geocoding, and POI searches using Nominatim API
   - **OpenRouteService Server (ORSServer)**: Handles routing, distance calculations, and nearby POI searches

2. **Gemini Provider**
   - Lightweight provider connecting OpenAI Agents SDK with Gemini LLM
   - Orchestrates the tool-calling loop
   - Converts tool functions to Gemini-compatible format

3. **Agent SDK App**
   - Registers all map servers as tools
   - Creates the main AgentsSDKMapAssistant class
   - Provides unified interface for all map operations

4. **Jupyter Notebook Interface**
   - Individual test cases for each tool
   - Gradio web interface for user interaction
   - Direct tool testing capabilities

## Key Features

### OSM Server Capabilities
- **Geocode**: Convert place names to coordinates
- **Reverse Geocode**: Convert coordinates to addresses
- **Search POI**: Find points of interest by keyword and city

### ORS Server Capabilities
- **Route**: Get driving directions between points
- **Distance**: Calculate distances between locations
- **Nearby**: Find nearby points of interest

## Technology Stack

- **OpenAI Agents SDK**: Framework for building LLM agents
- **Gemini 2.0 Flash**: Google's latest LLM model
- **OpenStreetMap Nominatim**: Free geocoding service
- **OpenRouteService**: Routing and distance API
- **Gradio**: Web UI framework
- **Python**: asyncio for async operations

## Usage Flow

1. User sends a natural language query (e.g., "Find hotels in Bhamdoun mountain resort")
2. Gemini LLM processes the query and determines which tools to call
3. Agent SDK dispatches tool calls to appropriate servers
4. Servers make API calls to external services (OSM/ORS)
5. Results are returned to Gemini for processing
6. Gemini generates a natural language response
7. Response is displayed to the user

## Configuration

Required environment variables in `.env`:
- `ORS_API_KEY`: OpenRouteService API key
- `GEMINI_API_KEY`: Google Gemini API key
- `GEMINI_MODEL`: Gemini model name (default: gemini-2.0-flash)
- `OSM_COUNTRY_CODES`: Country codes for OSM searches (default: lb)

## Testing

The project includes:
- Unit tests for individual tools
- Integration tests through the Jupyter notebook
- Interactive testing via Gradio web interface

## Example Queries

- "Find the coordinates of Bhamdoun, the famous mountain resort town"
- "What place is located at 33.8080, 35.6450? I think it's a historic hotel"
- "Find cafes and restaurants in Bhamdoun, the mountain resort town"
- "Get a scenic route from Beirut to Bhamdoun mountain resort"
- "What's the driving distance from Beirut to Bhamdoun?"
- "Find hotels and chalets near Bhamdoun for a weekend getaway"

## Benefits

1. **Modular Design**: Separate servers for different map services
2. **Async Operations**: Non-blocking API calls for better performance
3. **LLM Integration**: Natural language interface for map queries
4. **Extensible**: Easy to add new map services or tools
5. **User-Friendly**: Gradio interface for easy interaction

## Future Enhancements

- Add more map service providers
- Implement caching for frequently used queries
- Add visualization of routes on actual maps
- Support for multiple countries and regions
- Enhanced error handling and retry logic
