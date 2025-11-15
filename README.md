# Weather Servers with OpenAI Agents SDK and MCP

MCP-compliant weather services implementation following Model Context Protocol conventions, designed to work with OpenAI Agents SDK and compatible with DeepSeek via OpenRouter. Uses OpenWeather API (Free Tier).

## Overview

This project implements two MCP-compliant weather servers using only **OpenWeather API Free Tier** features:

1. **Weather Forecast Server** - Current weather and 5-day forecasts (3-hour intervals)
2. **Air Quality Server** - Current air quality, pollution data, and forecasts

All servers are integrated into a unified AI agent using DeepSeek model via OpenRouter.

## Architecture

```
weather_servers/
├── forecast_server.py      # Weather forecasts & current conditions
└── air_quality_server.py   # Air quality & pollution data

weather_agent.py            # Main agent with DeepSeek integration
tests/                      # Comprehensive unit tests
```

## Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenWeather API key (free tier)
- OpenRouter API key (for DeepSeek model access)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd 503PC5
   ```

2. **Install dependencies**
   ```bash
   pip install httpx pydantic python-dotenv pytest pytest-asyncio
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running the Agent

```bash
python weather_agent.py
```

## Features Available (OpenWeather Free Tier)

### Weather Forecast Server

- **Current Weather** - Real-time weather conditions
  - Temperature, feels like, humidity
  - Wind speed and direction
  - Pressure, cloudiness, visibility
  - Weather description

- **5-Day Forecast** - 3-hour interval forecasts
  - Up to 40 data points (5 days × 8 intervals/day)
  - Temperature, precipitation probability
  - Weather conditions for each interval

- **Daily Summary** - Aggregated daily forecasts
  - Min/max temperatures per day
  - Average humidity and wind speed
  - Precipitation probability

### Air Quality Server

- **Current Air Quality** - Real-time pollution data
  - Air Quality Index (1-5 scale)
  - PM2.5 and PM10 particulate matter
  - CO, NO, NO2, O3, SO2, NH3 levels
  - Health recommendations

- **Air Quality Forecast** - Future pollution predictions
  - Up to 120 hours forecast
  - AQI trends
  - PM2.5, PM10, O3 predictions

## API Limitations (Free Tier)

- 60 API calls/minute
- 1,000,000 calls/month
- Weather alerts **NOT AVAILABLE** (requires One Call API 3.0 subscription)
- Hourly forecasts limited to 3-hour intervals
- Maximum 5-day forecast range

## Usage Examples

### Weather Forecast Server

```python
from weather_servers.forecast_server import WeatherForecastServer

server = WeatherForecastServer()

# Current weather
weather = await server.get_current_weather(location="London")
print(f"Temperature: {weather.temperature}°C")
print(f"Description: {weather.description}")

# 3-hour interval forecast
forecasts = await server.get_forecast(location="Paris")
for forecast in forecasts[:5]:
    print(f"{forecast.timestamp}: {forecast.temperature}°C")

# Daily summary
daily = await server.get_daily_summary(location="Tokyo")
for day in daily:
    print(f"{day.date.date()}: {day.temp_min}-{day.temp_max}°C")

await server.close()
```

### Air Quality Server

```python
from weather_servers.air_quality_server import AirQualityServer

server = AirQualityServer()

# Current air quality
air_quality = await server.get_current_air_quality(location="Beijing")
print(f"AQI: {air_quality.aqi} ({air_quality.aqi_description})")
print(f"PM2.5: {air_quality.pm2_5} μg/m³")
print(f"Health: {air_quality.health_recommendation}")

# Air quality forecast
forecasts = await server.get_air_quality_forecast(location="Delhi", hours=24)
for forecast in forecasts[:5]:
    print(f"{forecast.timestamp}: AQI {forecast.aqi}")

await server.close()
```

### Using the Agent

```python
from weather_agent import WeatherServicesAgent

agent = WeatherServicesAgent()

# Natural language queries
response = await agent.process_query("What's the weather in London?")
print(response)

response = await agent.process_query("Air quality forecast for Beijing")
print(response)

# Interactive session
await agent.interactive_session()
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=weather_servers

# Run specific test file
pytest tests/test_forecast_server.py -v
```

## Server Operations

### Weather Forecast Server

- `get_current_weather(location OR lat/lon)` - Current weather conditions
- `get_forecast(location OR lat/lon)` - 5-day, 3-hour interval forecast
- `get_daily_summary(location OR lat/lon)` - 5-day daily summary

### Air Quality Server

- `get_current_air_quality(location OR lat/lon)` - Current air quality
- `get_air_quality_forecast(location OR lat/lon, hours)` - AQI forecast
- `get_pollution_history(location OR lat/lon, start, end)` - Historical data

## MCP Compliance

All servers follow Model Context Protocol conventions:

- Clear operation definitions
- Type-safe parameters using Pydantic models
- Comprehensive error handling
- Async/await support for scalability

## DeepSeek Integration

The agent uses DeepSeek model via OpenRouter:

```python
# Configuration in .env
OPENROUTER_API_KEY=your_key_here
LLM_MODEL=deepseek/deepseek-r1t2-chimera:free
```

## Project Structure

```
503PC5/
├── README.md                      # This file
├── .env                           # API keys (not in git)
├── .env.example                   # Environment template
├── weather_agent.py               # Main agent with DeepSeek
├── weather_servers/               # Server implementations
│   ├── __init__.py
│   ├── forecast_server.py         # Weather forecasts
│   └── air_quality_server.py      # Air quality data
├── tests/                         # Unit tests
│   ├── test_forecast_server.py
│   └── test_air_quality_server.py
└── requirements.txt               # Python dependencies
```

## Dependencies

```
httpx>=0.24.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

## Troubleshooting

### API Key Issues

Ensure your `.env` file contains valid keys:
```bash
OPENWEATHER_API_KEY=your_actual_key
OPENROUTER_API_KEY=your_actual_key
```

### Rate Limiting

Free tier allows 60 calls/minute. If you hit limits:
- Add delays between requests
- Cache frequently accessed data
- Use batch operations where possible

### Location Not Found

Make sure location names are properly formatted:
- Good: "London", "New York,US", "Tokyo,JP"
- Bad: "london", "NYC" (may not work)

## What's NOT Available (Free Tier)

- Weather alerts and warnings (requires paid subscription)
- True hourly forecasts (only 3-hour intervals)
- More than 5 days of forecast
- UV index data (deprecated)
- Historical weather data (requires paid subscription)

## Resources

- [OpenWeather API Documentation](https://openweathermap.org/api)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [DeepSeek Model](https://www.deepseek.com/)

## License

Created for educational purposes as part of an MCP and OpenAI Agents SDK assignment.
