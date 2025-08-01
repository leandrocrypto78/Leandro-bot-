#!/bin/bash

echo "🚀 Starting Bulletproof USDC Bot..."

# Check if virtual environment exists
if [ ! -d "bot_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "python setup_bot.py"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source bot_env/bin/activate

# Set bot token
export TELEGRAM_BOT_TOKEN="8124805384:AAEr2uAubqKAkakfH9MZSJ8Uj1sSzccC36U"

# Run the bot
echo "🤖 Starting Bulletproof USDC Bot..."
python bulletproof_usdc_bot.py