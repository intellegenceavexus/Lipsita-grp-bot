import random
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

from config import GROUP_CHAT_ID
from memory import (
    current_week_number,
    scheduled_question_times,
    last_question_date,
    weekly_drop_count,
)

# ===============================
# CONFIG
# ===============================

IST = ZoneInfo("Asia/Kolkata")

MAX_DROPS_PER_WEEK = 4
START_HOUR = 8
END_HOUR = 23
END_MINUTE = 45

# ===============================
# QUESTION BANK
# ===============================

QUESTION_BANK = [
    {
        "subject": "Physics",
        "question": "A particle moves such that v = 3t² + 2t. Find displacement between t=0 to t=2s."
    },
    {
        "subject": "Chemistry",
        "question": "Calculate pH of a 0.01 M HCl solution."
    },
    {
        "subject": "Mathematics",
        "question": "If f(x) = x³ - 3x² + 2, find all critical points."
    },
    {
        "subject": "Physics",
        "question": "A block slides on a frictionless incline of angle θ. Find acceleration."
    },
    {
        "subject": "Mathematics",
        "question": "Evaluate ∫(2x + 1) dx."
    },
    {
        "subject": "Chemistry",
        "question": "Find oxidation number of sulfur in H₂SO₄."
    },
]

# ===============================
# WEEK UTILITIES
# ===============================

def get_current_week():
    return datetime.now(IST).isocalendar()[1]


def reset_week_if_needed():
    global current_week_number, scheduled_question_times, weekly_drop_count

    now_week = get_current_week()

    if now_week != current_week_number:
        current_week_number = now_week
        scheduled_question_times.clear()
        weekly_drop_count = 0


def get_remaining_days():
    now = datetime.now(IST)
    weekday = now.weekday()
    days = []

    for i in range(7 - weekday):
        future = now + timedelta(days=i)
        days.append(future.date())

    return days


def select_non_consecutive_days(days):
    random.shuffle(days)
    selected = []

    for day in days:
        if not selected:
            selected.append(day)
        else:
            if all(abs((day - s).days) > 1 for s in selected):
                selected.append(day)

        if len(selected) == MAX_DROPS_PER_WEEK:
            break

    return sorted(selected)


def generate_random_time():
    hour = random.randint(START_HOUR, END_HOUR)
    minute = random.randint(0, 59)

    if hour == END_HOUR:
        minute = random.randint(0, END_MINUTE)

    return time(hour=hour, minute=minute)


# ===============================
# QUESTION FORMAT
# ===============================

def format_question():
    q = random.choice(QUESTION_BANK)

    return (
        "🎯 IIT/NIT Aspirant?\n\n"
        "Do you really deserve that seat?\n"
        "Prove it.\n\n"
        f"📘 Quick JEE Challenge ({q['subject']})\n\n"
        f"{q['question']}\n\n"
        "No one’s watching.\n"
        "Answer it for yourself."
    )


# ===============================
# SCHEDULER GENERATOR
# ===============================

def generate_week_schedule():
    reset_week_if_needed()

    if weekly_drop_count >= MAX_DROPS_PER_WEEK:
        return []

    remaining_days = get_remaining_days()
    selected_days = select_non_consecutive_days(remaining_days)

    schedule = []

    for day in selected_days:
        drop_time = generate_random_time()
        scheduled_dt = datetime.combine(day, drop_time)
        scheduled_dt = scheduled_dt.replace(tzinfo=IST)

        schedule.append(scheduled_dt)

    return schedule


# ===============================
# ASYNC SENDER
# ===============================

async def send_weekly_question(context):
    global weekly_drop_count, last_question_date

    now = datetime.now(IST).date()

    # Prevent same day duplicate
    if last_question_date == now:
        return

    if weekly_drop_count >= MAX_DROPS_PER_WEEK:
        return

    message = format_question()

    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=message
    )

    last_question_date = now
    weekly_drop_count += 1