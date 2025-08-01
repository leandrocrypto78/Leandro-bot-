#!/usr/bin/env python3
"""
24/7 Bot Daemon - Keeps the bot running continuously
"""

import os
import sys
import time
import signal
import subprocess
import logging
from datetime import datetime
import psutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_daemon.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BotDaemon:
    def __init__(self):
        self.bot_process = None
        self.running = True
        self.restart_count = 0
        self.max_restarts = 1000  # Prevent infinite restart loops
        self.restart_delay = 5  # Seconds to wait before restart
        
        # Bot configuration
        self.bot_script = "bulletproof_usdc_bot.py"
        self.env_vars = {
            'TELEGRAM_BOT_TOKEN': '8124805384:AAEr2uAubqKAkakfH9MZSJ8Uj1sSzccC36U'
        }
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
        if self.bot_process:
            self.bot_process.terminate()
            try:
                self.bot_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.bot_process.kill()
    
    def check_bot_running(self):
        """Check if bot process is still running"""
        if self.bot_process is None:
            return False
        
        return self.bot_process.poll() is None
    
    def start_bot(self):
        """Start the bot process"""
        try:
            logger.info("🚀 Starting bot process...")
            
            # Activate virtual environment and start bot
            cmd = [
                sys.executable,  # Use current Python
                self.bot_script
            ]
            
            # Set environment variables
            env = os.environ.copy()
            env.update(self.env_vars)
            
            # Start the bot process
            self.bot_process = subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info(f"✅ Bot started with PID: {self.bot_process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            return False
    
    def stop_bot(self):
        """Stop the bot process"""
        if self.bot_process:
            logger.info("🛑 Stopping bot process...")
            self.bot_process.terminate()
            try:
                self.bot_process.wait(timeout=10)
                logger.info("✅ Bot stopped gracefully")
            except subprocess.TimeoutExpired:
                logger.warning("⚠️ Force killing bot process...")
                self.bot_process.kill()
            finally:
                self.bot_process = None
    
    def restart_bot(self):
        """Restart the bot process"""
        logger.info(f"🔄 Restarting bot (attempt {self.restart_count + 1}/{self.max_restarts})")
        self.stop_bot()
        time.sleep(self.restart_delay)
        
        if self.start_bot():
            self.restart_count += 1
            logger.info(f"✅ Bot restarted successfully (total restarts: {self.restart_count})")
        else:
            logger.error("❌ Failed to restart bot")
    
    def monitor_bot(self):
        """Main monitoring loop"""
        logger.info("🔍 Starting 24/7 bot monitoring...")
        
        while self.running:
            try:
                # Check if bot is running
                if not self.check_bot_running():
                    if self.restart_count >= self.max_restarts:
                        logger.error(f"❌ Max restarts reached ({self.max_restarts}), stopping daemon")
                        break
                    
                    logger.warning("⚠️ Bot process not running, restarting...")
                    self.restart_bot()
                else:
                    # Bot is running, just wait
                    time.sleep(30)  # Check every 30 seconds
                    
            except KeyboardInterrupt:
                logger.info("🛑 Received keyboard interrupt")
                break
            except Exception as e:
                logger.error(f"❌ Error in monitoring loop: {e}")
                time.sleep(10)
        
        # Cleanup
        self.stop_bot()
        logger.info("👋 Bot daemon stopped")

def main():
    """Main function"""
    print("🤖 24/7 Bot Daemon Starting...")
    print("=" * 50)
    
    # Check if bot script exists
    if not os.path.exists("bulletproof_usdc_bot.py"):
        print("❌ Error: bulletproof_usdc_bot.py not found!")
        print("Please make sure the bot file exists in the current directory.")
        return
    
    # Check if virtual environment exists
    if not os.path.exists("bot_env"):
        print("❌ Error: bot_env virtual environment not found!")
        print("Please run the setup first.")
        return
    
    # Start the daemon
    daemon = BotDaemon()
    
    try:
        # Start the bot initially
        if daemon.start_bot():
            print("✅ Bot started successfully")
            print("🔍 Monitoring bot 24/7...")
            print("Press Ctrl+C to stop")
            
            # Start monitoring
            daemon.monitor_bot()
        else:
            print("❌ Failed to start bot")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Daemon error: {e}")

if __name__ == "__main__":
    main()