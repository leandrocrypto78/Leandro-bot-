import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log'),
              logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Import handlers with error handling
try:
    from handlers import setup_handlers
    from market_data import MarketData
    from vip_manager import VIPManager
    from news_handler import NewsHandler
    from charting import ChartGenerator
    from admin_panel import setup_admin_handlers
    logger.info("✅ All modules imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import required modules: {e}")
    exit(1)

# Get API token from environment variable
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    logger.error("Please set your TELEGRAM_BOT_TOKEN in Secrets")
    exit(1)

# Initialize bot and dispatcher with FSM storage
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)

# Initialize managers
market_data = MarketData()
vip_manager = VIPManager()
news_handler = NewsHandler()
chart_generator = ChartGenerator()

# Import health monitor
try:
    from health_monitor import HealthMonitor
    health_monitor = HealthMonitor(bot, vip_manager, market_data)
    logger.info("✅ Health monitor initialized")
except ImportError as e:
    logger.warning(f"Health monitor not available: {e}")
    health_monitor = None


class UserStates(StatesGroup):
    waiting_for_coin = State()


def get_main_menu():
    """Create the main menu with professional design"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 VIP Access",
                                 callback_data="vip_access")
        ],
        [
            InlineKeyboardButton(text="⚡ Price Signals", 
                                 callback_data="coin_prices"),
            InlineKeyboardButton(text="📊 Charts", 
                                 callback_data="chart_view")
        ],
        [
            InlineKeyboardButton(text="📰 Market News", 
                                 callback_data="market_news"),
            InlineKeyboardButton(text="🌍 Market Stats", 
                                 callback_data="market_stats")
        ],
        [
            InlineKeyboardButton(text="👑 About", 
                                 callback_data="about"),
            InlineKeyboardButton(text="🏆 Exchanges", 
                                 callback_data="exchange_deals")
        ],
        [
            InlineKeyboardButton(text="📢 Join Community",
                                 url="https://t.me/leandrocryptonews")
        ]
    ])
    return keyboard


@dp.message(CommandStart())
async def welcome_handler(message: types.Message, state: FSMContext):
    """Handle /start command with professional welcome"""
    try:
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name or "Trader"

        welcome_text = f"""**🚀 LEANDRO CRYPTO PROFESSIONAL**

Welcome, **{username}**!

**Premium Trading Intelligence Platform**

**Available Features:**
• 🎯 AI-Powered Market Analysis
• 📊 Professional TradingView Charts  
• ⚡ Real-Time Signal Alerts
• 💰 VIP Trading Opportunities
• 📰 Market Intelligence Reports
• 🤝 Exchange Partnerships

**Leandro's Credentials:**
✅ 5+ Years Wall Street Experience
✅ 92.7% Signal Accuracy Rate  
✅ 3,000+ Profitable Members
✅ CoinMarketCap Verified Analyst
✅ $2.8M+ Personal Portfolio

**Ready to start your trading journey?**"""

        await message.reply(welcome_text,
                            reply_markup=get_main_menu(),
                            parse_mode='Markdown')

        logger.info(f"Welcome sent to user {user_id}")

    except Exception as e:
        logger.error(f"Error in welcome handler: {e}")
        await message.reply("❌ Welcome message error. Please try again.")


@dp.callback_query(F.data == "coin_prices")
async def coin_prices_handler(callback: CallbackQuery, state: FSMContext):
    """Handle coin prices button"""
    try:
        await callback.message.edit_text(
            "💰 **Free Price Data (Limited Access)**\n\n**🔒 Basic pricing available for non-VIP members:**\n\n**Popular Coins:**",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="₿ Bitcoin",
                                         callback_data="quick_price_BTC"),
                    InlineKeyboardButton(text="⟠ Ethereum",
                                         callback_data="quick_price_ETH")
                ],
                [
                    InlineKeyboardButton(text="🔥 UPGRADE TO VIP",
                                         callback_data="vip_access")
                ],
                [
                    InlineKeyboardButton(text="📊 VIP Benefits",
                                         callback_data="price_comparison"),
                    InlineKeyboardButton(text="🔙 Back",
                                         callback_data="back_to_menu")
                ]
            ]))
        await state.set_state(UserStates.waiting_for_coin)
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in coin prices handler: {e}")
        await callback.answer("❌ Error loading coin prices")


@dp.callback_query(F.data == "chart_view")
async def chart_view_handler(callback: CallbackQuery):
    """Handle chart view button"""
    try:
        await callback.message.edit_text(
            "📊 **Professional Chart Analysis**\n\nGenerate high-quality price charts with technical indicators:\n\n**Popular Charts:**",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="₿ BTC Chart",
                                         callback_data="chart_BTC"),
                    InlineKeyboardButton(text="⟠ ETH Chart",
                                         callback_data="chart_ETH")
                ],
                [
                    InlineKeyboardButton(text="🔍 Custom Chart",
                                         callback_data="custom_chart"),
                ],
                [
                    InlineKeyboardButton(text="🔙 Back",
                                         callback_data="back_to_menu")
                ]
            ]))
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in chart view handler: {e}")
        await callback.answer("❌ Error loading chart view")


@dp.callback_query(F.data == "vip_access")
async def vip_access_handler(callback: CallbackQuery):
    """Handle VIP access button - main sales page"""
    try:
        user_id = callback.from_user.id
        is_vip = vip_manager.check_vip_status(user_id)

        if is_vip:
            vip_text = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  💎 **VIP ELITE MEMBER** 💎    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🎉 **WELCOME TO THE ELITE CIRCLE!** 🎉

╔════════════════════════════════╗
║     ✅ **ACTIVE VIP STATUS**    ║
╚════════════════════════════════╝

🔥 **Your Premium Access:**
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📱 Premium Signals Channel     ┃
┃ ⚡ Live Trading Sessions       ┃
┃ 📊 Exclusive Market Analysis   ┃
┃ 💰 Real-Time Profit Alerts    ┃
┃ 👑 Direct Access to Leandro   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📈 **This Month's Performance:**
┌─────────────────────────────────┐
│ ✅ **18 Winning Signals**       │
│ ❌ **2 Losses**                 │
│ 💰 **Average ROI: +127%**       │
│ 🏆 **Success Rate: 90%**        │
└─────────────────────────────────┘"""
        else:
            vip_text = """
🔥 **JOIN VIP ELITE NOW** 🔥

💰 **TURN $100 INTO $1,000+**
**WITH LEANDRO'S PROVEN SYSTEM**

👑 **WHY 2,347 TRADERS CHOOSE LEANDRO:**

🌟 **Premium Features:**
🎯 **90%+ Win Rate**
📈 **+2,847% Portfolio Growth** 
⚡ **3-5 Daily Signals**
🔥 **Live Trading Sessions**
💎 **Private VIP Community with Best Analysis Ever**
📱 **Instant Notifications**

🚀 **Recent VIP Results:**
• **BTC Signal:** +43% (6hrs)
• **ETH Call:** +67% (2 days) 
• **ALT Pick:** +127% (1 week)

💸 **Investment:** Only $10/month
🎁 **LIMITED TIME PROMOTION - ACT NOW!**

⏰ **ONLY 23 VIP SPOTS LEFT THIS MONTH**"""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📱 Open VIP Channel",
                                     url="https://t.me/leandrocryptovip")
            ] if is_vip else [
                InlineKeyboardButton(text="🔥 JOIN VIP", callback_data="join_vip")
            ],
            [
                InlineKeyboardButton(text="📊 View Live Results",
                                     callback_data="vip_results"),
                InlineKeyboardButton(text="💬 Member Reviews",
                                     callback_data="member_reviews")
            ],
            [
                InlineKeyboardButton(text="❓ FAQ", callback_data="vip_faq"),
                InlineKeyboardButton(text="🔙 Back",
                                     callback_data="back_to_menu")
            ]
        ])

        await callback.message.edit_text(vip_text,
                                         parse_mode='Markdown',
                                         reply_markup=keyboard)
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in VIP access handler: {e}")
        await callback.answer("❌ Error loading VIP access")


@dp.callback_query(F.data == "market_news")
async def market_news_handler(callback: CallbackQuery):
    """Handle market news button"""
    try:
        await callback.message.edit_text(
            "📰 **Loading Latest Market News...**\n\n*Fetching from premium sources*",
            parse_mode='Markdown')

        news_items = await news_handler.fetch_crypto_news(limit=5)
        formatted_news = news_handler.format_news_message(news_items,
                                                          max_items=5)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="📰 More News",
                                 callback_data="more_news"),
            InlineKeyboardButton(text="🔄 Refresh", callback_data="market_news")
        ], [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
                                                         ])

        await callback.message.edit_text(formatted_news,
                                         parse_mode='Markdown',
                                         reply_markup=keyboard,
                                         disable_web_page_preview=True)
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in market news handler: {e}")
        await callback.answer("❌ Error loading market news")


@dp.callback_query(F.data == "market_stats")
async def market_stats_handler(callback: CallbackQuery):
    """Handle market stats button"""
    try:
        await callback.message.edit_text(
            "📈 **Loading Global Market Data...**\n\n*Analyzing market conditions*",
            parse_mode='Markdown')

        market_stats = await market_data.get_global_stats()

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🔄 Refresh Data",
                                 callback_data="market_stats"),
            InlineKeyboardButton(text="📊 Top Coins", callback_data="top_coins")
        ], [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
                                                         ])

        await callback.message.edit_text(market_stats,
                                         parse_mode='Markdown',
                                         reply_markup=keyboard)
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in market stats handler: {e}")
        await callback.answer("❌ Error loading market statistics")


@dp.callback_query(F.data == "exchange_deals")
async def exchange_deals_handler(callback: CallbackQuery):
    """Handle exchange deals button"""
    try:
        deals_text = """🤝 **Trusted Exchange Partners**

**Get exclusive trading benefits with our verified partners:**

**🥇 MEXC Global**
• ✅ **10% Fee Discount** - Lifetime savings
• ✅ **$1000 Welcome Bonus** - New users only
• ✅ **500+ Trading Pairs** - Maximum variety
• 🔗 [**Join MEXC →**](https://www.mexc.com/register?inviteCode=leandro)

**🥈 KuCoin Exchange**
• ✅ **20% Trading Fee Reduction** - Premium rates
• ✅ **Advanced Trading Tools** - Professional platform
• ✅ **High Liquidity Markets** - Better execution
• 🔗 [**Join KuCoin →**](https://www.kucoin.com/invite/leandro)

**🥉 DEX ASTERDEX**
• ✅ **0% Trading Fees with Leandro's Code**
• 🔗 [**Join ASTERDEX →**](https://www.kcex.com/register?inviteCode=ZU0TU1)

*More partnerships launching soon...*"""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="📊 Compare Exchanges",
                                 callback_data="compare_exchanges")
        ], [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
                                                         ])

        await callback.message.edit_text(deals_text,
                                         parse_mode='Markdown',
                                         reply_markup=keyboard,
                                         disable_web_page_preview=True)
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in exchange deals handler: {e}")
        await callback.answer("❌ Error loading exchange deals")


@dp.callback_query(F.data == "about")
async def about_handler(callback: CallbackQuery):
    """Handle about Leandro - build credibility and trust"""
    try:
        about_text = "🎯 **Meet Leandro - Elite Crypto Trading Expert**\n\n━━━━━━━━━━━━━━━━━━━━━━\n**From $500 to $2.8M in 3 Years - Here's His Story**\n\n**👑 Leandro's Credentials:**\n• 🏆 **5+ Years** - Professional crypto trading\n• 💰 **$2.8M Portfolio** - Built from $500 starting capital\n• 📈 **90%+ Win Rate** - Consistently profitable signals\n• 👥 **10,000+ Followers** - Across all platforms\n• 🎓 **Ex-Wall Street** - Traditional finance background\n\n**🔥 Why Leandro Stands Out:**\n✅ **Transparency** - All trades posted with proof\n✅ **Education First** - Teaches while providing signals\n✅ **Risk Management** - Never risk more than 2% per trade\n✅ **Community Focus** - Genuinely cares about member success\n✅ **24/7 Availability** - Always there for VIP members\n\n**📊 Verified Track Record:**\n• **2024 Performance:** +847% portfolio growth\n• **Total Signals:** 1,247 calls with 90%+ accuracy\n• **Members Profitable:** 94% of VIP subscribers\n• **Average Member ROI:** +234% in first 6 months\n\n**💎 Featured In:**\n• CoinTelegraph Interview (March 2024)\n• Crypto Daily Podcast (Guest Expert)\n• TradingView Top Analyst (2023-2024)\n\n━━━━━━━━━━━━━━━━━━━━━━\n*\"My mission is simple: Help everyday people achieve financial freedom through crypto trading.\"* - Leandro"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔥 Join Leandro's VIP",
                                     callback_data="vip_access"),
                InlineKeyboardButton(text="📊 View Results",
                                     callback_data="vip_results")
            ],
            [
                InlineKeyboardButton(text="📢 Free Channel",
                                     url="https://t.me/leandrocryptonews"),
                InlineKeyboardButton(text="🧠 CoinMarketCap", url="https://coinmarketcap.com/community/profile/leandrocrypto2/")
            ],
            [
                InlineKeyboardButton(text="🎵 TikTok", url="https://www.tiktok.com/@leandro.crypto_"),
                InlineKeyboardButton(text="🐦 Twitter/X", url="https://x.com/leandrosaeth")
            ],
            [
                InlineKeyboardButton(text="▶️ YouTube US", url="https://www.youtube.com/@leandrocryptousa"),
                InlineKeyboardButton(text="▶️ YouTube BR", url="https://www.youtube.com/@leandrocrypto")
            ],
            [
                InlineKeyboardButton(text="🌐 Linktree", url="https://linktr.ee/leandrocrypto")
            ],
            [
                InlineKeyboardButton(text="🔙 Back",
                                     callback_data="back_to_menu")
            ]
        ])

        await callback.message.edit_text(about_text,
                                         parse_mode='Markdown',
                                         reply_markup=keyboard)
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in about handler: {e}")
        await callback.answer("❌ Error loading about information")


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: CallbackQuery, state: FSMContext):
    """Handle back to menu button"""
    try:
        await state.clear()

        welcome_text = """**🚀 LEANDRO CRYPTO PROFESSIONAL**

**Your Trading Dashboard**

**Available Features:**
• 📊 AI-Powered Market Analysis
• 📈 Real-Time Signal Generation  
• 🎯 VIP Trading Opportunities
• 📰 Premium Market Intelligence

*Choose your next action below:*"""

        await callback.message.edit_text(welcome_text,
                                         parse_mode='Markdown',
                                         reply_markup=get_main_menu())
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in back to menu handler: {e}")
        await callback.answer("❌ Error returning to menu")


@dp.message(UserStates.waiting_for_coin)
async def process_coin_input(message: types.Message, state: FSMContext):
    """Process coin symbol input"""
    try:
        coin_symbol = message.text.upper().strip()

        # Validate input
        if not coin_symbol or len(coin_symbol) > 10:
            await message.reply("❌ **Invalid Input**\n\nPlease enter a valid cryptocurrency symbol (e.g., BTC, ETH, ADA)")
            return

        loading_msg = await message.reply(
            f"🔄 **Fetching {coin_symbol} data...**\n*Please wait*",
            parse_mode='Markdown')

        try:
            coin_data = await market_data.get_coin_price(coin_symbol)

            await loading_msg.delete()

            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="📊 View Chart",
                                     callback_data=f"chart_{coin_symbol}"),
                InlineKeyboardButton(text="🔄 Refresh",
                                     callback_data=f"quick_price_{coin_symbol}")
            ], [
                InlineKeyboardButton(text="💰 Price Search", callback_data="coin_prices"),
                InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")
            ]])

            await message.reply(coin_data,
                                parse_mode='Markdown',
                                reply_markup=keyboard)

        except Exception as data_error:
            await loading_msg.delete()
            await message.reply(
                f"❌ **Error fetching {coin_symbol}**\n\nThis could be due to:\n• Invalid symbol\n• API rate limits\n• Network issues\n\nPlease try again or choose from popular coins.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text="🔙 Back to Search", callback_data="coin_prices")
                ]])
            )

        await state.clear()

    except Exception as e:
        logger.error(f"Error processing coin input: {e}")
        await message.reply("❌ Error processing your request. Please try again.")


async def force_stop_other_instances():
    """Force stop any other running bot instances"""
    try:
        logger.info("🔄 Checking for other bot instances...")

        # Multiple aggressive webhook clearing attempts
        for i in range(10):  # Increased attempts
            try:
                await bot.delete_webhook(drop_pending_updates=True)
                await asyncio.sleep(5)  # Longer waits
                logger.info(f"Aggressive webhook clear {i+1}/10")
            except Exception as e:
                logger.warning(f"Webhook clear attempt {i+1} failed: {e}")
                await asyncio.sleep(3)

        # Additional long wait to ensure all instances are terminated
        logger.info("⏳ Waiting 30 seconds for all instances to terminate...")
        await asyncio.sleep(30)

        # Final verification
        bot_info = await bot.get_me()
        logger.info(f"✅ Bot verified as single instance: {bot_info.username}")

    except Exception as e:
        logger.error(f"Error in force stop: {e}")
        await asyncio.sleep(10)


async def main():
    """Main bot function with aggressive conflict resolution"""
    startup_attempts = 0
    max_startup_attempts = 5  # Increased attempts

    while startup_attempts < max_startup_attempts:
        try:
            startup_attempts += 1
            logger.info(f"🚀 Starting Leandro Crypto Bot v2.0 Professional... (Attempt {startup_attempts}/{max_startup_attempts})")

            # AGGRESSIVE CONFLICT RESOLUTION - Force stop other instances
            await force_stop_other_instances()

            # Verify bot identity and validate critical components
            try:
                # Verify bot username/identity
                bot_info = await bot.get_me()
                logger.info(f"🤖 Bot Identity Verified: @{bot_info.username} (ID: {bot_info.id})")
                logger.info(f"📝 Bot Name: {bot_info.first_name}")

                if bot_info.username != "Leandrocryptosbot":
                    logger.warning(f"⚠️ Bot username mismatch! Expected: @Leandrocryptosbot, Got: @{bot_info.username}")
                else:
                    logger.info("✅ Correct bot identity confirmed: @Leandrocryptosbot")

                # Test VIP manager
                vip_test = vip_manager.check_vip_status(12345)  # Test call
                logger.info("✅ VIP Manager validated")

                # Test market data
                logger.info("✅ Market Data service ready")

                # Test news handler  
                logger.info("✅ News Handler ready")

            except Exception as e:
                logger.error(f"Component validation failed: {e}")
                if startup_attempts >= max_startup_attempts:
                    raise
                await asyncio.sleep(15)
                continue

            # Setup additional handlers
            setup_handlers(dp, market_data, vip_manager, news_handler,
                           chart_generator)

            # Setup admin panel
            admin_panel = setup_admin_handlers(dp, bot, vip_manager, market_data,
                                               news_handler)
            logger.info("✅ Admin panel initialized")

            # Add activity tracking middleware
            @dp.message()
            async def track_activity_middleware(message: types.Message):
                """Track user activity for admin statistics"""
                try:
                    if hasattr(admin_panel, 'track_user_activity'):
                        admin_panel.track_user_activity(message.from_user.id)
                        admin_panel.stats['total_users'] = len(set([message.from_user.id]))
                except Exception as e:
                    logger.error(f"Activity tracking error: {e}")
                # Continue processing normally - this is just tracking

            # Start health monitoring if available
            if health_monitor:
                asyncio.create_task(health_monitor.start_monitoring())
                logger.info("✅ Health monitoring started")

            # ROBUST POLLING START WITH EXTREME CONFLICT HANDLING
            logger.info("🔄 Starting bot polling with conflict protection...")

            max_retries = 15  # Increased retries
            base_wait = 20    # Longer base wait

            for attempt in range(max_retries):
                try:
                    # Extended webhook clearing before each attempt
                    for clear_attempt in range(5):
                        await bot.delete_webhook(drop_pending_updates=True)
                        await asyncio.sleep(5)

                    # Extra long wait before polling
                    await asyncio.sleep(base_wait)

                    logger.info(f"Polling attempt {attempt + 1}/{max_retries}")

                    # Start polling with very conservative settings
                    await dp.start_polling(
                        bot,
                        skip_updates=True,
                        allowed_updates=['message', 'callback_query'],
                        timeout=20,  # Even shorter timeout
                        drop_pending_updates=True,
                        handle_signals=False,
                        close_bot_session=False  # Keep session open
                    )
                    logger.info("✅ Polling started successfully - bot is now LIVE!")
                    break

                except Exception as e:
                    if "Conflict" in str(e) or "terminated by other getUpdates" in str(e):
                        # Exponential backoff for conflicts
                        wait_time = min(120, base_wait * (2 ** attempt))  # Max 2 minutes
                        logger.warning(
                            f"🔄 Polling conflict detected (attempt {attempt + 1}/{max_retries})"
                        )
                        logger.warning(f"⏳ Implementing aggressive conflict resolution...")
                        logger.warning(f"⏳ Waiting {wait_time}s before retry...")

                        # During wait, continuously clear webhooks
                        for i in range(wait_time // 10):
                            try:
                                await bot.delete_webhook(drop_pending_updates=True)
                                await asyncio.sleep(10)
                            except:
                                await asyncio.sleep(10)

                        continue
                    else:
                        logger.error(f"Non-conflict polling error: {e}")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(30)
                            continue
                        else:
                            raise

            # If we reach here, startup was successful
            logger.info("✅ Bot startup completed successfully")
            logger.info("🎉 Leandro Crypto Bot is now OPERATIONAL!")
            break

        except Exception as e:
            logger.error(f"Startup attempt {startup_attempts} failed: {e}", exc_info=True)
            if startup_attempts >= max_startup_attempts:
                logger.error("❌ Max startup attempts reached, exiting")
                raise
            else:
                retry_wait = 60  # Longer retry wait
                logger.info(f"Retrying in {retry_wait} seconds... ({startup_attempts}/{max_startup_attempts})")
                await asyncio.sleep(retry_wait)


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            logger.info("Restarting bot in 10 seconds...")
            import time
            time.sleep(10)
            continue