import os
from datetime import datetime

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

def get_timestamp():
    """Returns the current timestamp as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_event(event_type, details):
    """Logs an event to a file with a timestamp."""
    timestamp = get_timestamp()
    log_entry = f"[{timestamp}] {event_type.upper()}: {details}\n"

    log_file_path = os.path.join(log_dir, "event_log.txt")
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

def ensure_log_dir():
    """Ensures that the log directory exists."""
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def write_log(entry: str):
    """Append a raw log entry string to the input log file."""
    ensure_log_dir()
    log_file_path = os.path.join(log_dir, "input_log.txt")
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(entry)