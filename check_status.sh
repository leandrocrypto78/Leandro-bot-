#!/bin/bash

echo "🔍 Leandro Bot 24/7 Status Check"
echo "================================="

# Check daemon process
if [ -f "bot_daemon.pid" ]; then
    DAEMON_PID=$(cat bot_daemon.pid)
    if ps -p $DAEMON_PID > /dev/null; then
        echo "✅ Daemon Process: Running (PID: $DAEMON_PID)"
    else
        echo "❌ Daemon Process: Not running (stale PID file)"
    fi
else
    echo "❌ Daemon Process: No PID file found"
fi

# Check bot process
BOT_PID=$(pgrep -f "bulletproof_usdc_bot.py")
if [ ! -z "$BOT_PID" ]; then
    echo "✅ Bot Process: Running (PID: $BOT_PID)"
else
    echo "❌ Bot Process: Not running"
fi

# Check daemon log
if [ -f "bot_daemon.log" ]; then
    echo "📋 Daemon Log: Available"
    echo "   Last 3 lines:"
    tail -3 bot_daemon.log | sed 's/^/   /'
else
    echo "📋 Daemon Log: Not found"
fi

# Check bot log
if [ -f "perfect_usdc_bot.log" ]; then
    echo "📋 Bot Log: Available"
    echo "   Last 3 lines:"
    tail -3 perfect_usdc_bot.log | sed 's/^/   /'
else
    echo "📋 Bot Log: Not found"
fi

# Check uptime
if [ ! -z "$BOT_PID" ]; then
    UPTIME=$(ps -o etime= -p $BOT_PID 2>/dev/null)
    if [ ! -z "$UPTIME" ]; then
        echo "⏱️ Bot Uptime: $UPTIME"
    fi
fi

# Check memory usage
if [ ! -z "$BOT_PID" ]; then
    MEMORY=$(ps -o rss= -p $BOT_PID 2>/dev/null)
    if [ ! -z "$MEMORY" ]; then
        MEMORY_MB=$((MEMORY / 1024))
        echo "💾 Memory Usage: ${MEMORY_MB}MB"
    fi
fi

echo ""
echo "📊 Summary:"
if [ ! -z "$BOT_PID" ] && [ -f "bot_daemon.pid" ]; then
    echo "🎉 Bot Status: OPERATIONAL (24/7)"
    echo "🔗 Test your bot: @Leandrocryptobot"
else
    echo "❌ Bot Status: NOT RUNNING"
    echo "🚀 Start with: ./start_24_7.sh"
fi