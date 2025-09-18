#!/usr/bin/env python3
"""
MCP Server starter for Context Engineering
This module provides the Python wrapper to start the Node.js MCP server
"""

import subprocess
import sys
import os
import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_mcp_server():
    """Start the MCP server via stdio for Claude Desktop integration"""

    # Find the MCP server JavaScript file
    package_root = Path(__file__).parent.parent
    mcp_server_paths = [
        package_root / "mcp-server" / "context_mcp_server.js",
        Path(__file__).parent / "mcp_server" / "context_mcp_server.js",
    ]

    mcp_server_path = None
    for path in mcp_server_paths:
        if path.exists():
            mcp_server_path = path
            break

    if not mcp_server_path:
        logger.error("MCP server file not found")
        sys.exit(1)

    # Set up environment
    env = os.environ.copy()

    # Get project path from argument or environment
    project_path = os.environ.get("PROJECT_PATH", os.getcwd())
    env["PROJECT_PATH"] = project_path

    # Ensure API URLs are set
    if "CONTEXT_API_URL" not in env:
        env["CONTEXT_API_URL"] = "http://localhost:9001"
    if "AI_GUIDES_API_URL" not in env:
        env["AI_GUIDES_API_URL"] = "http://localhost:8888"

    logger.info(f"Starting MCP server from: {mcp_server_path}")
    logger.info(f"Project path: {project_path}")

    try:
        # Start the Node.js MCP server with stdio
        process = subprocess.run(
            ["node", str(mcp_server_path)],
            env=env,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )

        sys.exit(process.returncode)

    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_mcp_server()