

我将遵循您设定的规则。

根据README文件和前面分析的四类作战场景指标体系，我现在为程序编写准备创建INITIAL.md和CLAUDE.md文件。

## INITIAL.md

```markdown
# 多场景作战体系效能评估系统 (Multi-Scenario Combat System Effectiveness Assessment)

## FEATURE:

构建一个基于TOPSIS方法的多场景作战体系效能评估系统，支持四类典型水面作战场景：
1. **要峡封控作战体系评估**
2. **登陆场通道清扫作战体系评估** 
3. **水雷清排作战体系评估**
4. **近岸水下监视作战体系评估**

### 核心功能需求：

**1. 数据管理模块**
- 支持四类场景的输入要素管理（兵力、装备、环境）
- 标准化的评价指标体系（5个准则层，共78个具体指标）
- 支持多种数据源：仿真数据、试验数据、专家评估数据
- 数据验证与预处理（正向化、标准化）

**2. TOPSIS计算引擎**
- 完整的TOPSIS算法实现（6个标准步骤）
- 权重分配机制（支持AHP法、熵权法、主观赋权）
- 敏感性分析功能
- 批量计算与对比分析

**3. 结果分析与可视化**
- 相对贴近度计算与排序
- 多维度诊断分析（雷达图、柱状图）
- 交叉场景对比分析
- 详细的评估报告生成

**4. 用户界面**
- 命令行界面（CLI）支持批量处理
- Web界面支持交互式分析（使用Flask/FastAPI）
- 配置文件管理（YAML/JSON格式）

### 技术规格要求：

- **编程语言**: Python 3.8+
- **核心依赖**: NumPy, Pandas, SciPy, Matplotlib, Plotly
- **数据存储**: SQLite/PostgreSQL
- **配置管理**: YAML配置文件
- **日志系统**: 结构化日志记录
- **单元测试**: pytest覆盖率>90%

## EXAMPLES:

在examples/文件夹中应包含以下示例：

**examples/scenarios/**
- `chokepoint_blockade_sample.yaml` - 要峡封控场景的示例数据
- `landing_zone_clearance_sample.yaml` - 登陆场清扫场景的示例数据  
- `mine_countermeasures_sample.yaml` - 水雷清排场景的示例数据
- `underwater_surveillance_sample.yaml` - 水下监视场景的示例数据

**examples/calculations/**
- `topsis_basic_example.py` - 基础TOPSIS计算示例
- `weight_assignment_example.py` - 权重分配方法示例
- `sensitivity_analysis_example.py` - 敏感性分析示例

**examples/visualization/**
- `radar_chart_example.py` - 雷达图可视化示例
- `comparison_analysis_example.py` - 对比分析图表示例

## DOCUMENTATION:

### 算法文档
- TOPSIS方法理论基础：https://en.wikipedia.org/wiki/TOPSIS
- AHP层次分析法：https://en.wikipedia.org/wiki/Analytic_hierarchy_process
- 多属性决策分析理论

### 技术文档
- NumPy官方文档：https://numpy.org/doc/
- Pandas官方文档：https://pandas.pydata.org/docs/
- Matplotlib可视化：https://matplotlib.org/stable/contents.html
- Plotly交互式图表：https://plotly.com/python/

### 军事背景文档
- 作战效能评估理论
- 水面作战体系构成要素
- 多属性决策在军事领域的应用

## OTHER CONSIDERATIONS:

### 1. 数据安全与保密
- 涉及军事敏感数据，需要数据脱敏处理
- 所有示例数据使用虚拟/仿真数据
- 不在代码中硬编码敏感信息

### 2. 算法实现注意事项
- **数值稳定性**: TOPSIS计算中的除零处理、数值溢出防护
- **权重归一化**: 确保权重和为1，处理权重为负数的异常情况
- **指标类型处理**: 严格区分效益型和成本型指标的转换逻辑
- **矩阵运算优化**: 使用向量化操作提高计算效率

### 3. 扩展性设计
- **场景可扩展**: 支持新增作战场景而无需大幅修改代码
- **指标可配置**: 通过配置文件灵活调整指标体系
- **算法可插拔**: 支持其他MCDM方法（如ELECTRE、VIKOR）

### 4. 用户体验
- **进度显示**: 批量计算时显示进度条
- **错误处理**: 友好的错误提示和异常恢复
- **结果导出**: 支持PDF、Excel、PNG等多种格式输出
- **配置验证**: 输入数据的格式和范围校验

### 5. 性能要求
- **计算效率**: 支持1000+方案的批量对比分析
- **内存控制**: 大数据集处理时的内存优化
- **并行计算**: 支持多线程/多进程加速计算

### 6. 测试覆盖
- **单元测试**: 每个算法模块的独立测试
- **集成测试**: 完整流程的端到端测试
- **数值验证**: 与标准TOPSIS算例的结果对比验证
- **边界测试**: 极端数据情况下的稳定性测试

### 7. 常见陷阱
- **权重设置错误**: 权重分配不当导致结果偏差
- **指标冗余**: 高度相关的指标影响评估准确性
- **数据预处理**: 标准化方法选择对结果的影响
- **结果解释**: 相对贴近度的正确理解和应用

### 8. 开发优先级
1. **第一阶段**: 核心TOPSIS算法 + CLI界面 + 基础数据管理
2. **第二阶段**: Web界面 + 可视化功能 + 配置文件支持
3. **第三阶段**: 高级分析功能 + 性能优化 + 扩展接口
```

## CLAUDE.md

```markdown
# 作战体系效能评估系统开发规范

## 项目感知和背景理解
- 这是一个军事作战效能评估系统，涉及敏感的军事概念和数据
- 所有示例数据和测试用例必须使用虚构的、非敏感的数值
- 代码注释和文档中的军事术语使用标准化表述
- 始终记住这是一个多属性决策分析(MCDM)的工程实现项目

## 代码结构规范

### 模块组织
```
src/
├── combat_assessment/
│   ├── __init__.py
│   ├── core/                   # 核心算法模块
│   │   ├── __init__.py
│   │   ├── topsis.py          # TOPSIS算法实现
│   │   ├── weights.py         # 权重计算方法
│   │   └── preprocessing.py   # 数据预处理
│   ├── data/                  # 数据管理模块  
│   │   ├── __init__.py
│   │   ├── models.py          # 数据模型定义
│   │   ├── loader.py          # 数据加载器
│   │   └── validator.py       # 数据验证器
│   ├── scenarios/             # 场景定义模块
│   │   ├── __init__.py
│   │   ├── base.py           # 基础场景类
│   │   ├── chokepoint.py     # 要峡封控场景
│   │   ├── landing.py        # 登陆场清扫场景
│   │   ├── mcm.py            # 水雷清排场景
│   │   └── surveillance.py   # 水下监视场景
│   ├── analysis/             # 分析模块
│   │   ├── __init__.py
│   │   ├── sensitivity.py    # 敏感性分析
│   │   ├── comparison.py     # 对比分析
│   │   └── reporting.py      # 报告生成
│   ├── visualization/        # 可视化模块
│   │   ├── __init__.py
│   │   ├── charts.py         # 图表绘制
│   │   └── dashboard.py      # 仪表板
│   ├── cli/                  # 命令行界面
│   │   ├── __init__.py
│   │   └── commands.py       # CLI命令定义
│   └── web/                  # Web界面
│       ├── __init__.py
│       ├── app.py            # Web应用主文件
│       ├── routes.py         # 路由定义
│       └── templates/        # HTML模板
├── config/                   # 配置文件
├── tests/                    # 测试文件
└── examples/                 # 示例代码和数据
```

### 文件大小限制
- 单个Python文件不超过500行
- 复杂的类或函数拆分到独立模块
- 数据文件和配置文件采用合适的格式分割

## 编码规范

### Python代码风格
- 严格遵循 PEP 8 规范
- 使用 Black 进行代码格式化
- 使用 Flake8 进行代码质量检查
- 使用 mypy 进行类型检查

### 命名约定
- **类名**: PascalCase (如 `TopsisCalculator`)
- **函数/变量名**: snake_case (如 `calculate_distance`)
- **常量**: UPPER_SNAKE_CASE (如 `DEFAULT_WEIGHTS`)
- **私有成员**: 前缀下划线 (如 `_normalize_data`)

### 类型提示
- 所有公共函数必须包含类型提示
- 使用 `typing` 模块的高级类型
```python
from typing import List, Dict, Optional, Union, Tuple
import numpy as np
from numpy.typing import NDArray

def calculate_topsis(
    decision_matrix: NDArray[np.float64],
    weights: NDArray[np.float64],
    criteria_types: List[str]
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """计算TOPSIS相对贴近度"""
    pass
```

## 测试要求

### 测试覆盖率
- 单元测试覆盖率必须达到90%以上
- 核心算法模块覆盖率必须达到95%以上
- 使用 `pytest-cov` 生成覆盖率报告

### 测试结构
```
tests/
├── unit/              # 单元测试
│   ├── test_topsis.py
│   ├── test_weights.py
│   └── test_preprocessing.py
├── integration/       # 集成测试  
│   ├── test_scenarios.py
│   └── test_pipeline.py
├── fixtures/          # 测试数据
│   └── sample_data.yaml
└── conftest.py        # pytest配置
```

### 测试数据原则
- 所有测试数据使用虚构的数值
- 测试用例覆盖边界条件和异常情况
- 数值测试包含已知结果的对照验证

## 文档标准

### Docstring格式
使用 Google 风格的 docstring：

```python
def calculate_weighted_matrix(
    normalized_matrix: NDArray[np.float64],
    weights: NDArray[np.float64]
) -> NDArray[np.float64]:
    """计算加权标准化矩阵
    
    Args:
        normalized_matrix: 标准化决策矩阵，shape为(m, n)
        weights: 权重向量，shape为(n,)，元素和为1.0
        
    Returns:
        加权标准化矩阵，shape为(m, n)
        
    Raises:
        ValueError: 当权重向量长度与矩阵列数不匹配时
        
    Example:
        >>> matrix = np.array([[0.5, 0.3], [0.7, 0.4]])
        >>> weights = np.array([0.6, 0.4])
        >>> result = calculate_weighted_matrix(matrix, weights)
    """
    pass
```

### 注释原则
- 复杂算法必须包含详细的中文注释
- 数学公式使用LaTeX格式或文字描述
- 业务逻辑注释说明军事背景和实际意义

## 日志记录规范

### 日志配置
- 使用 `logging` 模块的结构化日志
- 支持不同级别的日志输出
- 日志格式包含时间戳、模块名、级别和消息

```python
import logging

logger = logging.getLogger(__name__)

# 示例用法
logger.info("开始执行TOPSIS计算，方案数量: %d", num_alternatives)
logger.warning("检测到权重和不为1，已自动归一化: %.4f", weight_sum)
logger.error("决策矩阵包含缺失值，行: %d, 列: %d", row, col)
```

### 日志内容规范
- **INFO级别**: 计算过程的关键步骤
- **WARNING级别**: 数据异常但可恢复的情况  
- **ERROR级别**: 严重错误和异常
- **DEBUG级别**: 详细的中间计算结果

## 安全和保密要求

### 数据处理
- 不在代码中硬编码任何敏感数据
- 敏感配置通过环境变量或加密配置文件管理
- 所有示例和测试数据使用虚构数值

### 代码审查
- 提交前检查是否包含敏感信息
- 变量命名避免暴露具体军事单位或装备型号
- 注释中使用通用化的描述

## 性能要求

### 算法效率
- 矩阵运算优先使用NumPy向量化操作
- 避免不必要的循环和重复计算
- 大数据集处理考虑内存优化

### 代码质量
- 使用适当的数据结构和算法
- 避免深度嵌套和过度复杂的逻辑
- 及时释放不需要的大对象

## 依赖管理

### 核心依赖
```
numpy>=1.21.0
pandas>=1.3.0  
scipy>=1.7.0
matplotlib>=3.4.0
plotly>=5.0.0
pyyaml>=6.0
click>=8.0.0
flask>=2.0.0
```

### 开发依赖
```
pytest>=6.0.0
pytest-cov>=3.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.910
```

## 错误处理规范

### 异常定义
- 为项目定义专门的异常类
- 异常信息要清晰、可操作
- 在适当层级捕获和处理异常

```python
class CombatAssessmentError(Exception):
    """作战效能评估系统基础异常"""
    pass

class InvalidDataError(CombatAssessmentError):
    """数据格式或内容无效异常"""
    pass

class CalculationError(CombatAssessmentError):
    """计算过程异常"""
    pass
```

### 输入验证
- 所有用户输入都要进行验证
- 提供有意义的错误消息和建议
- 数值范围和格式检查

## 配置管理

### 配置文件格式
使用YAML格式的配置文件：

```yaml
# config/scenarios.yaml
scenarios:
  chokepoint_blockade:
    name: "要峡封控"
    criteria:
      mission_accomplishment:
        weight: 0.35
        indicators:
          - name: "封锁成功率"
            type: "benefit"
            weight: 0.35
```

### 配置加载
- 支持分环境配置（开发、测试、生产）
- 配置验证和默认值处理
- 敏感配置的安全加载机制
```

这两个文件为后续的程序开发提供了明确的指导框架：
- **INITIAL.md** 定义了具体的功能需求、技术规格和开发注意事项
- **CLAUDE.md** 建立了项目开发的全局规范和编码标准

本轮修改已完成，请测试或继续下一需求。
