#!/bin/bash

echo "=========================================="
echo "🤖 Telegram Bot Launcher"
echo "=========================================="

# Check if token is provided as argument
if [ -z "$1" ]; then
    echo "❌ Error: Telegram Bot Token is required!"
    echo ""
    echo "Usage: $0 <YOUR_BOT_TOKEN>"
    echo ""
    echo "To get a bot token:"
    echo "1. Message @BotFather on Telegram"
    echo "2. Send /newbot command"
    echo "3. Follow the instructions"
    echo "4. Copy the token and run: $0 <token>"
    echo ""
    exit 1
fi

# Set the token as environment variable
export TELEGRAM_BOT_TOKEN="$1"

echo "✅ Bot token set successfully"
echo "🚀 Starting the Bulletproof USDC Bot..."
echo ""

# Run the bot
python3 bulletproof_usdc_bot.py