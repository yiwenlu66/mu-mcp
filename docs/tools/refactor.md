# Refactor Tool

Systematic refactoring analysis focusing on code smells, decomposition, and modernization.

## Thinking Mode

Default: `medium` (8,192 tokens). Use `high` for legacy systems or `max` for complex codebases.

## Workflow

**Investigation Phase:**
1. Claude analyzes code structure
2. Examines code smells and decomposition opportunities
3. Tracks findings and confidence levels
4. Signals completion when thorough

**Expert Analysis Phase:**
Provides prioritized refactoring recommendations with implementation guidance (skipped if confidence is `complete`).

## Model Recommendation

Gemini Pro recommended (1M context) for detecting cross-file dependencies and patterns.

## Example Prompts

```
"Use gemini pro to decompose my_crazy_big_class.m into smaller extensions"
"Using zen's refactor decompose the all_in_one_sync_code.swift into maintainable extensions"
```

💡**Example of a powerful prompt** to get the best out of both Claude + Flash's 1M Context: 
```
"First, think about how the authentication module works, find related classes and find
 any code smells, then using zen's refactor ask flash to confirm your findings but ask 
 it to find additional code smells and any other quick-wins and then fix these issues"
```

This results in Claude first performing its own expert analysis, encouraging it to think critically and identify links within the project code. It then prompts `flash` to review the same code with a hint—preventing it from duplicating Claude's findings and encouraging it to explore other areas that Claude did *not* discover.

## Key Features

- **Intelligent prioritization** - Will refuse to work on low priority issues if code is unwieldy large and requires decomposition first, helps identify poorly managed classes and files that need structural improvements before detail work
- **Top-down decomposition strategy** - Analyzes file → class → function levels systematically
- **Four refactor types**: `codesmells` (detect anti-patterns), `decompose` (break down large components), `modernize` (update language features), `organization` (improve structure)
- **Precise line-number references** - Provides exact line numbers for Claude to implement changes
- **Language-specific guidance** - Tailored suggestions for Python, JavaScript, Java, C#, Swift, and more
- **Style guide integration** - Uses existing project files as pattern references
- **Conservative approach** - Careful dependency analysis to prevent breaking changes
- **Multi-file analysis** - Understands cross-file relationships and dependencies
- **Priority sequencing** - Recommends implementation order for refactoring changes
- **Image support**: Analyze code architecture diagrams, legacy system charts: `"Refactor this legacy module using gemini pro with the current architecture diagram"`

## Refactor Types (Progressive Priority System)

**1. `decompose` (CRITICAL PRIORITY)** - Context-aware decomposition with adaptive thresholds:

**AUTOMATIC decomposition** (CRITICAL severity - blocks all other refactoring):
- Files >15,000 LOC, Classes >3,000 LOC, Functions >500 LOC

**EVALUATE decomposition** (contextual severity - intelligent assessment):
- Files >5,000 LOC, Classes >1,000 LOC, Functions >150 LOC
- Only recommends if genuinely improves maintainability
- Respects legacy stability, domain complexity, performance constraints
- Considers legitimate cases where size is justified (algorithms, state machines, generated code)

**2. `codesmells`** - Applied only after decomposition is complete:
- Detect long methods, complex conditionals, duplicate code, magic numbers, poor naming

**3. `modernize`** - Applied only after decomposition is complete:
- Update to modern language features (f-strings, async/await, etc.)

**4. `organization`** - Applied only after decomposition is complete:
- Improve logical grouping, separation of concerns, module structure

**Progressive Analysis:** The tool performs a top-down check (worse → bad → better) and refuses to work on lower-priority issues if critical decomposition is needed first. It understands that massive files and classes create cognitive overload that must be addressed before detail work can be effective. Legacy code that cannot be safely decomposed is handled with higher tolerance thresholds and context-sensitive exemptions.

## Tool Parameters

**Workflow Investigation Parameters (used during step-by-step process):**
- `step`: Current investigation step description (required for each step)
- `step_number`: Current step number in refactoring sequence (required)
- `total_steps`: Estimated total investigation steps (adjustable)
- `next_step_required`: Whether another investigation step is needed
- `findings`: Discoveries and refactoring opportunities in this step (required)
- `files_checked`: All files examined during investigation
- `relevant_files`: Files directly needing refactoring (required in step 1)
- `relevant_context`: Methods/functions/classes requiring refactoring
- `issues_found`: Refactoring opportunities with severity and type
- `confidence`: Confidence level in analysis completeness (exploring/incomplete/partial/complete)
- `backtrack_from_step`: Step number to backtrack from (for revisions)
- `hypothesis`: Current assessment of refactoring priorities

**Initial Configuration (used in step 1):**
- `prompt`: Description of refactoring goals, context, and specific areas of focus (required)
- `refactor_type`: codesmells|decompose|modernize|organization (default: codesmells)
- `model`: auto|pro|flash|flash-2.0|flashlite|o3|o3-mini|o4-mini|gpt4.1|gpt5|gpt5-mini|gpt5-nano (default: server default)
- `focus_areas`: Specific areas to focus on (e.g., 'performance', 'readability', 'maintainability', 'security')
- `style_guide_examples`: Optional existing code files to use as style/pattern reference (absolute paths)
- `thinking_mode`: minimal|low|medium|high|max (default: medium, Gemini only)
- `use_assistant_model`: Whether to use expert analysis phase (default: true, set to false to use Claude only)
- `continuation_id`: Thread continuation ID for multi-turn conversations

## Usage Examples

**Decomposition Analysis:**
```
"Analyze UserController.java for decomposition opportunities - it's becoming unwieldy"
```

**Code Smell Detection:**
```
"Use gemini to identify code smells in the authentication module with high thinking mode"
```

**Modernization:**
```
"Modernize legacy_parser.py to use modern Python features following examples/modern_patterns.py"
```

**Organization Improvement:**
```
"Refactor src/utils/ for better organization, focus on maintainability and readability"
```

**Legacy System Refactoring:**
```
"Use pro with max thinking to analyze this 10,000-line legacy file for decomposition strategy"
```

## Refactoring Strategy

**Top-Down Analysis:**
1. **File Level**: Identify oversized files that need splitting
2. **Class Level**: Find classes with too many responsibilities  
3. **Function Level**: Locate functions that are too complex or long
4. **Code Quality**: Address smells, modernization, and organization

**Context-Aware Decisions:**
- **Domain Complexity**: Some domains legitimately require larger classes
- **Performance Constraints**: Critical path code may resist decomposition
- **Legacy Stability**: Old, working code may need gentler refactoring
- **Test Coverage**: Refactoring recommendations consider testability

**Breaking Change Prevention:**
- Analyzes dependencies before suggesting splits
- Recommends gradual migration strategies
- Identifies public API impact
- Suggests backward compatibility approaches


## Output Format

Refactoring analysis includes:
- **Priority Assessment**: What needs attention first and why
- **Decomposition Strategy**: Specific file/class/function splitting recommendations
- **Implementation Plan**: Step-by-step refactoring sequence
- **Line-Number References**: Exact locations for changes
- **Dependency Analysis**: Impact assessment and migration strategies
- **Risk Assessment**: Potential breaking changes and mitigation strategies

## Advanced Features

**Adaptive Thresholds:**
The tool adjusts size thresholds based on context:
- **Generated Code**: Higher tolerance for large files
- **Algorithm Implementation**: Recognizes when size is justified
- **Legacy Systems**: More conservative recommendations
- **Test Files**: Different standards for test vs production code

**Cross-File Refactoring:**
Analyzes multiple files together to understand:
- Shared responsibilities that could be extracted
- Dependencies that complicate refactoring
- Opportunities for new abstractions
- Impact of changes across the codebase

## When to Use Refactor vs Other Tools

- **Use `refactor`** for: Structural improvements, decomposition, modernization, code organization
- **Use `codereview`** for: Finding bugs and security issues with immediate fixes
- **Use `analyze`** for: Understanding code without making change recommendations  
- **Use `debug`** for: Solving specific runtime issues rather than structural problems