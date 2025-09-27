"""
可视化组件模块
为作战体系效能评估系统提供图表生成功能
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ChartGenerator:
    """图表生成器"""

    def __init__(self):
        """初始化图表生成器"""
        # 中文指标名称映射
        self.chinese_indicator_names = {
            'overall_combat_power': '总体作战能力',
            'technological_superiority': '技术优势',
            'environmental_adaptability': '环境适应性',
            'mission_achievement': '任务达成度',
            'operational_efficiency': '作战效率'
        }

        # 颜色方案
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd',
            'light': '#8c564b'
        }

    def create_radar_chart(
        self,
        indicator_scores: Dict[str, float],
        scenario_type: str,
        title: str = "多维度评估结果"
    ) -> go.Figure:
        """
        创建雷达图

        Args:
            indicator_scores: 指标得分字典
            scenario_type: 场景类型
            title: 图表标题

        Returns:
            Plotly雷达图对象
        """
        try:
            # 获取中文名称
            indicator_names = [self.chinese_indicator_names.get(ind, ind) for ind in indicator_scores.keys()]
            scores = list(indicator_scores.values())

            # 创建雷达图
            fig = go.Figure()

            # 添加当前方案的数据
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=indicator_names,
                fill='toself',
                name='当前方案',
                line_color=self.colors['primary'],
                fillcolor=f'rgba(31, 119, 180, 0.3)',
                marker=dict(size=8)
            ))

            # 添加理想方案（全1）
            fig.add_trace(go.Scatterpolar(
                r=[1.0] * len(indicator_names),
                theta=indicator_names,
                fill='none',
                name='理想方案',
                line_color=self.colors['success'],
                line=dict(dash='dash'),
                marker=dict(size=6)
            ))

            # 设置布局
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1],
                        tick0=0,
                        dtick=0.2,
                        gridcolor='lightgray'
                    ),
                    angularaxis=dict(
                        gridcolor='lightgray',
                        tickfont=dict(size=12)
                    ),
                    bgcolor='rgba(240, 240, 240, 0.1)'
                ),
                showlegend=True,
                title=dict(
                    text=f"{title}<br><sub>{scenario_type}</sub>",
                    x=0.5,
                    xanchor='center',
                    font=dict(size=16)
                ),
                font=dict(family="Microsoft YaHei, sans-serif"),
                width=600,
                height=500,
                margin=dict(l=50, r=50, t=80, b=50)
            )

            return fig

        except Exception as e:
            logger.error(f"雷达图生成失败: {e}")
            # 返回一个空的图表
            fig = go.Figure()
            fig.add_annotation(text="图表生成失败", xref="paper", yref="paper", x=0.5, y=0.5)
            return fig

    def create_indicator_comparison_chart(
        self,
        indicator_scores: Dict[str, float],
        scenario_type: str,
        title: str = "各指标得分对比"
    ) -> go.Figure:
        """
        创建指标对比柱状图

        Args:
            indicator_scores: 指标得分字典
            scenario_type: 场景类型
            title: 图表标题

        Returns:
            Plotly柱状图对象
        """
        try:
            # 准备数据
            df = pd.DataFrame([
                {
                    '指标': self.chinese_indicator_names.get(ind, ind),
                    '得分': score,
                    '指标英文名': ind
                }
                for ind, score in indicator_scores.items()
            ])

            # 根据得分设置颜色
            colors = []
            for score in df['得分']:
                if score >= 0.8:
                    colors.append(self.colors['success'])
                elif score >= 0.6:
                    colors.append(self.colors['info'])
                elif score >= 0.4:
                    colors.append(self.colors['warning'])
                else:
                    colors.append(self.colors['light'])

            # 创建柱状图
            fig = go.Figure(data=[
                go.Bar(
                    x=df['指标'],
                    y=df['得分'],
                    text=df['得分'].apply(lambda x: f'{x:.3f}'),
                    textposition='auto',
                    marker_color=colors,
                    textfont=dict(size=12),
                    marker_line_color='rgb(0,0,0)',
                    marker_line_width=0.5
                )
            ])

            # 添加参考线
            fig.add_hline(y=0.8, line_dash="dash", line_color="green",
                         annotation_text="优秀线", annotation_position="top right")
            fig.add_hline(y=0.6, line_dash="dash", line_color="orange",
                         annotation_text="良好线", annotation_position="top right")

            # 设置布局
            fig.update_layout(
                title=dict(
                    text=f"{title}<br><sub>{scenario_type}</sub>",
                    x=0.5,
                    xanchor='center',
                    font=dict(size=16)
                ),
                xaxis_title="评估指标",
                yaxis_title="得分",
                yaxis=dict(range=[0, 1.1], tick0=0, dtick=0.2),
                font=dict(family="Microsoft YaHei, sans-serif", size=12),
                width=700,
                height=500,
                margin=dict(l=50, r=50, t=80, b=50),
                showlegend=False
            )

            return fig

        except Exception as e:
            logger.error(f"柱状图生成失败: {e}")
            # 返回一个空的图表
            fig = go.Figure()
            fig.add_annotation(text="图表生成失败", xref="paper", yref="paper", x=0.5, y=0.5)
            return fig

    def create_overall_score_gauge(
        self,
        overall_score: float,
        performance_level: str,
        title: str = "总体效能得分"
    ) -> go.Figure:
        """
        创建总体得分仪表盘

        Args:
            overall_score: 总体得分
            performance_level: 性能等级
            title: 图表标题

        Returns:
            Plotly仪表盘对象
        """
        try:
            # 创建仪表盘
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = overall_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f"{title}<br><span style='font-size:0.8em'>{performance_level}</span>"},
                delta = {'reference': 0.6, 'increasing': {'color': self.colors['success']}},
                gauge = {
                    'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': self.colors['primary']},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 0.4], 'color': self.colors['light']},
                        {'range': [0.4, 0.6], 'color': self.colors['warning']},
                        {'range': [0.6, 0.8], 'color': self.colors['info']},
                        {'range': [0.8, 1.0], 'color': self.colors['success']}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.8
                    }
                }
            ))

            # 设置布局
            fig.update_layout(
                font=dict(family="Microsoft YaHei, sans-serif", size=14),
                width=500,
                height=400,
                margin=dict(l=20, r=20, t=80, b=20)
            )

            return fig

        except Exception as e:
            logger.error(f"仪表盘生成失败: {e}")
            # 返回一个空的图表
            fig = go.Figure()
            fig.add_annotation(text="图表生成失败", xref="paper", yref="paper", x=0.5, y=0.5)
            return fig

    def create_comparison_table(
        self,
        indicator_scores: Dict[str, float],
        performance_level: str,
        ranking: int,
        scenario_type: str
    ) -> pd.DataFrame:
        """
        创建对比表格

        Args:
            indicator_scores: 指标得分字典
            performance_level: 性能等级
            ranking: 排名
            scenario_type: 场景类型

        Returns:
            表格DataFrame
        """
        try:
            # 准备表格数据
            table_data = []

            # 添加总体信息
            table_data.append({
                '项目': '总体得分',
                '数值': f"{indicator_scores.get('overall_score', 0):.3f}",
                '等级': performance_level,
                '排名': f"{ranking}"
            })

            # 添加各指标得分
            for ind, score in indicator_scores.items():
                level = self._get_score_level(score)
                table_data.append({
                    '项目': self.chinese_indicator_names.get(ind, ind),
                    '数值': f"{score:.3f}",
                    '等级': level,
                    '排名': '-'
                })

            # 创建DataFrame
            df = pd.DataFrame(table_data)
            df.index = range(1, len(df) + 1)
            df.index.name = '序号'

            return df

        except Exception as e:
            logger.error(f"表格生成失败: {e}")
            # 返回一个空的表格
            return pd.DataFrame({'错误': ['表格生成失败']})

    def _get_score_level(self, score: float) -> str:
        """根据得分获取等级"""
        if score >= 0.8:
            return "优秀"
        elif score >= 0.6:
            return "良好"
        elif score >= 0.4:
            return "一般"
        else:
            return "较差"

    def create_suggestions_chart(
        self,
        suggestions: List[str],
        title: str = "改进建议"
    ) -> go.Figure:
        """
        创建建议图表 - 使用卡片式设计

        Args:
            suggestions: 建议列表
            title: 图表标题

        Returns:
            Plotly图表对象
        """
        try:
            # 创建改进的建议图表，使用表格布局
            fig = go.Figure()

            # 计算卡片位置
            card_height = 0.18
            card_spacing = 0.22

            # 根据建议数量调整图表高度
            fig_height = max(250, len(suggestions) * 100 + 100)

            # 添加建议卡片
            for i, suggestion in enumerate(suggestions, 1):
                # 为每个建议创建一个卡片背景
                card_y = 1 - (i-1) * card_spacing

                # 添加卡片背景
                fig.add_shape(
                    type="rect",
                    x0=0.05, y0=card_y - card_height/2,
                    x1=0.95, y1=card_y + card_height/2,
                    fillcolor="rgba(240, 240, 240, 0.8)",
                    line=dict(color="rgba(100, 100, 100, 0.5)", width=1),
                    layer="below"
                )

                # 添加编号图标
                fig.add_annotation(
                    x=0.12,
                    y=card_y,
                    xref="paper",
                    yref="paper",
                    text=f"<b>{i}</b>",
                    showarrow=False,
                    font=dict(size=16, color="white"),
                    bgcolor=self.colors['primary'],
                    bordercolor="white",
                    borderwidth=2,
                    width=30,
                    height=30
                )

                # 添加建议文本（支持自动换行和更好的布局）
                words = list(suggestion)
                max_chars_per_line = 20
                if len(words) > max_chars_per_line:  # 如果文本太长，拆分成多行
                    lines = []
                    for j in range(0, len(words), max_chars_per_line):
                        line = ''.join(words[j:j + max_chars_per_line])
                        lines.append(line)
                    text = '<br>'.join(lines)
                else:
                    text = suggestion

                fig.add_annotation(
                    x=0.5,
                    y=card_y,
                    xref="paper",
                    yref="paper",
                    text=f"<b>{text}</b>",
                    showarrow=False,
                    font=dict(size=13, family="Microsoft YaHei, sans-serif", color="#333333"),
                    align="center",
                    valign="middle"
                )

            # 设置布局
            fig.update_layout(
                title=dict(
                    text=f"<b>{title}</b>",
                    x=0.5,
                    xanchor='center',
                    font=dict(size=18, family="Microsoft YaHei, sans-serif", color="#2c3e50")
                ),
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 1]),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 1]),
                font=dict(family="Microsoft YaHei, sans-serif"),
                width=500,
                height=fig_height,
                margin=dict(l=30, r=30, t=60, b=30),
                showlegend=False,
                plot_bgcolor="rgba(255, 255, 255, 0.8)",
                paper_bgcolor="rgba(255, 255, 255, 0.8)"
            )

            return fig

        except Exception as e:
            logger.error(f"建议图表生成失败: {e}")
            # 返回一个空的图表
            fig = go.Figure()
            fig.add_annotation(text="图表生成失败", xref="paper", yref="paper", x=0.5, y=0.5)
            return fig

    def create_comprehensive_dashboard(
        self,
        topsis_result,
        scenario_type: str
    ) -> Tuple[List[go.Figure], pd.DataFrame]:
        """
        创建综合仪表板

        Args:
            topsis_result: TOPSIS评估结果
            scenario_type: 场景类型

        Returns:
            (图表列表, 表格DataFrame)
        """
        try:
            charts = []

            # 1. 总体得分仪表盘
            gauge_chart = self.create_overall_score_gauge(
                topsis_result.overall_score,
                topsis_result.performance_level,
                "总体效能得分"
            )
            charts.append(gauge_chart)

            # 2. 雷达图
            radar_chart = self.create_radar_chart(
                topsis_result.indicator_scores,
                scenario_type,
                "多维度评估结果"
            )
            charts.append(radar_chart)

            # 3. 指标对比柱状图
            bar_chart = self.create_indicator_comparison_chart(
                topsis_result.indicator_scores,
                scenario_type,
                "各指标得分对比"
            )
            charts.append(bar_chart)

            # 4. 建议图表
            if topsis_result.suggestions:
                suggestions_chart = self.create_suggestions_chart(
                    topsis_result.suggestions,
                    "改进建议"
                )
                charts.append(suggestions_chart)

            # 5. 详细表格
            table_df = self.create_comparison_table(
                topsis_result.indicator_scores,
                topsis_result.performance_level,
                topsis_result.ranking,
                scenario_type
            )

            return charts, table_df

        except Exception as e:
            logger.error(f"综合仪表板生成失败: {e}")
            # 返回空的结果
            empty_fig = go.Figure()
            empty_fig.add_annotation(text="仪表板生成失败", xref="paper", yref="paper", x=0.5, y=0.5)
            return [empty_fig], pd.DataFrame({'错误': ['仪表板生成失败']})


# 使用示例和测试函数
def test_visualization():
    """测试可视化功能"""
    generator = ChartGenerator()

    # 测试数据
    indicator_scores = {
        'overall_combat_power': 0.8,
        'technological_superiority': 0.7,
        'environmental_adaptability': 0.6,
        'mission_achievement': 0.9,
        'operational_efficiency': 0.5
    }

    # 测试雷达图
    print("=== 测试雷达图 ===")
    radar_fig = generator.create_radar_chart(indicator_scores, "chokepoint_blockade")
    print(f"雷达图创建成功: {type(radar_fig)}")

    # 测试柱状图
    print("\n=== 测试柱状图 ===")
    bar_fig = generator.create_indicator_comparison_chart(indicator_scores, "chokepoint_blockade")
    print(f"柱状图创建成功: {type(bar_fig)}")

    # 测试仪表盘
    print("\n=== 测试仪表盘 ===")
    gauge_fig = generator.create_overall_score_gauge(0.75, "良好", "总体效能得分")
    print(f"仪表盘创建成功: {type(gauge_fig)}")

    # 测试表格
    print("\n=== 测试表格 ===")
    table_df = generator.create_comparison_table(indicator_scores, "良好", 2, "chokepoint_blockade")
    print(f"表格创建成功:\n{table_df}")

    # 测试建议图表
    print("\n=== 测试建议图表 ===")
    suggestions = [
        "作战体系效能良好，可针对薄弱环节进行优化",
        "建议重点提升作战效率",
        "建议充分发挥优势领域的带动作用"
    ]
    suggestions_fig = generator.create_suggestions_chart(suggestions)
    print(f"建议图表创建成功: {type(suggestions_fig)}")

    # 测试综合仪表板
    print("\n=== 测试综合仪表板 ===")
    from utils.topsis import TopsisResult
    test_result = TopsisResult(
        overall_score=0.75,
        performance_level="良好",
        indicator_scores=indicator_scores,
        ranking=2,
        suggestions=suggestions,
        calculation_details={}
    )

    charts, table = generator.create_comprehensive_dashboard(test_result, "chokepoint_blockade")
    print(f"综合仪表板创建成功: {len(charts)}个图表, 表格形状: {table.shape}")


if __name__ == "__main__":
    test_visualization()