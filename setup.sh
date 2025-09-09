#!/bin/bash

echo "🚀 μ-MCP Server Setup (with uv)"
echo "=============================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    echo "✅ uv installed successfully"
else
    echo "✅ uv is already installed"
fi

# Install dependencies using uv
echo ""
echo "📥 Installing dependencies..."
uv pip sync requirements.txt

# Check for API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo ""
    echo "⚠️  OPENROUTER_API_KEY not set!"
    echo "Please add to your shell profile:"
    echo "export OPENROUTER_API_KEY='your-api-key'"
    echo ""
    echo "Get your API key at: https://openrouter.ai/keys"
else
    echo "✅ OpenRouter API key found"
fi

# Create MCP config
echo ""
echo "📝 Add to Claude Desktop config (~/.config/claude/claude_desktop_config.json):"
echo ""
cat << EOF
{
  "mcpServers": {
    "mu-mcp": {
      "command": "uv",
      "args": ["--directory", "$(pwd)", "run", "python", "$(pwd)/server.py"],
      "env": {
        "OPENROUTER_API_KEY": "\$OPENROUTER_API_KEY"
      }
    }
  }
}
EOF

echo ""
echo "✅ Setup complete! Restart Claude Desktop to use μ-MCP server."
echo ""
echo "To test the server manually, run:"
echo "  uv run python server.py"