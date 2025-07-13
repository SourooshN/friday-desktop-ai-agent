# core/brain/model_selector.py

"""
A simple façade over our agent_router to provide a consistent
`query_model()` API and abstract away HTTP details.
"""

from core.brain.agent_router import route_task

def query_model(query: str) -> str:
    """
    Send the raw user query to the appropriate Ollama model
    via our agent_router logic, and return its response.
    """
    return route_task(query)
