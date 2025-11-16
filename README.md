# Weather Services Agent with LLM Integration

MCP-compliant weather services implementation with real LLM integration via OpenRouter. Features natural language interaction using free LLM models (Qwen 2.5 7B) and OpenWeather API (Free Tier).

## Overview

This project implements two MCP-compliant weather servers integrated with an intelligent agent that uses real LLMs for natural language understanding and tool selection:

1. **Weather Forecast Server** - Current weather and 5-day forecasts (3-hour intervals)
2. **Air Quality Server** - Current air quality, pollution data, and forecasts
3. **Weather Services Agent** - LLM-powered agent with prompt-based tool calling

The agent uses **OpenRouter** for accessing free LLM models (default: Qwen 2.5 7B Instruct) and implements intelligent tool selection through prompt engineering rather than native function calling.

## Architecture

```
weather_servers/
├── __init__.py
├── forecast_server.py      # Weather forecasts & current conditions
└── air_quality_server.py   # Air quality & pollution data

weather_agent.py            # Main agent with LLM integration
tests/                      # Unit tests for both servers
├── test_forecast_server.py
└── test_air_quality_server.py
```

## Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenWeather API key (free tier from https://openweathermap.org/api)
- OpenRouter API key (free tier from https://openrouter.ai/)

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

   Or install manually:
   ```bash
   pip install openai httpx pydantic python-dotenv pytest pytest-asyncio
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:
   ```bash
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   LLM_BASE_URL=https://openrouter.ai/api/v1
   LLM_MODEL=qwen/qwen-2.5-7b-instruct:free
   ```

### Running the Agent

```bash
python weather_agent.py
```

This will:
1. Run example queries demonstrating LLM-powered tool selection
2. Start an interactive session where you can ask natural language questions

## Features

### Weather Forecast Server

Available tools (accessible via direct function calls or through the agent):

- **`get_current_weather(location)`** - Current weather conditions
  - Temperature, feels like, humidity
  - Wind speed and direction
  - Pressure, cloudiness, visibility
  - Weather description

- **`get_forecast(location)`** - 5-day forecast (3-hour intervals)
  - Up to 40 data points (5 days × 8 intervals/day)
  - Temperature, precipitation probability
  - Weather conditions for each interval

- **`get_daily_summary(location)`** - 5-day daily summary
  - Min/max temperatures per day
  - Average humidity and wind speed
  - Precipitation probability

### Air Quality Server

Available tools:

- **`get_air_quality(location)`** - Current air quality
  - Air Quality Index (1-5 scale)
  - PM2.5 and PM10 particulate matter
  - CO, NO, NO2, O3, SO2, NH3 levels
  - Health recommendations

- **`get_pollution_forecast(location, hours=24)`** - Air quality forecast
  - Up to 120 hours forecast
  - AQI trends
  - PM2.5, PM10, O3 predictions

### LLM Agent Integration

The `WeatherServicesAgent` provides:

- **Natural Language Understanding** - Parses user queries using LLM
- **Intelligent Tool Selection** - Automatically selects appropriate weather tools
- **Prompt-Based Tool Calling** - Uses JSON-based tool selection (works with any LLM)
- **Natural Response Generation** - Formats API data into friendly responses
- **Interactive Session** - Chat-based interface for weather queries

## Usage Examples

### Using the Agent (Recommended)

```python
from weather_agent import WeatherServicesAgent
import asyncio

async def main():
    agent = WeatherServicesAgent()

    # Natural language queries - the LLM handles tool selection
    response = await agent.process_query("What's the weather in London?")
    print(response)

    response = await agent.process_query("Show me air quality in Beijing")
    print(response)

    response = await agent.process_query("Give me a 5-day forecast for Paris")
    print(response)

    # Interactive session
    await agent.interactive_session()

asyncio.run(main())
```

### Direct Server Usage

```python
from weather_servers.forecast_server import get_current_weather, get_forecast, get_daily_summary
from weather_servers.air_quality_server import get_air_quality, get_pollution_forecast
import asyncio

async def main():
    # Current weather
    weather = await get_current_weather(location="London")
    print(f"Temperature: {weather['temperature']}°C")
    print(f"Description: {weather['description']}")

    # 5-day forecast
    forecasts = await get_forecast(location="Paris")
    for forecast in forecasts[:5]:
        print(f"{forecast['timestamp']}: {forecast['temperature']}°C")

    # Daily summary
    daily = await get_daily_summary(location="Tokyo")
    for day in daily:
        print(f"{day['date']}: {day['temp_min']}-{day['temp_max']}°C")

    # Current air quality
    air_quality = await get_air_quality(location="Beijing")
    print(f"AQI: {air_quality['aqi']}")
    print(f"PM2.5: {air_quality['pm2_5']} μg/m³")

    # Air quality forecast
    aq_forecast = await get_pollution_forecast(location="Delhi", hours=24)
    for forecast in aq_forecast[:5]:
        print(f"{forecast['timestamp']}: AQI {forecast['aqi']}")

asyncio.run(main())
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_forecast_server.py -v

# Run with coverage
pytest --cov=weather_servers
```

## How the LLM Integration Works

The agent uses a **prompt-based approach** for tool calling that works with any LLM:

1. **Tool Selection Phase**:
   - User query is sent to LLM with system prompt describing available tools
   - LLM returns JSON object specifying which tool to use and parameters
   - Example: `{"tool": "get_current_weather", "parameters": {"location": "London"}}`

2. **Tool Execution Phase**:
   - Agent parses JSON response and extracts tool name and parameters
   - Executes the selected tool function with provided parameters
   - Retrieves data from OpenWeather API

3. **Response Formatting Phase**:
   - Raw API data is sent back to LLM with formatting instructions
   - LLM generates natural, conversational response
   - User receives friendly, informative answer

This approach:
- Works with free models on OpenRouter (no native function calling required)
- Provides robust tool selection through prompt engineering
- Handles JSON extraction from various LLM response formats
- Generates natural language responses from structured data

## API Limitations (OpenWeather Free Tier)

- 60 API calls/minute
- 1,000,000 calls/month
- Weather alerts **NOT AVAILABLE** (requires One Call API 3.0 subscription)
- Hourly forecasts limited to 3-hour intervals
- Maximum 5-day forecast range

## MCP Compliance

All servers follow Model Context Protocol conventions:

- Clear operation definitions with documented parameters
- Type-safe parameters using Pydantic models for validation
- Comprehensive error handling with meaningful messages
- Async/await support for scalability and performance
- Standardized response formats

## LLM Configuration

The agent uses OpenRouter to access free LLM models. Configuration in `.env`:

```bash
OPENROUTER_API_KEY=your_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=qwen/qwen-2.5-7b-instruct:free
```

**Supported free models on OpenRouter**:
- `qwen/qwen-2.5-7b-instruct:free` (default, recommended)
- `meta-llama/llama-3.2-3b-instruct:free`
- `google/gemma-2-9b-it:free`

The prompt-based approach works with any model, including paid models for better performance.

## Project Structure

```
503PC5/
├── README.md                      # This file
├── .env                           # API keys (not in git)
├── .gitignore                     # Git ignore rules
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
├── weather_agent.py               # Main agent with LLM integration
├── weather_servers/               # MCP server implementations
│   ├── __init__.py
│   ├── forecast_server.py         # Weather forecasts
│   └── air_quality_server.py      # Air quality data
├── tests/                         # Unit tests
│   ├── test_forecast_server.py    # Forecast server tests
│   └── test_air_quality_server.py # Air quality server tests
├── ASSIGNMENT_CHECKLIST.md        # Assignment requirements
├── REFLECTION.md                  # Implementation reflection
├── SUMMARY.md                     # Project summary
└── SCREENCAST_SCRIPT.md           # Demo script
```

## Dependencies

```
openai>=2.0.0          # OpenAI SDK for LLM API calls
httpx>=0.24.0          # HTTP client for weather APIs
pydantic>=2.0.0        # Data validation
python-dotenv>=1.0.0   # Environment variable management
pytest>=7.0.0          # Testing framework
pytest-asyncio>=0.21.0 # Async test support
```

## Troubleshooting

### API Key Issues

Ensure your `.env` file contains valid keys:
```bash
OPENWEATHER_API_KEY=your_actual_key
OPENROUTER_API_KEY=your_actual_key
```

Test your keys:
- OpenWeather: https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY
- OpenRouter: Check dashboard at https://openrouter.ai/

### Rate Limiting

Free tier allows 60 calls/minute. If you hit limits:
- Add delays between requests using `asyncio.sleep()`
- Cache frequently accessed data
- Reduce number of example queries

### Location Not Found

Make sure location names are properly formatted:
- Good: "London", "New York,US", "Tokyo,JP", "Paris,FR"
- Bad: "london" (case shouldn't matter but try capitalized), "NYC" (use full name)

### LLM Response Parsing Errors

If the agent fails to parse LLM responses:
- Try a different model (some are more consistent with JSON formatting)
- Check OpenRouter service status
- Verify OPENROUTER_API_KEY is valid

## What's NOT Available (Free Tier)

**OpenWeather API limitations**:
- Weather alerts and warnings (requires paid subscription)
- True hourly forecasts (only 3-hour intervals available)
- More than 5 days of forecast
- UV index data (deprecated by OpenWeather)
- Historical weather data (requires paid subscription)

**LLM limitations**:
- Free models may have rate limits or daily quotas
- Response quality varies by model
- No guaranteed uptime for free tier

## Resources

- [OpenWeather API Documentation](https://openweathermap.org/api)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [OpenAI SDK Documentation](https://platform.openai.com/docs/api-reference)

## License

Created for educational purposes as part of an MCP and LLM integration assignment.
