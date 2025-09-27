"""
输入验证模块
为作战体系效能评估系统提供参数验证功能
"""

import yaml
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    error_message: Optional[str] = None
    warning_message: Optional[str] = None
    parameter_name: Optional[str] = None
    actual_value: Optional[float] = None
    expected_range: Optional[Tuple[float, float]] = None

class ParameterValidator:
    """参数验证器"""

    def __init__(self, config_path: str = "config/scenarios.yaml"):
        """
        初始化验证器

        Args:
            config_path: 场景配置文件路径
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"配置文件未找到: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"配置文件格式错误: {e}")
            raise

    def validate_parameter(
        self,
        parameter_name: str,
        value: float,
        scenario_type: str
    ) -> ValidationResult:
        """
        验证单个参数

        Args:
            parameter_name: 参数名称
            value: 参数值
            scenario_type: 场景类型

        Returns:
            验证结果
        """
        try:
            # 获取场景配置
            scenario = self.config['scenarios'][scenario_type]

            # 查找参数定义
            param_def = None
            for param in scenario['parameters']:
                if param['name'] == parameter_name:
                    param_def = param
                    break

            if param_def is None:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"参数 '{parameter_name}' 在场景 '{scenario_type}' 中未定义",
                    parameter_name=parameter_name,
                    actual_value=value
                )

            # 检查值范围
            min_val = param_def['min_value']
            max_val = param_def['max_value']

            if not (min_val <= value <= max_val):
                return ValidationResult(
                    is_valid=False,
                    error_message=f"参数 '{parameter_name}' 的值 {value} 超出有效范围 [{min_val}, {max_val}]",
                    parameter_name=parameter_name,
                    actual_value=value,
                    expected_range=(min_val, max_val)
                )

            # 检查类型
            if not isinstance(value, (int, float)):
                return ValidationResult(
                    is_valid=False,
                    error_message=f"参数 '{parameter_name}' 的值必须是数字类型",
                    parameter_name=parameter_name,
                    actual_value=value
                )

            # 检查数值合理性（可选）
            warning = self._check_reasonability(parameter_name, value, param_def)

            return ValidationResult(
                is_valid=True,
                warning_message=warning,
                parameter_name=parameter_name,
                actual_value=value,
                expected_range=(min_val, max_val)
            )

        except Exception as e:
            logger.error(f"参数验证失败: {e}")
            return ValidationResult(
                is_valid=False,
                error_message=f"参数验证过程中发生错误: {str(e)}",
                parameter_name=parameter_name,
                actual_value=value
            )

    def _check_reasonability(self, parameter_name: str, value: float, param_def: Dict) -> Optional[str]:
        """
        检查参数值的合理性

        Args:
            parameter_name: 参数名称
            value: 参数值
            param_def: 参数定义

        Returns:
            警告信息，如果没有问题则返回None
        """
        # 根据参数类型检查合理性
        param_type = param_def.get('type', '')

        if param_type == 'force':
            # 兵力参数检查
            if value <= 0:
                return f"兵力参数 '{parameter_name}' 的值应该大于0"

        elif param_type == 'equipment':
            # 装备性能参数检查
            if 0 <= value <= 1:
                if value > 0.95:
                    return f"装备性能 '{parameter_name}' 的值 {value} 接近上限，请确认是否合理"

        elif param_type == 'environment':
            # 环境条件参数检查
            if parameter_name in ['sea_state', 'weather_severity']:
                if value > 4:
                    return f"恶劣的{param_def['description']}可能影响作战效果"

        elif param_type == 'mission':
            # 任务需求参数检查
            if parameter_name in ['response_time', 'mission_duration']:
                if value > param_def['max_value'] * 0.8:
                    return f"{param_def['description']}较长，可能影响任务完成效率"

        return None

    def validate_all_parameters(
        self,
        parameters: Dict[str, float],
        scenario_type: str
    ) -> Tuple[bool, List[ValidationResult]]:
        """
        验证所有参数

        Args:
            parameters: 参数字典
            scenario_type: 场景类型

        Returns:
            (是否全部有效, 验证结果列表)
        """
        results = []
        all_valid = True

        # 验证提供的参数
        for param_name, value in parameters.items():
            result = self.validate_parameter(param_name, value, scenario_type)
            results.append(result)
            if not result.is_valid:
                all_valid = False

        # 检查必需参数是否缺失
        scenario = self.config['scenarios'][scenario_type]
        required_params = [p['name'] for p in scenario['parameters']]
        missing_params = set(required_params) - set(parameters.keys())

        if missing_params:
            for param_name in missing_params:
                results.append(ValidationResult(
                    is_valid=False,
                    error_message=f"缺少必需参数: '{param_name}'",
                    parameter_name=param_name
                ))
            all_valid = False

        return all_valid, results

    def get_parameter_info(self, scenario_type: str) -> Dict[str, Dict[str, Any]]:
        """
        获取场景的参数信息

        Args:
            scenario_type: 场景类型

        Returns:
            参数信息字典
        """
        scenario = self.config['scenarios'][scenario_type]
        param_info = {}

        for param in scenario['parameters']:
            param_info[param['name']] = {
                'type': param['type'],
                'min_value': param['min_value'],
                'max_value': param['max_value'],
                'default_value': param['default_value'],
                'description': param['description'],
                'is_benefit': param['is_benefit']
            }

        return param_info

    def get_user_friendly_error(self, result: ValidationResult) -> str:
        """
        获取用户友好的错误信息

        Args:
            result: 验证结果

        Returns:
            用户友好的错误信息
        """
        if result.is_valid:
            return ""

        error_msg = result.error_message or ""

        # 根据错误类型提供更友好的建议
        if "超出范围" in error_msg:
            param_info = result.parameter_name
            if result.expected_range:
                min_val, max_val = result.expected_range
                return f"{error_msg}，建议值在 {min_val} 到 {max_val} 之间"

        elif "未定义" in error_msg:
            return f"参数 '{result.parameter_name}' 在当前场景中不存在，请检查参数名称"

        elif "类型" in error_msg:
            return f"参数 '{result.parameter_name}' 必须是数字，请输入有效的数值"

        elif "缺少必需参数" in error_msg:
            return f"请填写所有必需的参数，缺少: {result.parameter_name}"

        return error_msg


# 使用示例和测试函数
def test_validation():
    """测试验证功能"""
    validator = ParameterValidator()

    # 测试有效参数
    print("=== 测试有效参数 ===")
    result1 = validator.validate_parameter("force_size", 500, "chokepoint_blockade")
    print(f"force_size=500: {result1.is_valid}, {result1.error_message or '通过'}")

    result2 = validator.validate_parameter("weapon_effectiveness", 0.8, "chokepoint_blockade")
    print(f"weapon_effectiveness=0.8: {result2.is_valid}, {result2.error_message or '通过'}")

    # 测试无效参数
    print("\n=== 测试无效参数 ===")
    result3 = validator.validate_parameter("force_size", 1500, "chokepoint_blockade")
    print(f"force_size=1500: {result3.is_valid}, {result3.error_message}")

    result4 = validator.validate_parameter("invalid_param", 100, "chokepoint_blockade")
    print(f"invalid_param=100: {result4.is_valid}, {result4.error_message}")

    # 测试批量验证
    print("\n=== 测试批量验证 ===")
    test_params = {
        "force_size": 600,
        "ship_count": 30,
        "weapon_effectiveness": 0.75,
        "sea_state": 3,
        "invalid_param": 100
    }

    all_valid, results = validator.validate_all_parameters(test_params, "chokepoint_blockade")
    print(f"全部有效: {all_valid}")
    for result in results:
        if not result.is_valid:
            print(f"  错误: {validator.get_user_friendly_error(result)}")
        elif result.warning_message:
            print(f"  警告: {result.warning_message}")

    # 获取参数信息
    print("\n=== 参数信息 ===")
    param_info = validator.get_parameter_info("chokepoint_blockade")
    for param_name, info in list(param_info.items())[:3]:  # 只显示前3个
        print(f"{param_name}: {info['description']} (范围: {info['min_value']}-{info['max_value']})")


if __name__ == "__main__":
    test_validation()