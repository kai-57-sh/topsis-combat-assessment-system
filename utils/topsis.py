"""
简化TOPSIS算法实现
专为作战体系效能评估优化
基于 examples/topsis.py 但针对5-8个核心指标进行简化
"""

import numpy as np
import yaml
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class TopsisResult:
    """TOPSIS评估结果"""
    overall_score: float
    performance_level: str
    indicator_scores: Dict[str, float]
    ranking: int
    suggestions: List[str]
    calculation_details: Dict[str, Any]

class CombatTopsis:
    """作战体系效能TOPSIS评估器"""

    def __init__(self, config_path: str = "config/weights.yaml"):
        """
        初始化TOPSIS评估器

        Args:
            config_path: 权重配置文件路径
        """
        self.config = self._load_config(config_path)
        self.indicators = list(self.config['indicator_mapping'].keys())

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

    def normalize_parameters_to_indicators(
        self,
        scenario_params: Dict[str, float],
        scenario_type: str
    ) -> Dict[str, float]:
        """
        将输入参数标准化映射到5个核心评估指标

        Args:
            scenario_params: 场景参数字典
            scenario_type: 场景类型

        Returns:
            标准化后的指标得分字典
        """
        indicator_scores = {}

        for indicator, related_params in self.config['indicator_mapping'].items():
            # 找到相关的参数值
            related_values = []
            for param in related_params:
                if param in scenario_params:
                    value = scenario_params[param]
                    # 检查参数是否在场景配置中
                    if self._is_valid_parameter(param, value, scenario_type):
                        related_values.append(value)
                    else:
                        logger.warning(f"参数 {param} 值 {value} 超出范围")

            if related_values:
                # 计算该指标的综合得分
                indicator_scores[indicator] = self._calculate_indicator_score(
                    related_values, indicator, scenario_type
                )
            else:
                # 如果没有相关参数，使用默认值
                indicator_scores[indicator] = 0.5

        return indicator_scores

    def _is_valid_parameter(self, param_name: str, value: float, scenario_type: str) -> bool:
        """检查参数值是否有效"""
        try:
            with open("config/scenarios.yaml", 'r', encoding='utf-8') as file:
                scenarios_config = yaml.safe_load(file)

            scenario = scenarios_config['scenarios'][scenario_type]
            for param in scenario['parameters']:
                if param['name'] == param_name:
                    return param['min_value'] <= value <= param['max_value']

            return False
        except Exception as e:
            logger.error(f"参数验证失败: {e}")
            return False

    def _calculate_indicator_score(
        self,
        values: List[float],
        indicator: str,
        scenario_type: str
    ) -> float:
        """
        计算单个指标的得分

        Args:
            values: 相关参数值列表
            indicator: 指标名称
            scenario_type: 场景类型

        Returns:
            标准化后的指标得分 (0-1之间)
        """
        if not values:
            return 0.5

        # 简单的加权平均计算
        # 这里可以根据实际需求使用更复杂的算法
        weights = self.config['weights'][scenario_type]['indicators']

        # 基于指标类型进行不同的标准化处理
        if indicator == 'overall_combat_power':
            # 作战能力：数值越大越好，需要考虑量纲差异
            normalized_values = [min(max(v / 1000, 0), 1) for v in values]
        elif indicator == 'technological_superiority':
            # 技术优势：已经是0-1范围的可以直接使用
            normalized_values = [min(max(v, 0), 1) for v in values]
        elif indicator == 'environmental_adaptability':
            # 环境适应性：需要根据参数类型正向或反向处理
            normalized_values = [min(max(v / 10, 0), 1) for v in values]
        elif indicator == 'mission_achievement':
            # 任务达成度：已经是比例形式
            normalized_values = [min(max(v, 0), 1) for v in values]
        elif indicator == 'operational_efficiency':
            # 作战效率：时间类指标需要反向处理
            normalized_values = [min(max(1 / (v + 1), 0), 1) for v in values]
        else:
            # 默认处理
            normalized_values = [min(max(v, 0), 1) for v in values]

        # 计算加权平均
        if normalized_values:
            return np.mean(normalized_values)
        else:
            return 0.5

    def calculate_topsis(
        self,
        indicator_scores: Dict[str, float],
        scenario_type: str
    ) -> TopsisResult:
        """
        执行TOPSIS计算

        Args:
            indicator_scores: 指标得分字典
            scenario_type: 场景类型

        Returns:
            TOPSIS评估结果
        """
        try:
            # 构建决策矩阵
            # 这里我们只有一个方案，但为了TOPSIS算法，我们创建几个参考方案
            alternatives = self._create_reference_alternatives(indicator_scores)

            # 获取指标权重
            weights = self._get_indicator_weights(scenario_type)

            # 确定指标类型（都是效益型，越大越好）
            criteria_types = [True] * len(self.indicators)

            # 执行TOPSIS计算
            result = self._topsis_calculation(alternatives, weights, criteria_types)

            # 生成评估结果
            # 当前方案现在在矩阵中的位置是2（索引2）
            current_index = 2
            overall_score = result['scores'][current_index]
            performance_level = self._get_performance_level(overall_score)
            ranking = result['ranking'][current_index] + 1  # 排名从1开始

            suggestions = self._generate_suggestions(indicator_scores, overall_score)

            return TopsisResult(
                overall_score=overall_score,
                performance_level=performance_level,
                indicator_scores=indicator_scores,
                ranking=ranking,
                suggestions=suggestions,
                calculation_details=result
            )

        except Exception as e:
            logger.error(f"TOPSIS计算失败: {e}")
            raise

    def _create_reference_alternatives(self, current_scores: Dict[str, float]) -> np.ndarray:
        """创建参考方案用于TOPSIS比较"""
        # 当前方案
        current = [current_scores[indicator] for indicator in self.indicators]

        # 创建基于历史数据或标准的参考方案
        # 这些方案代表不同能力水平的典型配置

        # 优秀方案（各项指标都较好，但不是完美的1.0）
        excellent = [0.85, 0.90, 0.80, 0.85, 0.75]  # 根据指标特点调整

        # 良好方案（各项指标中等偏上）
        good = [0.70, 0.75, 0.65, 0.70, 0.60]

        # 一般方案（各项指标中等）
        average = [0.55, 0.60, 0.50, 0.55, 0.45]

        # 较差方案（各项指标偏低）
        poor = [0.40, 0.45, 0.35, 0.40, 0.30]

        # 构建决策矩阵，按能力水平排序
        return np.array([excellent, good, current, average, poor])

    def _get_indicator_weights(self, scenario_type: str) -> np.ndarray:
        """获取指标权重"""
        weights_config = self.config['weights'][scenario_type]['indicators']
        weights = [weights_config[indicator] for indicator in self.indicators]

        # 确保权重和为1
        weights = np.array(weights)
        weights = weights / np.sum(weights)

        return weights

    def _topsis_calculation(
        self,
        decision_matrix: np.ndarray,
        weights: np.ndarray,
        criteria_types: List[bool]
    ) -> Dict[str, Any]:
        """
        执行TOPSIS算法计算

        Args:
            decision_matrix: 决策矩阵 (方案数 × 指标数)
            weights: 权重向量
            criteria_types: 指标类型列表 (True=效益型, False=成本型)

        Returns:
            计算结果字典
        """
        # 步骤1: 数据标准化
        normalized_matrix = self._normalize_matrix(decision_matrix)

        # 步骤2: 计算加权标准化矩阵
        weighted_matrix = self._calculate_weighted_matrix(normalized_matrix, weights)

        # 步骤3: 确定正负理想解
        ideal_best, ideal_worst = self._find_ideal_solutions(weighted_matrix, criteria_types)

        # 步骤4: 计算距离
        distances = self._calculate_distances(weighted_matrix, ideal_best, ideal_worst)

        # 步骤5: 计算相对贴近度
        similarity_scores = self._calculate_similarity(distances)

        # 步骤6: 排序
        rankings = np.argsort(-similarity_scores)

        return {
            'scores': similarity_scores,
            'ranking': rankings,
            'normalized_matrix': normalized_matrix,
            'weighted_matrix': weighted_matrix,
            'ideal_best': ideal_best,
            'ideal_worst': ideal_worst,
            'distances': distances
        }

    def _normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """向量标准化"""
        # 计算每列的平方和的平方根
        column_sums = np.sqrt(np.sum(matrix**2, axis=0))
        # 避免除零
        column_sums = np.where(column_sums == 0, 1, column_sums)
        return matrix / column_sums

    def _calculate_weighted_matrix(
        self,
        normalized_matrix: np.ndarray,
        weights: np.ndarray
    ) -> np.ndarray:
        """计算加权标准化矩阵"""
        return normalized_matrix * weights

    def _find_ideal_solutions(
        self,
        weighted_matrix: np.ndarray,
        criteria_types: List[bool]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """确定正负理想解"""
        ideal_best = np.zeros(weighted_matrix.shape[1])
        ideal_worst = np.zeros(weighted_matrix.shape[1])

        for j in range(weighted_matrix.shape[1]):
            if criteria_types[j]:  # 效益型指标
                ideal_best[j] = np.max(weighted_matrix[:, j])
                ideal_worst[j] = np.min(weighted_matrix[:, j])
            else:  # 成本型指标
                ideal_best[j] = np.min(weighted_matrix[:, j])
                ideal_worst[j] = np.max(weighted_matrix[:, j])

        return ideal_best, ideal_worst

    def _calculate_distances(
        self,
        weighted_matrix: np.ndarray,
        ideal_best: np.ndarray,
        ideal_worst: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """计算到正负理想解的距离"""
        m = weighted_matrix.shape[0]

        best_distances = np.zeros(m)
        worst_distances = np.zeros(m)

        for i in range(m):
            # 到正理想解的距离
            best_distances[i] = np.sqrt(
                np.sum((weighted_matrix[i] - ideal_best) ** 2)
            )
            # 到负理想解的距离
            worst_distances[i] = np.sqrt(
                np.sum((weighted_matrix[i] - ideal_worst) ** 2)
            )

        return best_distances, worst_distances

    def _calculate_similarity(
        self,
        distances: Tuple[np.ndarray, np.ndarray]
    ) -> np.ndarray:
        """计算相对贴近度"""
        best_distances, worst_distances = distances

        # 避免除零错误
        similarity = worst_distances / (best_distances + worst_distances + 1e-10)

        # 处理NaN值
        similarity = np.nan_to_num(similarity)

        return similarity

    def _get_performance_level(self, score: float) -> str:
        """根据得分返回性能等级"""
        if score >= 0.8:
            return "优秀"
        elif score >= 0.6:
            return "良好"
        elif score >= 0.4:
            return "一般"
        else:
            return "较差"

    def _generate_suggestions(
        self,
        indicator_scores: Dict[str, float],
        overall_score: float
    ) -> List[str]:
        """生成改进建议"""
        suggestions = []

        # 基于总体得分的建议
        if overall_score >= 0.8:
            suggestions.append("作战体系效能优秀，建议保持现有配置")
        elif overall_score >= 0.6:
            suggestions.append("作战体系效能良好，可针对薄弱环节进行优化")
        elif overall_score >= 0.4:
            suggestions.append("作战体系效能一般，需要重点改进关键指标")
        else:
            suggestions.append("作战体系效能较差，建议全面重新评估")

        # 基于各项指标的建议
        weakest_indicator = min(indicator_scores.items(), key=lambda x: x[1])
        strongest_indicator = max(indicator_scores.items(), key=lambda x: x[1])

        if weakest_indicator[1] < 0.5:
            indicator_names = {
                'overall_combat_power': '总体作战能力',
                'technological_superiority': '技术优势',
                'environmental_adaptability': '环境适应性',
                'mission_achievement': '任务达成度',
                'operational_efficiency': '作战效率'
            }
            suggestions.append(
                f"建议重点提升{indicator_names.get(weakest_indicator[0], weakest_indicator[0])}"
            )

        if strongest_indicator[1] > 0.8:
            suggestions.append("建议充分发挥优势领域的带动作用")

        return suggestions


# 使用示例和测试函数
def test_topsis_algorithm():
    """测试TOPSIS算法"""
    # 创建评估器
    topsis = CombatTopsis()

    # 模拟要峡封控场景的参数输入
    scenario_params = {
        'force_size': 600,
        'ship_count': 30,
        'aircraft_count': 60,
        'personnel_quality': 0.85,
        'weapon_effectiveness': 0.75,
        'sensor_capability': 0.8,
        'communication_reliability': 0.9,
        'electronic_warfare': 0.65,
        'sea_state': 2,
        'visibility': 0.7,
        'weather_severity': 2,
        'blockade_effectiveness': 0.85,
        'response_time': 4,
        'mission_duration': 48
    }

    # 映射到指标
    indicator_scores = topsis.normalize_parameters_to_indicators(
        scenario_params, 'chokepoint_blockade'
    )

    print("指标得分:")
    for indicator, score in indicator_scores.items():
        print(f"  {indicator}: {score:.3f}")

    # 执行TOPSIS计算
    result = topsis.calculate_topsis(indicator_scores, 'chokepoint_blockade')

    print(f"\n评估结果:")
    print(f"  总体得分: {result.overall_score:.3f}")
    print(f"  性能等级: {result.performance_level}")
    print(f"  排名: {result.ranking}")
    print(f"  改进建议:")
    for suggestion in result.suggestions:
        print(f"    - {suggestion}")

if __name__ == "__main__":
    test_topsis_algorithm()