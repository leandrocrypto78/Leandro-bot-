#!/bin/bash

echo "🤖 Starting Simple 24/7 Bot Service..."
echo "======================================"

# Kill any existing processes
echo "🛑 Stopping any existing bot processes..."
pkill -f bulletproof_usdc_bot.py
pkill -f simple_daemon.py
sleep 2

# Start the simple daemon in background
echo "🚀 Starting simple daemon in background..."
nohup python simple_daemon.py > daemon_output.log 2>&1 &

# Get the daemon PID
DAEMON_PID=$!
echo "✅ Simple daemon started with PID: $DAEMON_PID"

# Save PID to file
echo $DAEMON_PID > simple_daemon.pid

# Wait and check status
sleep 10
echo ""
echo "📊 Checking bot status..."

# Check if daemon is running
if ps -p $DAEMON_PID > /dev/null; then
    echo "✅ Daemon is running"
else
    echo "❌ Daemon failed to start"
    exit 1
fi

# Check if bot is running
BOT_PID=$(pgrep -f bulletproof_usdc_bot.py)
if [ ! -z "$BOT_PID" ]; then
    echo "✅ Bot is running (PID: $BOT_PID)"
    echo ""
    echo "🎉 Bot is now running 24/7!"
    echo "📋 Check status: ./check_simple_status.sh"
    echo "📋 View logs: tail -f simple_daemon.log"
    echo "🛑 Stop: ./stop_simple_24_7.sh"
else
    echo "❌ Bot is not running yet, checking logs..."
    echo "📋 Check daemon output: cat daemon_output.log"
fi