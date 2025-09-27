"""
可视化测试
测试图表生成功能的正确性
"""

import pytest
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.visualization import ChartGenerator
from utils.topsis import TopsisResult
import plotly.graph_objects as go


class TestChartGenerator:
    """图表生成器测试类"""

    def setup_method(self):
        """测试前设置"""
        self.generator = ChartGenerator()

    def test_init(self):
        """测试初始化"""
        assert self.generator is not None
        assert hasattr(self.generator, 'chinese_indicator_names')
        assert hasattr(self.generator, 'colors')

    def test_chinese_indicator_names(self):
        """测试中文指标名称映射"""
        names = self.generator.chinese_indicator_names

        assert isinstance(names, dict)
        assert len(names) > 0

        # 检查主要指标
        assert 'overall_combat_power' in names
        assert 'technological_superiority' in names
        assert 'environmental_adaptability' in names
        assert 'mission_achievement' in names
        assert 'operational_efficiency' in names

        # 检查中文映射
        assert names['overall_combat_power'] == '总体作战能力'
        assert names['technological_superiority'] == '技术优势'

    def test_colors(self):
        """测试颜色方案"""
        colors = self.generator.colors

        assert isinstance(colors, dict)
        assert len(colors) > 0

        # 检查主要颜色
        assert 'primary' in colors
        assert 'secondary' in colors
        assert 'success' in colors
        assert 'warning' in colors
        assert 'info' in colors

    def test_create_radar_chart(self):
        """测试雷达图创建"""
        indicator_scores = {
            'overall_combat_power': 0.8,
            'technological_superiority': 0.7,
            'environmental_adaptability': 0.6,
            'mission_achievement': 0.9,
            'operational_efficiency': 0.5
        }

        fig = self.generator.create_radar_chart(indicator_scores, "chokepoint_blockade")

        # 验证返回类型
        assert isinstance(fig, go.Figure)

        # 验证图表数据
        assert len(fig.data) > 0

        # 验证图表布局
        assert fig.layout.title.text is not None

    def test_create_indicator_comparison_chart(self):
        """测试指标对比图创建"""
        indicator_scores = {
            'overall_combat_power': 0.8,
            'technological_superiority': 0.7,
            'environmental_adaptability': 0.6,
            'mission_achievement': 0.9,
            'operational_efficiency': 0.5
        }

        fig = self.generator.create_indicator_comparison_chart(indicator_scores, "chokepoint_blockade")

        # 验证返回类型
        assert isinstance(fig, go.Figure)

        # 验证图表数据
        assert len(fig.data) > 0

        # 验证是柱状图
        assert hasattr(fig.data[0], 'type') and fig.data[0].type == 'bar'

    def test_create_overall_score_gauge(self):
        """测试总体得分仪表盘创建"""
        fig = self.generator.create_overall_score_gauge(0.75, "良好", "总体效能得分")

        # 验证返回类型
        assert isinstance(fig, go.Figure)

        # 验证图表数据
        assert len(fig.data) > 0

        # 验证是指示器类型
        assert hasattr(fig.data[0], 'type') and fig.data[0].type == 'indicator'

    def test_create_comparison_table(self):
        """测试对比表格创建"""
        indicator_scores = {
            'overall_combat_power': 0.8,
            'technological_superiority': 0.7,
            'environmental_adaptability': 0.6,
            'mission_achievement': 0.9,
            'operational_efficiency': 0.5
        }

        df = self.generator.create_comparison_table(
            indicator_scores, "良好", 2, "chokepoint_blockade"
        )

        # 验证返回类型
        assert hasattr(df, 'shape')  # DataFrame-like

        # 验证表格结构
        assert len(df) > 0
        assert len(df.columns) > 0

    def test_create_suggestions_chart(self):
        """测试建议图表创建"""
        suggestions = [
            "建议1：提升作战能力",
            "建议2：优化装备配置",
            "建议3：加强训练"
        ]

        fig = self.generator.create_suggestions_chart(suggestions)

        # 验证返回类型
        assert isinstance(fig, go.Figure)

        # 验证图表布局
        assert fig.layout.title.text is not None

    def test_get_score_level(self):
        """测试得分等级获取"""
        assert self.generator._get_score_level(0.85) == "优秀"
        assert self.generator._get_score_level(0.75) == "良好"
        assert self.generator._get_score_level(0.55) == "一般"
        assert self.generator._get_score_level(0.35) == "较差"

    def test_create_comprehensive_dashboard(self):
        """测试综合仪表板创建"""
        indicator_scores = {
            'overall_combat_power': 0.8,
            'technological_superiority': 0.7,
            'environmental_adaptability': 0.6,
            'mission_achievement': 0.9,
            'operational_efficiency': 0.5
        }

        topsis_result = TopsisResult(
            overall_score=0.75,
            performance_level="良好",
            indicator_scores=indicator_scores,
            ranking=2,
            suggestions=["建议1", "建议2"],
            calculation_details={}
        )

        charts, table_df = self.generator.create_comprehensive_dashboard(
            topsis_result, "chokepoint_blockade"
        )

        # 验证返回类型
        assert isinstance(charts, list)
        assert len(charts) > 0

        # 验证所有图表都是Figure类型
        for chart in charts:
            assert isinstance(chart, go.Figure)

        # 验证表格
        assert hasattr(table_df, 'shape')  # DataFrame-like

    def test_edge_cases(self):
        """测试边界情况"""
        # 测试空数据
        empty_scores = {}
        fig = self.generator.create_radar_chart(empty_scores, "chokepoint_blockade")
        assert isinstance(fig, go.Figure)

        # 测试极值
        extreme_scores = {
            'overall_combat_power': 0.0,
            'technological_superiority': 1.0,
            'environmental_adaptability': 0.5,
            'mission_achievement': 0.0,
            'operational_efficiency': 1.0
        }

        fig = self.generator.create_indicator_comparison_chart(extreme_scores, "chokepoint_blockade")
        assert isinstance(fig, go.Figure)

        # 测试空建议列表
        empty_suggestions = []
        fig = self.generator.create_suggestions_chart(empty_suggestions)
        assert isinstance(fig, go.Figure)

    def test_error_handling(self):
        """测试错误处理"""
        # 测试无效指标名称
        invalid_scores = {'invalid_indicator': 0.5}
        fig = self.generator.create_radar_chart(invalid_scores, "chokepoint_blockade")
        assert isinstance(fig, go.Figure)

        # 测试无效得分值
        invalid_scores = {
            'overall_combat_power': -0.1,  # 负值
            'technological_superiority': 1.5,  # 超过1
        }

        fig = self.generator.create_indicator_comparison_chart(invalid_scores, "chokepoint_blockade")
        assert isinstance(fig, go.Figure)

    def test_chart_layout_properties(self):
        """测试图表布局属性"""
        indicator_scores = {
            'overall_combat_power': 0.8,
            'technological_superiority': 0.7,
            'environmental_adaptability': 0.6,
            'mission_achievement': 0.9,
            'operational_efficiency': 0.5
        }

        # 测试雷达图布局
        radar_fig = self.generator.create_radar_chart(indicator_scores, "chokepoint_blockade")
        assert radar_fig.layout.width == 600
        assert radar_fig.layout.height == 500
        assert radar_fig.layout.showlegend is True

        # 测试柱状图布局
        bar_fig = self.generator.create_indicator_comparison_chart(indicator_scores, "chokepoint_blockade")
        assert bar_fig.layout.width == 700
        assert bar_fig.layout.height == 500
        assert bar_fig.layout.showlegend is False

        # 测试仪表盘布局
        gauge_fig = self.generator.create_overall_score_gauge(0.75, "良好")
        assert gauge_fig.layout.width == 500
        assert gauge_fig.layout.height == 400

    def test_different_scenarios(self):
        """测试不同场景的图表生成"""
        scenarios = ["chokepoint_blockade", "landing_zone_clearance",
                    "mine_countermeasures", "underwater_surveillance"]

        indicator_scores = {
            'overall_combat_power': 0.8,
            'technological_superiority': 0.7,
            'environmental_adaptability': 0.6,
            'mission_achievement': 0.9,
            'operational_efficiency': 0.5
        }

        for scenario in scenarios:
            # 测试雷达图
            radar_fig = self.generator.create_radar_chart(indicator_scores, scenario)
            assert isinstance(radar_fig, go.Figure)
            assert scenario in radar_fig.layout.title.text

            # 测试柱状图
            bar_fig = self.generator.create_indicator_comparison_chart(indicator_scores, scenario)
            assert isinstance(bar_fig, go.Figure)
            assert scenario in bar_fig.layout.title.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])