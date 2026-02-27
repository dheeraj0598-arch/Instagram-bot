import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime

# =============================================
# SETTINGS — reads from Railway environment variables
# =============================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
YOUR_CHAT_ID = int(os.environ.get("CHAT_ID", "987654321"))
# =============================================

# /start command — shows main menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != YOUR_CHAT_ID:
        return  # Block other users

    keyboard = [
        [InlineKeyboardButton("▶️ Run DM Script Now", callback_data="run_dms")],
        [InlineKeyboardButton("📊 View DM Report", callback_data="dm_report")],
        [InlineKeyboardButton("📋 Request Log File", callback_data="view_log")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to your Instagram Automation Bot!\n\n"
        "Bot is running 24/7 on Railway ✅\n\n"
        "What do you want to do?",
        reply_markup=reply_markup
    )

# Handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "run_dms":
        await query.edit_message_text(
            "📡 Command sent to your PC!\n\n"
            "Make sure listener.py is running on your PC.\n"
            "DM script will start shortly ⏳"
        )
        await context.bot.send_message(
            chat_id=YOUR_CHAT_ID,
            text="✅ DM trigger command sent!\n\nYour PC listener will start instagram_dm_v6.py now."
        )

    elif query.data == "dm_report":
        await context.bot.send_message(
            chat_id=YOUR_CHAT_ID,
            text="📊 *DM Report*\n\n"
                 "To see your DM log, make sure listener.py is running on your PC.\n"
                 "Type /report to request latest log from PC.",
            parse_mode="Markdown"
        )

    elif query.data == "view_log":
        await context.bot.send_message(
            chat_id=YOUR_CHAT_ID,
            text="📋 Log file is stored on your PC.\n\n"
                 "Make sure listener.py is running on your PC to receive log files."
        )

# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != YOUR_CHAT_ID:
        return
    await update.message.reply_text(
        "✅ *Bot Status*\n\n"
        "🟢 Telegram Bot: ONLINE (Railway)\n"
        "🖥️ PC Script: Check your PC\n\n"
        "Bot is running 24/7 on Railway!",
        parse_mode="Markdown"
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != YOUR_CHAT_ID:
        return
    await update.message.reply_text(
        "📖 *Available Commands:*\n\n"
        "/start — Show main menu\n"
        "/status — Check bot status\n"
        "/help — Show this help\n\n"
        "🖥️ *PC Listener Commands:*\n"
        "Make sure listener.py is running on your PC for full functionality!",
        parse_mode="Markdown"
    )

# Send daily report automatically at 9 PM
async def send_daily_report(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now().strftime("%d %b %Y")
    await context.bot.send_message(
        chat_id=YOUR_CHAT_ID,
        text=f"📊 *Daily Report — {today}*\n\n"
             f"🤖 Bot is running 24/7 ✅\n"
             f"Check your PC listener for DM stats!\n\n"
             f"Keep growing! 🚀",
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Daily report at 9 PM
    app.job_queue.run_daily(
        send_daily_report,
        time=datetime.strptime("21:00", "%H:%M").time()
    )

    print("✅ Bot is running on Railway!")
    app.run_polling()

if __name__ == "__main__":
    main()
