#!/bin/bash

echo "🚀 Starting Enhanced Leandro Bot..."
echo "==================================="

# Kill any existing processes
echo "🛑 Stopping any existing bot processes..."
pkill -f enhanced_bot.py
pkill -f bulletproof_usdc_bot.py
sleep 2

# Set environment variables
export TELEGRAM_BOT_TOKEN="8124805384:AAEr2uAubqKAkakfH9MZSJ8Uj1sSzccC36U"

# Start the enhanced bot in background
echo "🚀 Starting enhanced bot in background..."
source bot_env/bin/activate
nohup python enhanced_bot.py > enhanced_bot_output.log 2>&1 &

# Get the bot PID
BOT_PID=$!
echo "✅ Enhanced bot started with PID: $BOT_PID"

# Save PID to file
echo $BOT_PID > enhanced_bot.pid

# Wait and check status
sleep 5
echo ""
echo "📊 Checking bot status..."

if ps -p $BOT_PID > /dev/null; then
    echo "✅ Enhanced bot is running successfully!"
    echo ""
    echo "🎉 Enhanced Bot Features:"
    echo "✅ Fixed payment options - all packages work smoothly"
    echo "✅ Enhanced news section with real content"
    echo "✅ Updated About section with Leandro's Linktree info"
    echo "✅ Complete language translations"
    echo "✅ Improved user friendliness and navigation"
    echo "✅ Simplified interface for non-technical users"
    echo ""
    echo "📋 Check status: ./check_enhanced_status.sh"
    echo "📋 View logs: tail -f enhanced_bot.log"
    echo "🛑 Stop: ./stop_enhanced_bot.sh"
else
    echo "❌ Enhanced bot failed to start!"
    echo "📋 Check logs: cat enhanced_bot_output.log"
    exit 1
fi