"""
Demo: POI (Points of Interest) Server
Shows place search, nearby search, and place details features
"""

import asyncio
import sys
sys.path.append('..')

from map_servers.poi_server import POIServer


async def demo_nearby_search():
    """Demo nearby place search"""
    print("\n" + "="*60)
    print("📍 Nearby Search Demo")
    print("="*60)

    server = POIServer()

    # Search near Empire State Building
    center = (40.7484, -73.9857)

    print(f"\n🔍 Searching near Empire State Building")
    print(f"   📌 Location: {center[0]}, {center[1]}")
    print(f"   🎯 Radius: 3000m\n")

    pois = await server.search_nearby(
        latitude=center[0],
        longitude=center[1],
        radius_meters=3000,
        limit=10
    )

    print(f"📋 Found {len(pois)} places:\n")

    for i, poi in enumerate(pois, 1):
        print(f"{i}. {poi.name}")
        print(f"   📁 Category: {poi.category}")
        if poi.distance_meters:
            print(f"   📏 Distance: {poi.distance_meters:.0f}m ({poi.distance_meters/1000:.2f}km)")
        if poi.rating:
            print(f"   ⭐ Rating: {poi.rating}/5.0")
        if poi.address:
            print(f"   📮 Address: {poi.address}")
        print()

    await server.close()


async def demo_category_search():
    """Demo search by category"""
    print("\n" + "="*60)
    print("🍽️  Category Search Demo")
    print("="*60)

    server = POIServer()

    categories = [
        ("restaurant", "🍽️"),
        ("cafe", "☕"),
        ("museum", "🏛️"),
        ("park", "🌳")
    ]

    center = (40.7484, -73.9857)

    for category, icon in categories:
        print(f"\n{icon} Searching for {category}s...")

        pois = await server.search_nearby(
            latitude=center[0],
            longitude=center[1],
            radius_meters=5000,
            category=category,
            limit=3
        )

        if pois:
            print(f"   Found {len(pois)} {category}s:\n")
            for poi in pois:
                print(f"   • {poi.name}")
                if poi.rating:
                    print(f"     ⭐ {poi.rating}/5.0")
                if poi.distance_meters:
                    print(f"     📏 {poi.distance_meters/1000:.2f}km away")
                print()
        else:
            print(f"   No {category}s found\n")

    await server.close()


async def demo_text_search():
    """Demo text-based search"""
    print("\n" + "="*60)
    print("🔍 Text Search Demo")
    print("="*60)

    server = POIServer()

    queries = [
        "coffee",
        "museum",
        "park",
        "landmark"
    ]

    center = (40.7484, -73.9857)

    for query in queries:
        print(f"\n🔍 Searching for: '{query}'")

        results = await server.search_text(
            query=query,
            latitude=center[0],
            longitude=center[1],
            radius_meters=5000,
            limit=3
        )

        if results:
            print(f"   📋 Found {len(results)} results:\n")
            for result in results:
                print(f"   • {result.name}")
                if result.category:
                    print(f"     📁 {result.category}")
                if result.rating:
                    print(f"     ⭐ {result.rating}/5.0")
                if result.description:
                    print(f"     ℹ️  {result.description[:60]}...")
                print()
        else:
            print(f"   No results found\n")

    await server.close()


async def demo_place_details():
    """Demo getting detailed place information"""
    print("\n" + "="*60)
    print("ℹ️  Place Details Demo")
    print("="*60)

    server = POIServer()

    places = [
        "Empire State Building",
        "Central Park",
        "The Metropolitan Museum of Art"
    ]

    for place_name in places:
        print(f"\n🔍 Getting details for: {place_name}")

        details = await server.get_place_details(place_name)

        if details:
            print(f"\n📍 {details.name}")
            print(f"   📁 Category: {details.category}")
            print(f"   📌 Location: {details.latitude}, {details.longitude}")

            if details.address:
                print(f"   📮 Address: {details.address}")

            if details.rating:
                stars = "⭐" * int(details.rating)
                print(f"   {stars} {details.rating}/5.0")

            if details.price_level:
                dollars = "$" * details.price_level
                print(f"   💰 Price: {dollars}")

            if details.phone:
                print(f"   📞 Phone: {details.phone}")

            if details.website:
                print(f"   🌐 Website: {details.website}")

            if details.opening_hours:
                print(f"   🕐 Hours:")
                for hours in details.opening_hours:
                    print(f"      {hours}")

            if details.description:
                print(f"   ℹ️  {details.description}")

            print()
        else:
            print(f"   ❌ Place not found\n")

    await server.close()


async def demo_filtered_search():
    """Demo search with filters"""
    print("\n" + "="*60)
    print("🔎 Filtered Search Demo")
    print("="*60)

    server = POIServer()

    print(f"\n🔍 Finding highly-rated affordable restaurants")
    print(f"   Filters: Rating ≥ 4.0, Price Level ≤ 2\n")

    restaurants = await server.search_by_category(
        category="restaurant",
        latitude=40.7484,
        longitude=-73.9857,
        radius_meters=5000,
        min_rating=4.0,
        max_price_level=2,
        limit=5
    )

    if restaurants:
        print(f"📋 Found {len(restaurants)} restaurants:\n")
        for i, restaurant in enumerate(restaurants, 1):
            print(f"{i}. {restaurant.name}")
            print(f"   ⭐ Rating: {restaurant.rating}/5.0")
            if restaurant.price_level:
                print(f"   💰 Price: {'$' * restaurant.price_level}")
            if restaurant.distance_meters:
                print(f"   📏 Distance: {restaurant.distance_meters/1000:.2f}km")
            if restaurant.address:
                print(f"   📮 {restaurant.address}")
            print()
    else:
        print("   No restaurants found matching criteria\n")

    await server.close()


async def demo_comparison():
    """Demo comparing multiple places"""
    print("\n" + "="*60)
    print("⚖️  Place Comparison Demo")
    print("="*60)

    server = POIServer()

    print(f"\n🔍 Comparing NYC landmarks:\n")

    landmarks = [
        "Empire State Building",
        "Times Square",
        "Central Park"
    ]

    comparison = []
    for name in landmarks:
        details = await server.get_place_details(name)
        if details:
            comparison.append(details)

    # Print comparison table
    print(f"{'Place':<30} {'Rating':<10} {'Category':<15}")
    print("-" * 55)

    for place in comparison:
        rating = f"{place.rating}/5.0" if place.rating else "N/A"
        print(f"{place.name:<30} {rating:<10} {place.category:<15}")

    print()

    # Find highest rated
    rated_places = [p for p in comparison if p.rating is not None]
    if rated_places:
        best = max(rated_places, key=lambda x: x.rating)
        print(f"🏆 Highest Rated: {best.name} ({best.rating}/5.0)\n")

    await server.close()


async def main():
    """Run all POI demos"""
    print("\n🚀 Starting POI Server Demos")
    print("="*60)

    try:
        await demo_nearby_search()
        await demo_category_search()
        await demo_text_search()
        await demo_place_details()
        await demo_filtered_search()
        await demo_comparison()

        print("\n" + "="*60)
        print("✅ All demos completed successfully!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}\n")
        raise


if __name__ == "__main__":
    asyncio.run(main())
