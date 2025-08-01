import logging
import asyncio
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class HealthMonitor:
    """Health monitoring system for the bot"""
    
    def __init__(self, bot, vip_manager, market_data):
        self.bot = bot
        self.vip_manager = vip_manager
        self.market_data = market_data
        self.monitoring = False
        self.health_stats = {
            'start_time': datetime.now(),
            'uptime': 0,
            'total_requests': 0,
            'errors': 0,
            'last_check': None
        }
        logger.info("✅ Health Monitor initialized")
    
    async def start_monitoring(self):
        """Start health monitoring"""
        self.monitoring = True
        logger.info("🔄 Health monitoring started")
        
        while self.monitoring:
            try:
                await self.check_health()
                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def stop_monitoring(self):
        """Stop health monitoring"""
        self.monitoring = False
        logger.info("⏹️ Health monitoring stopped")
    
    async def check_health(self):
        """Perform health check"""
        try:
            # Check bot connectivity
            bot_info = await self.bot.get_me()
            
            # Update health stats
            self.health_stats['last_check'] = datetime.now()
            self.health_stats['uptime'] = (datetime.now() - self.health_stats['start_time']).total_seconds()
            
            # Log health status
            logger.info(f"✅ Health check passed - Bot: @{bot_info.username}, Uptime: {self.health_stats['uptime']:.0f}s")
            
        except Exception as e:
            self.health_stats['errors'] += 1
            logger.error(f"❌ Health check failed: {e}")
    
    def get_health_status(self) -> Dict:
        """Get current health status"""
        return {
            'status': 'healthy' if self.monitoring else 'stopped',
            'uptime': self.health_stats['uptime'],
            'total_requests': self.health_stats['total_requests'],
            'errors': self.health_stats['errors'],
            'last_check': self.health_stats['last_check']
        }
    
    def increment_requests(self):
        """Increment request counter"""
        self.health_stats['total_requests'] += 1