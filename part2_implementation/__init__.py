"""
Part 2 Implementation - Map Agent with Custom Map Servers.

This package provides:
- TOOLS: List of available map agent tools
- AgentsSDKMapAssistant: Map assistant class
- agent: Pre-configured agent instance
- run_with_tools: Function to run Gemini with tools
"""

__all__ = ['TOOLS', 'AgentsSDKMapAssistant', 'agent', 'run_with_tools']

# Lazy imports to avoid initialization issues
def __getattr__(name):
    """Lazy import to avoid premature initialization."""
    if name in __all__:
        if name in ['TOOLS', 'AgentsSDKMapAssistant', 'agent']:
            from .agent_sdk_app import TOOLS, AgentsSDKMapAssistant, agent
            globals().update({'TOOLS': TOOLS, 'AgentsSDKMapAssistant': AgentsSDKMapAssistant, 'agent': agent})
            return globals()[name]
        elif name == 'run_with_tools':
            from .gemini_provider import run_with_tools
            globals()['run_with_tools'] = run_with_tools
            return run_with_tools
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
