# core/brain/self_optimizer.py

import sqlite3
from datetime import datetime
from collections import Counter

from core.brain.memory import DB_PATH

def summarize_interactions():
    """
    Read the memory DB and produce summary statistics:
    - total interactions
    - counts per category
    - counts per model
    - average response length
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT category, model, LENGTH(response) FROM interactions")
    rows = cursor.fetchall()
    conn.close()

    total = len(rows)
    categories = [r[0] for r in rows]
    models     = [r[1] for r in rows]
    lengths    = [r[2] for r in rows if isinstance(r[2], int)]

    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_interactions": total,
        "by_category": dict(Counter(categories)),
        "by_model": dict(Counter(models)),
        "avg_response_length": round(sum(lengths) / len(lengths), 2) if lengths else 0
    }
    return summary

def print_summary(summary: dict):
    """Nicely print the summary."""
    print(f"🧠 Friday Memory Summary @ {summary['timestamp']}")
    print(f"  • Total interactions: {summary['total_interactions']}")
    print("  • By category:")
    for cat, cnt in summary["by_category"].items():
        print(f"    – {cat}: {cnt}")
    print("  • By model:")
    for mdl, cnt in summary["by_model"].items():
        print(f"    – {mdl}: {cnt}")
    print(f"  • Avg response length: {summary['avg_response_length']} chars")

if __name__ == "__main__":
    summary = summarize_interactions()
    print_summary(summary)
