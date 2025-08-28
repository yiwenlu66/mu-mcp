# ThinkDeep Tool

Multi-stage investigation for complex problems. Challenges assumptions and finds edge cases.

## Thinking Mode

Default: `high` (16,384 tokens). Claude auto-selects based on complexity.

## Example Prompt

```
Think deeper about my authentication design with pro using max thinking mode and brainstorm to come up 
with the best architecture for my project
```

## Features

- Second opinion on analysis
- Challenges assumptions and edge cases
- Alternative approaches
- Architecture validation
- File and image support
- Critical evaluation of suggestions
- Web search for documentation

## Tool Parameters

- `prompt`: Your current thinking/analysis to extend and validate (required)
- `model`: auto|pro|flash|flash-2.0|flashlite|o3|o3-mini|o4-mini|gpt4.1|gpt5|gpt5-mini|gpt5-nano (default: server default)
- `problem_context`: Additional context about the problem or goal
- `focus_areas`: Specific aspects to focus on (architecture, performance, security, etc.)
- `files`: Optional file paths or directories for additional context (absolute paths)
- `images`: Optional images for visual analysis (absolute paths)
- `temperature`: Temperature for creative thinking (0-1, default 0.7)
- `thinking_mode`: minimal|low|medium|high|max (default: high, Gemini only)
- `use_websearch`: Enable web search for documentation and insights (default: true)
- `continuation_id`: Continue previous conversations

## Usage Examples

**Architecture Design:**
```
"Think deeper about my microservices authentication strategy with pro using max thinking mode"
```

**With File Context:**
```
"Use gemini to think deeper about my API design with reference to api/routes.py and models/user.py"
```

**Visual Analysis:**
```
"Think deeper about this system architecture diagram with gemini pro - identify potential bottlenecks"
```

**Problem Solving:**
```
"I'm considering using GraphQL vs REST for my API. Think deeper about the trade-offs with o3 using high thinking mode"
```

**Code Review Enhancement:**
```
"Think deeper about the security implications of this authentication code with pro"
```


## Enhanced Critical Evaluation Process

The `thinkdeep` tool includes a unique two-stage process:

1. **Gemini's Analysis**: Extended reasoning with specialized thinking capabilities
2. **Claude's Critical Evaluation**: Claude reviews Gemini's suggestions, considers:
   - Context and constraints of your specific situation
   - Potential risks and implementation challenges
   - Trade-offs and alternatives
   - Final synthesized recommendation

This ensures you get both deep reasoning and practical, context-aware advice.

## When to Use ThinkDeep vs Other Tools

- **Use `thinkdeep`** for: Extending specific analysis, challenging assumptions, architectural decisions
- **Use `chat`** for: Open-ended brainstorming and general discussions
- **Use `analyze`** for: Understanding existing code without extending analysis
- **Use `codereview`** for: Finding specific bugs and security issues