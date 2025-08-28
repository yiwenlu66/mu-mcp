# Version Tool

Shows server version, configuration, and available tools.

## Usage

```
"Get zen to show its version"
```

## Features

- Server version and build details
- Configuration and capabilities
- Tool inventory and status
- System health verification
- Debug information

## Output Information

The tool provides:

**Version Details:**
- Server version number
- Build timestamp and commit information
- MCP protocol version compatibility
- Python runtime version

**Configuration Summary:**
- Active providers and their status
- Default model configuration
- Feature flags and settings
- Environment configuration overview

**Tool Availability:**
- Complete list of available tools
- Tool version information
- Capability status for each tool

**System Information:**
- Server uptime and status
- Memory and resource usage (if available)
- Conversation memory status
- Server process information

## Example Output

```
🔧 Zen MCP Server Information

📋 Version: 2.15.0
🏗️ Build: 2024-01-15T10:30:00Z (commit: abc123f)
🔌 MCP Protocol: 1.0.0
🐍 Python Runtime: 3.11.7

⚙️ Configuration:
• Default Model: auto
• Providers: Google ✅, OpenAI ✅, Custom ✅
• Conversation Memory: Active ✅
• Web Search: Enabled

🛠️ Available Tools (12):
• chat - General development chat & collaborative thinking
• thinkdeep - Extended reasoning partner  
• consensus - Multi-model perspective gathering
• codereview - Professional code review
• precommit - Pre-commit validation
• debug - Expert debugging assistant
• analyze - Smart file analysis
• refactor - Intelligent code refactoring
• tracer - Static code analysis prompt generator
• testgen - Comprehensive test generation
• listmodels - List available models
• version - Server information

🔍 System Status:
• Server Uptime: 2h 35m
• Memory Storage: Active
• Server Process: Running
```

## When to Use Version Tool

- **Troubleshooting**: When experiencing issues with the server or tools
- **Configuration verification**: To confirm your setup is correct
- **Support requests**: To provide system information when asking for help
- **Update checking**: To verify you're running the latest version
- **Capability discovery**: To understand what features are available

## Debug Information

The version tool can help diagnose common issues:

**Connection Problems:**
- Verify server is running and responsive
- Check MCP protocol compatibility
- Confirm tool availability

**Configuration Issues:**
- Validate provider setup
- Check API key configuration status
- Verify feature enablement

**Performance Troubleshooting:**
- Server uptime and stability
- Resource usage patterns
- Memory storage health

## Tool Parameters

This tool requires no parameters - it provides comprehensive server information automatically.


