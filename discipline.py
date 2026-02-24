import time
from collections import deque
from config import ADMIN_USERNAMES

# -----------------------------
# CONFIG (Discipline Rules)
# -----------------------------

MESSAGE_LIMIT = 15          # 15 messages
TIME_WINDOW = 60            # 60 seconds
COOLDOWN_TIME = 180         # 3 minutes (in seconds)

# -----------------------------
# Internal State
# -----------------------------

message_timestamps = deque()
last_warning_time = 0


def check_discipline(message_username):

    global last_warning_time

    # Ignore admin messages
    if message_username in ADMIN_USERNAMES:
        return None

    current_time = time.time()

    # Add current timestamp
    message_timestamps.append(current_time)

    # Remove timestamps older than TIME_WINDOW
    while message_timestamps and current_time - message_timestamps[0] > TIME_WINDOW:
        message_timestamps.popleft()

    # Check if threshold exceeded
    if len(message_timestamps) >= MESSAGE_LIMIT:

        # Check cooldown
        if current_time - last_warning_time > COOLDOWN_TIME:

            last_warning_time = current_time

            return (
                "⚠️ Chatting won’t increase percentile.\n"
                "Studying will.\n"
                "JEE is near. Control yourself."
            )

    return None