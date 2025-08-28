# DocGen Tool

Generates documentation with complexity analysis and gotcha warnings.

## Workflow

**Investigation Phase:**
1. Discovers all files needing documentation
2. Documents files one-by-one
3. Tracks progress with counters
4. Completes when all files documented

**Documentation Includes:**
- Function complexity analysis
- Call flow and dependencies
- Gotchas and edge cases

## Model Recommendation

Gemini Pro or O3 recommended for understanding complex relationships and edge cases.

## Example Prompts

**Basic Usage:**
```
"Use zen to generate documentation for the UserManager class"
"Document the authentication module with complexity analysis using gemini pro"
"Add comprehensive documentation to all methods in src/payment_processor.py"
```

## Key Features

- **Systematic file-by-file approach** - Complete documentation with progress tracking and validation
- **Modern documentation styles** - Enforces /// for Objective-C/Swift, /** */ for Java/JavaScript, etc.
- **Complexity analysis** - Big O notation for algorithms and performance characteristics
- **Call flow documentation** - Dependencies and method relationships
- **Counter-based completion** - Prevents stopping until all files are documented
- **Large file handling** - Systematic portion-by-portion documentation for comprehensive coverage
- **Final verification scan** - Mandatory check to ensure no functions are missed
- **Bug tracking** - Surfaces code issues without altering logic
- **Configuration parameters** - Control complexity analysis, call flow, and inline comments

## Tool Parameters

**Workflow Parameters (used during step-by-step process):**
- `step`: Current step description - discovery phase (step 1) or documentation phase (step 2+)
- `step_number`: Current step number in documentation sequence (required)
- `total_steps`: Dynamically calculated as 1 + total_files_to_document
- `next_step_required`: Whether another step is needed
- `findings`: Discoveries about code structure and documentation needs (required)
- `relevant_files`: Files being actively documented in current step
- `num_files_documented`: Counter tracking completed files (required)
- `total_files_to_document`: Total count of files needing documentation (required)

**Configuration Parameters (required fields):**
- `document_complexity`: Include Big O complexity analysis (default: true)
- `document_flow`: Include call flow and dependency information (default: true)
- `update_existing`: Update existing documentation when incorrect/incomplete (default: true)
- `comments_on_complex_logic`: Add inline comments for complex algorithmic steps (default: true)

## Usage Examples

**Class Documentation:**
```
"Generate comprehensive documentation for the PaymentProcessor class including complexity analysis"
```

**Module Documentation:**
```
"Document all functions in the authentication module with call flow information"
```

**API Documentation:**
```
"Create documentation for the REST API endpoints in api/users.py with parameter gotchas"
```

**Algorithm Documentation:**
```
"Document the sorting algorithm in utils/sort.py with Big O analysis and edge cases"
```

**Library Documentation:**
```
"Add comprehensive documentation to the utility library with usage examples and warnings"
```

## Documentation Standards

**Function/Method Documentation:**
- Parameter types and descriptions
- Return value documentation with types
- Algorithmic complexity analysis (Big O notation)
- Call flow and dependency information
- Purpose and behavior explanation
- Exception types and conditions

**Gotchas and Edge Cases:**
- Parameter combinations that produce unexpected results
- Hidden dependencies on global state or environment
- Order-dependent operations where sequence matters
- Performance implications and bottlenecks
- Thread safety considerations
- Platform-specific behavior differences

**Code Quality Documentation:**
- Inline comments for complex logic
- Design pattern explanations
- Architectural decision rationale
- Usage examples and best practices

## Documentation Features Generated

**Complexity Analysis:**
- Time complexity (Big O notation)
- Space complexity when relevant
- Worst-case, average-case, and best-case scenarios
- Performance characteristics and bottlenecks

**Call Flow Documentation:**
- Which methods/functions this code calls
- Which methods/functions call this code
- Key dependencies and interactions
- Side effects and state modifications
- Data flow through functions

**Gotchas Documentation:**
- Non-obvious parameter interactions
- Hidden state dependencies
- Silent failure conditions
- Resource management requirements
- Version compatibility issues
- Platform-specific behaviors

## Incremental Documentation Approach

**Key Benefits:**
- **Immediate value delivery** - Code becomes more maintainable right away
- **Iterative improvement** - Pattern recognition across multiple analysis rounds
- **Quality validation** - Testing documentation effectiveness during workflow
- **Reduced cognitive load** - Focus on one function/method at a time

**Workflow Process:**
1. **Analyze and Document**: Examine each function and immediately add documentation
2. **Continue Analyzing**: Move to next function while building understanding
3. **Refine and Standardize**: Review and improve previously added documentation

## Language Support

**Modern Documentation Style Enforcement:**
- **Python**: Triple-quote docstrings with type hints
- **Objective-C**: /// comments
- **Swift**: /// comments
- **JavaScript/TypeScript**: /** */ JSDoc style
- **Java**: /** */ Javadoc style  
- **C#**: /// XML documentation comments
- **C/C++**: /// for documentation comments
- **Go**: // comments above functions/types
- **Rust**: /// for documentation comments

## Documentation Quality Features

**Comprehensive Coverage:**
- All public methods and functions
- Complex private methods requiring explanation
- Class and module-level documentation
- Configuration and setup requirements

**Developer-Focused:**
- Clear explanations of non-obvious behavior
- Usage examples for complex APIs
- Warning about common pitfalls
- Integration guidance and best practices

**Maintainable Format:**
- Consistent documentation style
- Appropriate level of detail
- Cross-references and links
- Version and compatibility notes


