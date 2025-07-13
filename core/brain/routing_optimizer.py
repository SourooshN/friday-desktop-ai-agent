# core/brain/routing_optimizer.py

import json
import sqlite3
import os
from collections import Counter

from core.brain.memory import DB_PATH

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "routing_config.json")

# Threshold: if >X% of a category's commands were routed via fallback,
# suggest adding new keywords from their commands.
FALLBACK_CATEGORY = "general"
THRESHOLD_PERCENT = 0.5  # 50%

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def optimize_routing():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT category, command FROM interactions")
    rows = cursor.fetchall()
    conn.close()

    # Count how many commands per intended category were sent to 'general'
    counts = Counter()
    fallback_counts = Counter()
    for cat, cmd in rows:
        counts[cat] += 1
        if cat != FALLBACK_CATEGORY and cat == FALLBACK_CATEGORY:
            fallback_counts[cat] += 1

    config = load_config()
    updated = False

    # For each non-general category, if many of its commands fell back,
    # add unique words from those commands into the keyword list.
    for cat in config:
        if cat == FALLBACK_CATEGORY:
            continue
        total = counts.get(cat, 0)
        fallback = fallback_counts.get(cat, 0)
        if total > 0 and (fallback / total) > THRESHOLD_PERCENT:
            # Gather candidate keywords
            cursor = sqlite3.connect(DB_PATH).cursor()
            cursor.execute(
                "SELECT command FROM interactions WHERE category=?",
                (cat,)
            )
            cmds = [row[0].lower().split() for row in cursor.fetchall()]
            # Flatten and pick top 5 frequent words excluding existing
            words = [w for sub in cmds for w in sub if w.isalpha()]
            freq = Counter(words)
            existing = set(config[cat])
            additions = [w for w, _ in freq.most_common() if w not in existing and len(w) > 3][:5]
            if additions:
                config[cat].extend(additions)
                updated = True

    if updated:
        save_config(config)
        print(f"[OPTIMIZER] Updated routing_config.json with new keywords.")
    else:
        print("[OPTIMIZER] No changes needed.")

if __name__ == "__main__":
    optimize_routing()
