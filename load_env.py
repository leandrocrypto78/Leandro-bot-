#!/usr/bin/env python3
"""
Load environment variables from .env file
"""

import os

def load_env_file():
    """Load environment variables from .env file"""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Environment variables loaded from .env file")
    else:
        print("⚠️ No .env file found")

if __name__ == "__main__":
    load_env_file()