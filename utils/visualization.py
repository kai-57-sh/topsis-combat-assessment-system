"""
可视化组件模块 - 简化版本
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

    def create_suggestions_chart(
        self,
        suggestions: List[str],
        title: str = "改进建议"
    ) -> go.Figure:
        """
        创建建议图表 - 简化版本

        Args:
            suggestions: 建议列表
            title: 图表标题

        Returns:
            Plotly图表对象
        """
        try:
            # 创建简单的建议图表
            fig = go.Figure()

            # 添加建议文本
            for i, suggestion in enumerate(suggestions, 1):
                fig.add_annotation(
                    x=0.5,
                    y=1 - (i-1) * 0.15,
                    xref="paper",
                    yref="paper",
                    text=f"{i}. {suggestion}",
                    showarrow=False,
                    font=dict(size=12, family="Microsoft YaHei, sans-serif"),
                    bgcolor="rgba(240, 240, 240, 0.8)",
                    bordercolor="gray",
                    borderwidth=1,
                    borderpad=8
                )

            # 设置布局
            fig.update_layout(
                title=dict(
                    text=title,
                    x=0.5,
                    xanchor='center',
                    font=dict(size=16)
                ),
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                font=dict(family="Microsoft YaHei, sans-serif"),
                width=600,
                height=250,
                margin=dict(l=50, r=50, t=80, b=50),
                showlegend=False
            )

            return fig

        except Exception as e:
            logger.error(f"建议图表生成失败: {e}")
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
                '数值': f"{performance_level}",
                '等级': f"{ranking}",
                '得分': '-'
            })

            # 添加各指标得分
            for ind, score in indicator_scores.items():
                level = self._get_score_level(score)
                table_data.append({
                    '项目': self.chinese_indicator_names.get(ind, ind),
                    '数值': f"{score:.3f}",
                    '等级': level,
                    '得分': score
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