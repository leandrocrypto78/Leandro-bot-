#!/bin/bash

echo "🤖 Enhanced Leandro Bot Management"
echo "=================================="

case "$1" in
    start)
        echo "🚀 Starting enhanced bot..."
        ./start_enhanced_bot.sh
        ;;
    stop)
        echo "🛑 Stopping enhanced bot..."
        ./stop_enhanced_bot.sh
        ;;
    restart)
        echo "🔄 Restarting enhanced bot..."
        ./stop_enhanced_bot.sh
        sleep 3
        ./start_enhanced_bot.sh
        ;;
    status)
        echo "📊 Checking enhanced bot status..."
        ./check_enhanced_status.sh
        ;;
    logs)
        echo "📋 Showing enhanced bot logs..."
        echo "=== Enhanced Bot Log ==="
        tail -10 enhanced_bot.log
        ;;
    watch)
        echo "👀 Watching enhanced bot logs (Ctrl+C to stop)..."
        tail -f enhanced_bot.log
        ;;
    test)
        echo "🧪 Testing enhanced bot functionality..."
        source bot_env/bin/activate
        python check_usdc_status.py
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|watch|test}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the enhanced bot"
        echo "  stop    - Stop the enhanced bot"
        echo "  restart - Restart the enhanced bot"
        echo "  status  - Check enhanced bot status"
        echo "  logs    - Show recent logs"
        echo "  watch   - Watch logs in real-time"
        echo "  test    - Test bot functionality"
        echo ""
        echo "🎉 Enhanced Bot Features:"
        echo "✅ Fixed payment options - all packages work smoothly"
        echo "✅ Enhanced news section with real content"
        echo "✅ Updated About section with Leandro's Linktree info"
        echo "✅ Complete language translations"
        echo "✅ Improved user friendliness and navigation"
        echo "✅ Simplified interface for non-technical users"
        echo ""
        echo "Current status:"
        ./check_enhanced_status.sh
        ;;
esac