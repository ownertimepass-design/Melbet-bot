# 🤖 MB_P2P_bot — সেটআপ গাইড
## Melbet Affiliate Telegram Bot

---

## ধাপ ১ — BotFather থেকে Token নিন

1. Telegram-এ **@BotFather** সার্চ করুন
2. `/newbot` টাইপ করুন
3. বটের নাম দিন: `MB P2P Bot`
4. Username দিন: `MB_P2P_bot`
5. BotFather আপনাকে একটি **Token** দেবে
   - দেখতে এরকম: `7xxxxxxxxx:AAxxxxxxxxxxxxxxxxxxxxxx`
6. এই Token টি কপি করুন

---

## ধাপ ২ — .env ফাইলে Token বসান

`.env` ফাইল খুলুন এবং লিখুন:
```
BOT_TOKEN=7xxxxxxxxx:AAxxxxxxxxxxxxxxxxxxxxxx
ADMIN_ID=আপনার_টেলিগ্রাম_আইডি
```

> আপনার Telegram ID জানতে @userinfobot-এ `/start` দিন

---

## ধাপ ৩ — ফ্রিতে হোস্ট করুন (Railway.app)

### Railway দিয়ে (সবচেয়ে সহজ — ফ্রি):

1. **https://railway.app** এ যান
2. GitHub দিয়ে Sign Up করুন
3. "New Project" → "Deploy from GitHub repo"
4. এই ফোল্ডারটি GitHub-এ আপলোড করুন
5. Environment Variables-এ BOT_TOKEN ও ADMIN_ID বসান
6. Deploy করুন — বট ২৪/৭ চলবে! ✅

### অথবা Render.com দিয়ে:
1. **https://render.com** এ যান
2. New → Web Service
3. GitHub repo সংযুক্ত করুন
4. Start Command: `python bot.py`
5. Environment Variables যোগ করুন

---

## ধাপ ৪ — লোকালি চালান (PC/Laptop থেকে)

```bash
# Python ইনস্টল থাকতে হবে (python.org থেকে)

# ১. এই ফোল্ডারে Terminal/CMD খুলুন
cd melbet_bot

# ২. Dependencies ইনস্টল করুন
pip install -r requirements.txt

# ৩. বট চালান
python bot.py
```

---

## বট কী কী করতে পারে:

| ফিচার | বিবরণ |
|-------|-------|
| 🎰 রেজিস্ট্রেশন | Melbet Affiliate লিংকে পাঠায় |
| ⚽ লাইভ স্কোর | স্পোর্টস অডস ও লিংক |
| 🖼 ব্যানার | প্রমো মিডিয়া গাইড |
| 💳 ডিপোজিট | bKash/Nagad/Crypto গাইড |
| 💸 উইথড্র | উইথড্র পদ্ধতি |
| 🆘 সাপোর্ট | সমস্যার সমাধান |
| 📩 Admin Alert | নতুন ইউজার নোটিফিকেশন |

---

## কমান্ড লিস্ট:

```
/start    — বট শুরু
/help     — সাহায্য
/register — রেজিস্ট্রেশন
/live     — লাইভ স্কোর
/deposit  — ডিপোজিট গাইড
/withdraw — উইথড্র গাইড
/banner   — ব্যানার
/support  — সাপোর্ট
/about    — আমাদের সম্পর্কে
```

---

## সমস্যা হলে যোগাযোগ করুন ✉️
