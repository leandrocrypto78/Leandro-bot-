#!/usr/bin/env python3
"""
Bot Status Check Script
"""

import os
import subprocess
import asyncio
from aiogram import Bot

def check_bot_process():
    """Check if bot process is running"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'main_1753060384126.py' in result.stdout:
            return True
        return False
    except:
        return False

def check_token():
    """Check if token is set"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        # Try reading from .env file
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('TELEGRAM_BOT_TOKEN='):
                        token = line.split('=', 1)[1].strip()
                        break
    return token

async def test_bot_connection(token):
    """Test bot connection"""
    try:
        bot = Bot(token=token)
        info = await bot.get_me()
        await bot.session.close()
        return True, info
    except Exception as e:
        return False, str(e)

async def main():
    """Main status check"""
    print("🔍 BOT STATUS CHECK")
    print("=" * 50)
    
    # Check bot process
    print("1. Checking bot process...")
    if check_bot_process():
        print("   ✅ Bot process is running")
    else:
        print("   ❌ Bot process is not running")
    
    # Check token
    print("\n2. Checking bot token...")
    token = check_token()
    if token:
        print("   ✅ Bot token is set")
        print(f"   Token: {token[:20]}...")
    else:
        print("   ❌ Bot token is not set")
        return
    
    # Test connection
    print("\n3. Testing bot connection...")
    success, result = await test_bot_connection(token)
    if success:
        print("   ✅ Bot connection successful")
        print(f"   Bot name: {result.first_name}")
        print(f"   Bot username: @{result.username}")
    else:
        print(f"   ❌ Bot connection failed: {result}")
        return
    
    print("\n" + "=" * 50)
    print("🎉 BOT STATUS: OPERATIONAL")
    print("\n📋 Next Steps:")
    print("1. Open Telegram")
    print("2. Search for your bot: @Leandrocryptobot")
    print("3. Send /start command")
    print("4. The bot should respond with welcome message and menu")

if __name__ == "__main__":
    asyncio.run(main())