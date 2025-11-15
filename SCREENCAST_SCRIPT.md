# Screencast Script: Weather Servers with OpenAI Agents SDK

## Duration: 5-7 minutes

## Outline

### 1. Introduction (30-45 seconds)
- Welcome and project overview
- Introduce MCP and OpenAI Agents SDK
- Show project structure
- Mention using OpenWeather API and DeepSeek model

### 2. MCP Concepts (45-60 seconds)
- Quick explanation of Model Context Protocol
- Why it matters for AI agents
- How our weather servers follow MCP conventions
- Benefits of standardized protocols for weather data

### 3. Server Demonstrations (3-4 minutes)

#### Weather Forecast Server (90 seconds)
```bash
cd 503PC5
python -c "
import asyncio
from weather_servers.forecast_server import WeatherForecastServer

async def demo():
    server = WeatherForecastServer()

    # Current weather
    print('=== Current Weather in London ===')
    weather = await server.get_current_weather(location='London')
    print(f'Temperature: {weather.temperature}°C')
    print(f'Feels like: {weather.feels_like}°C')
    print(f'Description: {weather.description}')
    print(f'Humidity: {weather.humidity}%')

    # 5-day forecast
    print('\n=== 5-Day Forecast (3-hour intervals) ===')
    forecasts = await server.get_forecast(location='London')
    for f in forecasts[:8]:  # Show first day
        print(f'{f.timestamp}: {f.temperature}°C - {f.description}')

    await server.close()

asyncio.run(demo())
"
```
- Show current weather with real data
- Show 3-hour interval forecast
- Highlight temperature, precipitation probability

#### Air Quality Server (90 seconds)
```bash
python -c "
import asyncio
from weather_servers.air_quality_server import AirQualityServer

async def demo():
    server = AirQualityServer()

    # Current air quality
    print('=== Current Air Quality in Beijing ===')
    aq = await server.get_current_air_quality(location='Beijing')
    print(f'AQI: {aq.aqi} ({aq.aqi_description})')
    print(f'PM2.5: {aq.pm2_5} μg/m³')
    print(f'PM10: {aq.pm10} μg/m³')
    print(f'Health: {aq.health_recommendation}')

    # Forecast
    print('\n=== 24-Hour Air Quality Forecast ===')
    forecasts = await server.get_air_quality_forecast(location='Beijing', hours=24)
    for f in forecasts[:6]:
        print(f'{f.timestamp}: AQI {f.aqi}')

    await server.close()

asyncio.run(demo())
"
```
- Show air quality data with health recommendations
- Show AQI forecast
- Highlight particulate matter levels

#### Full Agent Demo (90 seconds)
```bash
python weather_agent.py
```
- Show agent handling natural language queries
- Demonstrate how it routes to weather or air quality tools
- Show multiple query types (current, forecast, air quality)

### 4. Code Walkthrough (60-90 seconds)
- Open `weather_servers/forecast_server.py` in editor
- Show Pydantic models for type safety (CurrentWeather, HourlyForecast)
- Show async API calls to OpenWeather
- Highlight error handling for invalid locations
- Show function tools for OpenAI Agents SDK integration

### 5. Testing (30-45 seconds)
```bash
pytest tests/ -v
```
- Run the test suite
- Show tests for both servers
- Explain testing with real API calls

### 6. Challenges and Solutions (45-60 seconds)
- **API Tier Limitations**: Weather alerts not available in free tier, had to design around this constraint
- **3-Hour Intervals**: Free tier only provides 3-hour forecasts, not true hourly
- **Model Integration**: Using DeepSeek via OpenRouter instead of direct OpenAI
- **Async Complexity**: Managing async sessions and proper resource cleanup
- **Geocoding**: Converting location names to coordinates for API calls

### 7. Conclusion (30 seconds)
- Recap: Built 2 MCP-compliant weather servers with real API integration
- Uses OpenWeather free tier and DeepSeek model
- Production-ready with comprehensive tests
- Thank you

## Key Points to Emphasize

1. **MCP Compliance**: All servers follow MCP conventions with clear operations and parameters
2. **Real API Integration**: Using actual OpenWeather API, not mock data
3. **Type Safety**: Pydantic models ensure data validation (AQI 1-5, coordinates validation)
4. **Async Operations**: Efficient handling of API requests
5. **Free Tier Design**: Worked within OpenWeather free tier limitations
6. **DeepSeek Integration**: Using DeepSeek model via OpenRouter for LLM capabilities
7. **Comprehensive Testing**: Tests verify real API functionality
8. **Health Recommendations**: Air quality server provides actionable health advice

## Commands to Run

```bash
# Setup
cd 503PC5
cat README.md  # Show documentation
cat .env  # Show API keys configured

# Test individual servers
python -c "import asyncio; from weather_servers.forecast_server import get_current_weather; print(asyncio.run(get_current_weather(location='London')))"

python -c "import asyncio; from weather_servers.air_quality_server import get_air_quality; print(asyncio.run(get_air_quality(location='Beijing')))"

# Run agent
python weather_agent.py

# Tests
pytest tests/ -v

# Show structure
ls -R weather_servers/
ls tests/
```

## Visual Elements

- Terminal with clear, large font
- VS Code for code walkthrough
- Show project structure
- Highlight API responses with real data
- Show test output with green checkmarks
- Display .env file with API keys (for demo purposes)

## Speaking Points

**Opening**: "Today I'm demonstrating weather servers built with the Model Context Protocol and OpenAI Agents SDK. This project implements two MCP-compliant servers for weather forecasts and air quality monitoring, using the OpenWeather API and Minstral via OpenRouter."

**During Weather Demo**: "The weather forecast server provides real-time weather conditions and 5-day forecasts. Notice the actual temperature and weather description coming from OpenWeather's API. The forecasts are in 3-hour intervals, which is what the free tier provides."

**During Air Quality Demo**: "The air quality server delivers real pollution data including AQI, PM2.5, and other pollutants. It provides health recommendations based on the AQI level—notice how it warns about health effects when pollution is high. This is real data for Beijing, which often has air quality concerns."

**During Agent Demo**: "The agent uses Minstral model to understand natural language and route queries to the appropriate server. Ask about weather, it calls the forecast server. Ask about air quality, it uses the air quality server. The integration is seamless."

**Testing**: "Tests verify the servers work with the actual OpenWeather API. We test current weather, forecasts, air quality, and error handling for invalid locations."

**Challenges**: "The main challenge was working within free tier limitations. Weather alerts require a paid subscription, so we excluded them. We only get 3-hour forecast intervals, not true hourly data. The solution was designing servers that provide maximum value within those constraints. Integration with DeepSeek via OpenRouter required configuring the base URL and model correctly."

**Closing**: "This project demonstrates building production-ready weather servers following MCP conventions with real API integration. The servers use OpenWeather's free tier and integrate with DeepSeek for intelligent query routing. It's type-safe, well-tested, and ready for real-world use. Future enhancements could include caching, weather map visualization, and integration with calendar apps. Thank you!"

## Tips for Recording

1. **Audio**: Use good microphone, minimize background noise
2. **Video**: Screen resolution 1920x1080, ensure code is readable
3. **Pacing**: Speak clearly, not too fast
4. **Preparation**: Test all commands beforehand, ensure API keys work
5. **Backup**: Have screenshots ready in case API is down
6. **Editing**: Cut any API wait times or errors
7. **Captions**: Consider adding subtitles for accessibility

## API Considerations

- Ensure OpenWeather API key has remaining quota
- Test API calls before recording
- Have backup data/screenshots if API fails
- Note that API responses may vary based on current weather
- Air quality data may be unavailable for some locations

## Post-Production Checklist

- [ ] Trim beginning and end
- [ ] Cut any long API waits or errors
- [ ] Add title slide with name and date
- [ ] Add section markers for each server demo
- [ ] Check audio levels
- [ ] Blur API keys if showing .env file
- [ ] Export in high quality (1080p minimum)
- [ ] Upload to platform (YouTube, Vimeo, etc.)
- [ ] Test playback before submission
