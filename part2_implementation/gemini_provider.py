"""
Gemini Provider using modern google-generativeai SDK.
Based on official Google AI examples for function calling.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Callable, Any

# Load environment variables
load_dotenv()


def setup_gemini():
    """Initialize Gemini with API key from environment."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_KEY_HERE":
        raise ValueError("GEMINI_API_KEY not set in .env file")

    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config={"temperature": 0.5}
    )


async def run_with_tools(prompt: str, tools: List[Callable], agent: Any) -> str:
    """
    Run Gemini with automatic function calling.

    Uses the modern SDK approach where Python functions are passed directly
    and the SDK handles everything automatically.

    Args:
        prompt: User's text prompt
        tools: List of tool functions (with proper docstrings and type hints)
        agent: Agent instance (not used in modern SDK, kept for compatibility)

    Returns:
        Final text response from Gemini
    """
    # Setup model
    model = setup_gemini()

    print(f"\nUser: {prompt}\n")

    # Enable automatic function calling
    # The SDK will:
    # 1. Convert functions to declarations
    # 2. Detect when model wants to call a function
    # 3. Execute the function
    # 4. Send results back to model
    # 5. Get final response
    #
    # All automatically!

    chat = model.start_chat(enable_automatic_function_calling=True)

    # Send message with tools
    response = chat.send_message(
        prompt,
        tools=tools  # Just pass the functions directly!
    )

    # The response will already have the final answer
    # after all function calls are complete
    return response.text


# Alternative: Manual function calling (if you want more control)
async def run_with_manual_tools(prompt: str, tools: List[Callable], agent: Any) -> str:
    """
    Run Gemini with manual function calling for more control.

    This gives you visibility into what's happening at each step.
    """
    model = setup_gemini()

    print(f"\nUser: {prompt}\n")

    # Create chat without automatic calling
    chat = model.start_chat(enable_automatic_function_calling=False)

    # Send initial message
    response = chat.send_message(prompt, tools=tools)

    # Manual tool calling loop
    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # Get function calls from response
        function_calls = []
        try:
            for part in response.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_calls.append(part.function_call)
        except:
            pass

        # If no function calls, we're done
        if not function_calls:
            break

        # Execute each function call
        function_responses = []
        for fc in function_calls:
            func_name = fc.name
            func_args = dict(fc.args)

            print(f"→ Calling: {func_name}")
            print(f"  Args: {func_args}")

            # Find and call the function
            result = None
            for tool in tools:
                if tool.__name__ == func_name:
                    try:
                        # Handle async functions
                        import asyncio
                        if asyncio.iscoroutinefunction(tool):
                            result = await tool(**func_args)
                        else:
                            result = tool(**func_args)
                        print(f"  Result: {result}\n")
                    except Exception as e:
                        result = {"error": str(e)}
                        print(f"  Error: {e}\n")
                    break

            if result is None:
                result = {"error": f"Function {func_name} not found"}

            # Add to responses
            function_responses.append(
                genai.protos.FunctionResponse(
                    name=func_name,
                    response={"result": result}
                )
            )

        # Send function results back
        response = chat.send_message(
            genai.protos.Content(
                parts=[
                    genai.protos.Part(function_response=fr)
                    for fr in function_responses
                ]
            ),
            tools=tools
        )

    # Return final text
    return response.text
