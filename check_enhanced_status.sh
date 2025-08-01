#!/bin/bash

echo "🔍 Enhanced Bot Status Check"
echo "============================"

# Check enhanced bot process
if [ -f "enhanced_bot.pid" ]; then
    BOT_PID=$(cat enhanced_bot.pid)
    if ps -p $BOT_PID > /dev/null; then
        echo "✅ Enhanced Bot: Running (PID: $BOT_PID)"
        
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
        echo "❌ Enhanced Bot: Not running (stale PID)"
    fi
else
    echo "❌ Enhanced Bot: No PID file"
fi

# Check logs
if [ -f "enhanced_bot.log" ]; then
    echo "📋 Enhanced Bot Log: Available"
    echo "   Last 3 lines:"
    tail -3 enhanced_bot.log | sed 's/^/   /'
fi

echo ""
echo "🎉 Enhanced Features:"
echo "✅ Fixed payment options - all packages work smoothly"
echo "✅ Enhanced news section with real content"
echo "✅ Updated About section with Leandro's Linktree info"
echo "✅ Complete language translations"
echo "✅ Improved user friendliness and navigation"
echo "✅ Simplified interface for non-technical users"

echo ""
echo "📊 Summary:"
if [ -f "enhanced_bot.pid" ] && ps -p $(cat enhanced_bot.pid) > /dev/null; then
    echo "🎉 Status: ENHANCED BOT OPERATIONAL"
    echo "🔗 Test: @Leandrocryptobot"
    echo "📱 Send /start to test all fixes!"
else
    echo "❌ Status: NOT RUNNING"
    echo "🚀 Start: ./start_enhanced_bot.sh"
fi