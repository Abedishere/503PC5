"""
Demo: Full Map Services Agent
Demonstrates the integrated agent handling complex queries
"""

import asyncio
import sys
sys.path.append('..')

from agent import MapServicesAgent


async def demo_agent_queries():
    """Demo agent handling various queries"""
    print("\n" + "="*60)
    print("🤖 Map Services Agent Demo")
    print("="*60)

    agent = MapServicesAgent()

    # Various types of queries
    queries = [
        {
            "query": "What are the coordinates of the Empire State Building?",
            "icon": "📍",
            "type": "Geocoding"
        },
        {
            "query": "Find restaurants near Times Square",
            "icon": "🍽️",
            "type": "POI Search"
        },
        {
            "query": "Calculate the route from Empire State Building to Central Park",
            "icon": "🛣️",
            "type": "Routing"
        },
        {
            "query": "Tell me about Central Park",
            "icon": "ℹ️",
            "type": "Place Details"
        },
        {
            "query": "What's the address at coordinates 40.7484, -73.9857?",
            "icon": "🗺️",
            "type": "Reverse Geocoding"
        },
        {
            "query": "Find museums nearby",
            "icon": "🏛️",
            "type": "Category Search"
        }
    ]

    for i, item in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"{item['icon']} Query {i}: {item['type']}")
        print(f"{'='*60}")
        print(f"\n❓ User: {item['query']}")

        response = await agent.process_query(item['query'])

        print(f"\n🤖 Agent: {response}")

        # Brief pause between queries
        await asyncio.sleep(1)

    print(f"\n{'='*60}")
    print("✅ Agent demo completed!")
    print(f"{'='*60}\n")


async def demo_complex_scenario():
    """Demo agent handling a complex multi-step scenario"""
    print("\n" + "="*60)
    print("🎯 Complex Scenario Demo: Planning a NYC Visit")
    print("="*60)

    agent = MapServicesAgent()

    scenario = [
        {
            "step": "Find a starting point",
            "query": "What are the coordinates of Times Square?",
            "icon": "📍"
        },
        {
            "step": "Find nearby attractions",
            "query": "Find landmarks and museums nearby",
            "icon": "🏛️"
        },
        {
            "step": "Plan lunch",
            "query": "Find restaurants near here",
            "icon": "🍽️"
        },
        {
            "step": "Calculate travel time",
            "query": "How far is it from Times Square to Central Park?",
            "icon": "🛣️"
        }
    ]

    print("\n📋 Scenario: Tourist visiting NYC for the first time")
    print("    They want to explore Times Square area, then visit Central Park\n")

    for i, step in enumerate(scenario, 1):
        print(f"\n{'-'*60}")
        print(f"{step['icon']} Step {i}: {step['step']}")
        print(f"{'-'*60}")
        print(f"❓ {step['query']}")

        response = await agent.process_query(step['query'])

        print(f"\n💬 {response}")

        await asyncio.sleep(1)

    print(f"\n{'='*60}")
    print("✅ Complex scenario completed!")
    print("   The agent successfully helped plan a NYC visit")
    print(f"{'='*60}\n")


async def demo_comparison_query():
    """Demo agent comparing different options"""
    print("\n" + "="*60)
    print("⚖️  Comparison Demo: Different Travel Modes")
    print("="*60)

    agent = MapServicesAgent()

    print("\n📋 Scenario: Comparing travel options\n")

    modes = ["driving", "walking", "cycling", "transit"]

    print("❓ How can I get from Empire State Building to Central Park?\n")

    for mode in modes:
        icon = {"driving": "🚗", "walking": "🚶", "cycling": "🚴", "transit": "🚇"}[mode]
        print(f"\n{icon} Checking {mode}...")

        query = f"Calculate {mode} route from Empire State Building to Central Park"
        response = await agent.process_query(query)

        # Extract key info (simplified for demo)
        print(f"   {response[:200]}...")

        await asyncio.sleep(0.5)

    print(f"\n{'='*60}")
    print("✅ Comparison complete!")
    print(f"{'='*60}\n")


async def demo_recommendation_scenario():
    """Demo agent providing recommendations"""
    print("\n" + "="*60)
    print("💡 Recommendation Demo")
    print("="*60)

    agent = MapServicesAgent()

    print("\n📋 Scenario: Tourist looking for recommendations\n")

    recommendations = [
        ("coffee shops", "☕"),
        ("parks", "🌳"),
        ("museums", "🏛️")
    ]

    location = "near Empire State Building"

    for place_type, icon in recommendations:
        print(f"\n{icon} Finding {place_type} {location}...")

        query = f"Find {place_type} {location}"
        response = await agent.process_query(query)

        print(f"   {response[:150]}...")

        await asyncio.sleep(0.5)

    print(f"\n{'='*60}")
    print("✅ Recommendations provided!")
    print(f"{'='*60}\n")


async def demo_interactive_session_preview():
    """Preview of interactive session capabilities"""
    print("\n" + "="*60)
    print("🗣️  Interactive Session Preview")
    print("="*60)

    agent = MapServicesAgent()

    print("\n💬 Sample conversation with the agent:\n")

    conversation = [
        ("User", "Hello! I'm planning a trip to NYC. Can you help?"),
        ("Agent", "Of course! I can help you with locations, routes, and finding places in NYC. What would you like to know?"),
        ("User", "What's interesting near Times Square?"),
        ("Agent", "[Agent searches for POIs] I found several interesting places near Times Square..."),
        ("User", "How do I get from Times Square to Central Park?"),
        ("Agent", "[Agent calculates route] The distance is about 2.5km, which takes approximately 30 minutes by walking..."),
    ]

    for speaker, message in conversation:
        icon = "👤" if speaker == "User" else "🤖"
        print(f"{icon} {speaker}: {message}\n")
        await asyncio.sleep(0.5)

    print(f"{'='*60}")
    print("ℹ️  To run a full interactive session, uncomment the line")
    print("   'await agent.interactive_session()' in agent.py")
    print(f"{'='*60}\n")


async def main():
    """Run all full agent demos"""
    print("\n🚀 Starting Full Agent Demos")
    print("="*60)

    try:
        await demo_agent_queries()
        await demo_complex_scenario()
        await demo_comparison_query()
        await demo_recommendation_scenario()
        await demo_interactive_session_preview()

        print("\n" + "="*60)
        print("🎉 All agent demos completed successfully!")
        print("="*60)
        print("\n📝 Key Takeaways:")
        print("   • The agent can handle geocoding, routing, and POI queries")
        print("   • It intelligently routes queries to appropriate tools")
        print("   • It can handle complex multi-step scenarios")
        print("   • It provides natural, conversational responses")
        print("   • Compatible with OpenAI and DeepSeek LLMs")
        print("\n" + "="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}\n")
        raise


if __name__ == "__main__":
    asyncio.run(main())
