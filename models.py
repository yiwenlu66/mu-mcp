"""OpenRouter model registry and capabilities."""

import os
from dataclasses import dataclass
from typing import Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


@dataclass
class ModelCapabilities:
    """Model metadata for routing and selection."""
    
    name: str  # Full OpenRouter model path
    description: str  # What the model is best for


# OpenRouter model registry - popular models with good support
OPENROUTER_MODELS = {
    # OpenAI Models
    "gpt-5": ModelCapabilities(
        name="openai/gpt-5",
        description="Most advanced OpenAI model with extended context. Excels at complex reasoning, coding, and multimodal understanding",
    ),
    "gpt-5-mini": ModelCapabilities(
        name="openai/gpt-5-mini",
        description="Efficient GPT-5 variant. Balances performance and cost for general-purpose tasks",
    ),
    "gpt-4o": ModelCapabilities(
        name="openai/gpt-4o",
        description="Multimodal model supporting text, image, audio, and video. Strong at creative writing and following complex instructions",
    ),
    "o3": ModelCapabilities(
        name="openai/o3",
        description="Advanced reasoning model with tool integration and visual reasoning. Excels at mathematical proofs and complex problem-solving",
    ),
    "o3-mini": ModelCapabilities(
        name="openai/o3-mini",
        description="Production-ready small reasoning model with function calling and structured outputs. Good for systematic problem-solving",
    ),
    "o3-mini-high": ModelCapabilities(
        name="openai/o3-mini-high",
        description="Enhanced O3 Mini with deeper reasoning, better accuracy vs standard O3 Mini",
    ),
    "o4-mini": ModelCapabilities(
        name="openai/o4-mini",
        description="Fast reasoning model optimized for speed. Exceptional at math, coding, and visual tasks with tool support",
    ),
    "o4-mini-high": ModelCapabilities(
        name="openai/o4-mini-high",
        description="Premium O4 Mini variant with enhanced reasoning depth and accuracy",
    ),
    
    # Anthropic Models
    "sonnet": ModelCapabilities(
        name="anthropic/claude-sonnet-4",
        description="Industry-leading coding model with superior instruction following. Excellent for software development and technical writing",
    ),
    "opus": ModelCapabilities(
        name="anthropic/claude-opus-4.1",
        description="Most capable Claude model for sustained complex work. Strongest at deep analysis and long-running tasks",
    ),
    "haiku": ModelCapabilities(
        name="anthropic/claude-3.5-haiku",
        description="Fast, efficient model matching previous flagship performance. Great for high-volume, quick-response scenarios",
    ),
    
    # Google Models
    "gemini-2.5-pro": ModelCapabilities(
        name="google/gemini-2.5-pro",
        description="Massive context window with thinking mode. Best for analyzing huge datasets, codebases, and STEM reasoning",
    ),
    "gemini-2.5-flash": ModelCapabilities(
        name="google/gemini-2.5-flash",
        description="Best price-performance with thinking capabilities. Ideal for high-volume tasks with multimodal and multilingual support",
    ),
    
    # DeepSeek Models
    "deepseek-chat": ModelCapabilities(
        name="deepseek/deepseek-chat-v3.1",
        description="Hybrid model switching between reasoning and direct modes. Strong multilingual support and code completion",
    ),
    "deepseek-r1": ModelCapabilities(
        name="deepseek/deepseek-r1",
        description="Open-source reasoning model with exceptional math capabilities. Highly cost-effective for complex reasoning tasks",
    ),
    
    # X.AI Models
    "grok-4": ModelCapabilities(
        name="x-ai/grok-4",
        description="Multimodal model with strong reasoning and analysis capabilities. Excellent at complex problem-solving and scientific tasks",
    ),
    "grok-code-fast-1": ModelCapabilities(
        name="x-ai/grok-code-fast-1",
        description="Ultra-fast coding specialist optimized for IDE integration. Best for rapid code generation and bug fixes",
    ),
    
    # Qwen Models
    "qwen3-max": ModelCapabilities(
        name="qwen/qwen3-max",
        description="Trillion-parameter model with ultra-long context. Excels at complex reasoning, structured data, and creative tasks",
    ),
}


def get_allowed_models() -> dict[str, ModelCapabilities]:
    """Get models filtered by OPENROUTER_ALLOWED_MODELS env var."""
    allowed = os.getenv("OPENROUTER_ALLOWED_MODELS", "")
    
    if not allowed:
        # No restrictions, return all models
        return OPENROUTER_MODELS
    
    # Parse comma-separated list
    allowed_names = [name.strip().lower() for name in allowed.split(",")]
    filtered = {}
    
    for key, model in OPENROUTER_MODELS.items():
        # Check main key
        if key.lower() in allowed_names:
            filtered[key] = model
            continue
                
        # Check full model name
        if model.name.split("/")[-1].lower() in allowed_names:
            filtered[key] = model
    
    return filtered


def resolve_model(name: str) -> Optional[str]:
    """Resolve a model name to the full OpenRouter model path."""
    if not name:
        return None
        
    name_lower = name.lower()
    
    # Check if it's already a full path
    if "/" in name:
        return name
    
    # Check available models
    models = get_allowed_models()
    
    # Direct key match
    if name_lower in models:
        return models[name_lower].name
    
    # Check by model name suffix
    for key, model in models.items():
        if model.name.endswith(f"/{name_lower}"):
            return model.name
    
    return None


def get_short_name(full_name: str) -> Optional[str]:
    """Get the short name (key) for a full model path.
    
    Args:
        full_name: Full OpenRouter model path (e.g., "openai/gpt-5")
        
    Returns:
        Short name key (e.g., "gpt-5") or None if not found
    """
    if not full_name:
        return None
    
    # Check available models for matching full name
    models = get_allowed_models()
    
    for key, model in models.items():
        if model.name == full_name:
            return key
    
    # If not found in registry, return None
    # This handles cases where a custom full path was used
    return None
