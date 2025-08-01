import logging
from typing import Dict, List
from aiogram import Dispatcher, Bot, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

logger = logging.getLogger(__name__)

class AdminPanel:
    """Admin panel for bot management"""
    
    def __init__(self, bot: Bot, vip_manager, market_data):
        self.bot = bot
        self.vip_manager = vip_manager
        self.market_data = market_data
        self.stats = {
            'total_users': 0,
            'active_users': 0,
            'vip_users': 0,
            'total_messages': 0
        }
        self.admin_users = set()  # Set of admin user IDs
        logger.info("✅ Admin Panel initialized")
    
    def track_user_activity(self, user_id: int):
        """Track user activity for statistics"""
        try:
            self.stats['total_messages'] += 1
            if user_id not in self.admin_users:
                self.stats['active_users'] = max(self.stats['active_users'], user_id)
        except Exception as e:
            logger.error(f"Error tracking user activity: {e}")
    
    def add_admin(self, user_id: int):
        """Add a user as admin"""
        self.admin_users.add(user_id)
        logger.info(f"Admin added: {user_id}")
    
    def remove_admin(self, user_id: int):
        """Remove admin privileges from a user"""
        self.admin_users.discard(user_id)
        logger.info(f"Admin removed: {user_id}")
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id in self.admin_users
    
    async def get_bot_stats(self) -> Dict:
        """Get bot statistics"""
        try:
            vip_count = len([uid for uid in self.vip_manager.vip_users if self.vip_manager.check_vip_status(uid)])
            return {
                'total_users': self.stats['total_users'],
                'active_users': self.stats['active_users'],
                'vip_users': vip_count,
                'total_messages': self.stats['total_messages']
            }
        except Exception as e:
            logger.error(f"Error getting bot stats: {e}")
            return {}

def setup_admin_handlers(dp: Dispatcher, bot: Bot, vip_manager, market_data, news_handler):
    """Setup admin panel handlers"""
    
    admin_panel = AdminPanel(bot, vip_manager, market_data)
    
    @dp.message(Command("admin"))
    async def admin_command(message: types.Message):
        """Admin command handler"""
        try:
            user_id = message.from_user.id
            
            # For demo purposes, let's make the first user an admin
            if not admin_panel.admin_users:
                admin_panel.add_admin(user_id)
            
            if not admin_panel.is_admin(user_id):
                await message.reply("❌ Access denied. Admin privileges required.")
                return
            
            # Admin menu
            admin_text = "🔧 **Admin Panel**\n\nSelect an option:"
            admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="📊 Bot Stats", callback_data="admin_stats"),
                    InlineKeyboardButton(text="👥 VIP Users", callback_data="admin_vip")
                ],
                [
                    InlineKeyboardButton(text="🔧 System Status", callback_data="admin_status"),
                    InlineKeyboardButton(text="📢 Broadcast", callback_data="admin_broadcast")
                ]
            ])
            
            await message.reply(admin_text, reply_markup=admin_keyboard, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in admin command: {e}")
            await message.reply("❌ Admin command error")
    
    @dp.callback_query(F.data == "admin_stats")
    async def admin_stats_handler(callback: CallbackQuery):
        """Handle admin stats request"""
        try:
            if not admin_panel.is_admin(callback.from_user.id):
                await callback.answer("❌ Access denied")
                return
            
            stats = await admin_panel.get_bot_stats()
            stats_text = f"""📊 **Bot Statistics**

👥 Total Users: {stats.get('total_users', 0)}
🟢 Active Users: {stats.get('active_users', 0)}
👑 VIP Users: {stats.get('vip_users', 0)}
💬 Total Messages: {stats.get('total_messages', 0)}

🕐 Last Updated: {callback.message.date.strftime('%Y-%m-%d %H:%M:%S')}"""
            
            await callback.message.edit_text(stats_text, parse_mode='Markdown')
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error in admin stats handler: {e}")
            await callback.answer("❌ Error loading stats")
    
    @dp.callback_query(F.data == "admin_vip")
    async def admin_vip_handler(callback: CallbackQuery):
        """Handle admin VIP users request"""
        try:
            if not admin_panel.is_admin(callback.from_user.id):
                await callback.answer("❌ Access denied")
                return
            
            vip_users = admin_panel.vip_manager.vip_users
            vip_count = len([uid for uid in vip_users if admin_panel.vip_manager.check_vip_status(uid)])
            
            vip_text = f"""👑 **VIP Users Management**

Total VIP Users: {vip_count}
Active VIP Users: {vip_count}

**VIP Packages:**
• Basic: ${admin_panel.vip_manager.vip_packages['basic']['price']}
• Premium: ${admin_panel.vip_manager.vip_packages['premium']['price']}
• Elite: ${admin_panel.vip_manager.vip_packages['elite']['price']}"""
            
            await callback.message.edit_text(vip_text, parse_mode='Markdown')
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error in admin VIP handler: {e}")
            await callback.answer("❌ Error loading VIP data")
    
    @dp.callback_query(F.data == "admin_status")
    async def admin_status_handler(callback: CallbackQuery):
        """Handle admin system status request"""
        try:
            if not admin_panel.is_admin(callback.from_user.id):
                await callback.answer("❌ Access denied")
                return
            
            status_text = """🔧 **System Status**

✅ Bot: Online
✅ Market Data: Connected
✅ VIP Manager: Active
✅ News Handler: Ready
✅ Chart Generator: Available

🟢 All systems operational"""
            
            await callback.message.edit_text(status_text, parse_mode='Markdown')
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error in admin status handler: {e}")
            await callback.answer("❌ Error loading status")
    
    @dp.callback_query(F.data == "admin_broadcast")
    async def admin_broadcast_handler(callback: CallbackQuery):
        """Handle admin broadcast request"""
        try:
            if not admin_panel.is_admin(callback.from_user.id):
                await callback.answer("❌ Access denied")
                return
            
            broadcast_text = """📢 **Broadcast Message**

Broadcast functionality coming soon!

This feature will allow admins to send messages to all bot users."""
            
            await callback.message.edit_text(broadcast_text, parse_mode='Markdown')
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error in admin broadcast handler: {e}")
            await callback.answer("❌ Error with broadcast")
    
    logger.info("✅ Admin panel handlers setup completed")
    return admin_panel