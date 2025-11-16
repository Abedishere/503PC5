# Map Agent Project

A Map Agent that uses custom map servers (OpenRouteService and OpenStreetMap) as tools for a Gemini LLM. The agent can handle various map-related queries through natural language interaction.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file from the template:
```bash
cp .env.example .env
```

Then edit `.env` and add your API keys:
- **ORS_API_KEY**: Get free key at https://openrouteservice.org/dev/#/signup
- **GEMINI_API_KEY**: Get free key at https://makersuite.google.com/app/apikey
- **OSM_COUNTRY_CODES**: Set to 'lb' for Lebanon (or your country code)

### 3. Run the Agent
```bash
jupyter notebook map_agent.ipynb
```

## Features

### Map Operations

1. **Geocoding** - Convert place names to coordinates
   - Example: "Find the coordinates of Bhamdoun, the famous mountain resort town"

2. **Reverse Geocoding** - Convert coordinates to addresses
   - Example: "What place is located at 33.8080, 35.6450? I think it's a historic hotel"

3. **POI Search** - Find points of interest
   - Example: "Find cafes and restaurants in Bhamdoun, the mountain resort town"

4. **Routing** - Get scenic driving directions
   - Example: "Get a scenic route from Beirut to Bhamdoun mountain resort"

5. **Distance** - Calculate distances between locations
   - Example: "What's the driving distance from Beirut to Bhamdoun?"

6. **Nearby POI** - Find nearby points of interest
   - Example: "Find hotels and chalets near Bhamdoun for a weekend getaway"

## Project Structure

```
.
├── part2_implementation/
│   ├── servers/
│   │   ├── ors_server.py          # OpenRouteService API
│   │   └── osm_server.py          # OpenStreetMap API
│   ├── agent_sdk_app.py           # Agent & tool registration
│   └── gemini_provider.py         # Gemini LLM integration
├── reading_exploration/
│   └── mcp_summary.md             # Architecture docs
├── map_agent.ipynb                # Main notebook
├── verify_map_agent.py            # Setup verification
├── requirements.txt               # Dependencies
└── .env                           # API configuration
```

## Usage

### Jupyter Notebook (Recommended)
1. Open `map_agent.ipynb`
2. Run the setup cell
3. Try the test cases
4. Launch the Gradio web interface

### Python Script
```python
import asyncio
import sys
sys.path.insert(0, 'part2_implementation')

from part2_implementation.gemini_provider import run_with_tools
from part2_implementation.agent_sdk_app import TOOLS, agent

async def test():
    response = await run_with_tools(
        "Find hotels and chalets in Bhamdoun for a mountain getaway",
        TOOLS,
        agent
    )
    print(response)

asyncio.run(test())
```

## Example Queries

### Simple Queries
- "Find cafes and restaurants in Bhamdoun mountain resort"
- "What's the distance from Beirut to Bhamdoun?"
- "Find the coordinates of Bhamdoun, Lebanon"

### Complex Queries
- "Find hotels in Bhamdoun and tell me the driving distance from Beirut"
- "Get a scenic route from Beirut to Bhamdoun and tell me about it"

### Multi-step Queries
- "What are the coordinates of Bhamdoun, then find mountain cafes nearby"

## Verification

Run the verification script to check your setup:
```bash
python verify_map_agent.py
```

Expected output when everything is configured:
```
[OK] Environment Configuration: PASSED
[OK] Python Dependencies: PASSED
[OK] Project Structure: PASSED
[OK] Component Imports: PASSED
```

## Technologies

- **OpenStreetMap Nominatim** - Free geocoding service
- **OpenRouteService** - Routing and distance API
- **Google Gemini** - LLM for natural language processing
- **Gradio** - Web UI framework
- **Python asyncio** - Asynchronous operations

## API Documentation

- OpenRouteService: https://openrouteservice.org/dev/#/api-docs
- Nominatim (OSM): https://nominatim.org/release-docs/latest/api/Overview/
- Gemini: https://ai.google.dev/docs

## Additional Documentation

- **QUICK_START.md** - Fast 3-step setup guide
- **MAP_AGENT_README.md** - Detailed documentation
- **MAP_AGENT_PROJECT_SUMMARY.md** - Complete project overview
- **reading_exploration/mcp_summary.md** - Architecture details

## Troubleshooting

**"Module not found" error?**
```bash
pip install -r requirements.txt
```

**Verification fails?**
Run `python verify_map_agent.py` and follow the output instructions.

## License

Educational project for demonstrating map-based LLM agents.
