#!/usr/bin/env python3
"""
Context Engineering MCP - CLI entry point
Provides command-line interface for starting the MCP server
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_package_root() -> Path:
    """Get the package root directory"""
    return Path(__file__).parent.parent

def find_mcp_server() -> Optional[Path]:
    """Find the MCP server JavaScript file"""
    package_root = get_package_root()

    # Check multiple possible locations - prefer standalone version
    possible_paths = [
        package_root / "mcp-server" / "standalone_mcp_server.js",
        Path(__file__).parent / "mcp-server" / "standalone_mcp_server.js",
        package_root / "mcp-server" / "context_mcp_server.js",
        package_root / "context_mcp_server.js",
        Path(__file__).parent / "mcp_server" / "context_mcp_server.js",
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None

def start_mcp_server(project_path: Optional[str] = None, port: Optional[int] = None) -> None:
    """
    Start the Context Engineering MCP server (Pure Python version)

    Args:
        project_path: Path to the project directory (defaults to current directory)
        port: Port for the API servers (not used in pure Python version)
    """
    # Set project path
    if project_path:
        os.chdir(project_path)
    else:
        project_path = os.getcwd()

    logger.info(f"Starting Context Engineering MCP server for project: {project_path}")

    # Load .env.local or .env file from project directory
    env_local_file = Path(project_path) / ".env.local"
    env_file = Path(project_path) / ".env"

    if env_local_file.exists():
        logger.info(f"Loading environment from: {env_local_file}")
        try:
            from dotenv import load_dotenv
            load_dotenv(env_local_file)
        except ImportError:
            logger.warning("python-dotenv not installed, loading env manually")
    elif env_file.exists():
        logger.info(f"Loading environment from: {env_file}")
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            logger.warning("python-dotenv not installed, loading env manually")

    # Use Pure Python MCP Server (no Node.js required)
    logger.info("Starting Pure Python MCP Server (no Node.js dependencies)")

    # Set environment variables
    env = os.environ.copy()
    env["PROJECT_PATH"] = project_path

    if port:
        env["CONTEXT_API_PORT"] = str(port)
        env["AI_GUIDES_API_PORT"] = str(port - 1)  # Use port-1 for AI guides

    # Check for GEMINI_API_KEY
    if not env.get("GEMINI_API_KEY"):
        # Try to load from project .env.local or .env file
        for env_file_name in [".env.local", ".env"]:
            env_file = Path(project_path) / env_file_name
            if env_file.exists():
                with open(env_file) as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY="):
                            key = line.strip().split("=", 1)[1].strip('"').strip("'")
                            if key and key != "" and not key.startswith("your-"):
                                env["GEMINI_API_KEY"] = key
                                logger.info(f"GEMINI_API_KEY loaded from {env_file_name}")
                                break
                if env.get("GEMINI_API_KEY"):
                    break

        if not env.get("GEMINI_API_KEY"):
            logger.warning("GEMINI_API_KEY not found. Create a .env.local file with GEMINI_API_KEY=your-key")
            logger.warning("Some features may be limited without the API key.")

    # Import and run the pure Python MCP server
    try:
        from .pure_mcp_server import PurePythonMCPServer

        # Create and run the server
        server = PurePythonMCPServer()
        server.run()

    except KeyboardInterrupt:
        logger.info("MCP server stopped by user")
        sys.exit(0)
    except ImportError as e:
        logger.error(f"Failed to import Pure Python MCP server: {e}")
        logger.error("Please ensure the package is properly installed")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        sys.exit(1)

def setup_services(install_deps: bool = True) -> None:
    """
    Setup Context Engineering services

    Args:
        install_deps: Whether to install dependencies
    """
    package_root = get_package_root()

    logger.info("Setting up Context Engineering services...")

    # Install Python dependencies if needed
    if install_deps:
        logger.info("Installing Python dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", str(package_root)
        ], check=True)

    # Install Node.js dependencies
    mcp_server_dir = package_root / "mcp-server"
    if mcp_server_dir.exists():
        logger.info("Installing Node.js dependencies...")
        subprocess.run(["npm", "install"], cwd=str(mcp_server_dir), check=True)

    logger.info("Setup complete!")

def generate_config() -> dict:
    """Generate Claude Desktop configuration"""
    package_root = get_package_root()
    mcp_server_path = find_mcp_server()

    if not mcp_server_path:
        logger.error("MCP server file not found")
        return {}

    config = {
        "mcpServers": {
            "context-engineering": {
                "command": "node",
                "args": [str(mcp_server_path)],
                "env": {
                    "CONTEXT_API_URL": "http://localhost:9001",
                    "AI_GUIDES_API_URL": "http://localhost:8888"
                }
            }
        }
    }

    return config

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Context Engineering MCP - Advanced AI-powered context management"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start MCP server command
    start_parser = subparsers.add_parser(
        "start-mcp-server",
        help="Start the MCP server for Claude Desktop/Code integration"
    )
    start_parser.add_argument(
        "--project",
        type=str,
        default=os.environ.get("PWD", os.getcwd()),
        help="Project directory path (defaults to $PWD or current directory)"
    )
    start_parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port for API servers (defaults to 9001)"
    )

    # Setup command
    setup_parser = subparsers.add_parser(
        "setup",
        help="Setup Context Engineering services"
    )
    setup_parser.add_argument(
        "--no-deps",
        action="store_true",
        help="Skip dependency installation"
    )

    # Config command
    config_parser = subparsers.add_parser(
        "config",
        help="Generate Claude Desktop configuration"
    )
    config_parser.add_argument(
        "--output",
        type=str,
        help="Output file path for configuration"
    )

    # Quickstart command
    quickstart_parser = subparsers.add_parser(
        "quickstart",
        help="Interactive quickstart setup (API key + MCP installation)"
    )

    # Version command
    parser.add_argument(
        "--version",
        action="version",
        version="Context Engineering MCP v2.0.0"
    )

    args = parser.parse_args()

    # Execute command
    if args.command == "start-mcp-server":
        start_mcp_server(args.project, args.port)

    elif args.command == "setup":
        setup_services(not args.no_deps)

    elif args.command == "config":
        config = generate_config()
        config_json = json.dumps(config, indent=2)

        if args.output:
            with open(args.output, "w") as f:
                f.write(config_json)
            logger.info(f"Configuration written to: {args.output}")
        else:
            print(config_json)

    elif args.command == "quickstart":
        from .setup import quickstart
        quickstart()

    else:
        # Default action - start MCP server
        start_mcp_server()

if __name__ == "__main__":
    main()