"""
Simple test to verify the Map Agent works.
Run this FIRST before trying Jupyter.
"""

import asyncio
import sys
import os

# Add to path
sys.path.insert(0, os.path.dirname(__file__))

async def main():
    print("=" * 60)
    print("MAP AGENT SIMPLE TEST")
    print("=" * 60)
    print()

    # Test 1: Import modules
    print("Test 1: Importing modules...")
    try:
        from part2_implementation.gemini_provider import run_with_tools
        from part2_implementation.agent_sdk_app import TOOLS, agent
        print("[OK] Modules imported successfully")
        print(f"[OK] Loaded {len(TOOLS)} tools\n")
    except Exception as e:
        print(f"[ERROR] Import failed: {e}")
        return

    # Test 2: Simple geocoding
    print("=" * 60)
    print("Test 2: Geocoding Bhamdoun Mountain Resort")
    print("=" * 60)
    try:
        response = await run_with_tools(
            "Where is Bhamdoun, the famous mountain resort town in Lebanon? Give me its coordinates.",
            TOOLS,
            agent
        )
        print(f"\nResponse: {response}\n")
        print("[OK] Geocoding test passed!")
    except Exception as e:
        print(f"[ERROR] Geocoding failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
