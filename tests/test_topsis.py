"""
TOPSIS算法测试
测试核心算法功能的正确性
"""

import pytest
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.topsis import CombatTopsis, TopsisResult
import numpy as np


class TestCombatTopsis:
    """TOPSIS算法测试类"""

    def setup_method(self):
        """测试前设置"""
        self.topsis = CombatTopsis()

    def test_init(self):
        """测试初始化"""
        assert self.topsis is not None
        assert hasattr(self.topsis, 'config')
        assert hasattr(self.topsis, 'indicators')
        assert len(self.topsis.indicators) > 0

    def test_load_config(self):
        """测试配置加载"""
        config = self.topsis._load_config("config/weights.yaml")
        assert 'weights' in config
        assert 'indicator_mapping' in config
        assert 'chokepoint_blockade' in config['weights']

    def test_normalize_parameters_to_indicators(self):
        """测试参数到指标的映射"""
        scenario_params = {
            'force_size': 600,
            'ship_count': 30,
            'weapon_effectiveness': 0.8,
            'sensor_capability': 0.9,
            'communication_reliability': 0.85,
            'sea_state': 2,
            'visibility': 0.7,
            'blockade_effectiveness': 0.85,
            'response_time': 4,
            'mission_duration': 48
        }

        indicator_scores = self.topsis.normalize_parameters_to_indicators(
            scenario_params, 'chokepoint_blockade'
        )

        # 验证返回的指标
        assert isinstance(indicator_scores, dict)
        assert len(indicator_scores) > 0

        # 验证指标值的范围
        for indicator, score in indicator_scores.items():
            assert 0 <= score <= 1, f"指标 {indicator} 的值 {score} 超出范围 [0,1]"

    def test_calculate_topsis(self):
        """测试TOPSIS计算"""
        indicator_scores = {
            'overall_combat_power': 0.75,
            'technological_superiority': 0.8,
            'environmental_adaptability': 0.65,
            'mission_achievement': 0.85,
            'operational_efficiency': 0.7
        }

        result = self.topsis.calculate_topsis(indicator_scores, 'chokepoint_blockade')

        # 验证返回结果类型
        assert isinstance(result, TopsisResult)

        # 验证结果属性
        assert hasattr(result, 'overall_score')
        assert hasattr(result, 'performance_level')
        assert hasattr(result, 'indicator_scores')
        assert hasattr(result, 'ranking')
        assert hasattr(result, 'suggestions')

        # 验证得分范围
        assert 0 <= result.overall_score <= 1
        assert result.performance_level in ['优秀', '良好', '一般', '较差']
        assert result.ranking > 0
        assert isinstance(result.suggestions, list)

    def test_topsis_calculation_steps(self):
        """测试TOPSIS计算步骤"""
        # 创建测试数据
        decision_matrix = np.array([
            [0.8, 0.7, 0.9, 0.6, 0.8],  # 当前方案
            [1.0, 1.0, 1.0, 1.0, 1.0],  # 理想方案
            [0.0, 0.0, 0.0, 0.0, 0.0],  # 最差方案
            [0.5, 0.5, 0.5, 0.5, 0.5]   # 平均方案
        ])

        weights = np.array([0.25, 0.20, 0.15, 0.25, 0.15])
        criteria_types = [True, True, True, True, True]  # 都是效益型指标

        result = self.topsis._topsis_calculation(decision_matrix, weights, criteria_types)

        # 验证结果结构
        assert 'scores' in result
        assert 'ranking' in result
        assert 'normalized_matrix' in result
        assert 'weighted_matrix' in result
        assert 'distances' in result

        # 验证得分
        scores = result['scores']
        assert len(scores) == 4
        assert all(0 <= score <= 1 for score in scores)

        # 验证排名
        rankings = result['ranking']
        assert len(rankings) == 4
        assert all(0 <= rank < 4 for rank in rankings)

    def test_normalize_matrix(self):
        """测试矩阵标准化"""
        matrix = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        normalized = self.topsis._normalize_matrix(matrix)

        # 验证形状
        assert normalized.shape == matrix.shape

        # 验证每列的平方和为1
        column_sums = np.sum(normalized**2, axis=0)
        assert all(np.abs(s - 1) < 1e-10 for s in column_sums)

    def test_calculate_weighted_matrix(self):
        """测试加权矩阵计算"""
        normalized_matrix = np.array([
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6]
        ])
        weights = np.array([0.25, 0.35, 0.40])

        weighted = self.topsis._calculate_weighted_matrix(normalized_matrix, weights)

        # 验证计算结果
        expected = normalized_matrix * weights
        assert np.allclose(weighted, expected)

    def test_find_ideal_solutions(self):
        """测试理想解确定"""
        weighted_matrix = np.array([
            [0.8, 0.7, 0.9],
            [0.6, 0.8, 0.7],
            [0.9, 0.6, 0.8]
        ])
        criteria_types = [True, True, False]  # 效益型，效益型，成本型

        ideal_best, ideal_worst = self.topsis._find_ideal_solutions(
            weighted_matrix, criteria_types
        )

        # 验证理想解
        assert len(ideal_best) == 3
        assert len(ideal_worst) == 3

        # 验证效益型指标
        assert ideal_best[0] == 0.9  # 第一列最大值
        assert ideal_best[1] == 0.8  # 第二列最大值
        assert ideal_worst[2] == 0.9  # 第三列最大值（成本型指标）

    def test_calculate_distances(self):
        """测试距离计算"""
        weighted_matrix = np.array([
            [0.8, 0.7, 0.9],
            [0.6, 0.8, 0.7]
        ])
        ideal_best = np.array([0.9, 0.8, 0.9])
        ideal_worst = np.array([0.6, 0.7, 0.7])

        best_distances, worst_distances = self.topsis._calculate_distances(
            weighted_matrix, ideal_best, ideal_worst
        )

        # 验证距离数量
        assert len(best_distances) == 2
        assert len(worst_distances) == 2

        # 验证距离为正数
        assert all(d >= 0 for d in best_distances)
        assert all(d >= 0 for d in worst_distances)

    def test_calculate_similarity(self):
        """测试相对贴近度计算"""
        best_distances = np.array([0.5, 0.3, 0.7])
        worst_distances = np.array([0.8, 0.6, 0.4])

        similarity = self.topsis._calculate_similarity((best_distances, worst_distances))

        # 验证贴近度范围
        assert len(similarity) == 3
        assert all(0 <= s <= 1 for s in similarity)

        # 验证计算公式
        expected = worst_distances / (best_distances + worst_distances + 1e-10)
        assert np.allclose(similarity, expected)

    def test_get_performance_level(self):
        """测试性能等级获取"""
        assert self.topsis._get_performance_level(0.85) == "优秀"
        assert self.topsis._get_performance_level(0.75) == "良好"
        assert self.topsis._get_performance_level(0.55) == "一般"
        assert self.topsis._get_performance_level(0.35) == "较差"

    def test_generate_suggestions(self):
        """测试建议生成"""
        indicator_scores = {
            'overall_combat_power': 0.3,
            'technological_superiority': 0.9,
            'environmental_adaptability': 0.4,
            'mission_achievement': 0.8,
            'operational_efficiency': 0.6
        }

        suggestions = self.topsis._generate_suggestions(indicator_scores, 0.5)

        # 验证建议
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

        # 验证建议内容
        suggestions_text = ' '.join(suggestions)
        assert '较差' in suggestions_text or '一般' in suggestions_text
        assert '建议' in suggestions_text

    def test_edge_cases(self):
        """测试边界情况"""
        # 测试全零值
        zero_scores = {ind: 0.0 for ind in self.topsis.indicators}
        result = self.topsis.calculate_topsis(zero_scores, 'chokepoint_blockade')
        assert result.overall_score >= 0

        # 测试全1值
        one_scores = {ind: 1.0 for ind in self.topsis.indicators}
        result = self.topsis.calculate_topsis(one_scores, 'chokepoint_blockade')
        assert result.overall_score <= 1

    def test_invalid_input_handling(self):
        """测试无效输入处理"""
        # 测试空的参数字典
        empty_params = {}
        indicator_scores = self.topsis.normalize_parameters_to_indicators(
            empty_params, 'chokepoint_blockade'
        )
        assert isinstance(indicator_scores, dict)

        # 测试无效的参数值
        invalid_params = {'invalid_param': 999}
        indicator_scores = self.topsis.normalize_parameters_to_indicators(
            invalid_params, 'chokepoint_blockade'
        )
        assert isinstance(indicator_scores, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])