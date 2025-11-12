# Screencast Script: Map Servers with OpenAI Agents SDK

## Duration: 5-7 minutes

## Outline

### 1. Introduction (30-45 seconds)
- Welcome and project overview
- Introduce MCP and OpenAI Agents SDK
- Show project structure

### 2. MCP Concepts (45-60 seconds)
- Quick explanation of Model Context Protocol
- Why it matters for AI agents
- How our servers follow MCP conventions

### 3. Server Demonstrations (3-4 minutes)

#### Geocoding Server (60 seconds)
```bash
cd 503PC5
python examples/demo_geocoding.py
```
- Show forward geocoding (address → coordinates)
- Show reverse geocoding (coordinates → address)
- Highlight the results

#### Routing Server (60 seconds)
```bash
python examples/demo_routing.py
```
- Calculate a route between two points
- Show different transportation modes
- Display distance and duration

#### POI Server (60 seconds)
```bash
python examples/demo_poi.py
```
- Search for nearby restaurants
- Filter by category
- Show place details with ratings

#### Full Agent (60 seconds)
```bash
python agent.py
```
- Show agent handling natural language queries
- Demonstrate how it routes to appropriate tools
- Show multiple query types

### 4. Code Walkthrough (60-90 seconds)
- Open `map_servers/geocoding_server.py` in editor
- Show Pydantic models for type safety
- Show async operations
- Highlight mock data and API placeholders
- Show how to switch to real APIs

### 5. Testing (30-45 seconds)
```bash
pytest tests/ -v
```
- Run the test suite
- Show comprehensive coverage
- Explain importance of testing

### 6. Challenges and Solutions (45-60 seconds)
- Discuss API compatibility challenge
- Show how abstraction solved it
- Mention async complexity
- Explain DeepSeek compatibility

### 7. Conclusion (30 seconds)
- Recap what was built
- Mention future enhancements
- Thank you

## Key Points to Emphasize

1. **MCP Compliance**: All servers follow MCP conventions with clear operations and parameters
2. **Type Safety**: Pydantic models ensure data validation
3. **Async Operations**: Efficient handling of concurrent requests
4. **Comprehensive Testing**: 50+ test cases covering all functionality
5. **Flexible Integration**: Works with OpenAI, DeepSeek, or other LLM providers
6. **Mock Data**: Enables development and testing without API keys
7. **Production-Ready**: Error handling, validation, and proper resource management

## Commands to Run

```bash
# Setup
cd 503PC5
cat README.md  # Show documentation

# Demos
python examples/demo_geocoding.py
python examples/demo_routing.py
python examples/demo_poi.py
python agent.py

# Tests
pytest tests/ -v

# Show structure
tree -I '__pycache__|*.pyc|.git'
```

## Visual Elements

- Terminal with clear, large font
- VS Code or editor for code walkthrough
- Show project structure
- Highlight key code sections
- Show test output with green checkmarks

## Speaking Points

**Opening**: "Today I'm demonstrating map servers built with the Model Context Protocol and OpenAI Agents SDK. This project implements three MCP-compliant servers for geocoding, routing, and points of interest."

**During Geocoding Demo**: "The geocoding server converts addresses to coordinates and vice versa. Notice how the results include confidence scores and detailed location information."

**During Routing Demo**: "The routing server calculates routes between points. It supports multiple transportation modes—driving, walking, cycling, and transit—each with different distances and times."

**During POI Demo**: "The POI server helps discover places. You can search by category, filter by rating and price, and get detailed information about specific locations."

**During Agent Demo**: "The agent intelligently routes queries to the appropriate tools. When you ask about coordinates, it uses geocoding. For routes, it calls the routing server. It handles natural language and provides conversational responses."

**Code Walkthrough**: "The code uses Pydantic for type safety—notice how coordinates are validated and ratings are constrained to 0-5. All operations are async for performance. The mock data allows testing without API keys, but switching to real APIs is straightforward—just uncomment these lines."

**Testing**: "Comprehensive tests ensure reliability. We have over 50 test cases covering normal operations, edge cases, and error conditions."

**Challenges**: "The main challenge was making the servers work with different API providers. The solution was careful abstraction—the interface remains consistent regardless of whether you're using Google Maps, OpenStreetMap, or Mapbox."

**Closing**: "This project demonstrates building production-ready AI agent tools following MCP conventions. The servers are type-safe, well-tested, and compatible with multiple LLM providers. Future enhancements could include real API integration, visualization, and more sophisticated agent behaviors. Thank you!"

## Tips for Recording

1. **Audio**: Use good microphone, minimize background noise
2. **Video**: Screen resolution 1920x1080, ensure code is readable
3. **Pacing**: Speak clearly, not too fast
4. **Preparation**: Test all commands beforehand
5. **Backup**: Have screenshots ready in case demos fail
6. **Editing**: Cut any long pauses or errors
7. **Captions**: Consider adding subtitles for accessibility

## Post-Production Checklist

- [ ] Trim beginning and end
- [ ] Cut any long waits or errors
- [ ] Add title slide with name and date
- [ ] Add section markers/chapters if platform supports
- [ ] Check audio levels
- [ ] Export in high quality (1080p minimum)
- [ ] Upload to platform (YouTube, Vimeo, etc.)
- [ ] Test playback before submission
