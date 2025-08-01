#!/bin/bash

echo "🚀 Starting Leandro Crypto Bot..."

# Check if virtual environment exists
if [ ! -d "bot_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "python setup_bot.py"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source bot_env/bin/activate

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ Found .env file"
else
    echo "⚠️ No .env file found. Please set up your bot token:"
    echo "python setup_bot.py"
    exit 1
fi

# Run the bot
echo "🤖 Starting bot..."
python main_1753060384126.py