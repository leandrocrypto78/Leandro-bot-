#!/bin/bash

echo "🛑 Stopping Leandro Bot 24/7 Service..."
echo "======================================="

# Check if PID file exists
if [ -f "bot_daemon.pid" ]; then
    DAEMON_PID=$(cat bot_daemon.pid)
    echo "📋 Found daemon PID: $DAEMON_PID"
    
    # Check if process is still running
    if ps -p $DAEMON_PID > /dev/null; then
        echo "🛑 Stopping daemon process..."
        kill $DAEMON_PID
        
        # Wait for graceful shutdown
        sleep 5
        
        # Check if still running
        if ps -p $DAEMON_PID > /dev/null; then
            echo "⚠️ Force killing daemon process..."
            kill -9 $DAEMON_PID
        fi
        
        echo "✅ Daemon stopped"
    else
        echo "ℹ️ Daemon process not running"
    fi
    
    # Remove PID file
    rm -f bot_daemon.pid
else
    echo "ℹ️ No PID file found"
fi

# Kill any remaining bot processes
echo "🛑 Stopping any remaining bot processes..."
pkill -f bulletproof_usdc_bot.py
pkill -f bot_daemon.py

# Wait a moment
sleep 2

# Check if any processes are still running
if pgrep -f "bulletproof_usdc_bot.py\|bot_daemon.py" > /dev/null; then
    echo "⚠️ Some processes still running, force killing..."
    pkill -9 -f bulletproof_usdc_bot.py
    pkill -9 -f bot_daemon.py
else
    echo "✅ All bot processes stopped"
fi

echo ""
echo "🎉 Bot 24/7 service stopped successfully!"