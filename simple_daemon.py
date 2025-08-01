#!/usr/bin/env python3
"""
Simple 24/7 Bot Daemon - Robust background operation
"""

import os
import sys
import time
import subprocess
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simple_daemon.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def start_bot():
    """Start the bot process"""
    try:
        logger.info("🚀 Starting bot process...")
        
        # Set environment variables
        env = os.environ.copy()
        env['TELEGRAM_BOT_TOKEN'] = '8124805384:AAEr2uAubqKAkakfH9MZSJ8Uj1sSzccC36U'
        
        # Start the bot
        process = subprocess.Popen(
            [sys.executable, 'bulletproof_usdc_bot.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        logger.info(f"✅ Bot started with PID: {process.pid}")
        return process
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        return None

def monitor_bot():
    """Monitor and restart bot if needed"""
    logger.info("🔍 Starting 24/7 bot monitoring...")
    
    restart_count = 0
    max_restarts = 1000
    
    while restart_count < max_restarts:
        try:
            # Start bot
            process = start_bot()
            if not process:
                logger.error("❌ Failed to start bot, retrying in 30 seconds...")
                time.sleep(30)
                restart_count += 1
                continue
            
            # Monitor bot process
            while process.poll() is None:
                time.sleep(30)  # Check every 30 seconds
            
            # Bot process ended
            exit_code = process.returncode
            logger.warning(f"⚠️ Bot process ended with code {exit_code}")
            
            restart_count += 1
            logger.info(f"🔄 Restarting bot (attempt {restart_count}/{max_restarts})")
            time.sleep(5)  # Wait before restart
            
        except KeyboardInterrupt:
            logger.info("🛑 Received keyboard interrupt, stopping...")
            break
        except Exception as e:
            logger.error(f"❌ Error in monitoring: {e}")
            time.sleep(10)
            restart_count += 1
    
    logger.info("👋 Bot monitoring stopped")

if __name__ == "__main__":
    print("🤖 Simple 24/7 Bot Daemon Starting...")
    print("=" * 50)
    
    # Check if bot file exists
    if not os.path.exists("bulletproof_usdc_bot.py"):
        print("❌ Error: bulletproof_usdc_bot.py not found!")
        sys.exit(1)
    
    # Check if virtual environment exists
    if not os.path.exists("bot_env"):
        print("❌ Error: bot_env not found!")
        sys.exit(1)
    
    print("✅ Starting bot monitoring...")
    monitor_bot()