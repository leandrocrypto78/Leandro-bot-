#!/bin/bash

echo "🛑 Stopping Enhanced Bot..."
echo "==========================="

# Stop enhanced bot
if [ -f "enhanced_bot.pid" ]; then
    BOT_PID=$(cat enhanced_bot.pid)
    echo "📋 Found bot PID: $BOT_PID"
    
    if ps -p $BOT_PID > /dev/null; then
        echo "🛑 Stopping enhanced bot..."
        kill $BOT_PID
        sleep 3
        
        if ps -p $BOT_PID > /dev/null; then
            echo "⚠️ Force killing bot..."
            kill -9 $BOT_PID
        fi
        echo "✅ Bot stopped"
    else
        echo "ℹ️ Bot not running"
    fi
    
    rm -f enhanced_bot.pid
fi

# Kill any remaining processes
echo "🛑 Stopping any remaining processes..."
pkill -f enhanced_bot.py

sleep 2

# Check if any processes remain
if pgrep -f "enhanced_bot.py" > /dev/null; then
    echo "⚠️ Force killing remaining processes..."
    pkill -9 -f enhanced_bot.py
fi

echo "✅ All enhanced bot processes stopped"