#!/usr/bin/env python3
"""
Bot Setup Script
This script helps you set up and run the Leandro Crypto Bot
"""

import os
import sys
import subprocess

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if virtual environment exists
    if not os.path.exists("bot_env"):
        print("❌ Virtual environment not found. Creating...")
        subprocess.run([sys.executable, "-m", "venv", "bot_env"])
        print("✅ Virtual environment created")
    
    # Check if aiogram is installed
    try:
        import aiogram
        print("✅ aiogram is installed")
    except ImportError:
        print("❌ aiogram not installed. Installing...")
        subprocess.run(["./bot_env/bin/pip", "install", "aiogram"])
        print("✅ aiogram installed")

def get_bot_token():
    """Get bot token from user"""
    print("\n🤖 BOT TOKEN SETUP")
    print("=" * 50)
    print("To get a bot token:")
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot command")
    print("3. Follow the instructions to create your bot")
    print("4. Copy the token (looks like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)")
    print("=" * 50)
    
    token = input("\nEnter your bot token: ").strip()
    
    if not token:
        print("❌ No token provided. Please get a token from @BotFather first.")
        return None
    
    if ":" not in token:
        print("❌ Invalid token format. Token should contain a colon (:).")
        return None
    
    return token

def set_environment_variable(token):
    """Set the environment variable"""
    print(f"\n🔧 Setting environment variable...")
    
    # Set for current session
    os.environ['TELEGRAM_BOT_TOKEN'] = token
    
    # Also save to a .env file for future use
    with open('.env', 'w') as f:
        f.write(f'TELEGRAM_BOT_TOKEN={token}\n')
    
    print("✅ Environment variable set")
    print("✅ Token saved to .env file")

def test_bot_connection(token):
    """Test if the bot token is valid"""
    print("\n🧪 Testing bot connection...")
    
    try:
        import asyncio
        from aiogram import Bot
        
        async def test_connection():
            bot = Bot(token=token)
            try:
                bot_info = await bot.get_me()
                print(f"✅ Bot connection successful!")
                print(f"🤖 Bot name: {bot_info.first_name}")
                print(f"👤 Bot username: @{bot_info.username}")
                await bot.session.close()
                return True
            except Exception as e:
                print(f"❌ Bot connection failed: {e}")
                return False
        
        return asyncio.run(test_connection())
        
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def run_bot():
    """Run the bot"""
    print("\n🚀 Starting the bot...")
    print("Press Ctrl+C to stop the bot")
    
    try:
        # Activate virtual environment and run bot
        if os.name == 'nt':  # Windows
            subprocess.run(["./bot_env/Scripts/python", "main_1753060384126.py"])
        else:  # Linux/Mac
            subprocess.run(["./bot_env/bin/python", "main_1753060384126.py"])
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

def main():
    """Main setup function"""
    print("🚀 LEANDRO CRYPTO BOT SETUP")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Check if token is already set
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        # Get token from user
        token = get_bot_token()
        if not token:
            print("\n❌ Setup incomplete. Please get a bot token and try again.")
            return
        
        # Set environment variable
        set_environment_variable(token)
    else:
        print("✅ Bot token already set")
    
    # Test connection
    if not test_bot_connection(token):
        print("\n❌ Bot token is invalid. Please check your token and try again.")
        return
    
    # Ask if user wants to run the bot
    print("\n" + "=" * 50)
    run_now = input("Do you want to start the bot now? (y/n): ").lower().strip()
    
    if run_now in ['y', 'yes']:
        run_bot()
    else:
        print("\n📋 To run the bot later:")
        print("1. Activate virtual environment: source bot_env/bin/activate")
        print("2. Run: python main_1753060384126.py")
        print("\n🎉 Setup complete! Your bot is ready to run.")

if __name__ == "__main__":
    main()