import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
LINK = "https://melbet.com"

WELCOME = "🎯 *স্বাগতম MB P2P Bot-এ!*\n\n🏆 *Melbet Official Affiliate Bot*\n\n✅ রেজিস্ট্রেশন\n✅ লাইভ স্কোর\n✅ ব্যানার/ভিডিও\n✅ ডিপোজিট/উইথড্র\n✅ সাপোর্ট\n\nমেনু থেকে বেছে নিন 👇"

def mkb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 রেজিস্ট্রেশন", callback_data="reg")],
        [InlineKeyboardButton("⚽ লাইভ স্কোর", callback_data="live"), InlineKeyboardButton("🖼 ব্যানার", callback_data="banner")],
        [InlineKeyboardButton("💳 ডিপোজিট", callback_data="dep"), InlineKeyboardButton("💸 উইথড্র", callback_data="with")],
        [InlineKeyboardButton("🆘 সাপোর্ট", callback_data="sup"), InlineKeyboardButton("ℹ️ সম্পর্কে", callback_data="about")],
    ])

def bk():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 মেইন মেনু", callback_data="home")]])

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, parse_mode=ParseMode.MARKDOWN, reply_markup=mkb())

async def btn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    if d == "home":
        await q.edit_message_text(WELCOME, parse_mode=ParseMode.MARKDOWN, reply_markup=mkb())
    elif d == "reg":
        await q.edit_message_text("🎰 *রেজিস্ট্রেশন*\n\n✅ ১০০% বোনাস\n✅ bKash/Nagad\n✅ ২৪/৭ সাপোর্ট", parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ রেজিস্ট্রেশন করুন!", url=LINK)],[InlineKeyboardButton("🔙 মেইন মেনু", callback_data="home")]]))
    elif d == "live":
        await q.edit_message_text("⚽ *লাইভ স্কোর*\n\n🔴 ১০০+ ম্যাচ লাইভ!\n⚽ Football | 🏏 Cricket\n🏀 Basketball | 🎾 Tennis", parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔴 লাইভ দেখুন", url=LINK)],[InlineKeyboardButton("🔙 মেইন মেনু", callback_data="home")]]))
    elif d == "banner":
        await q.edit_message_text("🖼 *ব্যানার ও ভিডিও*\n\n📘 Facebook Banner\n📸 Instagram Post\n🎬 Promo Video\n\n📩 Admin-এ যোগাযোগ করুন।", parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 Admin", url="https://t.me/MB_P2P_Support")],[InlineKeyboardButton("🔙 মেইন মেনু", callback_data="home")]]))
    elif d == "dep":
        await q.edit_message_text("💳 *ডিপোজিট গাইড*\n\n✅ bKash/Nagad/Rocket\n✅ USDT/BTC\n\n⚡ সর্বনিম্ন: ৳200\n⚡ সময়: ১-৫ মিনিট", parse_mode=ParseMode.MARKDOWN, reply_markup=bk())
    elif d == "with":
        await q.edit_message_text("💸 *উইথড্র গাইড*\n\n✅ bKash: ৳200-৳50,000\n✅ Nagad: ৳200-৳50,000\n\n⏱ ১৫ মিনিট-২৪ ঘণ্টা", parse_mode=ParseMode.MARKDOWN, reply_markup=bk())
    elif d == "sup":
        await q.edit_message_text("🆘 *সাপোর্ট*\n\n💬 @MB\\_P2P\\_Support\n🕐 ২৪/৭", parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 সাপোর্ট", url="https://t.me/MB_P2P_Support")],[InlineKeyboardButton("🔙 মেইন মেনু", callback_data="home")]]))
    elif d == "about":
        await q.edit_message_text("ℹ️ *MB P2P Bot*\n\n🤖 Melbet Affiliate\n🌍 Bangladesh\n⚠️ ১৮+ only", parse_mode=ParseMode.MARKDOWN, reply_markup=bk())

async def msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("মেনু থেকে বেছে নিন 👇", reply_markup=mkb())

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("BOT_TOKEN not set!")
        exit(1)
    print("Bot starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CallbackQueryHandler(btn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
    print("Bot running!")
    app.run_polling()
