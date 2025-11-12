"""
Demo: Geocoding Server
Shows forward and reverse geocoding capabilities
"""

import asyncio
import sys
sys.path.append('..')

from map_servers.geocoding_server import GeocodingServer


async def demo_forward_geocoding():
    """Demo forward geocoding (address to coordinates)"""
    print("\n" + "="*60)
    print("📍 Forward Geocoding Demo")
    print("="*60)

    server = GeocodingServer()

    addresses = [
        "Empire State Building, New York",
        "Central Park, NYC",
        "Times Square, Manhattan",
        "Brooklyn Bridge, New York"
    ]

    for address in addresses:
        print(f"\n🔍 Geocoding: {address}")
        results = await server.forward_geocode(address, limit=1)

        if results:
            result = results[0]
            print(f"   📌 Coordinates: {result.latitude}, {result.longitude}")
            print(f"   ✅ Confidence: {result.confidence:.2f}")
            print(f"   🏙️  City: {result.city}")
            print(f"   🌍 Country: {result.country}")
        else:
            print("   ❌ No results found")

    await server.close()


async def demo_reverse_geocoding():
    """Demo reverse geocoding (coordinates to address)"""
    print("\n" + "="*60)
    print("🗺️  Reverse Geocoding Demo")
    print("="*60)

    server = GeocodingServer()

    coordinates = [
        (40.7484, -73.9857, "Empire State Building"),
        (40.7829, -73.9654, "Central Park"),
        (40.7580, -73.9855, "Times Square"),
        (40.7061, -74.0087, "Brooklyn Bridge")
    ]

    for lat, lon, name in coordinates:
        print(f"\n🔍 Reverse geocoding: {lat}, {lon} ({name})")
        result = await server.reverse_geocode(lat, lon)

        print(f"   📍 Address: {result.address}")
        print(f"   ✅ Confidence: {result.confidence:.2f}")
        if result.city:
            print(f"   🏙️  City: {result.city}")
        if result.country:
            print(f"   🌍 Country: {result.country}")

    await server.close()


async def demo_batch_geocoding():
    """Demo batch geocoding"""
    print("\n" + "="*60)
    print("📦 Batch Geocoding Demo")
    print("="*60)

    server = GeocodingServer()

    addresses = [
        "Statue of Liberty, New York",
        "One World Trade Center, NYC",
        "Metropolitan Museum of Art, New York"
    ]

    print(f"\n🔍 Batch geocoding {len(addresses)} addresses...")
    results = await server.batch_geocode(addresses)

    for i, (address, result_list) in enumerate(zip(addresses, results), 1):
        print(f"\n{i}. {address}")
        if result_list:
            result = result_list[0]
            print(f"   📌 {result.latitude}, {result.longitude}")
        else:
            print("   ❌ No results")

    await server.close()


async def demo_geocoding_with_multiple_results():
    """Demo geocoding with multiple results"""
    print("\n" + "="*60)
    print("🔢 Multiple Results Demo")
    print("="*60)

    server = GeocodingServer()

    # Ambiguous query that might return multiple results
    query = "Washington"

    print(f"\n🔍 Geocoding ambiguous query: '{query}'")
    results = await server.forward_geocode(query, limit=5)

    print(f"\n📋 Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.address}")
        print(f"   📌 {result.latitude}, {result.longitude}")
        print(f"   ✅ Confidence: {result.confidence:.2f}")

    await server.close()


async def main():
    """Run all geocoding demos"""
    print("\n🚀 Starting Geocoding Server Demos")
    print("="*60)

    try:
        await demo_forward_geocoding()
        await demo_reverse_geocoding()
        await demo_batch_geocoding()
        await demo_geocoding_with_multiple_results()

        print("\n" + "="*60)
        print("✅ All demos completed successfully!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}\n")
        raise


if __name__ == "__main__":
    asyncio.run(main())
