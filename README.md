# Map Servers with OpenAI Agents SDK and MCP

A comprehensive implementation of map-based services following Model Context Protocol (MCP) conventions, designed to work with OpenAI Agents SDK and compatible with alternative LLM providers like DeepSeek.

## 🎯 Overview

This project implements three MCP-compliant map servers:

1. **Geocoding Server** - Convert addresses to coordinates and vice versa
2. **Routing Server** - Calculate routes, distances, and travel times
3. **POI Server** - Search for and discover points of interest

All servers are integrated into a unified AI agent that can intelligently handle location-based queries.

## 🏗️ Architecture

```
map_servers/
├── geocoding_server.py   # Address ↔ Coordinates conversion
├── routing_server.py      # Route calculation & navigation
└── poi_server.py          # Points of interest search

agent.py                   # Main agent with all tools integrated
tests/                     # Comprehensive unit tests
examples/                  # Demo scripts and usage examples
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- API keys (optional for mock data)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd 503PC5
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

### Configuration for DeepSeek

To use DeepSeek instead of OpenAI:

```bash
# In your .env file:
LLM_API_KEY=your_deepseek_api_key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

### Running the Agent

```bash
python agent.py
```

This will run example queries demonstrating each server's capabilities.

## 📖 Usage Examples

### Geocoding Server

```python
from map_servers.geocoding_server import GeocodingServer

server = GeocodingServer()

# Forward geocoding (address to coordinates)
results = await server.forward_geocode("Empire State Building")
print(f"Coordinates: {results[0].latitude}, {results[0].longitude}")

# Reverse geocoding (coordinates to address)
result = await server.reverse_geocode(40.7484, -73.9857)
print(f"Address: {result.address}")

await server.close()
```

### Routing Server

```python
from map_servers.routing_server import RoutingServer

server = RoutingServer()

# Calculate route
route = await server.calculate_route(
    origin_lat=40.7484, origin_lon=-73.9857,
    dest_lat=40.7829, dest_lon=-73.9654,
    mode="driving"
)

print(f"Distance: {route.distance_meters}m")
print(f"Duration: {route.duration_seconds}s")
print(f"Steps: {len(route.steps)}")

await server.close()
```

### POI Server

```python
from map_servers.poi_server import POIServer

server = POIServer()

# Find nearby places
pois = await server.search_nearby(
    latitude=40.7484,
    longitude=-73.9857,
    category="restaurant",
    radius_meters=2000,
    limit=5
)

for poi in pois:
    print(f"{poi.name} - {poi.distance_meters}m away")

# Text search
results = await server.search_text("coffee shops", latitude=40.7484, longitude=-73.9857)

await server.close()
```

### Using the Agent

```python
from agent import MapServicesAgent

agent = MapServicesAgent()

# Process natural language queries
response = await agent.process_query("Find restaurants near Times Square")
print(response)

# Interactive session
await agent.interactive_session()
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=map_servers --cov-report=html

# Run specific test file
pytest tests/test_geocoding_server.py -v

# Run specific test
pytest tests/test_geocoding_server.py::test_forward_geocode -v
```

## 🔧 Server Operations

### Geocoding Server Operations

- `forward_geocode(address, limit)` - Convert address to coordinates
- `reverse_geocode(latitude, longitude)` - Convert coordinates to address
- `batch_geocode(addresses)` - Geocode multiple addresses at once

### Routing Server Operations

- `calculate_route(origin_lat, origin_lon, dest_lat, dest_lon, mode)` - Calculate route
- `calculate_distance_matrix(origins, destinations, mode)` - Distance matrix
- `get_route_alternatives(origin_lat, origin_lon, dest_lat, dest_lon, alternatives)` - Get alternative routes

### POI Server Operations

- `search_nearby(latitude, longitude, radius_meters, category, limit)` - Find nearby places
- `search_text(query, latitude, longitude, radius_meters, limit)` - Text-based search
- `get_place_details(place_name)` - Get detailed place information
- `search_by_category(category, latitude, longitude, radius_meters, min_rating, max_price_level, limit)` - Category search with filters

## 🎨 Features

### MCP Compliance

All servers follow Model Context Protocol conventions:
- Clear operation definitions
- Type-safe parameters using Pydantic models
- Comprehensive error handling
- Async/await support for scalability

### OpenAI Agents SDK Integration

- Function tools with automatic schema generation
- Type annotations for parameter validation
- Docstrings for tool descriptions
- Compatible with OpenAI and DeepSeek LLMs

### Production-Ready Features

- ✅ Comprehensive unit tests (50+ test cases)
- ✅ Mock data for development and testing
- ✅ Async HTTP sessions with connection pooling
- ✅ Input validation with Pydantic
- ✅ Error handling and graceful degradation
- ✅ Rate limiting support (configurable)
- ✅ Batch operations for efficiency

## 🔌 API Integration

The servers use placeholder/mock data by default. To integrate with real APIs:

### OpenStreetMap (Nominatim) - Free

```python
server = GeocodingServer(
    base_url="https://nominatim.openstreetmap.org"
)
```

### Google Maps API

```python
# Geocoding
server = GeocodingServer(
    api_key="your_google_api_key",
    base_url="https://maps.googleapis.com/maps/api/geocode"
)

# POI
poi_server = POIServer(
    api_key="your_google_api_key"
)
```

### Mapbox

```python
server = RoutingServer(
    api_key="your_mapbox_api_key",
    base_url="https://api.mapbox.com"
)
```

### OSRM (Open Source Routing Machine) - Free

```python
server = RoutingServer(
    base_url="http://router.project-osrm.org"
)
```

## 📊 Project Structure

```
503PC5/
├── README.md                      # This file
├── SUMMARY.md                     # MCP concepts and analysis
├── REFLECTION.md                  # Lessons learned
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── agent.py                       # Main agent integration
├── map_servers/                   # Server implementations
│   ├── __init__.py
│   ├── geocoding_server.py        # Geocoding service
│   ├── routing_server.py          # Routing service
│   └── poi_server.py              # POI service
├── tests/                         # Unit tests
│   ├── __init__.py
│   ├── test_geocoding_server.py
│   ├── test_routing_server.py
│   └── test_poi_server.py
└── examples/                      # Demo scripts
    ├── demo_geocoding.py
    ├── demo_routing.py
    ├── demo_poi.py
    └── demo_full_agent.py
```

## 🎥 Video Demonstration

[Link to screencast video will be here]

The screencast demonstrates:
1. Introduction to the project and MCP concepts
2. Each map server in action with live queries
3. The integrated agent handling complex multi-step tasks
4. Challenges faced and solutions implemented

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is created for educational purposes as part of an assignment on Model Context Protocol and OpenAI Agents SDK.

## 🔗 Resources

- [Model Context Protocol Announcement](https://www.anthropic.com/news/model-context-protocol)
- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [OpenStreetMap Nominatim API](https://nominatim.openstreetmap.org/)
- [OSRM Routing Engine](http://project-osrm.org/)
- [DeepSeek API Documentation](https://platform.deepseek.com/docs)

## ❓ Troubleshooting

### "Module not found" errors

```bash
pip install -r requirements.txt
```

### API rate limiting

The mock implementations avoid this issue. For real APIs, consider:
- Implementing exponential backoff
- Using the `MAX_REQUESTS_PER_MINUTE` environment variable
- Caching frequently accessed data

### Tests failing

```bash
# Ensure you're in the project root
cd /path/to/503PC5

# Run tests with verbose output
pytest -v

# Check for missing dependencies
pip install -r requirements.txt
```

## 👨‍💻 Author

Created by Abedishere for the MCP and OpenAI Agents SDK assignment.

## 🙏 Acknowledgments

- Anthropic for developing the Model Context Protocol
- OpenAI for the Agents SDK
- OpenStreetMap community for free mapping data
- OSRM project for open-source routing
