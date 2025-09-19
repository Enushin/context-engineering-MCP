# Context Engineering MCP

> Installable MCP Package for Any Project - Claude Desktop/Code Integration Ready

[日本語](README.md) | English

## Overview

Context Engineering MCP is a comprehensive MCP package that revolutionizes AI context management. Install it in any project to add advanced context management capabilities.

### Key Features

- **15 MCP Tools**: AI guide management, context optimization, template management
- **Gemini 2.0 Flash Integration**: Semantic search and analysis
- **52% Token Reduction**: AI-powered optimization
- **Project Independent**: Available for any project

## Installation

### 🚀 One-Step Installation (Easiest)

Run in your project directory:

#### Method 1: Local Script
```bash
curl -sSL https://raw.githubusercontent.com/Enushin/context-engineering-MCP/main/install.sh | bash
```

#### Method 2: Python Command
```bash
uvx --from git+https://github.com/Enushin/context-engineering-MCP ce-quickstart
```

Both methods will:
- Prompt for GEMINI_API_KEY input
- Automatically create .env file
- Register MCP tools with Claude

### 🛠 Manual Installation (2 Steps)

#### Step 1: Set API Key
```bash
echo "GEMINI_API_KEY=your-actual-key" > .env
```

#### Step 2: Add MCP Tools
```bash
claude mcp add context-eng -- uvx --from git+https://github.com/Enushin/context-engineering-MCP context-engineering-mcp start-mcp-server --project "$PWD"
```

### 💻 Claude Desktop Configuration (Manual)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "context-engineering": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Enushin/context-engineering-MCP",
        "context-engineering-mcp",
        "start-mcp-server",
        "--project",
        "${PROJECT_PATH}"
      ],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

## Usage

### Basic Usage

In your project directory:

```bash
# Start MCP server (via Claude)
uvx --from git+https://github.com/Enushin/context-engineering-MCP \
  context-engineering-mcp start-mcp-server --project "$PWD"
```

### Environment Variables (Important)

MCP tools automatically load GEMINI_API_KEY from your project's `.env` file:

```bash
# Create .env file in project root
cat > .env << EOF
GEMINI_API_KEY=your-actual-api-key-here
EOF
```

Or set as a global environment variable:

```bash
# Add to ~/.zshrc or ~/.bashrc
export GEMINI_API_KEY="your-actual-api-key-here"
source ~/.zshrc  # Apply immediately
```

### Available Commands

```bash
# Start MCP server
context-engineering-mcp start-mcp-server --project /path/to/project

# Run setup
context-engineering-mcp setup

# Generate Claude Desktop config
context-engineering-mcp config --output claude_config.json
```

## MCP Tool List

### AI Guide Management (4 tools)
- `list_ai_guides` - Get guide list
- `search_ai_guides` - Keyword search
- `search_guides_with_gemini` - AI search
- `analyze_guide` - Guide analysis

### Context Management (7 tools)
- `create_context_session` - Create session
- `create_context_window` - Create window
- `add_context_element` - Add element
- `analyze_context` - Quality analysis
- `optimize_context` - Optimization
- `auto_optimize_context` - Auto-optimization
- `get_context_stats` - Get statistics

### Template Management (4 tools)
- `create_prompt_template` - Create template
- `generate_prompt_template` - AI generation
- `list_prompt_templates` - List display
- `render_template` - Rendering

## 👨‍💻 Project Integration Examples

### 1. Use in New Project

```bash
# Create project
mkdir my-ai-project
cd my-ai-project

# One-step installation
curl -sSL https://raw.githubusercontent.com/Enushin/context-engineering-MCP/main/install.sh | bash
# Or: uvx --from git+https://github.com/Enushin/context-engineering-MCP ce-quickstart

# Start using in Claude Desktop
```

### 2. Integrate with Existing Project

```bash
cd existing-project

# One-step installation (interactive API key input)
curl -sSL https://raw.githubusercontent.com/Enushin/context-engineering-MCP/main/install.sh | bash

# 15 tools now available in Claude Desktop/Code
```

## For Developers

### Local Development

```bash
# Clone repository
git clone https://github.com/Enushin/context-engineering-MCP.git
cd context-engineering-MCP

# Setup development environment
pip install -e ".[dev]"
cd mcp-server && npm install

# Run tests
pytest
npm test
```

### Package Structure

```
context-engineering-MCP/
├── context_engineering_mcp/   # Python package
│   ├── __init__.py
│   ├── cli.py                # CLI entry point
│   └── mcp_server.py         # MCP server wrapper
├── mcp-server/               # Node.js MCP server
│   └── context_mcp_server.js
├── pyproject.toml           # Package configuration
└── README.md
```

## Troubleshooting

### GEMINI_API_KEY Error
```bash
# Set environment variable
export GEMINI_API_KEY="your-actual-key"

# Or .env file
echo "GEMINI_API_KEY=your-actual-key" > .env
```

### Node.js Error
```bash
# Node.js 18+ required
node --version  # Check for v18.0.0 or higher
```

### Port Conflict
```bash
# Use custom port
context-engineering-mcp start-mcp-server --port 9002
```

## License

MIT License

## Acknowledgments

This project was inspired by [ShunsukeHayashi/context_engineering_MCP](https://github.com/ShunsukeHayashi/context_engineering_MCP). We appreciate the excellent architecture and concepts of the original project.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

Issues: [GitHub Issues](https://github.com/Enushin/context-engineering-MCP/issues)

---

**Context Engineering MCP** - Advanced context management for any project.