# Screencast Presentation Script
## Building Map Servers with OpenAI Agents SDK (Using Gemini)

**Duration: 5-7 minutes**

---

## Introduction (0:00 - 0:45)

**[Show title slide or project folder]**

"Hello! Today I'm presenting my Map Agent project for the Map Servers assignment. I've built a custom map agent system that integrates two map service providers - OpenStreetMap and OpenRouteService - with Google's Gemini LLM using concepts inspired by the OpenAI Agents SDK."

**[Open browser to Hugging Face MCP article]**

"Before diving into my implementation, let me briefly discuss the Model Context Protocol that inspired this architecture."

---

## Part 1: MCP Concepts Overview (0:45 - 2:00)

**[Show reading_exploration/mcp_summary.md or highlight key points]**

### Key MCP Concepts:

1. **Protocol-based Communication**
   "The Model Context Protocol establishes a standardized way for LLMs to interact with external tools and services. Instead of hardcoding integrations, MCP defines a clean interface between the model and its context providers."

2. **Server Architecture**
   "In MCP, servers expose specific capabilities through well-defined tool interfaces. Each server handles a domain - in my case, geocoding and routing services."

3. **Tool Registration**
   "Tools are registered with type hints and docstrings, allowing the LLM to understand what each tool does and when to use it. This is key for automatic function calling."

**[Transition to code]**

"With these concepts in mind, let me show you how I implemented two custom map servers."

---

## Part 2: Implementation Overview (2:00 - 3:30)

**[Open VS Code or editor with project structure visible]**

### Server 1: OpenStreetMap Server (OSMServer)

**[Show part2_implementation/servers/osm_server.py]**

"My first server uses the OpenStreetMap Nominatim API. It implements three operations:"

1. **Geocoding** - Converts place names to coordinates
   ```python
   def geocode(self, place: str) -> Dict[str, Any]:
       """Convert a place name to geographic coordinates."""
   ```

2. **Reverse Geocoding** - Converts coordinates to addresses
   ```python
   def reverse(self, lat: float, lon: float) -> Dict[str, Any]:
       """Convert coordinates to a human-readable address."""
   ```

3. **POI Search** - Finds points of interest
   ```python
   def search_poi(self, query: str, city: str = None) -> Dict[str, Any]:
       """Find points of interest based on keyword."""
   ```

"Notice the type hints and docstrings - these are crucial for the LLM to understand how to use each tool."

### Server 2: OpenRouteService Server (ORSServer)

**[Show part2_implementation/servers/ors_server.py]**

"My second server uses OpenRouteService for routing operations:"

1. **Route** - Get driving directions
2. **Distance** - Calculate distances
3. **Nearby** - Find nearby POIs

**[Show agent_sdk_app.py]**

"Both servers are registered as tools in agent_sdk_app.py, creating a unified TOOLS list that Gemini can access."

---

## Part 3: Live Demonstration (3:30 - 6:00)

**[Open Jupyter notebook: map_agent.ipynb]**

"Now let's see the agent in action with real queries focused on Bhamdoun, a beautiful mountain resort town in Lebanon."

### Demo 1: Geocoding
**[Run cell 5]**

"First, let's find the coordinates of Bhamdoun:"
- Query: "Find the coordinates of Bhamdoun, Lebanon - the famous mountain resort town"
- **[Show response]** "The agent correctly identifies this needs the geocode tool and returns the coordinates."

### Demo 2: POI Search
**[Run cell 9]**

"Next, let's find cafes and restaurants in this mountain town:"
- Query: "Find cafes and restaurants in Bhamdoun, the mountain resort town"
- **[Show response]** "The agent uses the search_poi tool and returns relevant results."

### Demo 3: Distance Calculation
**[Run cell 13]**

"Now let's calculate the distance from Beirut to Bhamdoun:"
- Query: "What's the driving distance from Beirut to Bhamdoun mountain resort?"
- **[Show response]** "The agent first geocodes both locations, then uses the distance tool to calculate the route distance."

### Demo 4: Complex Multi-step Query
**[Run cell 15 or type custom query]**

"Finally, let's try a more complex query that requires multiple tools:"
- Query: "Find hotels and chalets near Bhamdoun for a weekend getaway"
- **[Show response]** "The agent automatically orchestrates multiple API calls and synthesizes a helpful response."

**[Optional: Show Gradio interface]**

"I've also created a web interface using Gradio for interactive testing."
- **[Launch Gradio]** "Users can ask questions in natural language and get immediate responses."

---

## Part 4: Testing & Verification (6:00 - 6:30)

**[Show terminal or VS Code terminal]**

### Unit Tests
```bash
pytest test_map_agent.py -v
```

**[Show test output]**

"All four test cases pass:
- test_geocode: Bhamdoun geocoding ✅
- test_reverse: Reverse geocoding ✅
- test_poi: POI search ✅
- test_distance: Distance calculation ✅"

### Verification Script
```bash
python verify_map_agent.py
```

**[Show verification output]**

"The verification script confirms:
- Environment configuration ✅
- Dependencies installed ✅
- Project structure correct ✅
- All components import successfully ✅"

---

## Conclusion (6:30 - 7:00)

**[Return to code or slides]**

### Summary

"To summarize what I've built:

1. **Two custom map servers** following MCP-inspired patterns:
   - OSMServer for geocoding and POI searches
   - ORSServer for routing and distance calculations

2. **Six distinct operations** across both servers, all accessible through natural language

3. **Integration with Gemini LLM** using automatic function calling

4. **Complete testing suite** with pytest and verification scripts

5. **User-friendly interfaces** - both Jupyter notebook and Gradio web app"

### Key Achievements

✅ Implemented MCP-style server architecture
✅ Created tools with proper type hints and documentation
✅ Integrated with Gemini LLM (OpenAI Agents SDK alternative)
✅ Built comprehensive test suite
✅ Demonstrated real-world use cases with Bhamdoun, Lebanon

"The project is fully functional and ready for real-world map queries. Thank you for watching!"

---

## Technical Notes for Recording

### Before Recording:
1. ✅ Restart Jupyter kernel to clear cache
2. ✅ Close unnecessary applications
3. ✅ Set browser zoom to comfortable level
4. ✅ Have all files open in tabs
5. ✅ Test queries beforehand to know expected results

### During Recording:
- Speak clearly and at moderate pace
- Show code briefly but don't dwell too long
- Focus on demonstrating functionality
- Keep within 5-7 minute timeframe
- Highlight the Bhamdoun mountain resort theme

### Camera/Audio:
- Use good microphone
- Minimize background noise
- Screen resolution: 1920x1080 recommended
- Use screen recording software (OBS, QuickTime, etc.)

---

## Quick Demo Checklist

- [ ] MCP concepts explained
- [ ] Both servers shown (OSMServer & ORSServer)
- [ ] At least 3 operations demonstrated live
- [ ] Multi-step query shown
- [ ] Tests run successfully
- [ ] Project structure explained
- [ ] Real API integration shown (not mocked)
- [ ] Natural language interface highlighted
