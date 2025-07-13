# core/brain/config/routing_config.py

import os
import json

# Path to your JSON file of routing rules
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "routing_config.json")

try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        ROUTING_CONFIG = json.load(f)
except FileNotFoundError:
    # Fallback if you haven’t created the JSON yet:
    ROUTING_CONFIG = {
        "default": "nous-hermes:13b"
    }
