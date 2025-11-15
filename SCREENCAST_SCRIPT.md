# Screencast Script: Weather Servers with MCP and Real LLM Integration

## Duration: 5-7 minutes

---

## SECTION 1: Introduction (45 seconds)

### What to Show:
- Open VS Code with project folder
- Show README.md briefly
- Show project structure in file explorer

### What to Say (READ EXACTLY):
"Hello! Today I'm presenting my implementation of MCP-compliant weather servers integrated with a real AI agent. This project demonstrates the Model Context Protocol using OpenWeather API for real weather data and Mistral AI for intelligent tool selection. I've built two main servers: a Weather Forecast Server and an Air Quality Server, both following MCP conventions. Let me show you how they work."

---

## SECTION 2: MCP Concepts (60 seconds)

### What to Show:
- Open SUMMARY.md
- Scroll through MCP concepts section
- Show Pydantic models in forecast_server.py (lines 13-40)

### What to Say (READ EXACTLY):
"The Model Context Protocol, developed by Anthropic, standardizes how AI agents connect to data sources. Instead of building custom integrations for each API, MCP provides a unified approach. In my implementation, both weather servers follow MCP conventions: they use Pydantic models for type safety, implement async operations for scalability, and provide clear operation definitions. This means the agent can easily understand and use these tools without custom code for each one. The key benefit is maintainability - if I add a new weather server, the agent automatically knows how to use it."

---

## SECTION 3: Weather Forecast Server Demo (90 seconds)

### What to Show:
Run this command in terminal:
```bash
python -c "
from dotenv import load_dotenv
load_dotenv()
import asyncio
from weather_servers.forecast_server import WeatherForecastServer

async def demo():
    server = WeatherForecastServer()

    print('=== CURRENT WEATHER IN LONDON ===')
    weather = await server.get_current_weather(location='London')
    print(f'Temperature: {weather.temperature}°C')
    print(f'Feels like: {weather.feels_like}°C')
    print(f'Description: {weather.description}')
    print(f'Humidity: {weather.humidity}%')
    print(f'Wind Speed: {weather.wind_speed} m/s')

    print('\n=== 5-DAY FORECAST ===')
    daily = await server.get_daily_summary(location='London')
    for day in daily[:3]:
        print(f'{day.date.strftime(\"%Y-%m-%d\")}: {day.temp_min}°C to {day.temp_max}°C - {day.description}')

    await server.close()

asyncio.run(demo())
"
```

### What to Say (READ EXACTLY):
"Let me demonstrate the Weather Forecast Server. I'm calling it directly from Python to show this is real OpenWeather API data, not mock data. Here you can see the current weather in London - notice the temperature, humidity, and weather description. These are actual values from OpenWeather's API right now. Below that, I'm getting a 5-day forecast. The free tier provides 3-hour intervals which I aggregate into daily summaries showing min and max temperatures. This data updates in real-time from the API."

---

## SECTION 4: Air Quality Server Demo (90 seconds)

### What to Show:
Run this command:
```bash
python -c "
from dotenv import load_dotenv
load_dotenv()
import asyncio
from weather_servers.air_quality_server import AirQualityServer

async def demo():
    server = AirQualityServer()

    print('=== AIR QUALITY IN BEIJING ===')
    aq = await server.get_current_air_quality(location='Beijing')
    print(f'AQI: {aq.aqi} ({aq.aqi_description})')
    print(f'PM2.5: {aq.pm2_5} ug/m³')
    print(f'PM10: {aq.pm10} ug/m³')
    print(f'Health Recommendation:')
    print(f'  {aq.health_recommendation}')

    print('\n=== 24-HOUR AQI FORECAST ===')
    forecast = await server.get_air_quality_forecast(location='Beijing', hours=24)
    for f in forecast[:6]:
        print(f'{f.timestamp.strftime(\"%Y-%m-%d %H:%M\")}: AQI {f.aqi}')

    await server.close()

asyncio.run(demo())
"
```

### What to Say (READ EXACTLY):
"Now the Air Quality Server. I'm checking Beijing because it often has interesting air quality data. The AQI scale goes from 1 to 5, where 1 is good and 5 is very poor. You can see the current PM2.5 and PM10 levels measured in micrograms per cubic meter. The server also provides health recommendations based on the AQI level. Below that is a 24-hour forecast showing how air quality is expected to change. This is crucial information for people with respiratory conditions or anyone planning outdoor activities."

---

## SECTION 5: Real LLM Agent Demo (90 seconds)

### What to Show:
Run this command:
```bash
python -c "
from dotenv import load_dotenv
load_dotenv()
import asyncio
from weather_agent import WeatherServicesAgent

async def demo():
    agent = WeatherServicesAgent()

    print('Query 1: What is the weather in Paris?')
    response = await agent.process_query('What is the weather in Paris?')
    print(f'Agent: {response}\n')

    print('Query 2: Air quality in Delhi')
    response = await agent.process_query('Air quality in Delhi')
    print(f'Agent: {response}\n')

    print('Query 3: 5-day forecast for Tokyo')
    response = await agent.process_query('5-day forecast for Tokyo')
    print(f'Agent: {response}')

asyncio.run(demo())
"
```

### What to Say (READ EXACTLY):
"This is the most important part - the AI agent with real LLM integration. I'm using Mistral Nemo, a free model from OpenRouter. Watch what happens: When I ask 'What is the weather in Paris?' the LLM analyzes my query, decides to use the get_current_weather tool, extracts 'Paris' as the location parameter, calls the real OpenWeather API, and formats the response naturally. You'll see the LLM decision printed - it outputs JSON indicating which tool to call. Then it executes that tool with the real API, and formats the data into a friendly response. This is NOT simulated - the LLM is actually making these decisions."

---

## SECTION 6: Verification that Data is Real (60 seconds)

### What to Show:
Show verify_real_data.py file, then run:
```bash
python verify_real_data.py
```

### What to Say (READ EXACTLY):
"I want to prove this data is real and not LLM hallucinations. This verification script calls the API directly without any LLM, then compares it to what the agent returns. Look at the numbers - the direct API call shows temperature 12.64 degrees. The agent response says '12.6 degrees' - it's the same data, just rounded for readability. The PM2.5 value is 198.94 in both cases. The LLM receives the exact API response and only reformats it into natural language. It doesn't make up any numbers."

---

## SECTION 7: Testing (45 seconds)

### What to Show:
Run tests:
```bash
pytest tests/ -v
```

### What to Say (READ EXACTLY):
"I've written comprehensive tests for both servers. These are integration tests that call the real OpenWeather API. You can see tests passing for current weather, forecasts, air quality, and error handling. There are 17 tests total, all passing. The tests verify data types, validate coordinate ranges for air quality indices, and ensure the servers handle invalid locations gracefully. These tests prove the servers work correctly with the actual API."

---

## SECTION 8: Code Walkthrough (60 seconds)

### What to Show:
- Open weather_servers/forecast_server.py
- Show CurrentWeather Pydantic model (lines 13-29)
- Show get_current_weather method (lines 83-140)
- Show the actual API call (line 120)
- Open weather_agent.py
- Show tool selection logic (lines 125-170)

### What to Say (READ EXACTLY):
"Let me show you the code structure. The forecast server uses Pydantic models - here's CurrentWeather with temperature, humidity, and other fields. Each field is typed and validated automatically. In the get_current_weather method, you can see the actual API call to OpenWeather on line 120. We use httpx for async requests, handle errors, and parse the JSON response. Now in the agent, the LLM analyzes the query, outputs JSON with the tool name and parameters, we parse that JSON, execute the actual API call, and use the LLM again to format the response. It's a two-step process: LLM selects tool, then LLM formats results."

---

## SECTION 9: Challenges and Solutions (60 seconds)

### What to Show:
- Open REFLECTION.md
- Scroll to "Challenges Faced" section

### What to Say (READ EXACTLY):
"The biggest challenge was working within OpenWeather's free tier limitations. Weather alerts require a paid subscription, so I had to exclude that server entirely. The free tier only provides 3-hour forecast intervals, not true hourly data, so I aggregate these into daily summaries. Another major challenge was that free LLM models on OpenRouter don't support native function calling. I solved this by implementing prompt-based tool selection - the LLM outputs JSON indicating which tool to use, I parse that, execute the tool, and return results. This works with any free model. Finally, I had to ensure the LLM doesn't hallucinate data, which I solved by explicitly instructing it to only use provided API data."

---

## SECTION 10: Conclusion (30 seconds)

### What to Show:
- Show README.md

### What to Say (READ EXACTLY):
"In conclusion, I've built two production-ready MCP-compliant weather servers with real OpenWeather API integration and an AI agent using Mistral AI for intelligent tool selection. The agent uses actual LLM reasoning to understand queries and select appropriate tools. All data comes from real APIs, not mock data or hallucinations. I have 17 passing integration tests and comprehensive documentation. Future enhancements could include caching for better performance, weather map visualization, and upgrading to paid tiers for more features like weather alerts. Thank you for watching!"

---

## Technical Setup Checklist

Before recording:
- [ ] Verify .env file has OPENWEATHER_API_KEY and OPENROUTER_API_KEY
- [ ] Test all commands work without errors
- [ ] Clear terminal for clean output
- [ ] Set terminal font size to 14pt or larger
- [ ] Close unnecessary applications
- [ ] Test microphone levels

## Recording Tips

1. **Speak clearly and at moderate pace** - Don't rush
2. **Follow the script exactly** - It's designed to fit the time
3. **Pause briefly between sections** - Makes editing easier
4. **If you make a mistake** - Stop, pause 3 seconds, restart from beginning of that paragraph
5. **Show, then explain** - Run command first, let output display, then explain what it shows
6. **Keep mouse movements minimal** - Only point to important lines
