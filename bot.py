import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")
URL = "https://melbet.com"

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 Register Now", url=URL)],
        [InlineKeyboardButton("⚽ Live Score", callback_data="live"),
         InlineKeyboardButton("🖼 Banner", callback_data="banner")],
        [InlineKeyboardButton("💳 Deposit", callback_data="dep"),
         InlineKeyboardButton("💸 Withdraw", callback_data="wit")],
        [InlineKeyboardButton("🆘 Support", callback_data="sup")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 Welcome to MB P2P Bot!\n\nMelbet Official Affiliate Bot\n\nChoose from menu below:",
        reply_markup=menu()
    )

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    back = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="home")]])
    
    if q.data == "home":
        await q.edit_message_text("🎯 Welcome to MB P2P Bot!\n\nChoose from menu below:", reply_markup=menu())
    elif q.data == "live":
        await q.edit_message_text("⚽ Live Score & Odds\n\n100+ matches live now!\nFootball | Cricket | Basketball", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔴 View Live Odds", url=URL)],[InlineKeyboardButton("🔙 Back", callback_data="home")]]))
    elif q.data == "banner":
        await q.edit_message_text("🖼 Promo Banners\n\nFacebook | Instagram | Video\n\nContact admin for custom banners.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 Admin", url="https://t.me/MB_P2P_Support")],[InlineKeyboardButton("🔙 Back", callback_data="home")]]))
    elif q.data == "dep":
        await q.edit_message_text("💳 Deposit Guide\n\nbKash / Nagad / Rocket\nUSDT / BTC\n\nMin: 200 BDT\nTime: 1-5 min", reply_markup=back)
    elif q.data == "wit":
        await q.edit_message_text("💸 Withdraw Guide\n\nbKash: 200-50000 BDT\nNagad: 200-50000 BDT\n\nTime: 15min-24hr", reply_markup=back)
    elif q.data == "sup":
        await q.edit_message_text("🆘 Support\n\n@MB_P2P_Support\n24/7 available",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Support", url="https://t.me/MB_P2P_Support")],[InlineKeyboardButton("🔙 Back", callback_data="home")]]))

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choose from menu:", reply_markup=menu())

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(CallbackQueryHandler(callback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
print("Bot started!")
app.run_polling()
