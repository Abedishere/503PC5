"""
Weather Services Agent - Real LLM Integration
Integrates weather forecast and air quality servers following MCP conventions
Uses free LLM models via OpenRouter with prompt-based tool selection
"""

import os
import asyncio
import json
import re
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class WeatherServicesAgent:
    """
    Agent that integrates all weather services using real LLM with prompt-based tool calling
    Works with free models on OpenRouter
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize the Weather Services Agent

        Args:
            api_key: API key for LLM provider (OpenRouter)
            base_url: Base URL for API (OpenRouter)
            model: Model to use (free models via OpenRouter)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = model or os.getenv("LLM_MODEL", "qwen/qwen-2.5-7b-instruct:free")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is required")

        # Initialize OpenAI client with OpenRouter
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        # Import weather server functions
        from weather_servers.forecast_server import (
            get_current_weather,
            get_forecast,
            get_daily_summary
        )
        from weather_servers.air_quality_server import (
            get_air_quality,
            get_pollution_forecast
        )

        # Store function references
        self.tool_functions = {
            "get_current_weather": get_current_weather,
            "get_forecast": get_forecast,
            "get_daily_summary": get_daily_summary,
            "get_air_quality": get_air_quality,
            "get_pollution_forecast": get_pollution_forecast
        }

        print(f"Weather Services Agent initialized")
        print(f"LLM Provider: {self.base_url}")
        print(f"Model: {self.model}")
        print(f"Available tools: {len(self.tool_functions)}")

    def get_system_prompt(self) -> str:
        """Get the system prompt for the agent"""
        return """You are a helpful weather assistant with access to weather data tools.

Available tools:
1. get_current_weather(location="CityName") - Get current weather conditions
2. get_forecast(location="CityName") - Get 3-hour interval forecast for 5 days
3. get_daily_summary(location="CityName") - Get daily weather summary for 5 days
4. get_air_quality(location="CityName") - Get current air quality and pollution data
5. get_pollution_forecast(location="CityName", hours=24) - Get air quality forecast

When the user asks about weather, you MUST respond with a JSON object indicating which tool to use:
{
  "tool": "tool_name",
  "parameters": {"location": "CityName", ...}
}

Examples:
- User: "What's the weather in London?"
  Response: {"tool": "get_current_weather", "parameters": {"location": "London"}}

- User: "Air quality in Beijing"
  Response: {"tool": "get_air_quality", "parameters": {"location": "Beijing"}}

- User: "5-day forecast for Tokyo"
  Response: {"tool": "get_daily_summary", "parameters": {"location": "Tokyo"}}

IMPORTANT: Only respond with the JSON object, nothing else."""

    async def process_query(self, user_query: str) -> str:
        """
        Process a user query using LLM for tool selection

        Args:
            user_query: The user's natural language query

        Returns:
            Agent's response
        """
        print(f"\nProcessing query: {user_query}")

        # Step 1: Use LLM to select tool and extract parameters
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": user_query}
        ]

        try:
            # Get tool selection from LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3
            )

            llm_response = response.choices[0].message.content
            print(f"LLM decision: {llm_response}")

            # Parse the JSON response
            # Try to find JSON object in the response
            try:
                # First, try to parse the whole response as JSON
                tool_call = json.loads(llm_response.strip())
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from text
                # Look for JSON object with balanced braces
                brace_count = 0
                start_idx = None
                for i, char in enumerate(llm_response):
                    if char == '{':
                        if start_idx is None:
                            start_idx = i
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0 and start_idx is not None:
                            json_str = llm_response[start_idx:i+1]
                            try:
                                tool_call = json.loads(json_str)
                                break
                            except:
                                continue
                else:
                    raise json.JSONDecodeError("No valid JSON found", llm_response, 0)

            tool_name = tool_call.get("tool")
            parameters = tool_call.get("parameters", {})

            print(f"Parsed - Tool: {tool_name}, Parameters: {parameters}")

            if tool_name not in self.tool_functions:
                return f"Unknown tool: {tool_name}"

            print(f"Calling tool: {tool_name} with parameters: {parameters}")

            # Step 2: Execute the selected tool
            result = await self.tool_functions[tool_name](**parameters)

            # Step 3: Use LLM to format the response naturally
            format_messages = [
                {"role": "system", "content": "You are a helpful weather assistant. Format the following weather data into a natural, friendly response for the user. Be concise but informative. IMPORTANT: Only use the exact data provided - do not make up, guess, or infer any information. If data is missing, simply say so."},
                {"role": "user", "content": f"User asked: {user_query}\n\nTool used: {tool_name}\nData received from API: {result}\n\nProvide a natural response using ONLY this data:"}
            ]

            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=format_messages,
                temperature=0.7
            )

            return final_response.choices[0].message.content

        except json.JSONDecodeError:
            return f"I had trouble understanding the request. Could you please rephrase your question about weather or air quality?"
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    async def interactive_session(self):
        """Run an interactive session with the agent"""
        print("\n" + "="*60)
        print("Weather Services Agent - Interactive Session")
        print("="*60)
        print("\nI can help you with weather, forecasts, and air quality!")
        print("Type 'exit' or 'quit' to end the session.\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\nGoodbye! Stay safe and enjoy the weather!")
                    break

                if not user_input:
                    continue

                response = await self.process_query(user_input)
                print(f"\nAgent: {response}\n")

            except KeyboardInterrupt:
                print("\n\nSession interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")


async def main():
    """Main entry point for the agent"""
    # Initialize agent with free model via OpenRouter
    try:
        agent = WeatherServicesAgent()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please ensure OPENROUTER_API_KEY is set in your .env file")
        return

    # Example queries
    print("\n" + "="*60)
    print("Running Example Queries with Real LLM Tool Selection")
    print("="*60)

    examples = [
        "What's the current weather in London?",
        "Show me the air quality in Beijing",
        "5-day forecast for Paris"
    ]

    for i, query in enumerate(examples, 1):
        print(f"\nExample {i}: {query}")
        response = await agent.process_query(query)
        print(f"Response: {response}")
        await asyncio.sleep(2)

    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60)

    # Interactive session
    print("\nStarting interactive session...")
    await agent.interactive_session()


if __name__ == "__main__":
    asyncio.run(main())
