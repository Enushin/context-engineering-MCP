#!/usr/bin/env python3
"""
Pure Python MCP Server Implementation
No Node.js dependencies required - works with any Python environment
"""

import sys
import json
import uuid
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import asyncio
from pathlib import Path

# Setup logging to stderr so it doesn't interfere with stdio communication
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

class PurePythonMCPServer:
    """
    Pure Python implementation of MCP Server
    Handles stdio communication without Node.js dependencies
    """

    def __init__(self):
        self.sessions = {}
        self.windows = {}
        self.templates = {}
        self.elements = {}

    def generate_id(self) -> str:
        """Generate unique ID"""
        return str(uuid.uuid4())

    def handle_initialize(self, request: Dict) -> Dict:
        """Handle initialization request"""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "protocolVersion": "0.1.0",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "context-engineering-mcp",
                    "version": "2.0.0"
                }
            }
        }

    def handle_list_tools(self, request: Dict) -> Dict:
        """Handle tools/list request"""
        tools = [
            {
                "name": "create_context_session",
                "description": "Create a new context engineering session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Session name",
                            "default": "New Session"
                        },
                        "description": {
                            "type": "string",
                            "description": "Session description",
                            "default": ""
                        }
                    }
                }
            },
            {
                "name": "create_context_window",
                "description": "Create a new context window in a session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "The session ID"
                        },
                        "max_tokens": {
                            "type": "integer",
                            "description": "Maximum tokens",
                            "default": 8192
                        },
                        "reserved_tokens": {
                            "type": "integer",
                            "description": "Reserved tokens",
                            "default": 512
                        }
                    },
                    "required": ["session_id"]
                }
            },
            {
                "name": "add_context_element",
                "description": "Add an element to a context window",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "window_id": {
                            "type": "string",
                            "description": "The context window ID"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to add"
                        },
                        "type": {
                            "type": "string",
                            "enum": ["system", "user", "assistant"],
                            "default": "user"
                        },
                        "priority": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 10,
                            "default": 5
                        }
                    },
                    "required": ["window_id", "content"]
                }
            },
            {
                "name": "get_context_stats",
                "description": "Get statistics about the context engineering system",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "create_prompt_template",
                "description": "Create a new prompt template",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Template name"
                        },
                        "description": {
                            "type": "string",
                            "description": "Template description"
                        },
                        "template": {
                            "type": "string",
                            "description": "Template content with {variables}"
                        },
                        "category": {
                            "type": "string",
                            "default": "general"
                        }
                    },
                    "required": ["name", "description", "template"]
                }
            },
            {
                "name": "list_prompt_templates",
                "description": "List available prompt templates",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Filter by category"
                        }
                    }
                }
            }
        ]

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "tools": tools
            }
        }

    def handle_tool_call(self, request: Dict) -> Dict:
        """Handle tools/call request"""
        params = request.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        try:
            result = None

            if tool_name == "create_context_session":
                session_id = self.generate_id()
                self.sessions[session_id] = {
                    "id": session_id,
                    "name": args.get("name", "New Session"),
                    "description": args.get("description", ""),
                    "created_at": datetime.now().isoformat(),
                    "windows": []
                }
                result = {
                    "success": True,
                    "session_id": session_id,
                    "message": f"Session created: {self.sessions[session_id]['name']}"
                }

            elif tool_name == "create_context_window":
                window_id = self.generate_id()
                session_id = args.get("session_id")

                if session_id not in self.sessions:
                    raise ValueError(f"Session {session_id} not found")

                self.windows[window_id] = {
                    "id": window_id,
                    "session_id": session_id,
                    "max_tokens": args.get("max_tokens", 8192),
                    "reserved_tokens": args.get("reserved_tokens", 512),
                    "elements": [],
                    "created_at": datetime.now().isoformat()
                }

                self.sessions[session_id]["windows"].append(window_id)

                result = {
                    "success": True,
                    "window_id": window_id,
                    "message": f"Context window created with {self.windows[window_id]['max_tokens']} max tokens"
                }

            elif tool_name == "add_context_element":
                window_id = args.get("window_id")

                if window_id not in self.windows:
                    raise ValueError(f"Window {window_id} not found")

                element_id = self.generate_id()
                element = {
                    "id": element_id,
                    "content": args.get("content"),
                    "type": args.get("type", "user"),
                    "priority": args.get("priority", 5),
                    "created_at": datetime.now().isoformat()
                }

                self.windows[window_id]["elements"].append(element_id)
                self.elements[element_id] = element

                result = {
                    "success": True,
                    "element_id": element_id,
                    "message": "Element added to context window",
                    "element_count": len(self.windows[window_id]["elements"])
                }

            elif tool_name == "get_context_stats":
                result = {
                    "sessions": len(self.sessions),
                    "windows": len(self.windows),
                    "templates": len(self.templates),
                    "total_elements": len(self.elements),
                    "status": "operational"
                }

            elif tool_name == "create_prompt_template":
                template_id = self.generate_id()
                self.templates[template_id] = {
                    "id": template_id,
                    "name": args.get("name"),
                    "description": args.get("description"),
                    "template": args.get("template"),
                    "category": args.get("category", "general"),
                    "created_at": datetime.now().isoformat()
                }

                result = {
                    "success": True,
                    "template_id": template_id,
                    "message": f"Template created: {self.templates[template_id]['name']}"
                }

            elif tool_name == "list_prompt_templates":
                category = args.get("category")
                templates = list(self.templates.values())

                if category:
                    templates = [t for t in templates if t["category"] == category]

                result = {
                    "templates": templates,
                    "total": len(templates)
                }

            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "error": str(e),
                                "tool": tool_name
                            }, indent=2)
                        }
                    ],
                    "isError": True
                }
            }

    def handle_request(self, request: Dict) -> Optional[Dict]:
        """Handle incoming JSON-RPC request"""
        method = request.get("method", "")

        logger.info(f"Handling method: {method}")

        if method == "initialize":
            return self.handle_initialize(request)
        elif method == "initialized":
            # No response needed for initialized notification
            return None
        elif method == "tools/list":
            return self.handle_list_tools(request)
        elif method == "tools/call":
            return self.handle_tool_call(request)
        elif method == "shutdown":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": None
            }
        else:
            # Unknown method
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    def run(self):
        """Main run loop for stdio communication"""
        logger.info("Starting Pure Python MCP Server (stdio mode)")

        try:
            while True:
                # Read from stdin (line by line)
                line = sys.stdin.readline()

                if not line:
                    logger.info("No more input, shutting down")
                    break

                line = line.strip()
                if not line:
                    continue

                # Check for Content-Length header (LSP-style communication)
                if line.startswith("Content-Length:"):
                    # Read the content length
                    content_length = int(line.split(":")[1].strip())

                    # Read the empty line
                    sys.stdin.readline()

                    # Read the JSON content
                    content = sys.stdin.read(content_length)

                    try:
                        request = json.loads(content)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON: {e}")
                        continue
                else:
                    # Try to parse as JSON directly
                    try:
                        request = json.loads(line)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON: {e}")
                        continue

                # Handle the request
                response = self.handle_request(request)

                if response:
                    # Send response with Content-Length header
                    response_json = json.dumps(response)
                    response_bytes = response_json.encode('utf-8')

                    sys.stdout.write(f"Content-Length: {len(response_bytes)}\r\n\r\n")
                    sys.stdout.write(response_json)
                    sys.stdout.flush()

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise

def main():
    """Main entry point"""
    server = PurePythonMCPServer()
    server.run()

if __name__ == "__main__":
    main()