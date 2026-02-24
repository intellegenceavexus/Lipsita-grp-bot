from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

# ===============================
# TIMEZONE
# ===============================

IST = ZoneInfo("Asia/Kolkata")

# =========================================================
# 🔐 ADMIN PROTECTION MEMORY
# =========================================================

# Track repeat offenders for roast escalation
user_offense_count = defaultdict(int)

# =========================================================
# 📅 QUESTION DROP MEMORY
# =========================================================

# Current ISO week number
current_week_number = datetime.now(IST).isocalendar()[1]

# Store scheduled datetime objects for this week
scheduled_question_times = []

# Track last drop date (date object)
last_question_date = None

# Track how many questions dropped this week
weekly_drop_count = 0

# =========================================================
# 🚀 START COMMAND STATE MACHINE MEMORY
# =========================================================

# First ever boot message flag (global)
start_boot_done = False

# -------------------------------
# NORMAL USER START STATE (GLOBAL GROUP LEVEL)
# -------------------------------

# Counts how many times /start used (after first boot)
normal_start_count = 0

# Timestamp when cycle began (starts from 2nd /start)
normal_cycle_start_time = None

# -------------------------------
# ADMIN START STATE (SEPARATE FLOW)
# -------------------------------

# Admin-specific counter
admin_start_count = 0

# Admin cycle timer
admin_cycle_start_time = None