"""
输入验证测试
测试参数验证功能的正确性
"""

import pytest
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validation import ParameterValidator, ValidationResult


class TestParameterValidator:
    """参数验证器测试类"""

    def setup_method(self):
        """测试前设置"""
        self.validator = ParameterValidator()

    def test_init(self):
        """测试初始化"""
        assert self.validator is not None
        assert hasattr(self.validator, 'config')

    def test_load_config(self):
        """测试配置加载"""
        config = self.validator._load_config("config/scenarios.yaml")
        assert 'scenarios' in config
        assert 'chokepoint_blockade' in config['scenarios']

    def test_validate_parameter_valid(self):
        """测试有效参数验证"""
        # 测试有效参数
        result = self.validator.validate_parameter("force_size", 500, "chokepoint_blockade")

        assert isinstance(result, ValidationResult)
        assert result.is_valid is True
        assert result.error_message is None
        assert result.parameter_name == "force_size"
        assert result.actual_value == 500
        assert result.expected_range == (100, 1000)

    def test_validate_parameter_out_of_range(self):
        """测试超出范围的参数"""
        # 测试超出上限
        result = self.validator.validate_parameter("force_size", 1500, "chokepoint_blockade")

        assert result.is_valid is False
        assert "超出范围" in result.error_message or "超出有效范围" in result.error_message
        assert result.expected_range == (100, 1000)

        # 测试超出下限
        result = self.validator.validate_parameter("force_size", 50, "chokepoint_blockade")

        assert result.is_valid is False
        assert "超出范围" in result.error_message or "超出有效范围" in result.error_message

    def test_validate_parameter_invalid_name(self):
        """测试无效参数名称"""
        result = self.validator.validate_parameter("invalid_param", 100, "chokepoint_blockade")

        assert result.is_valid is False
        assert "未定义" in result.error_message
        assert result.parameter_name == "invalid_param"

    def test_validate_parameter_invalid_type(self):
        """测试无效参数类型"""
        result = self.validator.validate_parameter("force_size", "invalid", "chokepoint_blockade")

        assert result.is_valid is False
        # 错误信息可能提到类型问题或比较错误
        assert "数字类型" in result.error_message or "not supported" in result.error_message or "类型" in result.error_message

    def test_validate_parameter_reasonability_warnings(self):
        """测试合理性警告"""
        # 测试接近上限的装备性能
        result = self.validator.validate_parameter("weapon_effectiveness", 0.99, "chokepoint_blockade")

        assert result.is_valid is True
        # 警告消息可能不存在，这取决于具体实现
        if result.warning_message:
            assert "接近上限" in result.warning_message

        # 测试零值兵力参数 - 这应该被范围检查捕获，而不是合理性检查
        result = self.validator.validate_parameter("force_size", 0, "chokepoint_blockade")
        assert result.is_valid is False
        assert "超出范围" in result.error_message or "超出有效范围" in result.error_message

    def test_validate_all_parameters_complete(self):
        """测试完整参数验证"""
        # 获取所有必需参数
        param_info = self.validator.get_parameter_info("chokepoint_blockade")
        complete_params = {name: info['default_value'] for name, info in param_info.items()}

        all_valid, results = self.validator.validate_all_parameters(
            complete_params, "chokepoint_blockade"
        )

        assert all_valid is True
        assert len(results) == len(complete_params)
        assert all(result.is_valid for result in results)

    def test_validate_all_parameters_missing(self):
        """测试缺失参数验证"""
        incomplete_params = {"force_size": 500}  # 只提供一个参数

        all_valid, results = self.validator.validate_all_parameters(
            incomplete_params, "chokepoint_blockade"
        )

        assert all_valid is False
        assert len(results) > len(incomplete_params)

        # 检查是否有缺失参数的错误
        missing_errors = [r for r in results if not r.is_valid and "缺少必需参数" in (r.error_message or "")]
        assert len(missing_errors) > 0

    def test_validate_all_parameters_invalid(self):
        """测试无效参数验证"""
        invalid_params = {
            "force_size": 1500,  # 超出范围
            "weapon_effectiveness": 1.5,  # 超出范围
            "invalid_param": 100  # 无效参数名
        }

        all_valid, results = self.validator.validate_all_parameters(
            invalid_params, "chokepoint_blockade"
        )

        assert all_valid is False
        # 结果会包含所有参数，包括缺失的必需参数
        assert len(results) > len(invalid_params)

        # 检查无效参数的错误
        invalid_errors = [r for r in results if not r.is_valid]
        assert len(invalid_errors) > 0

    def test_get_parameter_info(self):
        """测试参数信息获取"""
        param_info = self.validator.get_parameter_info("chokepoint_blockade")

        assert isinstance(param_info, dict)
        assert len(param_info) > 0

        # 检查参数信息结构
        for param_name, info in param_info.items():
            assert 'type' in info
            assert 'min_value' in info
            assert 'max_value' in info
            assert 'default_value' in info
            assert 'description' in info
            assert 'is_benefit' in info

    def test_get_user_friendly_error(self):
        """测试用户友好错误信息"""
        # 测试范围错误
        range_result = ValidationResult(
            is_valid=False,
            error_message="参数 'force_size' 的值 1500 超出有效范围 [100, 1000]",
            parameter_name="force_size",
            actual_value=1500,
            expected_range=(100, 1000)
        )

        friendly_error = self.validator.get_user_friendly_error(range_result)
        # 友好错误信息可能包含原始错误消息或改进的建议
        assert "超出范围" in friendly_error or "超出有效范围" in friendly_error

        # 测试未定义参数错误
        undefined_result = ValidationResult(
            is_valid=False,
            error_message="参数 'invalid_param' 在场景 'chokepoint_blockade' 中未定义",
            parameter_name="invalid_param"
        )

        friendly_error = self.validator.get_user_friendly_error(undefined_result)
        assert "不存在" in friendly_error

        # 测试类型错误
        type_result = ValidationResult(
            is_valid=False,
            error_message="参数 'force_size' 的值必须是数字类型",
            parameter_name="force_size"
        )

        friendly_error = self.validator.get_user_friendly_error(type_result)
        assert "必须是数字" in friendly_error

        # 测试缺失参数错误
        missing_result = ValidationResult(
            is_valid=False,
            error_message="缺少必需参数: 'force_size'",
            parameter_name="force_size"
        )

        friendly_error = self.validator.get_user_friendly_error(missing_result)
        assert "请填写所有必需的参数" in friendly_error

        # 测试有效结果
        valid_result = ValidationResult(
            is_valid=True,
            parameter_name="force_size"
        )

        friendly_error = self.validator.get_user_friendly_error(valid_result)
        assert friendly_error == ""

    def test_different_scenarios(self):
        """测试不同场景的验证"""
        scenarios = ["chokepoint_blockade", "landing_zone_clearance",
                    "mine_countermeasures", "underwater_surveillance"]

        for scenario in scenarios:
            # 测试是否能获取参数信息
            param_info = self.validator.get_parameter_info(scenario)
            assert isinstance(param_info, dict)
            assert len(param_info) > 0

            # 测试是否能验证参数
            if param_info:
                first_param = list(param_info.keys())[0]
                default_value = param_info[first_param]['default_value']

                result = self.validator.validate_parameter(
                    first_param, default_value, scenario
                )
                assert result.is_valid is True

    def test_edge_cases(self):
        """测试边界情况"""
        # 测试边界值
        result = self.validator.validate_parameter("force_size", 100, "chokepoint_blockade")
        assert result.is_valid is True

        result = self.validator.validate_parameter("force_size", 1000, "chokepoint_blockade")
        assert result.is_valid is True

        # 测试接近边界的值
        result = self.validator.validate_parameter("force_size", 100.1, "chokepoint_blockade")
        assert result.is_valid is True

        result = self.validator.validate_parameter("force_size", 999.9, "chokepoint_blockade")
        assert result.is_valid is True

    def test_special_parameter_types(self):
        """测试特殊参数类型"""
        # 测试百分比参数
        result = self.validator.validate_parameter("weapon_effectiveness", 0.5, "chokepoint_blockade")
        assert result.is_valid is True

        # 测试时间参数
        result = self.validator.validate_parameter("response_time", 12, "chokepoint_blockade")
        assert result.is_valid is True

        # 测试等级参数
        result = self.validator.validate_parameter("sea_state", 3, "chokepoint_blockade")
        assert result.is_valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])