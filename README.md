# μ-MCP Server

**μ** (mu) = micro, minimal - in sardonic contrast to zen-mcp's 10,000+ lines of orchestration.

A pure MCP server that does one thing well: enable chat with AI models via OpenRouter.

## Philosophy

Following UNIX principles:
- **Do one thing well**: Provide access to AI models
- **No hardcoded control flow**: The AI agents decide everything
- **Minimal interface**: One tool, clean parameters
- **Persistent state**: Conversations persist across sessions
- **Model agnostic**: Support any OpenRouter model

## Features

- ✅ **Multi-model conversations** - Switch models mid-conversation
- ✅ **Persistent storage** - Conversations saved to disk
- ✅ **Model registry** - Curated models with capabilities
- ✅ **LLM-driven model selection** - Calling agent picks the best model
- ✅ **Reasoning effort control** - Simple pass-through to OpenRouter (low/medium/high)
- ✅ **MCP prompts** - Slash commands `/mu:chat` and `/mu:continue`
- ✅ **Token-based budgeting** - Smart file truncation
- ✅ **Proper MIME types** - Correct image format handling

## What's NOT Included

- ❌ Workflow orchestration (let AI decide)
- ❌ Step tracking (unnecessary complexity)
- ❌ Confidence levels (trust the models)
- ❌ Expert validation (models are the experts)
- ❌ Hardcoded procedures (pure AI agency)
- ❌ Web search implementation (just ask Claude)
- ❌ Multiple providers (OpenRouter handles all)

## Setup

### Quick Install (with uv)

1. **Get OpenRouter API key**: https://openrouter.ai/keys

2. **Run setup script**:
   ```bash
   ./setup.sh
   ```
   
   This will:
   - Install `uv` if not present (blazing fast Python package manager)
   - Install dependencies
   - Show you the Claude Desktop config

3. **Add to Claude Desktop config** (`~/.config/claude/claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "mu-mcp": {
         "command": "uv",
         "args": ["--directory", "/path/to/mu-mcp", "run", "python", "/path/to/mu-mcp/server.py"],
         "env": {
           "OPENROUTER_API_KEY": "your-key-here"
         }
       }
     }
   }
   ```

4. **Restart Claude Desktop**

### Manual Install (traditional)

If you prefer pip/venv:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Then use this Claude Desktop config:
```json
{
  "mcpServers": {
    "mu-mcp": {
      "command": "/path/to/mu-mcp/venv/bin/python",
      "args": ["/path/to/mu-mcp/server.py"],
      "env": {
        "OPENROUTER_API_KEY": "your-key-here"
      }
    }
  }
}

## Usage

### Basic Chat
```
/mu:chat
Then specify model and prompt: "Use gpt-5 to explain quantum computing"
```

### Continue Conversations
```
/mu:continue
Automatically uses the latest conversation's continuation_id
```

### Challenge Mode
```
/mu:challenge
Encourages critical thinking and avoids reflexive agreement
```

### Multi-AI Discussion
```
/mu:discuss
Orchestrate multi-turn discussions among diverse AI models
```

### Model Selection
```
Chat with GPT-5 about code optimization
Chat with O3 Mini High for complex reasoning
Chat with DeepSeek R1 for systematic analysis  
Chat with Claude about API design
```

### Reasoning Effort Control
```
Chat with o3-mini using high reasoning effort for complex problems
Chat with gpt-5 using low reasoning effort for quick responses
Chat with o4-mini-high using medium reasoning effort for balanced analysis
```

Note: Reasoning effort is automatically ignored by models that don't support it.

### With Files and Images
```
Review this code: /path/to/file.py
Analyze this diagram: /path/to/image.png
```

### Model Selection by LLM
The calling LLM agent (Claude) sees all available models with their descriptions and capabilities, allowing intelligent selection based on:
- Task requirements and complexity
- Performance vs cost trade-offs  
- Specific model strengths
- Context window needs
- Image support requirements

## Architecture

```
server.py         # MCP server with prompt handlers
chat_handler.py   # Chat logic with multi-model support
models.py         # Model registry and capabilities
prompts.py        # System prompts for peer AI collaboration
storage.py        # Persistent conversation storage
.env.example      # Configuration template
```

## Configuration

### Environment Variables

- `OPENROUTER_API_KEY` - Your OpenRouter API key (required)
- `OPENROUTER_ALLOWED_MODELS` - Comma-separated list of allowed models (optional)
- `LOG_LEVEL` - Logging verbosity (DEBUG, INFO, WARNING, ERROR)

## Why μ-MCP?

### The Problem with zen-mcp-server

zen-mcp grew to **10,000+ lines** trying to control AI behavior:
- 15+ specialized tools with overlapping functionality
- Complex workflow orchestration that limits AI agency
- Hardcoded decision trees that prescribe solutions
- "Step tracking" and "confidence levels" that add noise
- Redundant schema fields and validation layers

### The μ-MCP Approach

**Less code, more capability**:
- Single tool that does one thing perfectly
- AI agents make all decisions
- Clean, persistent conversation state
- Model capabilities, not hardcoded behaviors
- Trust in AI intelligence over procedural control

### Philosophical Difference

**zen-mcp**: "Let me orchestrate 12 steps for you to debug this code"
**μ-mcp**: "Here's the model catalog. Pick what you need."

The best tool is the one that gets out of the way.

## Related Projects

- [zen-mcp-server](https://github.com/winnative/zen-mcp-server) - The bloated alternative we're reacting against

## License

MIT