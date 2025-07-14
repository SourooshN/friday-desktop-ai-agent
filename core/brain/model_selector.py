# core/brain/model_selector.py

from core.brain.config.routing_config import ROUTING_CONFIG

def select_model_for_intent(intent: str) -> str:
    """
    Return the model for a given intent,
    falling back to 'general' if not found.
    """
    model = ROUTING_CONFIG.get(intent)
    if not model:
        model = ROUTING_CONFIG.get("general")
    return model
