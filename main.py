from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    CommandHandler,
)

from datetime import time, datetime, timedelta
from zoneinfo import ZoneInfo

from config import TOKEN, ADMIN_USERNAMES
from admin_protection import analyze_admin_message
from countdown import send_daily_countdown
from discipline import check_discipline

from question_drop import (
    generate_week_schedule,
    send_weekly_question,
)

from memory import (
    scheduled_question_times,
    start_boot_done,
    normal_start_count,
    normal_cycle_start_time,
    admin_start_count,
    admin_cycle_start_time,
)

import memory  # IMPORTANT for modifying global state

IST = ZoneInfo("Asia/Kolkata")
RESET_HOURS = 7


# ===============================
# START COMMAND (STATE MACHINE)
# ===============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global RESET_HOURS

    if not update.message:
        return

    username = update.message.from_user.username or ""
    now = datetime.now(IST)
    is_admin = username in ADMIN_USERNAMES

    # ===============================
    # 1️⃣ FIRST EVER BOOT
    # ===============================

    if not memory.start_boot_done:
        memory.start_boot_done = True

        await update.message.reply_text(
            "Swagat toh kro humara 🗿\n"
            "Aachuka haiiii Lalalalalala ka Sarkaari Bot 🗿 🙈\n"
            "Phool Patte Barsao bhaiii 🗿 🍇\n"
            "Abb Admin pe jo bhaari... uspe chadha dega mai Gaadi 👹\n"
            "Thoda phool barsaake dekho admin pe... ashirvaad kaha kaha se tapakta hai dekh lena 🐣\n\n"
            "Aur mere liye? Na kaan hai na samaan hai...\n"
            "Z+ security mode: sirf admin pe dhyaan hai 🎯\n"
            "(Rocky Bhaiii music, haan pasand h bhai mujhe tu seedha dekhke chal na 😭)\n\n"
            "Toh chaliye shuru krte hai bina kisi bak....loli k 🤓 (gande soch vaale aadmi 👺🫵)"
        )
        
        return

    # ===============================
    # 2️⃣ ADMIN FLOW
    # ===============================

    if is_admin:

        # Reset logic
        if memory.admin_cycle_start_time:
            if now - memory.admin_cycle_start_time >= timedelta(hours=RESET_HOURS):
                memory.admin_start_count = 0
                memory.admin_cycle_start_time = None

        # Behaviour
        if memory.admin_start_count == 0:
            memory.admin_start_count = 1
            memory.admin_cycle_start_time = now

            await update.message.reply_text(
                "Maharaani ji Kripya aap toh aise peeche lath naa maare 🙏"
            )
            return

        elif memory.admin_start_count == 1:
            memory.admin_start_count = 2

            await update.message.reply_text(
                "Thike maii Chup baith gyaa parr aapko bol thodi kuch sktee 😌"
            )
            return

        else:
            return  # silent after 3rd


    # ===============================
    # 3️⃣ NORMAL USER FLOW (GLOBAL)
    # ===============================

    # Reset logic
    if memory.normal_cycle_start_time:
        if now - memory.normal_cycle_start_time >= timedelta(hours=RESET_HOURS):
            memory.normal_start_count = 0
            memory.normal_cycle_start_time = None

    # 2nd time (first after boot) → silent + start cycle
    if memory.normal_start_count == 0:
        memory.normal_start_count = 1
        memory.normal_cycle_start_time = now
        return

    elif memory.normal_start_count == 1:
        memory.normal_start_count = 2

        await update.message.reply_text(
            "Areyyy zinda huuu abb kya ghar pe aake baat kru shant baithh hatt!!"
        )
        return

    elif memory.normal_start_count == 2:
        memory.normal_start_count = 3

        await update.message.reply_text(
            "Areyyy firr Danda ghusata haii andheyyy Hu toh yahii Kya chaiyee!!"
        )
        return

    elif memory.normal_start_count == 3:
        memory.normal_start_count = 4

        await update.message.reply_text(
            "Arey ye konse Aam k khajoor hai fir dabata hai... abb kuch bolega hi nhii hatt gende"
        )
        return

    else:
        return  # silent from 6th onward


# ===============================
# WELCOME NEW MEMBERS
# ===============================

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.new_chat_members:
        return

    for member in update.message.new_chat_members:

        name = member.first_name

        welcome_message = (
            f"👋 Welcome {name}!\n\n"
            "📚 This is a JEE 2026 focused group.\n"
            "⚠️ Discipline matters here.\n"
            "⏳ Countdown is active.\n\n"
            "Focus on PYQs. Avoid distractions."
        )

        await update.message.reply_text(welcome_message)


# ===============================
# MESSAGE HANDLER
# ===============================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Safety first
    if not update.message or not update.message.text:
        return

    message = update.message.text
    lower_msg = message.lower()

    bot_username = context.bot.username.lower()
    greetings = ["hi", "hello", "hey", "hii", "helo"]

    # Bot tag + greeting detection
    if f"@{bot_username}" in lower_msg and any(word in lower_msg for word in greetings):
        await update.message.reply_text(
            "Bhaii Bnane vale ko Bulaa usne reply hi set nhi kiya mai Barbola thodi hu khudse bolne lagu... Koii na hota hai broh Paani peele. Wallah Hu Alyam 😭=="
        )
        return

    username = update.message.from_user.username or ""
    user_id = update.message.from_user.id

    # Admin Protection
    protection_response = analyze_admin_message(message, username, user_id)
    if protection_response:
        await update.message.reply_text(protection_response)

    # Discipline System
    discipline_response = check_discipline(username)
    if discipline_response:
        await update.message.reply_text(discipline_response)


# ===============================
# WEEKLY QUESTION INITIALIZER
# ===============================

async def weekly_question_initializer(context: ContextTypes.DEFAULT_TYPE):

    schedule = generate_week_schedule()
    job_queue = context.application.job_queue

    for scheduled_time in schedule:

        if scheduled_time not in scheduled_question_times:
            scheduled_question_times.append(scheduled_time)

            job_queue.run_once(
                send_weekly_question,
                when=scheduled_time,
                name=f"weekly_question_{scheduled_time}"
            )


# ===============================
# MAIN ENTRY POINT
# ===============================

def main():

    print("Booting GroupKaSarkarBot...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    )

    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member)
    )

    job_queue = app.job_queue

    job_queue.run_daily(
        send_daily_countdown,
        time=time(hour=6, minute=0, second=0),
        name="jee_daily_countdown"
    )

    job_queue.run_daily(
        weekly_question_initializer,
        time=time(hour=0, minute=5, second=0),
        name="weekly_question_initializer"
    )

    print("All Systems Active.")
    app.run_polling()


if __name__ == "__main__":
    main()