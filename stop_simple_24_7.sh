#!/bin/bash

echo "🛑 Stopping Simple 24/7 Bot Service..."
echo "======================================"

# Stop daemon
if [ -f "simple_daemon.pid" ]; then
    DAEMON_PID=$(cat simple_daemon.pid)
    echo "📋 Found daemon PID: $DAEMON_PID"
    
    if ps -p $DAEMON_PID > /dev/null; then
        echo "🛑 Stopping daemon..."
        kill $DAEMON_PID
        sleep 3
        
        if ps -p $DAEMON_PID > /dev/null; then
            echo "⚠️ Force killing daemon..."
            kill -9 $DAEMON_PID
        fi
        echo "✅ Daemon stopped"
    else
        echo "ℹ️ Daemon not running"
    fi
    
    rm -f simple_daemon.pid
fi

# Stop bot processes
echo "🛑 Stopping bot processes..."
pkill -f bulletproof_usdc_bot.py
pkill -f simple_daemon.py

sleep 2

# Check if any processes remain
if pgrep -f "bulletproof_usdc_bot.py\|simple_daemon.py" > /dev/null; then
    echo "⚠️ Force killing remaining processes..."
    pkill -9 -f bulletproof_usdc_bot.py
    pkill -9 -f simple_daemon.py
fi

echo "✅ All processes stopped"