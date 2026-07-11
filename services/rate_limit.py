from datetime import datetime

# Simple in-memory counter
daily_usage = {}

FREE_LIMIT = 100   # प्रति दिन 100 messages


def can_chat(user_id):
    today = datetime.now().strftime("%Y-%m-%d")

    if user_id not in daily_usage:
        daily_usage[user_id] = {
            "date": today,
            "count": 0
        }

    # नया दिन
    if daily_usage[user_id]["date"] != today:
        daily_usage[user_id] = {
            "date": today,
            "count": 0
        }

    if daily_usage[user_id]["count"] >= FREE_LIMIT:
        return False

    daily_usage[user_id]["count"] += 1
    return True
