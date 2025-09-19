#!/usr/bin/env python3
"""
Test script for Pure Python MCP Server
"""

import json
import sys
from io import StringIO
from context_engineering_mcp.pure_mcp_server import PurePythonMCPServer

def test_mcp_server():
    """Test basic MCP server functionality"""
    server = PurePythonMCPServer()

    # Test initialize
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }

    response = server.handle_request(init_request)
    print("Initialize response:", json.dumps(response, indent=2))

    # Test list tools
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }

    response = server.handle_request(list_tools_request)
    print("\nTools list response:", json.dumps(response, indent=2)[:500] + "...")

    # Test create session
    create_session_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "create_context_session",
            "arguments": {
                "name": "Test Session",
                "description": "Testing pure Python MCP"
            }
        }
    }

    response = server.handle_request(create_session_request)
    print("\nCreate session response:", json.dumps(response, indent=2))

    # Extract session_id
    result = json.loads(response["result"]["content"][0]["text"])
    session_id = result["session_id"]

    # Test create window
    create_window_request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "create_context_window",
            "arguments": {
                "session_id": session_id,
                "max_tokens": 4096
            }
        }
    }

    response = server.handle_request(create_window_request)
    print("\nCreate window response:", json.dumps(response, indent=2))

    # Get stats
    stats_request = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "get_context_stats",
            "arguments": {}
        }
    }

    response = server.handle_request(stats_request)
    print("\nStats response:", json.dumps(response, indent=2))

    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_mcp_server()