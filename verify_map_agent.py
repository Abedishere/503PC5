"""
Verification script for Map Agent setup.
Tests that all components are properly configured and accessible.
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check environment variables."""
    print("=" * 60)
    print("CHECKING ENVIRONMENT CONFIGURATION")
    print("=" * 60)

    load_dotenv()

    required_vars = {
        'ORS_API_KEY': os.getenv('ORS_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'GEMINI_MODEL': os.getenv('GEMINI_MODEL'),
        'OSM_COUNTRY_CODES': os.getenv('OSM_COUNTRY_CODES')
    }

    all_set = True
    for var, value in required_vars.items():
        if not value or value.startswith('YOUR_'):
            print(f"[X] {var}: NOT SET")
            all_set = False
        else:
            # Mask API keys for security
            if 'KEY' in var:
                display_value = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"[OK] {var}: {display_value}")

    print()
    return all_set

def check_dependencies():
    """Check required Python packages."""
    print("=" * 60)
    print("CHECKING PYTHON DEPENDENCIES")
    print("=" * 60)

    required_packages = [
        'requests',
        'dotenv',
        'gradio',
        'google.generativeai'
    ]

    all_installed = True
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'google.generativeai':
                __import__('google.generativeai')
            else:
                __import__(package)
            print(f"[OK] {package}: Installed")
        except ImportError:
            print(f"[X] {package}: NOT INSTALLED")
            all_installed = False

    print()
    return all_installed

def check_project_structure():
    """Check project file structure."""
    print("=" * 60)
    print("CHECKING PROJECT STRUCTURE")
    print("=" * 60)

    required_files = [
        'part2_implementation/__init__.py',
        'part2_implementation/agent_sdk_app.py',
        'part2_implementation/gemini_provider.py',
        'part2_implementation/servers/__init__.py',
        'part2_implementation/servers/ors_server.py',
        'part2_implementation/servers/osm_server.py',
        'map_agent.ipynb',
        'requirements.txt',
        '.env'
    ]

    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"[OK] {file_path}")
        else:
            print(f"[X] {file_path}: MISSING")
            all_exist = False

    print()
    return all_exist

def test_imports():
    """Test importing map agent components."""
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)

    try:
        sys.path.insert(0, 'part2_implementation')

        from part2_implementation.servers.osm_server import OSMServer
        print("[OK] OSMServer imported successfully")

        from part2_implementation.servers.ors_server import ORSServer
        print("[OK] ORSServer imported successfully")

        from part2_implementation.gemini_provider import run_with_tools
        print("[OK] Gemini provider imported successfully")

        from part2_implementation.agent_sdk_app import TOOLS, agent
        print(f"[OK] Agent SDK app imported successfully ({len(TOOLS)} tools registered)")

        print()
        return True
    except Exception as e:
        print(f"[X] Import failed: {str(e)}")
        print()
        return False

def main():
    """Run all verification checks."""
    print("\n")
    print("=" * 60)
    print(" " * 15 + "MAP AGENT VERIFICATION")
    print("=" * 60)
    print()

    # Run checks
    env_ok = check_environment()
    deps_ok = check_dependencies()
    struct_ok = check_project_structure()
    import_ok = test_imports()

    # Summary
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    checks = [
        ("Environment Configuration", env_ok),
        ("Python Dependencies", deps_ok),
        ("Project Structure", struct_ok),
        ("Component Imports", import_ok)
    ]

    all_passed = all(status for _, status in checks)

    for check_name, status in checks:
        symbol = "[OK]" if status else "[X]"
        print(f"{symbol} {check_name}: {'PASSED' if status else 'FAILED'}")

    print()

    if all_passed:
        print("SUCCESS! All checks passed! Your Map Agent is ready to use.")
        print()
        print("Next steps:")
        print("1. Make sure you have a Gemini API key in your .env file")
        print("2. Open map_agent.ipynb in Jupyter")
        print("3. Run the cells to test the agent")
        print("4. Launch the Gradio interface for interactive testing")
    else:
        print("WARNING: Some checks failed. Please address the issues above.")
        print()
        print("Common solutions:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Add missing API keys to .env file")
        print("- Verify all project files are in place")

    print()

if __name__ == "__main__":
    main()
