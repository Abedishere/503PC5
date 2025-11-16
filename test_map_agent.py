"""
Standalone test script for Map Agent.
Run this from command line to test without Jupyter caching issues.
"""

import asyncio
import sys
import os

# Add part2_implementation to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'part2_implementation'))

# Force reload of modules
if 'part2_implementation.gemini_provider' in sys.modules:
    del sys.modules['part2_implementation.gemini_provider']
if 'part2_implementation.agent_sdk_app' in sys.modules:
    del sys.modules['part2_implementation.agent_sdk_app']

from part2_implementation.gemini_provider import run_with_tools
from part2_implementation.agent_sdk_app import TOOLS, agent


async def test_geocode():
    """Test geocoding Bhamdoun, Lebanon"""
    print("=" * 60)
    print("TEST 1: Geocoding Bhamdoun, Lebanon")
    print("=" * 60)

    response = await run_with_tools(
        "Find the coordinates of Bhamdoun, Lebanon - the famous mountain resort town",
        TOOLS,
        agent
    )
    print("\n" + "=" * 60)
    print("RESPONSE:")
    print("=" * 60)
    print(response)
    print("\n")


async def test_reverse():
    """Test reverse geocoding for Grand Hotel Bhamdoun"""
    print("=" * 60)
    print("TEST 2: Reverse Geocoding - Historic Grand Hotel")
    print("=" * 60)

    response = await run_with_tools(
        "What place is located at coordinates 33.8080, 35.6450? I think it's a historic hotel",
        TOOLS,
        agent
    )
    print("\n" + "=" * 60)
    print("RESPONSE:")
    print("=" * 60)
    print(response)
    print("\n")


async def test_poi():
    """Test POI search for cafes and restaurants in Bhamdoun"""
    print("=" * 60)
    print("TEST 3: POI Search - Mountain Cafes")
    print("=" * 60)

    response = await run_with_tools(
        "Find cafes and restaurants in Bhamdoun, the mountain resort town",
        TOOLS,
        agent
    )
    print("\n" + "=" * 60)
    print("RESPONSE:")
    print("=" * 60)
    print(response)
    print("\n")


async def test_distance():
    """Test distance calculation from Beirut to Bhamdoun"""
    print("=" * 60)
    print("TEST 4: Distance Calculation - Mountain Escape")
    print("=" * 60)

    response = await run_with_tools(
        "What's the driving distance from Beirut to Bhamdoun mountain resort?",
        TOOLS,
        agent
    )
    print("\n" + "=" * 60)
    print("RESPONSE:")
    print("=" * 60)
    print(response)
    print("\n")


async def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗" if os.name != 'nt' else "=" * 60)
    print("MAP AGENT TEST SUITE")
    print("╚" + "=" * 58 + "╝" if os.name != 'nt' else "=" * 60)
    print("\n")

    # Verify tools loaded
    print(f"Loaded {len(TOOLS)} tools:")
    for tool in TOOLS:
        print(f"  - {tool.__name__}")
    print("\n")

    try:
        # Run tests
        await test_geocode()
        await test_reverse()
        await test_poi()
        await test_distance()

        print("\n")
        print("=" * 60)
        print("ALL TESTS COMPLETED!")
        print("=" * 60)
        print("\n")

    except Exception as e:
        print("\n")
        print("=" * 60)
        print("ERROR OCCURRED:")
        print("=" * 60)
        print(f"{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
