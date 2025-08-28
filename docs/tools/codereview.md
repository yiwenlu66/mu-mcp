# CodeReview Tool

Systematic code review with severity-based issue prioritization.

## Thinking Mode

Default: `medium` (8,192 tokens). Use `high` for security-critical code or `low` for quick checks.

## Workflow

**Investigation Phase:**
1. Claude plans review and analyzes code structure
2. Examines quality, security, performance, architecture
3. Tracks findings and confidence levels
4. Signals completion when comprehensive

**Expert Analysis Phase:**
Provides severity-categorized issues with recommendations (skipped if confidence is `certain`).

**Note:** Include "don't use any other model" to use Claude only.

## Model Recommendation

Gemini Pro/Flash recommended for large codebases (1M context window).

## Example Prompts

```
Perform a codereview with gemini pro and review auth.py for security issues and potential vulnerabilities.
I need an actionable plan but break it down into smaller quick-wins that we can implement and test rapidly 
```


## Features

- Issues prioritized by severity (CRITICAL → LOW)
- Review types: full, security, performance, quick
- Standards enforcement (PEP8, ESLint, etc.)
- Severity filtering
- Image support for screenshots
- Multi-file analysis
- Language-specific expertise
- Cross-file dependency detection

## Tool Parameters

**Workflow Investigation Parameters (used during step-by-step process):**
- `step`: Current investigation step description (required for each step)
- `step_number`: Current step number in review sequence (required)
- `total_steps`: Estimated total investigation steps (adjustable)
- `next_step_required`: Whether another investigation step is needed
- `findings`: Discoveries and evidence collected in this step (required)
- `files_checked`: All files examined during investigation
- `relevant_files`: Files directly relevant to the review (required in step 1)
- `relevant_context`: Methods/functions/classes central to review findings
- `issues_found`: Issues identified with severity levels
- `confidence`: Confidence level in review completeness (exploring/low/medium/high/certain)
- `backtrack_from_step`: Step number to backtrack from (for revisions)
- `images`: Visual references for review context

**Initial Review Configuration (used in step 1):**
- `prompt`: User's summary of what the code does, expected behavior, constraints, and review objectives (required)
- `model`: auto|pro|flash|flash-2.0|flashlite|o3|o3-mini|o4-mini|gpt4.1|gpt5|gpt5-mini|gpt5-nano (default: server default)
- `review_type`: full|security|performance|quick (default: full)
- `focus_on`: Specific aspects to focus on (e.g., "security vulnerabilities", "performance bottlenecks")
- `standards`: Coding standards to enforce (e.g., "PEP8", "ESLint", "Google Style Guide")
- `severity_filter`: critical|high|medium|low|all (default: all)
- `temperature`: Temperature for consistency (0-1, default 0.2)
- `thinking_mode`: minimal|low|medium|high|max (default: medium, Gemini only)
- `use_websearch`: Enable web search for best practices and documentation (default: true)
- `use_assistant_model`: Whether to use expert analysis phase (default: true, set to false to use Claude only)
- `continuation_id`: Continue previous review discussions

## Review Types

**Full Review (default):**
- Comprehensive analysis including bugs, security, performance, maintainability
- Best for new features or significant code changes

**Security Review:**
- Focused on security vulnerabilities and attack vectors
- Checks for common security anti-patterns
- Best for authentication, authorization, data handling code

**Performance Review:**
- Analyzes performance bottlenecks and optimization opportunities
- Memory usage, algorithmic complexity, resource management
- Best for performance-critical code paths

**Quick Review:**
- Fast style and basic issue check
- Lower token usage for rapid feedback
- Best for code formatting and simple validation

## Severity Levels

Issues are categorized and prioritized:

- **🔴 CRITICAL**: Security vulnerabilities, crashes, data corruption
- **🟠 HIGH**: Logic errors, performance issues, reliability problems  
- **🟡 MEDIUM**: Code smells, maintainability issues, minor bugs
- **🟢 LOW**: Style issues, documentation, minor improvements

## Usage Examples

**Basic Security Review:**
```
"Review the authentication module in auth/ for security vulnerabilities with gemini pro"
```

**Performance-Focused Review:**
```
"Use o3 to review backend/api.py for performance issues, focus on database queries and caching"
```

**Quick Style Check:**
```
"Quick review of utils.py with flash, only report critical and high severity issues"
```

**Standards Enforcement:**
```
"Review src/ directory against PEP8 standards with gemini, focus on code formatting and structure"
```

**Visual Context Review:**
```
"Review this authentication code along with the error dialog screenshot to understand the security implications"
```

## Best Practices

- **Provide context**: Describe what the code is supposed to do and any constraints
- **Use appropriate review types**: Security for auth code, performance for critical paths
- **Set severity filters**: Focus on critical issues for quick wins
- **Include relevant files**: Review related modules together for better context
- **Use parallel reviews**: Run multiple reviews with different models for comprehensive coverage
- **Follow up on findings**: Use the continuation feature to discuss specific issues in detail

## Output Format

Reviews include:
- **Executive Summary**: Overview of code quality and main concerns
- **Detailed Findings**: Specific issues with severity levels, line numbers, and recommendations
- **Quick Wins**: Easy-to-implement improvements with high impact
- **Long-term Improvements**: Structural changes for better maintainability
- **Security Considerations**: Specific security recommendations when relevant

