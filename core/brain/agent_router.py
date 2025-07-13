# core/brain/agent_router.py

from core.brain.config.routing_config import ROUTING_CONFIG
from core.brain.model_selector import select_model_for_intent
from core.llm.llm_interface import query_model
from core.brain.memory import log_interaction

def route_and_query(intent: str, text: str) -> str:
    """
    Determine which model to use based on the intent,
    query that model with the provided text,
    record the interaction in memory, and return the response.
    """
    model_name = select_model_for_intent(intent)
    response = query_model(model_name, text)
    log_interaction(intent=intent, 
                    command=text, 
                    model_name=model_name, 
                    response=response)
    return response
