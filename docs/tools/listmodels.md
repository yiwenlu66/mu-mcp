# ListModels Tool

Shows available AI models, aliases, context windows, and capabilities.

## Usage

```
"Use zen to list available models"
```

## Features

- Provider organization and status
- Model capabilities and context windows
- Alias mappings
- Configuration status
- Extended thinking and vision support

## Output Information

The tool displays:

**Provider Status:**
- Which providers are configured and available
- API key status (without revealing the actual keys)
- Provider priority order

**Model Details:**
- Full model names and their aliases
- Context window sizes (tokens)
- Special capabilities (thinking modes, vision support, etc.)
- Provider-specific features

**Capability Summary:**
- Which models support extended thinking
- Vision-capable models for image analysis
- Models with largest context windows
- Fastest models for quick tasks

## Example Output

```
📋 Available Models by Provider

🔹 Google (Gemini) - ✅ Configured
  • pro (gemini-2.5-pro) - 1M context, thinking modes
  • flash (gemini-2.0-flash-experimental) - 1M context, ultra-fast

🔹 OpenAI - ✅ Configured  
  • o3 (o3) - 200K context, strong reasoning
  • o3-mini (o3-mini) - 200K context, balanced
  • o4-mini (o4-mini) - 200K context, latest reasoning

🔹 Custom/Local - ✅ Configured
  • local-llama (llama3.2) - 128K context, local inference
  • Available at: http://localhost:11434/v1

🔹 OpenRouter - ❌ Not configured
  Set OPENROUTER_API_KEY to enable access to Claude, GPT-4, and more models
```

## When to Use ListModels

- **Model selection**: When you're unsure which models are available
- **Capability checking**: To verify what features each model supports
- **Configuration validation**: To confirm your API keys are working
- **Context planning**: To choose models based on content size requirements
- **Performance optimization**: To select the right model for speed vs quality trade-offs

## Configuration Dependencies

The available models depend on your configuration:

**API Keys Required:**
- `GEMINI_API_KEY` - Enables Gemini Pro and Flash models
- `OPENAI_API_KEY` - Enables OpenAI O3, O4-mini, and GPT models
- `OPENROUTER_API_KEY` - Enables access to multiple providers through OpenRouter
- `CUSTOM_API_URL` - Enables local/custom models (Ollama, vLLM, etc.)

**Model Restrictions:**
If you've set model usage restrictions via environment variables, the tool will show:
- Which models are allowed vs restricted
- Active restriction policies
- How to modify restrictions

## Tool Parameters

This tool requires no parameters - it simply queries the server configuration and displays all available information.


