#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║        MB_P2P_bot — Melbet Affiliate     ║
║     Telegram Bot by @MB_P2P_bot          ║
╚══════════════════════════════════════════╝
"""

import logging
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ParseMode
import aiohttp

# ─── CONFIG ───────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
AFFILIATE_LINK = "https://bit.ly/Official_melbetaffiliates"
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # আপনার Telegram User ID

# ─── LOGGING ──────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ══════════════════════════════════════════
#           TEXTS (Bangla + English)
# ══════════════════════════════════════════

WELCOME_TEXT = """
🎯 *স্বাগতম MB P2P Bot-এ!*
*Welcome to MB P2P Bot!*

━━━━━━━━━━━━━━━━━━━━━━
🏆 *Melbet Official Affiliate Bot*
━━━━━━━━━━━━━━━━━━━━━━

আমি আপনাকে সাহায্য করব:
I can help you with:

✅ Melbet-এ রেজিস্ট্রেশন
✅ লাইভ স্কোর ও অডস
✅ প্রমো ব্যানার ডাউনলোড
✅ ডিপোজিট/উইথড্র গাইড
✅ সাপোর্ট ও হেল্প

নিচের মেনু থেকে বেছে নিন 👇
*Choose from the menu below* 👇
"""

REGISTER_TEXT = """
🎰 *Melbet-এ রেজিস্ট্রেশন করুন!*
*Register on Melbet!*

━━━━━━━━━━━━━━━━━━━━━━

📌 *কেন Melbet?*
• ✅ ১০০+ স্পোর্টস মার্কেট
• ✅ লাইভ বেটিং সুবিধা
• ✅ ক্যাসিনো ও স্লটস
• ✅ দ্রুত পেমেন্ট (bKash/Nagad/Rocket)
• ✅ ২৪/৭ বাংলা সাপোর্ট
• ✅ ১০০% ওয়েলকাম বোনাস

━━━━━━━━━━━━━━━━━━━━━━
🎁 *নতুন একাউন্টে পাচ্ছেন:*
💰 ১ম ডিপোজিটে ১০০% বোনাস
🎯 ফ্রি বেট অফার
━━━━━━━━━━━━━━━━━━━━━━

👇 নিচের বাটনে ক্লিক করে রেজিস্ট্রেশন করুন:
"""

DEPOSIT_TEXT = """
💳 *ডিপোজিট গাইড | Deposit Guide*
━━━━━━━━━━━━━━━━━━━━━━

🇧🇩 *বাংলাদেশ থেকে ডিপোজিট:*

1️⃣ *bKash / Nagad / Rocket*
   • Melbet অ্যাপ খুলুন
   • Deposit → Mobile Banking
   • পরিমাণ লিখুন → Pay করুন

2️⃣ *ক্রিপ্টো (USDT/BTC)*
   • Deposit → Cryptocurrency
   • ওয়ালেট অ্যাড্রেস কপি করুন
   • ট্রান্সফার করুন

3️⃣ *ব্যাংক ট্রান্সফার*
   • Deposit → Bank Transfer
   • ব্যাংক ডিটেইলস দিন

━━━━━━━━━━━━━━━━━━━━━━
⚡ *সর্বনিম্ন ডিপোজিট: ৳200*
⚡ *প্রসেসিং টাইম: ১-৫ মিনিট*
━━━━━━━━━━━━━━━━━━━━━━

❓ সমস্যা? নিচে সাপোর্টে যোগাযোগ করুন।
"""

WITHDRAW_TEXT = """
💸 *উইথড্র গাইড | Withdraw Guide*
━━━━━━━━━━━━━━━━━━━━━━

📋 *উইথড্র করার নিয়ম:*

1️⃣ Melbet অ্যাপ/সাইটে লগইন করুন
2️⃣ Wallet → Withdrawal-এ যান
3️⃣ পেমেন্ট মেথড সিলেক্ট করুন
4️⃣ পরিমাণ লিখুন
5️⃣ Confirm করুন

━━━━━━━━━━━━━━━━━━━━━━
✅ *bKash:* ৳200 – ৳50,000
✅ *Nagad:* ৳200 – ৳50,000
✅ *Rocket:* ৳200 – ৳25,000
✅ *USDT:* $10+
━━━━━━━━━━━━━━━━━━━━━━

⏱ *প্রসেসিং টাইম: ১৫ মিনিট – ২৪ ঘণ্টা*

⚠️ *গুরুত্বপূর্ণ:* উইথড্রের আগে KYC ভেরিফিকেশন সম্পন্ন করুন।
"""

LIVE_SCORE_TEXT = """
⚽ *লাইভ স্কোর ও অডস*
*Live Score & Odds*

━━━━━━━━━━━━━━━━━━━━━━

🔴 *এখন লাইভ ম্যাচ দেখতে:*
Melbet অ্যাপে লগইন করুন
→ Live → Sports

━━━━━━━━━━━━━━━━━━━━━━
🏆 *আজকের বড় ম্যাচ:*

⚽ Premier League
🏀 NBA Basketball  
🎾 ATP Tennis
🏏 Cricket — IPL/BCB
🏐 Volleyball

━━━━━━━━━━━━━━━━━━━━━━
📱 *রিয়েল-টাইম অডস পেতে:*
নিচের বাটনে ক্লিক করুন 👇
"""

BANNER_TEXT = """
🖼 *প্রমো ব্যানার ও মিডিয়া*
*Promo Banners & Media*

━━━━━━━━━━━━━━━━━━━━━━

📥 *ডাউনলোড করুন:*

🔷 *সোশ্যাল মিডিয়া ব্যানার*
• Facebook Cover (1640×924)
• Instagram Post (1080×1080)
• Instagram Story (1080×1920)

🔷 *ভিডিও কন্টেন্ট*
• 15s প্রমো ভিডিও
• 30s ফুল ভিডিও

🔷 *টেক্সট ব্যানার*
• বাংলা ভার্সন
• English ভার্সন

━━━━━━━━━━━━━━━━━━━━━━
💡 *আপনার Affiliate Link যোগ করুন*
এবং সোশ্যাল মিডিয়ায় শেয়ার করুন!

📩 *কাস্টম ব্যানার চাইলে অ্যাডমিনকে জানান।*
"""

SUPPORT_TEXT = """
🆘 *সাপোর্ট ও হেল্প | Support & Help*
━━━━━━━━━━━━━━━━━━━━━━

📞 *যোগাযোগ করুন:*

💬 *Telegram:* @MB_P2P_Support
📧 *Email:* support@melbet.com
🌐 *Live Chat:* Melbet ওয়েবসাইটে

━━━━━━━━━━━━━━━━━━━━━━
🕐 *সাপোর্ট টাইম:*
২৪ ঘণ্টা / ৭ দিন

━━━━━━━━━━━━━━━━━━━━━━
❓ *সাধারণ সমস্যা:*
• একাউন্ট ভেরিফিকেশন
• ডিপোজিট সমস্যা
• উইথড্র দেরি
• বোনাস পাচ্ছেন না
• পাসওয়ার্ড রিসেট

নির্দিষ্ট সমস্যার জন্য নিচের বাটনে ক্লিক করুন 👇
"""

ABOUT_TEXT = """
ℹ️ *MB P2P Bot সম্পর্কে*
━━━━━━━━━━━━━━━━━━━━━━

🤖 *Bot:* @MB_P2P_bot
🏆 *Platform:* Melbet Official Affiliate
🌍 *দেশ:* Bangladesh & Global
📅 *ভার্সন:* v1.0

━━━━━━━━━━━━━━━━━━━━━━
*সেবাসমূহ:*
✅ Melbet রেজিস্ট্রেশন সহায়তা
✅ লাইভ স্কোর আপডেট
✅ প্রমো ব্যানার
✅ ডিপোজিট/উইথড্র গাইড
✅ ২৪/৭ সাপোর্ট

━━━━━━━━━━━━━━━━━━━━━━
⚠️ *দায়িত্বশীলভাবে বেটিং করুন।*
*Bet Responsibly. 18+ Only.*
"""


# ══════════════════════════════════════════
#              KEYBOARDS
# ══════════════════════════════════════════

def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🎰 রেজিস্ট্রেশন করুন", callback_data="register"),
        ],
        [
            InlineKeyboardButton("⚽ লাইভ স্কোর/অডস", callback_data="live_score"),
            InlineKeyboardButton("🖼 ব্যানার/ভিডিও", callback_data="banner"),
        ],
        [
            InlineKeyboardButton("💳 ডিপোজিট গাইড", callback_data="deposit"),
            InlineKeyboardButton("💸 উইথড্র গাইড", callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton("🆘 সাপোর্ট", callback_data="support"),
            InlineKeyboardButton("ℹ️ আমাদের সম্পর্কে", callback_data="about"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def register_keyboard():
    keyboard = [
        [InlineKeyboardButton("✅ এখনই রেজিস্ট্রেশন করুন!", url=AFFILIATE_LINK)],
        [InlineKeyboardButton("📱 Melbet App ডাউনলোড", url="https://melbet.com/app")],
        [InlineKeyboardButton("🔙 মেইন মেনু", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def live_score_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔴 Live Odds দেখুন", url=AFFILIATE_LINK)],
        [InlineKeyboardButton("⚽ Football", callback_data="sport_football"),
         InlineKeyboardButton("🏏 Cricket", callback_data="sport_cricket")],
        [InlineKeyboardButton("🏀 Basketball", callback_data="sport_basketball"),
         InlineKeyboardButton("🎾 Tennis", callback_data="sport_tennis")],
        [InlineKeyboardButton("🔙 মেইন মেনু", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def banner_keyboard():
    keyboard = [
        [InlineKeyboardButton("📘 Facebook Banner", callback_data="banner_fb")],
        [InlineKeyboardButton("📸 Instagram Banner", callback_data="banner_ig")],
        [InlineKeyboardButton("🎬 Promo Video", callback_data="banner_video")],
        [InlineKeyboardButton("📩 কাস্টম ব্যানার (Admin)", callback_data="banner_custom")],
        [InlineKeyboardButton("🔙 মেইন মেনু", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def support_keyboard():
    keyboard = [
        [InlineKeyboardButton("💬 Telegram সাপোর্ট", url="https://t.me/MB_P2P_Support")],
        [InlineKeyboardButton("❓ একাউন্ট সমস্যা", callback_data="issue_account"),
         InlineKeyboardButton("💰 পেমেন্ট সমস্যা", callback_data="issue_payment")],
        [InlineKeyboardButton("🎁 বোনাস সমস্যা", callback_data="issue_bonus"),
         InlineKeyboardButton("🔑 পাসওয়ার্ড রিসেট", callback_data="issue_password")],
        [InlineKeyboardButton("🔙 মেইন মেনু", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_keyboard():
    keyboard = [[InlineKeyboardButton("🔙 মেইন মেনু", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)


# ══════════════════════════════════════════
#              HANDLERS
# ══════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.first_name}) started the bot")

    # Admin notification
    if ADMIN_ID and context.bot:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🆕 নতুন ইউজার!\nName: {user.full_name}\nID: {user.id}\nUsername: @{user.username or 'N/A'}"
            )
        except Exception:
            pass

    await update.message.reply_text(
        text=WELCOME_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
📖 *সাহায্য | Help*
━━━━━━━━━━━━━━━━━━

*কমান্ড লিস্ট:*
/start — বট শুরু করুন
/help — সাহায্য
/register — রেজিস্ট্রেশন
/live — লাইভ স্কোর
/deposit — ডিপোজিট গাইড
/withdraw — উইথড্র গাইড
/banner — ব্যানার ডাউনলোড
/support — সাপোর্ট
/about — আমাদের সম্পর্কে
    """
    await update.message.reply_text(
        text=help_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )


async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=REGISTER_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=register_keyboard(),
    )


async def live_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=LIVE_SCORE_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=live_score_keyboard(),
    )


async def deposit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=DEPOSIT_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )


async def withdraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=WITHDRAW_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )


async def banner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=BANNER_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=banner_keyboard(),
    )


async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=SUPPORT_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=support_keyboard(),
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=ABOUT_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )


# ══════════════════════════════════════════
#          CALLBACK QUERY HANDLER
# ══════════════════════════════════════════

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── MAIN MENU ──
    if data == "main_menu":
        await query.edit_message_text(
            text=WELCOME_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu_keyboard(),
        )

    # ── REGISTER ──
    elif data == "register":
        await query.edit_message_text(
            text=REGISTER_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=register_keyboard(),
        )

    # ── LIVE SCORE ──
    elif data == "live_score":
        await query.edit_message_text(
            text=LIVE_SCORE_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=live_score_keyboard(),
        )

    # ── SPORTS ──
    elif data == "sport_football":
        text = """⚽ *Football লাইভ অডস*\n━━━━━━━━━━━━━━━━━━\n\nসরাসরি Melbet-এ লগইন করে\nলাইভ ফুটবল অডস দেখুন!\n\n🔴 এখন ১০০+ ম্যাচ লাইভ চলছে!"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔴 লাইভ ফুটবল দেখুন", url=AFFILIATE_LINK)],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="live_score")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    elif data == "sport_cricket":
        text = """🏏 *Cricket লাইভ অডস*\n━━━━━━━━━━━━━━━━━━\n\nIPL, BCB, T20 World Cup\nসব ম্যাচের লাইভ অডস পাচ্ছেন Melbet-এ!"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔴 লাইভ ক্রিকেট দেখুন", url=AFFILIATE_LINK)],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="live_score")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    elif data == "sport_basketball":
        text = """🏀 *Basketball লাইভ অডস*\n━━━━━━━━━━━━━━━━━━\n\nNBA সহ সকল বাস্কেটবল\nম্যাচের লাইভ অডস পাচ্ছেন!"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔴 লাইভ দেখুন", url=AFFILIATE_LINK)],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="live_score")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    elif data == "sport_tennis":
        text = """🎾 *Tennis লাইভ অডস*\n━━━━━━━━━━━━━━━━━━\n\nATP, WTA সব টুর্নামেন্টের\nলাইভ অডস পাচ্ছেন Melbet-এ!"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔴 লাইভ দেখুন", url=AFFILIATE_LINK)],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="live_score")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    # ── BANNER ──
    elif data == "banner":
        await query.edit_message_text(
            text=BANNER_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=banner_keyboard(),
        )

    elif data == "banner_fb":
        text = """📘 *Facebook Banner*\n━━━━━━━━━━━━━━━━━━\n\n✅ সাইজ: 1640 × 924 px\n✅ ফরম্যাট: JPG / PNG\n✅ ভাষা: বাংলা + English\n\n📩 Admin-এর কাছ থেকে ব্যানার পেতে:\n@MB_P2P_Support-এ মেসেজ করুন।"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 ব্যানার পেতে Admin-এ যোগাযোগ করুন", url="https://t.me/MB_P2P_Support")],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="banner")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    elif data == "banner_ig":
        text = """📸 *Instagram Banner*\n━━━━━━━━━━━━━━━━━━\n\n✅ Post: 1080 × 1080 px\n✅ Story: 1080 × 1920 px\n✅ Reel Thumbnail\n\n📩 Admin-এর কাছ থেকে পেতে যোগাযোগ করুন।"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Admin-এ যোগাযোগ করুন", url="https://t.me/MB_P2P_Support")],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="banner")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    elif data == "banner_video":
        text = """🎬 *Promo Video*\n━━━━━━━━━━━━━━━━━━\n\n✅ 15 সেকেন্ড শর্ট ভিডিও\n✅ 30 সেকেন্ড ফুল প্রমো\n✅ বাংলা ভয়েসওভার সহ\n\n📩 ভিডিও পেতে Admin-এ যোগাযোগ করুন।"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 ভিডিও পেতে যোগাযোগ করুন", url="https://t.me/MB_P2P_Support")],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="banner")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    elif data == "banner_custom":
        text = """🎨 *কাস্টম ব্যানার*\n━━━━━━━━━━━━━━━━━━\n\nআপনার পছন্দমতো কাস্টম ব্যানার তৈরি করতে Admin-এ যোগাযোগ করুন।\n\n📋 *কী কী জানাবেন:*\n• ব্যানারের সাইজ\n• প্ল্যাটফর্ম (FB/IG/Web)\n• ভাষা (বাংলা/English)\n• বিশেষ কিছু চাইলে"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Admin-এ যোগাযোগ করুন", url="https://t.me/MB_P2P_Support")],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="banner")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    # ── DEPOSIT / WITHDRAW ──
    elif data == "deposit":
        await query.edit_message_text(
            text=DEPOSIT_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )

    elif data == "withdraw":
        await query.edit_message_text(
            text=WITHDRAW_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )

    # ── SUPPORT ──
    elif data == "support":
        await query.edit_message_text(
            text=SUPPORT_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=support_keyboard(),
        )

    elif data == "issue_account":
        text = """👤 *একাউন্ট সমস্যা*\n━━━━━━━━━━━━━━━━━━\n\n❓ সাধারণ সমস্যা ও সমাধান:\n\n🔸 *ভেরিফিকেশন হচ্ছে না?*\n→ NID/Passport ছবি পুনরায় আপলোড করুন\n\n🔸 *লগইন হচ্ছে না?*\n→ পাসওয়ার্ড রিসেট করুন\n\n🔸 *একাউন্ট ব্লক?*\n→ Support-এ যোগাযোগ করুন\n\n📩 সমাধান না হলে Admin-এ যোগাযোগ করুন।"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Admin-এ যোগাযোগ করুন", url="https://t.me/MB_P2P_Support")],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="support")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    elif data == "issue_payment":
        text = """💳 *পেমেন্ট সমস্যা*\n━━━━━━━━━━━━━━━━━━\n\n🔸 *ডিপোজিট যোগ হচ্ছে না?*\n→ ১৫ মিনিট অপেক্ষা করুন\n→ Transaction ID সংরক্ষণ করুন\n→ Support-এ ID পাঠান\n\n🔸 *উইথড্র দেরি হচ্ছে?*\n→ ২৪ ঘণ্টা অপেক্ষা করুন\n→ KYC ভেরিফাই আছে কিনা চেক করুন\n\n📩 এখনো সমস্যা? Admin-এ যোগাযোগ করুন।"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Admin-এ যোগাযোগ করুন", url="https://t.me/MB_P2P_Support")],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="support")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    elif data == "issue_bonus":
        text = """🎁 *বোনাস সমস্যা*\n━━━━━━━━━━━━━━━━━━\n\n🔸 *ওয়েলকাম বোনাস পাননি?*\n→ প্রথম ডিপোজিটের ৩০ মিনিট পর দেখুন\n→ Bonuses সেকশনে গিয়ে Activate করুন\n\n🔸 *ফ্রি বেট পাননি?*\n→ Promo Code সঠিকভাবে ব্যবহার করুন\n→ Support-এ যোগাযোগ করুন\n\n📩 আরো সাহায্যের জন্য Admin-এ যোগাযোগ করুন।"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Admin-এ যোগাযোগ করুন", url="https://t.me/MB_P2P_Support")],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="support")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    elif data == "issue_password":
        text = """🔑 *পাসওয়ার্ড রিসেট*\n━━━━━━━━━━━━━━━━━━\n\n📋 *পাসওয়ার্ড রিসেট করার নিয়ম:*\n\n1️⃣ Melbet লগইন পেজে যান\n2️⃣ "Forgot Password?" এ ক্লিক করুন\n3️⃣ Email/Phone নম্বর দিন\n4️⃣ OTP কোড দিন\n5️⃣ নতুন পাসওয়ার্ড সেট করুন\n\n📩 সমস্যা হলে Admin-এ যোগাযোগ করুন।"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Melbet-এ যান", url=AFFILIATE_LINK)],
            [InlineKeyboardButton("💬 Admin-এ যোগাযোগ করুন", url="https://t.me/MB_P2P_Support")],
            [InlineKeyboardButton("🔙 পিছনে যান", callback_data="support")],
        ])
        await query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    # ── ABOUT ──
    elif data == "about":
        await query.edit_message_text(
            text=ABOUT_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )


# ══════════════════════════════════════════
#         MESSAGE HANDLER (Text)
# ══════════════════════════════════════════

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    text = update.message.text.lower()

    if any(w in text for w in ["register", "রেজিস্ট্রেশন", "সাইনআপ", "signup", "join"]):
        await update.message.reply_text(REGISTER_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=register_keyboard())
    elif any(w in text for w in ["live", "score", "স্কোর", "লাইভ", "odds", "অডস"]):
        await update.message.reply_text(LIVE_SCORE_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=live_score_keyboard())
    elif any(w in text for w in ["deposit", "ডিপোজিট", "টাকা দিন"]):
        await update.message.reply_text(DEPOSIT_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=back_keyboard())
    elif any(w in text for w in ["withdraw", "উইথড্র", "টাকা তুলুন"]):
        await update.message.reply_text(WITHDRAW_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=back_keyboard())
    elif any(w in text for w in ["banner", "ব্যানার", "video", "ভিডিও"]):
        await update.message.reply_text(BANNER_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=banner_keyboard())
    elif any(w in text for w in ["support", "সাপোর্ট", "help", "হেল্প", "সাহায্য"]):
        await update.message.reply_text(SUPPORT_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=support_keyboard())
    else:
        await update.message.reply_text(
            "🤖 আমি বুঝতে পারিনি। নিচের মেনু থেকে বেছে নিন:\n*I didn't understand. Please use the menu:*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu_keyboard(),
        )


# ══════════════════════════════════════════
#                  MAIN
# ══════════════════════════════════════════

def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ BOT_TOKEN সেট করুন! .env ফাইলে BOT_TOKEN=আপনার_টোকেন লিখুন।")
        return

    print("🚀 MB_P2P_bot চালু হচ্ছে...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("register", register_command))
    app.add_handler(CommandHandler("live", live_command))
    app.add_handler(CommandHandler("deposit", deposit_command))
    app.add_handler(CommandHandler("withdraw", withdraw_command))
    app.add_handler(CommandHandler("banner", banner_command))
    app.add_handler(CommandHandler("support", support_command))
    app.add_handler(CommandHandler("about", about_command))

    # Buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ Bot চালু আছে! থামাতে Ctrl+C চাপুন।")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
