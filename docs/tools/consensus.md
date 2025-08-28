# Consensus Tool

Multi-model perspectives with for/against stances for decision-making.

## Thinking Mode

Default: `medium` (8,192 tokens). Use `high` for architecture or `max` for critical decisions.

## Model Recommendation

Uses extended reasoning models for multi-perspective analysis.

## Workflow

1. Assign stances (for/against/neutral)
2. Gather model opinions
3. Synthesize balanced recommendation
4. Natural language stances supported

## Example Prompts

**For/Against Analysis:**
```
Use zen consensus with flash taking a supportive stance and pro being critical to evaluate whether 
we should migrate from REST to GraphQL for our API
```

**Multi-Model Technical Decision:**
```
Get consensus from o3, flash, and pro on our new authentication architecture. Have o3 focus on 
security implications, flash on implementation speed, and pro stay neutral for overall assessment
```

**Natural Language Stance Assignment:**
```
Use consensus tool with gemini being "for" the proposal and grok being "against" to debate 
whether we should adopt microservices architecture
```

```
I want to work on module X and Y, unsure which is going to be more popular with users of my app. 
Get a consensus from gemini supporting the idea for implementing X, grok opposing it, and flash staying neutral
```

## Key Features

- **Stance steering**: Assign specific perspectives (for/against/neutral) to each model with intelligent synonym handling
- **Custom stance prompts**: Provide specific instructions for how each model should approach the analysis
- **Ethical guardrails**: Models will refuse to support truly bad ideas regardless of assigned stance
- **Unknown stance handling**: Invalid stances automatically default to neutral with warning
- **Natural language support**: Use terms like "supportive", "critical", "oppose", "favor" - all handled intelligently
- **Sequential processing**: Reliable execution avoiding MCP protocol issues
- **Focus areas**: Specify particular aspects to emphasize (e.g., 'security', 'performance', 'user experience')
- **File context support**: Include relevant files for informed decision-making
- **Image support**: Analyze architectural diagrams, UI mockups, or design documents
- **Conversation continuation**: Build on previous consensus analysis with additional rounds
- **Web search capability**: Enhanced analysis with current best practices and documentation

## Tool Parameters

- `prompt`: Detailed description of the proposal or decision to analyze (required)
- `models`: List of model configurations with optional stance and custom instructions (required)
- `files`: Context files for informed analysis (absolute paths)
- `images`: Visual references like diagrams or mockups (absolute paths)
- `focus_areas`: Specific aspects to emphasize
- `temperature`: Control consistency (default: 0.2 for stable consensus)
- `thinking_mode`: Analysis depth (minimal/low/medium/high/max)
- `use_websearch`: Enable research for enhanced analysis (default: true)
- `continuation_id`: Continue previous consensus discussions

## Model Configuration Examples

**Basic For/Against:**
```json
[
    {"model": "flash", "stance": "for"},
    {"model": "pro", "stance": "against"}
]
```

**Custom Stance Instructions:**
```json
[
    {"model": "o3", "stance": "for", "stance_prompt": "Focus on implementation benefits and user value"},
    {"model": "flash", "stance": "against", "stance_prompt": "Identify potential risks and technical challenges"}
]
```

**Neutral Analysis:**
```json
[
    {"model": "pro", "stance": "neutral"},
    {"model": "o3", "stance": "neutral"}
]
```

## Usage Examples

**Architecture Decision:**
```
"Get consensus from pro and o3 on whether to use microservices vs monolith for our e-commerce platform"
```

**Technology Migration:**
```
"Use consensus with flash supporting and pro opposing to evaluate migrating from MySQL to PostgreSQL"
```

**Feature Priority:**
```
"Get consensus from multiple models on whether to prioritize mobile app vs web dashboard development first"
```

**With Visual Context:**
```
"Use consensus to evaluate this new UI design mockup - have flash support it and pro be critical"
```


## Ethical Guardrails

The consensus tool includes built-in ethical safeguards:
- Models won't support genuinely harmful proposals regardless of assigned stance
- Unknown or invalid stances automatically default to neutral
- Warning messages for potentially problematic requests
- Focus on constructive technical decision-making

## When to Use Consensus vs Other Tools

- **Use `consensus`** for: Multi-perspective analysis, structured debates, major technical decisions
- **Use `chat`** for: Open-ended discussions and brainstorming
- **Use `thinkdeep`** for: Extending specific analysis with deeper reasoning
- **Use `analyze`** for: Understanding existing systems without debate