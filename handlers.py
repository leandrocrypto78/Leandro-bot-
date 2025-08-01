import logging
from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

logger = logging.getLogger(__name__)

def setup_handlers(dp: Dispatcher, market_data, vip_manager, news_handler, chart_generator):
    """Setup all bot handlers"""
    
    @dp.callback_query(F.data.startswith("quick_price_"))
    async def quick_price_handler(callback: CallbackQuery):
        """Handle quick price requests"""
        try:
            coin = callback.data.replace("quick_price_", "").upper()
            await callback.answer(f"💰 {coin} price: $45,000 (Sample data)")
        except Exception as e:
            logger.error(f"Error in quick price handler: {e}")
            await callback.answer("❌ Error getting price")
    
    @dp.callback_query(F.data.startswith("chart_"))
    async def chart_handler(callback: CallbackQuery):
        """Handle chart requests"""
        try:
            coin = callback.data.replace("chart_", "").upper()
            await callback.answer(f"📊 {coin} chart generated (Sample)")
        except Exception as e:
            logger.error(f"Error in chart handler: {e}")
            await callback.answer("❌ Error generating chart")
    
    @dp.callback_query(F.data == "custom_chart")
    async def custom_chart_handler(callback: CallbackQuery):
        """Handle custom chart requests"""
        try:
            await callback.answer("📊 Custom chart feature coming soon!")
        except Exception as e:
            logger.error(f"Error in custom chart handler: {e}")
            await callback.answer("❌ Error with custom chart")
    
    @dp.callback_query(F.data == "price_comparison")
    async def price_comparison_handler(callback: CallbackQuery):
        """Handle price comparison requests"""
        try:
            await callback.answer("💰 VIP members get real-time prices!")
        except Exception as e:
            logger.error(f"Error in price comparison handler: {e}")
            await callback.answer("❌ Error with price comparison")
    
    logger.info("✅ Handlers setup completed")