# TestGen Tool

Generates test suites with edge case coverage for specific functions or classes.

## Thinking Mode

Default: `medium` (8,192 tokens). Use `high` for complex systems or `max` for exhaustive coverage.

## Workflow

**Investigation Phase:**
1. Claude analyzes code functionality
2. Examines critical paths and edge cases
3. Tracks test scenarios and coverage gaps

**Test Generation Phase:**
Creates framework-specific tests with edge case coverage.

## Model Recommendation

Gemini Pro or O3 recommended for analyzing complex code paths and dependencies.

## Example Prompts

**Basic Usage:**
```
"Use zen to generate tests for User.login() method"
"Generate comprehensive tests for the sorting method in src/new_sort.py using o3"
"Create tests for edge cases not already covered in our tests using gemini pro"
```

## Key Features

- **Multi-agent workflow** analyzing code paths and identifying realistic failure modes
- **Generates framework-specific tests** following project conventions
- **Supports test pattern following** when examples are provided
- **Dynamic token allocation** (25% for test examples, 75% for main code)
- **Prioritizes smallest test files** for pattern detection
- **Can reference existing test files**: `"Generate tests following patterns from tests/unit/"`
- **Specific code coverage** - target specific functions/classes rather than testing everything
- **Image support**: Test UI components, analyze visual requirements: `"Generate tests for this login form using the UI mockup screenshot"`
- **Edge case identification**: Systematic discovery of boundary conditions and error states
- **Realistic failure mode analysis**: Understanding what can actually go wrong in production
- **Integration test support**: Tests that cover component interactions and system boundaries

## Tool Parameters

**Workflow Investigation Parameters (used during step-by-step process):**
- `step`: Current investigation step description (required for each step)
- `step_number`: Current step number in test generation sequence (required)
- `total_steps`: Estimated total investigation steps (adjustable)
- `next_step_required`: Whether another investigation step is needed
- `findings`: Discoveries about functionality and test scenarios (required)
- `files_checked`: All files examined during investigation
- `relevant_files`: Files directly needing tests (required in step 1)
- `relevant_context`: Methods/functions/classes requiring test coverage
- `confidence`: Confidence level in test plan completeness (exploring/low/medium/high/certain)
- `backtrack_from_step`: Step number to backtrack from (for revisions)

**Initial Configuration (used in step 1):**
- `prompt`: Description of what to test, testing objectives, and specific scope/focus areas (required)
- `model`: auto|pro|flash|flash-2.0|flashlite|o3|o3-mini|o4-mini|gpt4.1|gpt5|gpt5-mini|gpt5-nano (default: server default)
- `test_examples`: Optional existing test files or directories to use as style/pattern reference (absolute paths)
- `thinking_mode`: minimal|low|medium|high|max (default: medium, Gemini only)
- `use_assistant_model`: Whether to use expert test generation phase (default: true, set to false to use Claude only)

## Usage Examples

**Method-Specific Tests:**
```
"Generate tests for User.login() method covering authentication success, failure, and edge cases"
```

**Class Testing:**
```
"Use pro to generate comprehensive tests for PaymentProcessor class with max thinking mode"
```

**Following Existing Patterns:**
```
"Generate tests for new authentication module following patterns from tests/unit/auth/"
```

**UI Component Testing:**
```
"Generate tests for this login form component using the UI mockup screenshot"
```

**Algorithm Testing:**
```
"Create thorough tests for the sorting algorithm in utils/sort.py, focus on edge cases and performance"
```

**Integration Testing:**
```
"Generate integration tests for the payment processing pipeline from order creation to completion"
```

## Test Generation Strategy

**Code Path Analysis:**
- Identifies all execution paths through the code
- Maps conditional branches and loops
- Discovers error handling paths
- Analyzes state transitions

**Edge Case Discovery:**
- Boundary value analysis (empty, null, max values)
- Invalid input scenarios
- Race conditions and timing issues
- Resource exhaustion cases

**Failure Mode Analysis:**
- External dependency failures
- Network and I/O errors
- Authentication and authorization failures
- Data corruption scenarios

**Framework Detection:**
The tool automatically detects and generates tests for:
- **Python**: pytest, unittest, nose2
- **JavaScript**: Jest, Mocha, Jasmine, Vitest
- **Java**: JUnit 4/5, TestNG, Mockito
- **C#**: NUnit, MSTest, xUnit
- **Swift**: XCTest
- **Go**: testing package
- **And more**: Adapts to project conventions

## Test Categories Generated

**Unit Tests:**
- Function/method behavior validation
- Input/output verification
- Error condition handling
- State change verification

**Integration Tests:**
- Component interaction testing
- API endpoint validation
- Database integration
- External service mocking

**Edge Case Tests:**
- Boundary conditions
- Invalid inputs
- Resource limits
- Concurrent access

**Performance Tests:**
- Response time validation
- Memory usage checks
- Load handling
- Scalability verification


## Test Quality Features

**Realistic Test Data:**
- Generates meaningful test data that represents real-world scenarios
- Avoids trivial test cases that don't add value
- Creates data that exercises actual business logic

**Comprehensive Coverage:**
- Happy path scenarios
- Error conditions and exceptions
- Edge cases and boundary conditions
- Integration points and dependencies

**Maintainable Code:**
- Clear test names that describe what's being tested
- Well-organized test structure
- Appropriate use of setup/teardown
- Minimal test data and mocking

## Advanced Features

**Pattern Following:**
When test examples are provided, the tool analyzes:
- Naming conventions and structure
- Assertion patterns and style
- Mocking and setup approaches
- Test data organization

**Large Context Analysis:**
With models like Gemini Pro, the tool can:
- Analyze extensive codebases for comprehensive test coverage
- Understand complex interactions across multiple modules
- Generate integration tests that span multiple components

**Visual Testing:**
For UI components and visual elements:
- Generate tests based on visual requirements
- Create accessibility testing scenarios
- Test responsive design behaviors

## When to Use TestGen vs Other Tools

- **Use `testgen`** for: Creating comprehensive test suites, filling test coverage gaps, testing new features
- **Use `debug`** for: Diagnosing specific test failures or runtime issues
- **Use `codereview`** for: Reviewing existing test quality and coverage
- **Use `analyze`** for: Understanding existing test structure without generating new tests