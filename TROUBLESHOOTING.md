# Troubleshooting Guide

## 🚨 Bot Not Responding to /start Command

### Step 1: Check if Bot is Running
```bash
# Check if bot process is running
ps aux | grep python | grep main_1753060384126
```

If no process is found, the bot is not running.

### Step 2: Check Bot Token
```bash
# Check if token is set
echo $TELEGRAM_BOT_TOKEN
```

If empty, you need to set up your bot token.

### Step 3: Get a Bot Token
1. Open Telegram
2. Search for @BotFather
3. Send `/newbot`
4. Follow instructions to create your bot
5. Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 4: Set Up Bot Token
**Option A: Use Setup Script (Recommended)**
```bash
python setup_bot.py
```

**Option B: Manual Setup**
```bash
# Set environment variable
export TELEGRAM_BOT_TOKEN="your_token_here"

# Or create .env file
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
```

### Step 5: Run the Bot
```bash
# Option A: Use run script
./run_bot.sh

# Option B: Manual run
source bot_env/bin/activate
python main_1753060384126.py
```

## 🔍 Common Issues

### Issue 1: "No module named 'aiogram'"
**Solution:**
```bash
source bot_env/bin/activate
pip install aiogram
```

### Issue 2: "Please set your TELEGRAM_BOT_TOKEN"
**Solution:**
- Run `python setup_bot.py` to set up your token
- Or manually set the environment variable

### Issue 3: Bot starts but doesn't respond
**Possible causes:**
1. Wrong bot token
2. Bot is not the same one you're messaging
3. Bot is in a group (should be private chat)

**Solutions:**
1. Verify token with @BotFather
2. Make sure you're messaging the correct bot
3. Start a private chat with your bot

### Issue 4: Bot responds but /start doesn't work
**Check:**
1. Bot is running (see logs)
2. No error messages in console
3. Bot has proper permissions

## 📋 Quick Setup Checklist

- [ ] Virtual environment created (`bot_env/`)
- [ ] aiogram installed (`pip install aiogram`)
- [ ] Bot token obtained from @BotFather
- [ ] Token set in environment or .env file
- [ ] Bot is running (`python main_1753060384126.py`)
- [ ] Bot responds to /start command

## 🛠️ Debug Commands

```bash
# Check bot status
python simple_test.py

# Check environment
echo $TELEGRAM_BOT_TOKEN

# Check if bot is running
ps aux | grep python

# View bot logs
tail -f bot.log

# Test bot connection
python -c "
import asyncio
from aiogram import Bot
import os
async def test():
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    try:
        info = await bot.get_me()
        print(f'Bot: @{info.username}')
        await bot.session.close()
    except Exception as e:
        print(f'Error: {e}')
asyncio.run(test())
"
```

## 📞 Getting Help

If you're still having issues:

1. **Check the logs**: Look at `bot.log` for error messages
2. **Verify token**: Make sure your bot token is correct
3. **Test connection**: Use the debug commands above
4. **Restart bot**: Stop and restart the bot process

## 🎯 Expected Behavior

When working correctly:
1. Bot starts without errors
2. You see "✅ All modules imported successfully"
3. You see "🎉 Leandro Crypto Bot is now OPERATIONAL!"
4. Sending `/start` to your bot shows welcome message with menu