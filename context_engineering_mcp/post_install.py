#!/usr/bin/env python3
"""
Post-installation script to ensure Node.js dependencies are installed
"""

import subprocess
import sys
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_node_dependencies():
    """Install Node.js dependencies for the MCP server"""

    # Find the mcp-server directory
    package_root = Path(__file__).parent.parent
    mcp_server_dir = package_root / "mcp-server"

    if not mcp_server_dir.exists():
        # Try relative to the package itself
        mcp_server_dir = Path(__file__).parent / "mcp-server"

    if not mcp_server_dir.exists():
        logger.warning("mcp-server directory not found")
        return False

    # Check if package.json exists
    package_json = mcp_server_dir / "package.json"
    if not package_json.exists():
        logger.warning("package.json not found in mcp-server directory")
        return False

    # Install dependencies
    try:
        logger.info(f"Installing Node.js dependencies in {mcp_server_dir}")
        result = subprocess.run(
            ["npm", "install", "--production"],
            cwd=mcp_server_dir,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            logger.info("Node.js dependencies installed successfully")
            return True
        else:
            logger.error(f"npm install failed: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.error("npm not found. Please install Node.js and npm")
        return False
    except Exception as e:
        logger.error(f"Error installing dependencies: {e}")
        return False

if __name__ == "__main__":
    success = install_node_dependencies()
    sys.exit(0 if success else 1)