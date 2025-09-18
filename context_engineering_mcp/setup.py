#!/usr/bin/env python3
"""
Context Engineering MCP - Interactive Setup Script
Called via: context-engineering-mcp quickstart
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional


def check_claude_cli() -> bool:
    """Check if Claude CLI is installed"""
    try:
        subprocess.run(["claude", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_or_create_api_key() -> str:
    """Get GEMINI_API_KEY from environment or prompt user"""
    # Check .env file first
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    key = line.strip().split("=", 1)[1].strip('"').strip("'")
                    if key and key != "your-api-key-here":
                        print("✓ GEMINI_API_KEY found in .env file")
                        return key

    # Check environment variable
    if os.environ.get("GEMINI_API_KEY"):
        print("✓ GEMINI_API_KEY found in environment")
        return os.environ["GEMINI_API_KEY"]

    # Prompt user
    print("\n🔑 GEMINI_API_KEY not found")
    print("Get your API key from: https://makersuite.google.com/app/apikey")

    api_key = input("Enter your GEMINI_API_KEY (or press Enter to skip): ").strip()

    if not api_key:
        api_key = "your-api-key-here"
        print("⚠ Skipping API key. You'll need to set it later in .env file")
    else:
        print("✓ API Key received")

    # Save to .env
    with open(".env", "a") as f:
        f.write(f"\nGEMINI_API_KEY={api_key}\n")

    return api_key


def quickstart():
    """Run interactive quickstart setup"""
    print("━" * 60)
    print("    Context Engineering MCP - Quick Setup    ")
    print("━" * 60)

    # Check Claude CLI
    if not check_claude_cli():
        print("❌ Claude CLI not found. Please install it first.")
        print("Visit: https://docs.anthropic.com/claude/docs/claude-desktop")
        sys.exit(1)

    print("✓ Claude CLI detected")

    # Get/Create API key
    api_key = get_or_create_api_key()

    # Run claude mcp add command
    print("\n📦 Installing Context Engineering MCP...")

    cmd = [
        "claude", "mcp", "add", "context-eng", "--",
        "uvx", "--from", "git+https://github.com/Enushin/context-engineering-MCP",
        "context-engineering-mcp", "start-mcp-server", "--project", os.getcwd()
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ MCP tools installed successfully!")
        else:
            print(f"⚠ Installation completed with warnings: {result.stderr}")
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        sys.exit(1)

    # Success message
    print("\n" + "━" * 60)
    print("    ✅ Setup Complete!    ")
    print("━" * 60)

    print("\n📚 Available Tools:")
    print("  • AI Guides Management (4 tools)")
    print("  • Context Management (7 tools)")
    print("  • Template Management (4 tools)")

    print("\n🚀 Next Steps:")
    print("  1. Restart Claude Desktop/Code")
    print("  2. MCP tools will be available automatically")

    if api_key == "your-api-key-here":
        print("\n⚠ Don't forget to update your GEMINI_API_KEY in .env file!")


if __name__ == "__main__":
    quickstart()