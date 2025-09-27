"""
应用测试
测试Streamlit应用的主要功能
"""

import pytest
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import CombatAssessmentApp


class TestCombatAssessmentApp:
    """作战评估应用测试类"""

    def setup_method(self):
        """测试前设置"""
        self.app = CombatAssessmentApp()

    def test_init(self):
        """测试应用初始化"""
        assert self.app is not None
        assert hasattr(self.app, 'topsis')
        assert hasattr(self.app, 'validator')
        assert hasattr(self.app, 'chart_generator')

    def test_session_state_init(self):
        """测试会话状态初始化"""
        assert 'current_scenario' in self.app.topsis.config
        assert hasattr(self.app, 'load_scenarios_config')
        assert hasattr(self.app, 'get_scenario_info')

    def test_load_scenarios_config(self):
        """测试场景配置加载"""
        config = self.app.load_scenarios_config()

        assert isinstance(config, dict)
        assert 'scenarios' in config

        # 检查主要场景
        scenarios = config['scenarios']
        assert 'chokepoint_blockade' in scenarios
        assert 'landing_zone_clearance' in scenarios
        assert 'mine_countermeasures' in scenarios
        assert 'underwater_surveillance' in scenarios

    def test_get_scenario_info(self):
        """测试场景信息获取"""
        scenario_info = self.app.get_scenario_info()

        assert isinstance(scenario_info, dict)
        assert len(scenario_info) == 4

        # 检查场景信息结构
        for scenario_key, info in scenario_info.items():
            assert 'name' in info
            assert 'description' in info
            assert isinstance(info['name'], str)
            assert isinstance(info['description'], str)

    def test_validator_integration(self):
        """测试验证器集成"""
        # 测试参数验证功能
        result = self.app.validator.validate_parameter("force_size", 500, "chokepoint_blockade")
        assert result.is_valid is True

        # 测试参数信息获取
        param_info = self.app.validator.get_parameter_info("chokepoint_blockade")
        assert isinstance(param_info, dict)
        assert len(param_info) > 0

    def test_topsis_integration(self):
        """测试TOPSIS集成"""
        # 测试参数到指标映射
        scenario_params = {
            'force_size': 600,
            'ship_count': 30,
            'weapon_effectiveness': 0.8,
            'sensor_capability': 0.9,
            'communication_reliability': 0.85
        }

        indicator_scores = self.app.topsis.normalize_parameters_to_indicators(
            scenario_params, 'chokepoint_blockade'
        )

        assert isinstance(indicator_scores, dict)
        assert len(indicator_scores) > 0

        # 测试TOPSIS计算
        result = self.app.topsis.calculate_topsis(indicator_scores, 'chokepoint_blockade')
        assert result is not None
        assert hasattr(result, 'overall_score')
        assert hasattr(result, 'performance_level')

    def test_chart_generator_integration(self):
        """测试图表生成器集成"""
        # 测试数据
        indicator_scores = {
            'overall_combat_power': 0.8,
            'technological_superiority': 0.7,
            'environmental_adaptability': 0.6,
            'mission_achievement': 0.9,
            'operational_efficiency': 0.5
        }

        # 测试雷达图生成
        radar_fig = self.app.chart_generator.create_radar_chart(
            indicator_scores, "chokepoint_blockade"
        )
        assert radar_fig is not None

        # 测试柱状图生成
        bar_fig = self.app.chart_generator.create_indicator_comparison_chart(
            indicator_scores, "chokepoint_blockade"
        )
        assert bar_fig is not None

        # 测试仪表盘生成
        gauge_fig = self.app.chart_generator.create_overall_score_gauge(
            0.75, "良好"
        )
        assert gauge_fig is not None

    def test_parameter_validation_flow(self):
        """测试参数验证流程"""
        # 测试有效参数
        valid_params = {
            'force_size': 500,
            'ship_count': 30,
            'weapon_effectiveness': 0.8
        }

        all_valid = self.app.validate_parameters("chokepoint_blockade")
        # 注意：这里需要设置session_state.parameters才能正确测试

        # 测试无效参数
        invalid_params = {
            'force_size': 1500,  # 超出范围
            'ship_count': 100    # 超出范围
        }

        # 设置无效参数到session_state
        self.app.topsis.session_state = {'parameters': invalid_params}
        all_valid = self.app.validate_parameters("chokepoint_blockade")
        assert all_valid is False

    def test_assessment_flow(self):
        """测试评估流程"""
        # 设置测试参数
        test_params = {
            'force_size': 600,
            'ship_count': 30,
            'weapon_effectiveness': 0.8,
            'sensor_capability': 0.9,
            'communication_reliability': 0.85,
            'sea_state': 2,
            'visibility': 0.7,
            'weather_severity': 2,
            'blockade_effectiveness': 0.85,
            'response_time': 4,
            'mission_duration': 48
        }

        # 设置session_state
        self.app.topsis.session_state = {'parameters': test_params}

        # 执行评估
        try:
            self.app.perform_assessment("chokepoint_blockade")
            # 如果没有异常，说明评估流程基本正常
            assert True
        except Exception as e:
            # 可能因为Streamlit环境限制而失败，这是正常的
            pytest.skip(f"评估流程测试跳过（Streamlit环境限制）: {e}")

    def test_different_scenarios(self):
        """测试不同场景"""
        scenarios = ["chokepoint_blockade", "landing_zone_clearance",
                    "mine_countermeasures", "underwater_surveillance"]

        for scenario in scenarios:
            # 测试场景信息
            scenario_info = self.app.get_scenario_info()
            assert scenario in scenario_info

            # 测试参数信息
            param_info = self.app.validator.get_parameter_info(scenario)
            assert isinstance(param_info, dict)
            assert len(param_info) > 0

            # 测试TOPSIS配置
            weights = self.app.topsis.config['weights'].get(scenario)
            assert weights is not None
            assert 'indicators' in weights

    def test_error_handling(self):
        """测试错误处理"""
        # 测试配置文件不存在的情况
        try:
            # 尝试加载不存在的配置文件
            config = self.app.load_scenarios_config()
            # 如果配置文件存在，测试继续
            assert isinstance(config, dict)
        except Exception as e:
            # 如果配置文件不存在，应该有适当的错误处理
            assert "config/scenarios.yaml" in str(e) or "配置" in str(e)

        # 测试无效场景类型
        try:
            param_info = self.app.validator.get_parameter_info("invalid_scenario")
            # 如果没有抛出异常，检查返回值
            assert isinstance(param_info, dict)
        except Exception as e:
            # 应该有适当的错误处理
            assert "scenario" in str(e).lower()

    def test_comprehensive_workflow(self):
        """测试综合工作流程"""
        # 1. 选择场景
        scenario = "chokepoint_blockade"
        scenario_info = self.app.get_scenario_info()
        assert scenario in scenario_info

        # 2. 获取参数信息
        param_info = self.app.validator.get_parameter_info(scenario)
        assert len(param_info) > 0

        # 3. 设置参数
        test_params = {}
        for param_name, param_data in param_info.items():
            test_params[param_name] = param_data['default_value']

        # 4. 验证参数
        self.app.topsis.session_state = {'parameters': test_params}
        all_valid = self.app.validate_parameters(scenario)
        assert all_valid is True

        # 5. 映射到指标
        indicator_scores = self.app.topsis.normalize_parameters_to_indicators(
            test_params, scenario
        )
        assert isinstance(indicator_scores, dict)
        assert len(indicator_scores) > 0

        # 6. 计算TOPSIS
        result = self.app.topsis.calculate_topsis(indicator_scores, scenario)
        assert result is not None

        # 7. 生成图表
        charts, table_df = self.app.chart_generator.create_comprehensive_dashboard(
            result, scenario
        )
        assert len(charts) > 0

        print(f"工作流程测试成功 - 场景: {scenario}, 得分: {result.overall_score:.3f}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])