"""
Demo: Routing Server
Shows route calculation, distance matrix, and navigation features
"""

import asyncio
import sys
sys.path.append('..')

from map_servers.routing_server import RoutingServer


async def demo_basic_routing():
    """Demo basic route calculation"""
    print("\n" + "="*60)
    print("🛣️  Basic Routing Demo")
    print("="*60)

    server = RoutingServer()

    routes = [
        ("Empire State Building", (40.7484, -73.9857), "Central Park", (40.7829, -73.9654)),
        ("Times Square", (40.7580, -73.9855), "Brooklyn Bridge", (40.7061, -74.0087)),
    ]

    for origin_name, (orig_lat, orig_lon), dest_name, (dest_lat, dest_lon) in routes:
        print(f"\n🚗 Route: {origin_name} → {dest_name}")

        route = await server.calculate_route(
            orig_lat, orig_lon,
            dest_lat, dest_lon,
            mode="driving"
        )

        print(f"   📏 Distance: {route.distance_meters:.0f}m ({route.distance_meters/1000:.2f}km)")
        print(f"   ⏱️  Duration: {route.duration_seconds:.0f}s ({route.duration_seconds/60:.1f} min)")
        print(f"   🚦 Steps: {len(route.steps)}")

        if route.warnings:
            print(f"   ⚠️  Warnings: {', '.join(route.warnings)}")

    await server.close()


async def demo_different_modes():
    """Demo routing with different transportation modes"""
    print("\n" + "="*60)
    print("🚶‍♂️ Transportation Modes Demo")
    print("="*60)

    server = RoutingServer()

    # Route from Empire State Building to Central Park
    origin = (40.7484, -73.9857)
    destination = (40.7829, -73.9654)

    modes = ["driving", "walking", "cycling", "transit"]

    print(f"\n📍 From: Empire State Building")
    print(f"📍 To: Central Park\n")

    for mode in modes:
        route = await server.calculate_route(
            origin[0], origin[1],
            destination[0], destination[1],
            mode=mode
        )

        icon = {"driving": "🚗", "walking": "🚶", "cycling": "🚴", "transit": "🚇"}[mode]
        print(f"{icon} {mode.upper()}")
        print(f"   Distance: {route.distance_meters/1000:.2f}km")
        print(f"   Duration: {route.duration_seconds/60:.1f} min\n")

    await server.close()


async def demo_route_steps():
    """Demo detailed route steps"""
    print("\n" + "="*60)
    print("🗺️  Route Steps Demo")
    print("="*60)

    server = RoutingServer()

    print(f"\n🚗 Calculating route with detailed steps...")

    route = await server.calculate_route(
        40.7484, -73.9857,  # Empire State Building
        40.7829, -73.9654,  # Central Park
        mode="driving"
    )

    print(f"\n📍 Total Distance: {route.distance_meters:.0f}m")
    print(f"⏱️  Total Duration: {route.duration_seconds/60:.1f} min")
    print(f"\n📋 Turn-by-turn directions:\n")

    for i, step in enumerate(route.steps, 1):
        print(f"{i}. {step.instruction}")
        print(f"   📏 {step.distance_meters:.0f}m")
        print(f"   ⏱️  {step.duration_seconds:.0f}s")
        if step.maneuver:
            print(f"   🔄 Maneuver: {step.maneuver}")
        print()

    await server.close()


async def demo_distance_matrix():
    """Demo distance matrix calculation"""
    print("\n" + "="*60)
    print("📊 Distance Matrix Demo")
    print("="*60)

    server = RoutingServer()

    origins = [
        (40.7484, -73.9857, "Empire State Building"),
        (40.7580, -73.9855, "Times Square"),
    ]

    destinations = [
        (40.7829, -73.9654, "Central Park"),
        (40.7061, -74.0087, "Brooklyn Bridge"),
        (40.7614, -73.9776, "Grand Central"),
    ]

    print("\n📍 Origins:")
    for i, (lat, lon, name) in enumerate(origins, 1):
        print(f"   {i}. {name}")

    print("\n📍 Destinations:")
    for i, (lat, lon, name) in enumerate(destinations, 1):
        print(f"   {i}. {name}")

    origin_coords = [(lat, lon) for lat, lon, _ in origins]
    dest_coords = [(lat, lon) for lat, lon, _ in destinations]

    matrix = await server.calculate_distance_matrix(
        origin_coords,
        dest_coords,
        mode="driving"
    )

    print("\n📊 Distance Matrix (km):")
    print("     ", end="")
    for _, _, name in destinations:
        print(f"{name[:15]:>15}", end=" ")
    print()

    for i, (_, _, origin_name) in enumerate(origins):
        print(f"{origin_name[:15]:>15}", end=" ")
        for j in range(len(destinations)):
            distance_km = matrix["distances_meters"][i][j] / 1000
            print(f"{distance_km:>14.2f}", end=" ")
        print()

    print("\n📊 Duration Matrix (min):")
    print("     ", end="")
    for _, _, name in destinations:
        print(f"{name[:15]:>15}", end=" ")
    print()

    for i, (_, _, origin_name) in enumerate(origins):
        print(f"{origin_name[:15]:>15}", end=" ")
        for j in range(len(destinations)):
            duration_min = matrix["durations_seconds"][i][j] / 60
            print(f"{duration_min:>14.1f}", end=" ")
        print()

    await server.close()


async def demo_alternative_routes():
    """Demo alternative route finding"""
    print("\n" + "="*60)
    print("🔀 Alternative Routes Demo")
    print("="*60)

    server = RoutingServer()

    print(f"\n🔍 Finding alternative routes...")
    print(f"📍 From: Empire State Building")
    print(f"📍 To: Central Park\n")

    routes = await server.get_route_alternatives(
        40.7484, -73.9857,
        40.7829, -73.9654,
        alternatives=3
    )

    for i, route in enumerate(routes, 1):
        print(f"Route {i}:")
        print(f"   📏 Distance: {route.distance_meters/1000:.2f}km")
        print(f"   ⏱️  Duration: {route.duration_seconds/60:.1f} min")
        if route.warnings:
            print(f"   ℹ️  Note: {route.warnings[0]}")
        print()

    await server.close()


async def main():
    """Run all routing demos"""
    print("\n🚀 Starting Routing Server Demos")
    print("="*60)

    try:
        await demo_basic_routing()
        await demo_different_modes()
        await demo_route_steps()
        await demo_distance_matrix()
        await demo_alternative_routes()

        print("\n" + "="*60)
        print("✅ All demos completed successfully!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}\n")
        raise


if __name__ == "__main__":
    asyncio.run(main())
