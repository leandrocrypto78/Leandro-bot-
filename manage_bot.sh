#!/bin/bash

echo "🤖 Leandro Bot 24/7 Management"
echo "=============================="

case "$1" in
    start)
        echo "🚀 Starting bot..."
        ./start_simple_24_7.sh
        ;;
    stop)
        echo "🛑 Stopping bot..."
        ./stop_simple_24_7.sh
        ;;
    restart)
        echo "🔄 Restarting bot..."
        ./stop_simple_24_7.sh
        sleep 3
        ./start_simple_24_7.sh
        ;;
    status)
        echo "📊 Checking status..."
        ./check_simple_status.sh
        ;;
    logs)
        echo "📋 Showing logs..."
        echo "=== Daemon Log ==="
        tail -10 simple_daemon.log
        echo ""
        echo "=== Bot Log ==="
        tail -10 perfect_usdc_bot.log
        ;;
    watch)
        echo "👀 Watching logs (Ctrl+C to stop)..."
        tail -f simple_daemon.log perfect_usdc_bot.log
        ;;
    test)
        echo "🧪 Testing bot connection..."
        source bot_env/bin/activate
        python check_usdc_status.py
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|watch|test}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the 24/7 bot service"
        echo "  stop    - Stop the bot service"
        echo "  restart - Restart the bot service"
        echo "  status  - Check bot status"
        echo "  logs    - Show recent logs"
        echo "  watch   - Watch logs in real-time"
        echo "  test    - Test bot functionality"
        echo ""
        echo "Current status:"
        ./check_simple_status.sh
        ;;
esac