from datetime import datetime
from config import JEE_TARGET_DATE, GROUP_CHAT_ID


def calculate_days_left():
    now = datetime.now()
    delta = JEE_TARGET_DATE - now
    return max(delta.days, 0)


async def send_daily_countdown(context):
    days_left = calculate_days_left()

    message = (
        f"🚨 {days_left} days left for JEE.\n"
        "Ab toh padh lo bhai.\n"
        "This is your last chance.\n"
        "Close Telegram. Open PYQs."
    )

    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=message
    )