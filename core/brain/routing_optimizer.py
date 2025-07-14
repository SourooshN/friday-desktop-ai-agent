# core/brain/routing_optimizer.py

import sqlite3
import json
import os
from core.brain.memory import DB_PATH

# Path to your JSON config
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "config",
    "routing_config.json"
)

def optimize_routing():
    """
    Analyze the interaction logs in the SQLite memory DB, determine the
    most-used model per category, and update routing_config.json accordingly.
    """
    # 1) Read counts of (category, model) from your memory DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, model, COUNT(*) AS cnt
        FROM interactions
        GROUP BY category, model
    """)
    rows = cursor.fetchall()
    conn.close()

    # 2) Build a stats dict: { category: { model: count, ... }, ... }
    stats = {}
    for category, model, cnt in rows:
        stats.setdefault(category, {})[model] = cnt

    # 3) Load existing routing config
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    updated = False

    # 4) For each category seen in stats, pick the model with highest count
    for category, model_counts in stats.items():
        best_model = max(model_counts, key=model_counts.get)
        if config.get(category) != best_model:
            print(f"[RoutingOptimizer] Updating '{category}': "
                  f"'{config.get(category)}' → '{best_model}'")
            config[category] = best_model
            updated = True

    # 5) Write file back if anything changed
    if updated:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print("[RoutingOptimizer] routing_config.json updated.")
    else:
        print("[RoutingOptimizer] No changes needed.")

if __name__ == "__main__":
    optimize_routing()
