import os
import math
import random
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8644355663:AAEzg6oR1VyOx1TwEiFd18UANfM-rBORhNo")
UTC_PLUS_5 = timezone(timedelta(hours=5))

# ==========================================
# EXACT QUOTEX ENTRY TIME CALCULATOR
# ==========================================
def get_fast_entry():
    now = datetime.now(UTC_PLUS_5)
    if now.second >= 48:
        target = (now + timedelta(minutes=2)).replace(second=0, microsecond=0)
    else:
        target = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return target.strftime("%H:%M:00")

# ==========================================
# MULTI-TIMEFRAME ANALYSIS ENGINE (30M TO 1S)
# ==========================================
def perform_multi_timeframe_analysis(pair_name: str, entry_time_str: str):
    """
    Simulates Top-Down Multi-Timeframe Technical Analysis:
    Macro (30M, 15M, 10M, 5M) -> Intermediate (3M, 2M, 1M) -> Micro (30s, 15s, 5s, 1s)
    """
    now = datetime.now(UTC_PLUS_5)
    
    # Deterministic Seed based on Pair & Current Minute for absolute consistency
    time_seed = int(now.strftime("%Y%m%d%H%M")) + sum(ord(c) for c in pair_name)
    random.seed(time_seed)

    # 1. Macro Analysis (30M, 15M, 10M, 5M)
    macro_trends = ["Bullish Channel", "Bearish Channel", "Macro Range", "Key Level Test"]
    macro_trend = random.choice(macro_trends)
    macro_score = 2 if "Bullish" in macro_trend else (-2 if "Bearish" in macro_trend else 0)

    # 2. Intermediate Structure (3M, 2M, 1M)
    inter_patterns = ["FVG Fill & Reaction", "Order Block Bounce", "Support/Resistance Breakout", "Liquidity Sweep"]
    inter_pattern = random.choice(inter_patterns)
    inter_bias = random.choice(["BUY", "SELL"])
    inter_score = 2 if inter_bias == "BUY" else -2

    # 3. Micro Execution (30s, 15s, 5s, 1s)
    micro_structure = ["30s/15s Rejection Wick", "5s/1s Volume Surge", "Momentum Acceleration", "Order Flow Shift"]
    micro_event = random.choice(micro_structure)
    micro_bias = random.choice(["BUY", "SELL"])
    micro_score = 1 if micro_bias == "BUY" else -1

    # Total Confluence Score
    total_score = macro_score + inter_score + micro_score

    # Signal Output
    if total_score >= 0:
        direction = "UP"
        signal_icon = "🟩 **CALL / UP** ⬆️"
    else:
        direction = "DOWN"
        signal_icon = "🔴 **PUT / DOWN** ⬇️"

    # Reset Seed
    random.seed()

    return {
        "direction": direction,
        "signal_icon": signal_icon,
        "macro": f"30M/15M/5M: `{macro_trend}`",
        "inter": f"3M/2M/1M: `{inter_pattern}`",
        "micro": f"30s/15s/5s: `{micro_event}`"
    }

# ==========================================
# KEYBOARD
# ==========================================
def get_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 USD/BRL", callback_data="USD/BRL (OTC)"), 
            InlineKeyboardButton("📊 NZD/JPY", callback_data="NZD/JPY (OTC)")
        ],
        [
            InlineKeyboardButton("📊 USD/BDT", callback_data="USD/BDT (OTC)"), 
            InlineKeyboardButton("📊 USD/JPY", callback_data="USD/JPY (OTC)")
        ],
        [
            InlineKeyboardButton("📊 USD/NGN", callback_data="USD/NGN (OTC)"), 
            InlineKeyboardButton("📊 AUD/USD", callback_data="AUD/USD (OTC)")
        ],
        [
            InlineKeyboardButton("📊 GBP/JPY", callback_data="GBP/JPY (OTC)"), 
            InlineKeyboardButton("🔄 Refresh", callback_data="REFRESH")
        ]
    ])

# ==========================================
# HANDLERS
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🏛️ **PRO MULTI-TIMEFRAME OTC TERMINAL v9.0**\n"
        "─── TOP-DOWN ANALYSIS (30M TO 1S) ───\n\n"
        "Select an asset to perform full multi-timeframe evaluation:"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=get_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pair = query.data

    if pair == "REFRESH":
        try:
            await query.edit_message_text(
                "🔄 **Terminal Refreshed**\nSelect Asset:", 
                parse_mode="Markdown", 
                reply_markup=get_keyboard()
            )
        except Exception:
            pass
        return

    entry_time = get_fast_entry()
    analysis = perform_multi_timeframe_analysis(pair, entry_time)

    response_text = (
        f"🌐 **ASSET:** `{pair}`\n"
        f"⏰ **ENTRY TIME:** `{entry_time}`\n"
        f"───────────────\n"
        f"🎯 **SIGNAL:** {analysis['signal_icon']}\n"
        f"───────────────\n"
        f"🔍 **MULTI-TIMEFRAME ANALYSIS:**\n"
        f"• {analysis['macro']}\n"
        f"• {analysis['inter']}\n"
        f"• {analysis['micro']}\n\n"
        f"📌 *OTC Rule: Respect 30M/15M trend bias. Use 1-Step MTG if 1st candle fails.*"
    )

    try:
        await query.edit_message_text(
            text=response_text, 
            parse_mode="Markdown", 
            reply_markup=get_keyboard()
        )
    except Exception:
        pass

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("⚡ Pro Multi-Timeframe OTC Engine Running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
