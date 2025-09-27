name: "TOPSIS Combat Assessment System - Streamlit Web Application"
description: |

## Purpose
Build a simplified combat system effectiveness assessment system with intuitive user interface supporting four combat scenarios, 15-20 input parameters per scenario, and comprehensive frontend display using TOPSIS algorithm.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Follow all rules in CLAUDE.md

---

## Goal
Create a Streamlit-based web application that allows users to:
1. Select from 4 combat scenarios (要峡封控, 登陆场清扫, 水雷清排, 近岸水下监视)
2. Input 15-20 key parameters per scenario (force configuration, equipment performance, environmental conditions, mission requirements)
3. Perform one-click assessment using simplified TOPSIS algorithm
4. Display comprehensive results with overall score (0-1), radar charts, bar charts, and improvement suggestions

## Why
- **User Value**: Provides intuitive combat effectiveness evaluation with clear visual feedback
- **Integration**: Works with existing TOPSIS implementation in examples/topsis.py
- **Problem Solved**: Complex multi-criteria decision making made accessible through simple interface

## What
A single-page Streamlit application with:
- **Scenario Selection**: Radio buttons or dropdown for 4 combat scenarios
- **Parameter Input**: Dynamic form showing 15-20 parameters based on selected scenario
- **Assessment Engine**: One-click TOPSIS calculation with 5-8 core indicators
- **Results Display**: Comprehensive visualization including:
  - Overall effectiveness score (0-1 scale)
  - Performance level rating (Excellent/Good/Average/Poor)
  - Radar chart for multi-dimensional analysis
  - Bar charts for indicator comparison
  - Detailed data table
  - Text-based improvement suggestions

### Success Criteria
- [ ] Users can select from 4 combat scenarios
- [ ] Each scenario shows 15-20 relevant input parameters
- [ ] Real-time input validation with user-friendly error messages
- [ ] One-click assessment generates results in <2 seconds
- [ ] Results display overall score with radar chart, bar charts, and suggestions
- [ ] Responsive design works on different screen sizes
- [ ] All code follows CLAUDE.md guidelines (single-file优先, 简化架构)

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- file: examples/topsis.py
  why: Existing TOPSIS implementation pattern, algorithm steps, mathematical formulas

- file: examples/app.py
  why: Flask API pattern, error handling, validation approaches

- url: https://docs.streamlit.io/
  why: Streamlit development patterns, form components, chart display methods

- url: https://plotly.com/python/radar-chart/
  why: Radar chart implementation for multi-dimensional assessment display

- url: https://plotly.com/python/bar-charts/
  why: Bar chart implementation for indicator comparison

- file: CLAUDE.md
  why: Project-specific conventions, simplified architecture, dataclasses usage

- file: INITIAL.md
  why: Feature requirements, technical specifications, user interface requirements
```

### Current Codebase Overview
```bash
/AII-wuqi/AII_home/fq_775/context-engineering-intro/
├── CLAUDE.md              # Project conventions (simplified approach)
├── INITIAL.md            # Feature requirements and specifications
├── examples/
│   ├── topsis.py        # Existing TOPSIS algorithm implementation
│   └── app.py           # Flask API example (reference for patterns)
├── config/               # Configuration directory (empty)
├── PRPs/                # PRP templates
└── tests/               # Tests directory (empty)
```

### Desired Codebase Structure
```bash
/AII-wuqi/AII_home/fq_775/context-engineering-intro/
├── CLAUDE.md              # Project conventions
├── INITIAL.md            # Feature requirements
├── app.py                # Main Streamlit application (NEW)
├── config/
│   ├── scenarios.yaml    # Scenario configurations (NEW)
│   └── weights.yaml      # Assessment weights (NEW)
├── utils/
│   ├── topsis.py         # Simplified TOPSIS algorithm (NEW)
│   ├── validation.py     # Input validation (NEW)
│   └── visualization.py  # Chart generation (NEW)
├── tests/
│   ├── test_topsis.py    # Algorithm tests (NEW)
│   ├── test_app.py       # UI tests (NEW)
│   └── fixtures/         # Test data (NEW)
└── examples/
    ├── demo_data.json    # Example data (NEW)
    └── usage_demo.py     # Usage demonstration (NEW)
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: Streamlit requires specific patterns for form state management
# Use st.session_state() for maintaining form data between reruns
# Example: if 'scenario' not in st.session_state: st.session_state.scenario = None

# CRITICAL: Plotly charts in Streamlit need specific configuration
# Use st.plotly_chart(fig, use_container_width=True) for responsive charts
# Radar charts need specific theta and r parameters

# CRITICAL: TOPSIS algorithm requires careful handling of benefit vs cost criteria
# Benefit criteria (higher is better): efficiency, success rate, capability
# Cost criteria (lower is better): time, cost, risk, resource consumption

# CRITICAL: Input validation must be user-friendly
# Use st.error() for validation errors, not exceptions that crash the app
# Provide range hints in input widgets (min_value, max_value, step)

# CRITICAL: Chinese characters need proper encoding
# Use UTF-8 encoding, ensure font support for Chinese characters in charts
```

## Implementation Blueprint

### Data Models and Structure
```python
# Using dataclasses for simplified data structures (per CLAUDE.md)
@dataclass
class CombatScenario:
    id: str
    name: str
    name_en: str
    parameters: List[Parameter]
    weights: Dict[str, float]

@dataclass
class Parameter:
    name: str
    name_en: str
    type: str  # 'force', 'equipment', 'environment', 'mission'
    min_value: float
    max_value: float
    default_value: float
    description: str
    is_benefit: bool  # True for benefit criteria, False for cost criteria

@dataclass
class AssessmentResult:
    overall_score: float
    performance_level: str
    indicator_scores: Dict[str, float]
    ranking: int
    suggestions: List[str]
```

### List of Tasks (in completion order)

```yaml
Task 1 - Setup Project Structure:
CREATE config/scenarios.yaml:
  - DEFINE 4 combat scenarios with parameters
  - INCLUDE parameter ranges, types, and benefit/cost flags
  - USE Chinese names with English descriptions

CREATE config/weights.yaml:
  - DEFINE default weights for each scenario
  - INCLUDE weight categories for different parameter types

Task 2 - Core TOPSIS Algorithm:
CREATE utils/topsis.py:
  - MIRROR pattern from: examples/topsis.py
  - SIMPLIFY to handle 5-8 indicators instead of full complexity
  - ADD input validation and error handling
  - PRESERVE mathematical correctness but optimize for speed

Task 3 - Input Validation:
CREATE utils/validation.py:
  - CREATE parameter range validation
  - ADD type checking for numeric inputs
  - INCLUDE user-friendly error messages in Chinese
  - USE st.error() for displaying validation errors

Task 4 - Visualization Components:
CREATE utils/visualization.py:
  - CREATE radar chart function using Plotly
  - CREATE bar chart function for indicator comparison
  - ADD overall score gauge/meter display
  - INCLUDE Chinese font support for chart labels

Task 5 - Main Application:
CREATE app.py:
  - BUILD scenario selection interface
  - DYNAMIC parameter input forms based on scenario
  - INTEGRATE TOPSIS calculation engine
  - DISPLAY comprehensive results with multiple charts
  - INCLUDE responsive design for different screen sizes

Task 6 - Configuration Files:
POPULATE config/scenarios.yaml:
  - DEFINE 15-20 parameters per scenario
  - INCLUDE realistic military assessment parameters
  - BALANCE benefit vs cost criteria

POPULATE config/weights.yaml:
  - CONFIGURE appropriate weights for different scenarios
  - ENSURE weights sum to 1.0 for each scenario

Task 7 - Tests:
CREATE tests/test_topsis.py:
  - TEST algorithm correctness with known inputs
  - INCLUDE edge cases (zero values, negative values)
  - VALIDATE ranking accuracy

CREATE tests/test_app.py:
  - TEST UI component rendering
  - VALIDATE form submission and data flow
  - INCLUDE integration tests for complete workflow

Task 8 - Documentation and Examples:
CREATE examples/demo_data.json:
  - PROVIDE sample data for each scenario
  - INCLUDE expected results for validation

CREATE examples/usage_demo.py:
  - DEMONSTRATE complete workflow
  - INCLUDE screenshots of expected output
```

### Per Task Pseudocode

```python
# Task 2 - Simplified TOPSIS Algorithm
def calculate_topsis(decision_matrix: np.ndarray, weights: np.ndarray, criteria_types: List[bool]) -> Dict:
    """
    Simplified TOPSIS calculation for combat assessment
    PATTERN: Follow examples/topsis.py but optimize for 5-8 indicators
    """
    # Step 1: Normalize decision matrix
    normalized_matrix = normalize_matrix(decision_matrix)

    # Step 2: Calculate weighted normalized matrix
    weighted_matrix = apply_weights(normalized_matrix, weights)

    # Step 3: Determine ideal solutions
    ideal_best, ideal_worst = find_ideal_solutions(weighted_matrix, criteria_types)

    # Step 4: Calculate distances
    distances = calculate_distances(weighted_matrix, ideal_best, ideal_worst)

    # Step 5: Calculate similarity scores
    similarity_scores = calculate_similarity(distances)

    return {
        'scores': similarity_scores,
        'ranking': np.argsort(-similarity_scores),
        'normalized_matrix': normalized_matrix,
        'weighted_matrix': weighted_matrix
    }

# Task 5 - Main Application Structure
def main():
    """Main Streamlit application"""
    st.title("作战体系效能评估系统")

    # CRITICAL: Use session_state for form persistence
    if 'scenario' not in st.session_state:
        st.session_state.scenario = None
        st.session_state.parameters = {}

    # Step 1: Scenario selection
    scenario = select_scenario()

    # Step 2: Dynamic parameter input
    parameters = input_parameters(scenario)

    # Step 3: Assessment button and processing
    if st.button("开始评估", type="primary"):
        result = perform_assessment(scenario, parameters)
        display_results(result)

    # CRITICAL: Handle form state properly to avoid resets
    st.session_state.parameters = parameters

# Task 4 - Radar Chart Generation
def create_radar_chart(indicator_scores: Dict[str, float], indicator_names: List[str]) -> go.Figure:
    """
    Create radar chart for multi-dimensional assessment display
    PATTERN: Use Plotly Scatterpolar for radar charts
    """
    fig = go.Figure(data=go.Scatterpolar(
        r=list(indicator_scores.values()),
        theta=indicator_names,
        fill='toself',
        name='当前方案'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=True,
        title="多维度评估结果"
    )

    return fig
```

### Integration Points
```yaml
CONFIG FILES:
  - scenarios.yaml: "Scenario definitions with parameters"
  - weights.yaml: "Assessment weights for each scenario"

UTILS INTEGRATION:
  - utils/topsis.py: "Core assessment algorithm"
  - utils/validation.py: "Input validation and error handling"
  - utils/visualization.py: "Chart generation functions"

STREAMLIT COMPONENTS:
  - st.radio(): "Scenario selection"
  - st.number_input(): "Parameter input with validation"
  - st.button(): "Trigger assessment"
  - st.plotly_chart(): "Display results"
  - st.columns(): "Responsive layout"
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
source venv_linux/bin/activate  # Use virtual environment per CLAUDE.md
python -m ruff check utils/topsis.py --fix
python -m mypy utils/topsis.py

# Expected: No errors. If errors exist, READ and fix them.
```

### Level 2: Unit Tests
```python
# CREATE tests/test_topsis.py with these test cases:
def test_topsis_calculation():
    """Test TOPSIS algorithm with known inputs"""
    matrix = np.array([[85, 0.8, 12], [78, 0.9, 18], [90, 0.7, 15]])
    weights = np.array([0.4, 0.3, 0.3])
    criteria_types = [True, True, False]  # benefit, benefit, cost

    result = calculate_topsis(matrix, weights, criteria_types)

    assert 'scores' in result
    assert len(result['scores']) == 3
    assert all(0 <= score <= 1 for score in result['scores'])

def test_input_validation():
    """Test parameter validation"""
    validator = ParameterValidator()

    # Valid input
    assert validator.validate_parameter("force_size", 100, "chokepoint")['valid']

    # Invalid input (out of range)
    result = validator.validate_parameter("force_size", 1000, "chokepoint")
    assert not result['valid']
    assert "超出范围" in result['error']

def test_chart_generation():
    """Test radar chart creation"""
    scores = {"火力": 0.8, "机动性": 0.6, "防护": 0.9}
    fig = create_radar_chart(scores, list(scores.keys()))

    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
```

```bash
# Run and iterate until passing:
python -m pytest tests/test_topsis.py -v
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test
```bash
# Start the Streamlit application
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Manual testing checklist:
# 1. Select each scenario and verify correct parameters appear
# 2. Input valid values and click assessment
# 3. Verify results display with charts and scores
# 4. Test invalid input handling
# 5. Verify responsive design on different screen sizes

# Expected: Application loads without errors, all buttons work, charts display correctly
```

## Final Validation Checklist
- [ ] All tests pass: `python -m pytest tests/ -v`
- [ ] No linting errors: `python -m ruff check utils/ app.py`
- [ ] No type errors: `python -m mypy utils/ app.py`
- [ ] Manual test successful: Access http://localhost:8501 and test all scenarios
- [ ] Each scenario shows correct 15-20 parameters
- [ ] Assessment completes in <2 seconds
- [ ] Charts display correctly with Chinese labels
- [ ] Error handling is user-friendly
- [ ] Application follows CLAUDE.md simplified architecture principles

---

## Anti-Patterns to Avoid
- ❌ Don't create complex multi-file architecture when single file works
- ❌ Don't use database when YAML configuration files suffice
- ❌ Don't skip input validation - validate all user inputs
- ❌ Don't ignore performance - optimize for <2 second response time
- ❌ Don't hardcode parameter values - use configuration files
- ❌ Don't create complex error handling - use simple st.error() messages
- ❌ Don't ignore Chinese character support - ensure proper encoding
- ❌ Don't skip tests - include unit tests for core algorithm

## PRP Quality Score: 9/10

High confidence for one-pass implementation success due to:
- Comprehensive context including existing codebase patterns
- Clear task breakdown with specific implementation guidance
- Validation loops that catch common issues early
- Specific library usage examples and gotchas documented
- Simplified architecture following project conventions