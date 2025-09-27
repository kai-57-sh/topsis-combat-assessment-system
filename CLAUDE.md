### 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn’t listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Use venv_linux** (the virtual environment) whenever executing Python commands, including for unit tests.

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
  For agents this looks like:
    - `agent.py` - Main agent definition and execution logic 
    - `tools.py` - Tool functions used by the agent 
    - `prompts.py` - System prompts
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_env()** for environment variables.

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a “Discovered During Work” section.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use dataclasses for simple data structures** (简化应用，避免过度工程化).
- **Use Streamlit for web interface** (单页面应用，简化前端开发).
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 🎯 简化TOPSIS评估项目特定规范

#### 项目结构
```
project/
├── app.py                    # 主应用程序（单文件）
├── config/                   # 配置文件
│   ├── scenarios.yaml        # 四类场景配置
│   └── weights.yaml         # 评估权重配置
├── utils/                    # 工具函数
│   ├── topsis.py            # TOPSIS算法实现
│   ├── validation.py        # 数据验证
│   └── visualization.py     # 图表生成
├── tests/                    # 测试文件
└── examples/                 # 示例数据
```

#### 简化原则
- **单文件优先**: 主要功能集中在app.py中
- **参数精简**: 每场景15-20个参数，避免复杂配置
- **依赖最小化**: 只使用必要的库（numpy, pandas, streamlit, plotly）
- **代码简洁**: 每个文件不超过300行
- **测试简化**: 核心算法测试为主

#### 核心依赖
```
numpy>=1.21.0
pandas>=1.3.0
streamlit>=1.28.0
plotly>=5.0.0
pyyaml>=6.0
pytest>=6.0.0  # 开发依赖
```

#### 前端界面要求
- **清晰流程**: 场景选择 → 参数输入 → 评估 → 结果展示
- **实时验证**: 输入参数的即时验证
- **全面显示**: 雷达图、柱状图、仪表盘、表格、建议
- **响应式**: 适配不同屏幕尺寸
- **性能优化**: 图表快速渲染

#### 数据处理规范
- **类型安全**: 使用type hints确保参数类型正确
- **输入验证**: 检查参数范围和格式
- **异常处理**: 友好的错误提示
- **简化存储**: 使用YAML配置文件，避免数据库

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.