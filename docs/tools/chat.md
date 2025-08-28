# Chat Tool

Collaborative thinking for brainstorming, second opinions, and exploring ideas.

## Thinking Mode

Default: `medium` (8,192 tokens). Use `low` for quick questions or `high` for complex discussions.

## Example Prompt

```
Chat with zen and pick the best model for this job. I need to pick between Redis and Memcached for session storage 
and I need an expert opinion for the project I'm working on. Get a good idea of what the project does, pick one of the two options
and then debate with the other models to give me a final verdict
```

## Features

- Second opinions and brainstorming
- Technology comparisons
- Architecture discussions
- File context support
- Image analysis (screenshots, diagrams)
- Web search for current documentation

## Tool Parameters

- `prompt`: Your question or discussion topic (required)
- `model`: auto|pro|flash|flash-2.0|flashlite|o3|o3-mini|o4-mini|gpt4.1|gpt5|gpt5-mini|gpt5-nano (default: server default)
- `files`: Optional files for context (absolute paths)
- `images`: Optional images for visual context (absolute paths)
- `temperature`: Response creativity (0-1, default 0.5)
- `thinking_mode`: minimal|low|medium|high|max (default: medium, Gemini only)
- `use_websearch`: Enable web search for documentation and insights (default: true)
- `continuation_id`: Continue previous conversations

## Usage Examples

**Basic Development Chat:**
```
"Chat with zen about the best approach for user authentication in my React app"
```

**Technology Comparison:**
```
"Use flash to discuss whether PostgreSQL or MongoDB would be better for my e-commerce platform"
```

**Architecture Discussion:**
```
"Chat with pro about microservices vs monolith architecture for my project, consider scalability and team size"
```

**File Context Analysis:**
```
"Use gemini to chat about the current authentication implementation in auth.py and suggest improvements"
```

**Visual Analysis:**
```
"Chat with gemini about this UI mockup screenshot - is the user flow intuitive?"
```

