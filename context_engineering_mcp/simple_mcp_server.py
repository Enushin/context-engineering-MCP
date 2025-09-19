#!/usr/bin/env python3
"""
Simplest possible MCP Server - for debugging
"""
import sys
import json

def main():
    """Ultra simple MCP server for testing"""
    sys.stderr.write("Simple MCP Server started\n")
    sys.stderr.flush()

    while True:
        # Read Content-Length header
        header_line = sys.stdin.readline()
        if not header_line:
            break

        if header_line.startswith("Content-Length:"):
            content_length = int(header_line.split(":")[1].strip())

            # Read blank line
            sys.stdin.readline()

            # Read content
            content = sys.stdin.read(content_length)
            request = json.loads(content)

            # Simple responses
            response = None

            if request.get("method") == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "0.1.0",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "simple-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
            elif request.get("method") == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": "test_tool",
                                "description": "A test tool",
                                "inputSchema": {"type": "object", "properties": {}}
                            }
                        ]
                    }
                }
            elif request.get("method") == "shutdown":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": None
                }

            if response:
                content = json.dumps(response)
                sys.stdout.write(f"Content-Length: {len(content)}\r\n\r\n{content}")
                sys.stdout.flush()

            if request.get("method") == "shutdown":
                break

if __name__ == "__main__":
    main()