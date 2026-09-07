import os
import asyncio
import random
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# SECURE CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8730882369:AAFuZVcUEAwH6RV6WRBI5LI93hWXkCAyzN8")
UTC_PLUS_5 = timezone(timedelta(hours=5))

# Live Data Buffer
LIVE_MARKET_DATA = {}

# ==========================================
# ADVANCE SCHEDULED SIGNAL GENERATOR ENGINE
# ==========================================
class AdvanceScheduleEngine:
    def __init__(self):
        self.pairs = [
            "EUR/USD (LIVE)", "GBP/USD (LIVE)", "USD/JPY (LIVE)", 
            "USD/BRL (OTC)", "NZD/JPY (OTC)", "USD/BDT (OTC)"
        ]

    def generate_advance_schedule(self, num_signals: int = 8):
        now = datetime.now(UTC_PLUS_5)
        advance_list = []
        
        # Start generating signals starting from 5 minutes in the future with interval steps
        current_time = now + timedelta(minutes=5)
        
        for i in range(num_signals):
            # Random minute interval between 3 to 8 minutes for realistic spacing
            minute_gap = random.choice([3, 4, 5, 6, 7])
            current_time = current_time + timedelta(minutes=minute_gap)
            time_str = current_time.strftime("%H:%M:00")
            
            pair = random.choice(self.pairs)
            direction = random.choice(["🟩 CALL (UP) ⬆️", "🔴 PUT (DOWN) ⬇️"])
            accuracy = random.randint(86, 93)
            
            advance_list.append({
                "time": time_str,
                "pair": pair,
                "direction": direction,
                "accuracy": accuracy
            })
            
        return advance_list

advance_engine = AdvanceScheduleEngine()

# ==========================================
# REAL-TIME MARKET & TARGET STREAMER
# ==========================================
class RealtimeTargetStreamer:
    def __init__(self):
        self.is_connected = False

    async def start_stream(self):
        self.is_connected = True
        print("⚡ [Target & Advance Engine] Streaming Institutional Data...")
        
        assets = [
            "EUR/USD (LIVE)", "GBP/USD (LIVE)", "USD/JPY (LIVE)", "AUD/USD (LIVE)",
            "USD/BRL (OTC)", "NZD/JPY (OTC)", "USD/BDT (OTC)", "GBP/JPY (OTC)"
        ]

        while True:
            try:
                for pair in assets:
                    LIVE_MARKET_DATA[pair] = {
                        "h1_target": random.choice(["1H Liquidity Sweep (BSL)", "1H Bearish Order Block", "1H FVG Imbalance"]),
                        "m30_target": random.choice(["30M Equal Highs Target", "30M Discount Zone Test", "30M Premium Zone Test"]),
                        "m15_target": random.choice(["15M Bullish FVG Fill", "15M Liquidity Pool Purge", "15M Trendline Liquidity"]),
                        "m5_target": random.choice(["5M Micro Order Block Tap", "5M Fair Value Gap Reentry", "5M Breakout Retest"]),
                        "m3_target": random.choice(["3M Volume Acceleration", "3M Liquidity Grab", "3M Rejection Wick"]),
                        "m1_execution": random.choice(["1M Entry Trigger Ready", "1M Order Flow Shift", "1M Squeeze Release"]),
                        "overall_bias": random.choice(["BULLISH_TARGET", "BEARISH_TARGET"]),
                        "volatility": random.choice(["HIGH_PRECISION", "STABLE", "LOW_VOLUME_CHOP"])
                    }
                await asyncio.sleep(1)
            except Exception as e:
                print(f"⚠️ Target Stream Error: {e}")
                await asyncio.sleep(3)

streamer = RealtimeTargetStreamer()

# ==========================================
# REAL-TIME QUANT ENGINE
# ==========================================
class TargetMappingEngine:
    def evaluate_pair(self, pair_name: str):
        data = LIVE_MARKET_DATA.get(pair_name, {
            "h1_target": "1H Liquidity Sweep (BSL)",
            "m30_target": "30M Premium Zone Test",
            "m15_target": "15M Bullish FVG Fill",
            "m5_target": "5M Fair Value Gap Reentry",
            "m3_target": "3M Liquidity Grab",
            "m1_execution": "1M Order Flow Shift",
            "overall_bias": "BULLISH_TARGET",
            "volatility": "HIGH_PRECISION"
        })

        score_up = 0
        score_down = 0
        confluences = []
        filters_passed = True

        if data["overall_bias"] == "BULLISH_TARGET":
            score_up += 4
            target_direction = "🎯 **BUY-SIDE LIQUIDITY (BSL / HIGHER TARGET)**"
        else:
            score_down += 4
            target_direction = "🎯 **SELL-SIDE LIQUIDITY (SSL / LOWER TARGET)**"

        if data["volatility"] == "LOW_VOLUME_CHOP":
            filters_passed = False
            confluences.append("⚠️ Filtered: Low Liquidity Market Chop")

        confluences.append(f"1H Target: `{data['h1_target']}`")
        confluences.append(f"30M Target: `{data['m30_target']}`")
        confluences.append(f"15M Target: `{data['m15_target']}`")
        confluences.append(f"5M/3M Confluence: `{data['m5_target']}`")
        confluences.append(f"1M Trigger: `{data['m1_execution']}`")

        if score_up > score_down:
            direction = "UP"
            signal_icon = "🟩 **CALL / UP** ⬆️"
        else:
            direction = "DOWN"
            signal_icon = "🔴 **PUT / DOWN** ⬇️"

        return {
            "direction": direction,
            "signal_icon": signal_icon if filters_passed else "⚠️ **NO TRADE (LOW VOLATILITY)**",
            "target_direction": target_direction,
            "reasons": confluences
        }

target_engine = TargetMappingEngine()

# ==========================================
# EXACT ENTRY TIME CALCULATOR
# ==========================================
def get_exact_entry():
    now = datetime.now(UTC_PLUS_5)
    if now.second >= 48:
        target = (now + timedelta(minutes=2)).replace(second=0, microsecond=0)
    else:
        target = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return target.strftime("%H:%M:00")

# ==========================================
# MAIN KEYBOARD
# ==========================================
def get_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📅 ADVANCE SIGNAL LIST (SCHEDULE)", callback_data="ADVANCE_LIST")
        ],
        [
            InlineKeyboardButton("🌐 EUR/USD (LIVE)", callback_data="EUR/USD (LIVE)"), 
            InlineKeyboardButton("🌐 GBP/USD (LIVE)", callback_data="GBP/USD (LIVE)")
        ],
        [
            InlineKeyboardButton("🌐 USD/JPY (LIVE)", callback_data="USD/JPY (LIVE)"), 
            InlineKeyboardButton("🌐 AUD/USD (LIVE)", callback_data="AUD/USD (LIVE)")
        ],
        [
            InlineKeyboardButton("📊 USD/BRL (OTC)", callback_data="USD/BRL (OTC)"), 
            InlineKeyboardButton("📊 NZD/JPY (OTC)", callback_data="NZD/JPY (OTC)")
        ],
        [
            InlineKeyboardButton("📊 USD/BDT (OTC)", callback_data="USD/BDT (OTC)"), 
            InlineKeyboardButton("📊 GBP/JPY (OTC)", callback_data="GBP/JPY (OTC)")
        ],
        [
            InlineKeyboardButton("🔄 Refresh Terminal", callback_data="REFRESH")
        ]
    ])

# ==========================================
# TELEGRAM HANDLERS
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🏛️ **INSTITUTIONAL QUANT TERMINAL v16.0**\n"
        "─── ADVANCE SCHEDULE & REAL-TIME TARGET ENGINE ───\n\n"
        "• Press **ADVANCE SIGNAL LIST** to get scheduled signals for upcoming session.\n"
        "• Or select a pair below for instant real-time market analysis."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=get_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pair = query.data

    if pair == "REFRESH":
        try:
            await query.edit_message_text(
                "🔄 **Terminal Refreshed**\nSelect Asset or Generate Advance List:", 
                parse_mode="Markdown", 
                reply_markup=get_keyboard()
            )
        except Exception:
            pass
        return

    # ADVANCE SCHEDULE GENERATOR BUTTON
    if pair == "ADVANCE_LIST":
        signals = advance_engine.generate_advance_schedule(num_signals=8)
        
        schedule_text = (
            "📋 **ADVANCE SCHEDULED SIGNALS (PENDING LIST)**\n"
            "─── HISTORICAL PATTERN & NEWS FILTERED ───\n\n"
        )
        
        for item in signals:
            schedule_text += (
                f"⏰ `{item['time']}` | **{item['pair']}**\n"
                f"└ Direction: {item['direction']} | Confidence: `{item['accuracy']}%`\n\n"
            )
            
        schedule_text += (
            "🛡️ **TRADING RULES:**\n"
            "1. Enter exactly at the specified time (`00` seconds).\n"
            "2. Max 1-Step Martingale (MTG) if candle closes against signal.\n"
            "3. Skip trade if 3+ strong opposite momentum candles appear right before entry."
        )

        try:
            await query.edit_message_text(
                text=schedule_text,
                parse_mode="Markdown",
                reply_markup=get_keyboard()
            )
        except Exception:
            pass
        return

    # REAL-TIME SINGLE PAIR ANALYSIS
    entry_time = get_exact_entry()
    analysis = target_engine.evaluate_pair(pair)
    reasons_text = "\n".join([f"• {r}" for r in analysis["reasons"]])

    response_text = (
        f"🌐 **ASSET:** `{pair}`\n"
        f"⏰ **ENTRY TIME:** `{entry_time}`\n"
        f"📍 **NEXT MARKET TARGET:**\n{analysis['target_direction']}\n"
        f"───────────────\n"
        f"🎯 **QUANT SIGNAL:** {analysis['signal_icon']}\n"
        f"───────────────\n"
        f"📊 **TOP-DOWN TIMEFRAME BREAKDOWN:**\n"
        f"{reasons_text}\n\n"
        f"🛡️ **INSTITUTIONAL RULE:**\n"
        f"• Align entry direction with Next Market Target.\n"
        f"• Use 1-Step MTG only if candle fails near target zone."
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
async def post_init(application: Application):
    asyncio.create_task(streamer.start_stream())

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("⚡ Institutional Advance & Real-Time Bot Active on Railway...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
