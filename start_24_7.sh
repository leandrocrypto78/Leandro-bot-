#!/bin/bash

echo "🤖 Starting Leandro Bot 24/7 Service..."
echo "========================================"

# Check if bot files exist
if [ ! -f "bulletproof_usdc_bot.py" ]; then
    echo "❌ Error: bulletproof_usdc_bot.py not found!"
    exit 1
fi

if [ ! -f "bot_daemon.py" ]; then
    echo "❌ Error: bot_daemon.py not found!"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "bot_env" ]; then
    echo "❌ Error: bot_env not found!"
    echo "Please run setup first."
    exit 1
fi

# Kill any existing bot processes
echo "🛑 Stopping any existing bot processes..."
pkill -f bulletproof_usdc_bot.py
pkill -f bot_daemon.py
sleep 2

# Set environment variables
export TELEGRAM_BOT_TOKEN="8124805384:AAEr2uAubqKAkakfH9MZSJ8Uj1sSzccC36U"

# Start the daemon in the background
echo "🚀 Starting bot daemon in background..."
nohup python bot_daemon.py > bot_daemon_output.log 2>&1 &

# Get the daemon PID
DAEMON_PID=$!
echo "✅ Bot daemon started with PID: $DAEMON_PID"

# Save PID to file for easy management
echo $DAEMON_PID > bot_daemon.pid

# Wait a moment and check if it's running
sleep 5
if ps -p $DAEMON_PID > /dev/null; then
    echo "✅ Bot daemon is running successfully!"
    echo "📊 Check status with: ./check_status.sh"
    echo "📋 View logs with: tail -f bot_daemon.log"
    echo "🛑 Stop with: ./stop_24_7.sh"
else
    echo "❌ Bot daemon failed to start!"
    echo "📋 Check logs: cat bot_daemon_output.log"
    exit 1
fi

echo ""
echo "🎉 Bot is now running 24/7!"
echo "The daemon will automatically restart the bot if it crashes."