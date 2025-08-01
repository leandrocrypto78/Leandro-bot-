#!/usr/bin/env python3
"""
Test script to verify bot functionality
"""

import asyncio
import logging
from main_1753060384126 import welcome_handler, get_main_menu
from aiogram.types import Message, User
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockMessage:
    """Mock message for testing"""
    def __init__(self, user_id=12345, username="testuser"):
        self.from_user = MockUser(user_id, username)
        self.text = "/start"
    
    async def reply(self, text, reply_markup=None, parse_mode=None):
        print(f"Bot would reply: {text}")
        if reply_markup:
            print(f"With keyboard: {reply_markup}")
        return True

class MockUser:
    """Mock user for testing"""
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.first_name = username

class MockFSMContext:
    """Mock FSM context for testing"""
    def __init__(self):
        self.storage = MemoryStorage()
    
    async def set_state(self, state):
        print(f"State set to: {state}")
    
    async def get_state(self):
        return None

async def test_start_command():
    """Test the /start command functionality"""
    print("🧪 Testing /start command...")
    
    # Create mock message and context
    message = MockMessage()
    state = MockFSMContext()
    
    try:
        # Test the welcome handler
        await welcome_handler(message, state)
        print("✅ /start command test passed!")
        
    except Exception as e:
        print(f"❌ /start command test failed: {e}")

async def test_main_menu():
    """Test the main menu generation"""
    print("\n🧪 Testing main menu generation...")
    
    try:
        menu = get_main_menu()
        print("✅ Main menu generated successfully!")
        print(f"Menu has {len(menu.inline_keyboard)} rows")
        
        for i, row in enumerate(menu.inline_keyboard):
            print(f"Row {i+1}: {[btn.text for btn in row]}")
            
    except Exception as e:
        print(f"❌ Main menu test failed: {e}")

async def main():
    """Run all tests"""
    print("🚀 Starting bot functionality tests...\n")
    
    await test_start_command()
    await test_main_menu()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())