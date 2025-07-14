# core/brain/agent_router.py

from core.brain.config.routing_config import ROUTING_CONFIG
from core.brain.model_selector import select_model_for_intent
from core.llm.llm_interface import query_model
from core.brain.memory import log_interaction

def route_and_query(intent: str, text: str) -> str:
    """
    Choose the right model based on intent (using routing_config),
    send it the text, log the interaction, and return the response.
    """
    model = select_model_for_intent(intent)
    response = query_model(model, text)
    log_interaction(intent, text, model, response)
    return response
