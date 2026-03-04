import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN")
URL = "https://melbet.com"

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 Register Now", url=URL)],
        [InlineKeyboardButton("⚽ Live Score", callback_data="live"), InlineKeyboardButton("🖼 Banner", callback_data="banner")],
        [InlineKeyboardButton("💳 Deposit", callback_data="dep"), InlineKeyboardButton("💸 Withdraw", callback_data="wit")],
        [InlineKeyboardButton("🆘 Support", callback_data="sup")],
    ])

def back():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="home")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 Welcome to MB P2P Bot!\nMelbet Official Affiliate\n\nChoose from menu:", reply_markup=menu())

async def cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "home":
        await q.edit_message_text("🎯 Welcome!\nChoose from menu:", reply_markup=menu())
    elif q.data == "live":
        await q.edit_message_text("⚽ Live Score\n100+ matches live!\nFootball | Cricket | Basketball",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔴 View Live", url=URL)],[InlineKeyboardButton("🔙 Back", callback_data="home")]]))
    elif q.data == "banner":
        await q.edit_message_text("🖼 Promo Banners\nFacebook | Instagram | Video",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 Admin", url="https://t.me/MB_P2P_Support")],[InlineKeyboardButton("🔙 Back", callback_data="home")]]))
    elif q.data == "dep":
        await q.edit_message_text("💳 Deposit\nbKash/Nagad/Rocket/USDT\nMin: 200 BDT", reply_markup=back())
    elif q.data == "wit":
        await q.edit_message_text("💸 Withdraw\nbKash/Nagad: 200-50000 BDT", reply_markup=back())
    elif q.data == "sup":
        await q.edit_message_text("🆘 Support: @MB_P2P_Support\n24/7 available",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Support", url="https://t.me/MB_P2P_Support")],[InlineKeyboardButton("🔙 Back", callback_data="home")]]))

async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choose from menu:", reply_markup=menu())

if __name__ == "__main__":
    print("Bot starting...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CallbackQueryHandler(cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
    print("Bot running!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
