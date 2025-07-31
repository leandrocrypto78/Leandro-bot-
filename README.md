# Leandro Telegram Bot

A comprehensive Telegram bot with USDC payment verification, VIP management, market data, and more features.

## Features

✅ **Bulletproof USDC Bot** - Self-contained with all critical issues fixed:
- USDC payment verification on Solana blockchain
- Consolidated FSM states with no conflicts
- No duplicate handlers
- Safe message editing
- Complete error handling
- Working VIP manager
- Multilingual system
- User-friendly payment flow
- Market data (prices, charts, news)
- Security vulnerabilities patched

## Setup Instructions

### Prerequisites
- Python 3.7+
- Telegram Bot Token from @BotFather

### Installation

1. **Clone/Download the project**
   ```bash
   # Files should be in your workspace
   ```

2. **Install dependencies**
   ```bash
   pip3 install --break-system-packages -r requirements.txt
   ```

3. **Get a Telegram Bot Token**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` command
   - Follow the instructions to create your bot
   - Copy the bot token

### Running the Bot

#### Option 1: Using the launcher script (Recommended)
```bash
./run_bot.sh YOUR_BOT_TOKEN_HERE
```

#### Option 2: Manual execution
```bash
export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
python3 bulletproof_usdc_bot.py
```

## Bot Commands

Once running, users can interact with the bot using:
- `/start` - Start the bot and see welcome message
- Various inline keyboards for navigation
- VIP features and payment processing
- Market data queries
- And much more!

## Files

- **`bulletproof_usdc_bot.py`** - Main bot file (self-contained, ready to run)
- **`main_1753060384126.py`** - Alternative version (requires external modules)
- **`requirements.txt`** - Python dependencies
- **`run_bot.sh`** - Easy launcher script

## Logs

The bot creates detailed logs in:
- `perfect_usdc_bot.log` - Main bot logs
- Console output for real-time monitoring

## Troubleshooting

1. **Import Errors**: Use the `bulletproof_usdc_bot.py` file - it's self-contained
2. **Permission Errors**: Use `--break-system-packages` flag with pip
3. **Token Errors**: Make sure your bot token is correct and properly set
4. **Network Issues**: Check your internet connection for Telegram API access

## Security

- Bot token is loaded from environment variables (not hardcoded)
- Security vulnerabilities have been patched
- Safe message handling implemented