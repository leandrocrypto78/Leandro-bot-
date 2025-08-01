#!/bin/bash

echo "🔍 Simple 24/7 Bot Status Check"
echo "================================"

# Check daemon
if [ -f "simple_daemon.pid" ]; then
    DAEMON_PID=$(cat simple_daemon.pid)
    if ps -p $DAEMON_PID > /dev/null; then
        echo "✅ Daemon: Running (PID: $DAEMON_PID)"
    else
        echo "❌ Daemon: Not running (stale PID)"
    fi
else
    echo "❌ Daemon: No PID file"
fi

# Check bot
BOT_PID=$(pgrep -f bulletproof_usdc_bot.py)
if [ ! -z "$BOT_PID" ]; then
    echo "✅ Bot: Running (PID: $BOT_PID)"
    
    # Get uptime
    UPTIME=$(ps -o etime= -p $BOT_PID 2>/dev/null)
    if [ ! -z "$UPTIME" ]; then
        echo "⏱️ Uptime: $UPTIME"
    fi
    
    # Get memory usage
    MEMORY=$(ps -o rss= -p $BOT_PID 2>/dev/null)
    if [ ! -z "$MEMORY" ]; then
        MEMORY_MB=$((MEMORY / 1024))
        echo "💾 Memory: ${MEMORY_MB}MB"
    fi
else
    echo "❌ Bot: Not running"
fi

# Check logs
if [ -f "simple_daemon.log" ]; then
    echo "📋 Daemon Log: Available"
    echo "   Last 2 lines:"
    tail -2 simple_daemon.log | sed 's/^/   /'
fi

if [ -f "perfect_usdc_bot.log" ]; then
    echo "📋 Bot Log: Available"
    echo "   Last 2 lines:"
    tail -2 perfect_usdc_bot.log | sed 's/^/   /'
fi

echo ""
echo "📊 Summary:"
if [ ! -z "$BOT_PID" ]; then
    echo "🎉 Status: OPERATIONAL (24/7)"
    echo "🔗 Test: @Leandrocryptobot"
else
    echo "❌ Status: NOT RUNNING"
    echo "🚀 Start: ./start_simple_24_7.sh"
fi