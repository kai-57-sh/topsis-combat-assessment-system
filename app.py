"""
作战体系效能评估系统 - Streamlit主应用 - 简化版本
基于TOPSIS算法的多场景作战效能评估工具
"""

import streamlit as st
import yaml
import sys
import os
from typing import Dict, Any, Optional
import logging

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.topsis import CombatTopsis, TopsisResult
from utils.validation import ParameterValidator, ValidationResult
from utils.visualization import ChartGenerator

# 设置页面配置
st.set_page_config(
    page_title="作战体系效能评估系统",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CombatAssessmentApp:
    """作战评估应用主类"""

    def __init__(self):
        """初始化应用"""
        self.topsis = CombatTopsis()
        self.validator = ParameterValidator()
        self.chart_generator = ChartGenerator()
        self._init_session_state()

    def _init_session_state(self):
        """初始化会话状态"""
        if 'current_scenario' not in st.session_state:
            st.session_state.current_scenario = None
        if 'parameters' not in st.session_state:
            st.session_state.parameters = {}
        if 'assessment_result' not in st.session_state:
            st.session_state.assessment_result = None
        if 'validation_results' not in st.session_state:
            st.session_state.validation_results = {}

    def load_scenarios_config(self) -> Dict[str, Any]:
        """加载场景配置"""
        try:
            with open("config/scenarios.yaml", 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            st.error(f"加载场景配置失败: {e}")
            return {}

    def get_scenario_info(self) -> Dict[str, str]:
        """获取场景信息"""
        scenarios = {
            'chokepoint_blockade': {
                'name': '要峡封控作战',
                'description': '评估要道封锁作战体系的效能'
            },
            'landing_zone_clearance': {
                'name': '登陆场通道清扫',
                'description': '评估登陆场清扫作战体系的效能'
            },
            'mine_countermeasures': {
                'name': '水雷清排作战',
                'description': '评估水雷清排作战体系的效能'
            },
            'underwater_surveillance': {
                'name': '近岸水下监视',
                'description': '评估近岸水下监视作战体系的效能'
            }
        }
        return scenarios

    def render_scenario_selection(self):
        """渲染场景选择界面"""
        st.title("🎯 作战体系效能评估系统")

        st.markdown("---")
        st.subheader("1. 选择评估场景")

        scenario_info = self.get_scenario_info()

        # 使用radio按钮选择场景
        selected_scenario = st.radio(
            "请选择作战场景:",
            options=list(scenario_info.keys()),
            format_func=lambda x: scenario_info[x]['name'],
            index=0,
            key="scenario_selection"
        )

        # 显示场景描述
        if selected_scenario:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**场景名称:** {scenario_info[selected_scenario]['name']}")
            with col2:
                st.markdown(f"**场景描述:** {scenario_info[selected_scenario]['description']}")

        # 如果场景改变，初始化该场景的默认参数
        if st.session_state.current_scenario != selected_scenario:
            st.session_state.current_scenario = selected_scenario
            st.session_state.assessment_result = None
            st.session_state.validation_results = {}

            # 初始化该场景的所有参数为默认值
            param_info = self.validator.get_parameter_info(selected_scenario)
            st.session_state.parameters = {}
            for param_name, param_data in param_info.items():
                st.session_state.parameters[param_name] = param_data['default_value']

        return selected_scenario

    def render_parameter_input(self, scenario_type: str):
        """渲染参数输入界面"""
        st.subheader("2. 输入评估参数")
        st.markdown("---")

        # 获取参数信息
        param_info = self.validator.get_parameter_info(scenario_type)

        # 按类型分组显示参数
        param_types = {
            'force': '兵力配置',
            'equipment': '装备性能',
            'environment': '环境条件',
            'mission': '任务需求'
        }

        for param_type, type_name in param_types.items():
            # 筛选当前类型的参数
            type_params = {k: v for k, v in param_info.items() if v['type'] == param_type}

            if type_params:
                st.markdown(f"#### {type_name}")

                # 使用列布局，每行显示2个参数
                cols = st.columns(2)
                for i, (param_name, param_data) in enumerate(type_params.items()):
                    col = cols[i % 2]

                    with col:
                        # 获取当前值或使用默认值
                        current_value = st.session_state.parameters.get(param_name, param_data['default_value'])

                        # 创建输入控件
                        # 确保所有数值类型一致
                        min_val = float(param_data['min_value'])
                        max_val = float(param_data['max_value'])
                        current_val = float(current_value)
                        default_val = float(param_data['default_value'])

                        # 根据参数范围智能调整步长
                        if max_val - min_val <= 1.0:
                            step_val = 0.01
                        elif max_val - min_val <= 10.0:
                            step_val = 0.1
                        else:
                            step_val = (max_val - min_val) / 100

                        input_widget = st.number_input(
                            label=param_data['description'],
                            min_value=min_val,
                            max_value=max_val,
                            value=current_val,
                            step=step_val,
                            key=f"{scenario_type}_{param_name}",
                            help=f"范围: {param_data['min_value']} - {param_data['max_value']}"
                        )

                        # 更新参数值
                        st.session_state.parameters[param_name] = input_widget

                        # 显示验证结果
                        if param_name in st.session_state.validation_results:
                            validation_result = st.session_state.validation_results[param_name]
                            if not validation_result.is_valid:
                                st.error(validation_result.error_message)
                            elif validation_result.warning_message:
                                st.warning(validation_result.warning_message)

    def validate_parameters(self, scenario_type: str) -> bool:
        """验证所有参数"""
        all_valid = True
        st.session_state.validation_results = {}

        # 确保所有必需参数都在session_state中
        param_info = self.validator.get_parameter_info(scenario_type)
        for param_name, param_data in param_info.items():
            if param_name not in st.session_state.parameters:
                # 使用默认值初始化缺失的参数
                st.session_state.parameters[param_name] = param_data['default_value']

        # 验证所有参数
        for param_name, value in st.session_state.parameters.items():
            result = self.validator.validate_parameter(param_name, value, scenario_type)
            st.session_state.validation_results[param_name] = result

            if not result.is_valid:
                all_valid = False

        return all_valid

    def perform_assessment(self, scenario_type: str):
        """执行评估"""
        try:
            # 显示加载状态
            with st.spinner("正在执行评估计算..."):
                # 参数验证
                all_valid = self.validate_parameters(scenario_type)

                if not all_valid:
                    st.error("❌ 参数验证失败，请检查以下错误：")

                    # 显示详细的验证错误信息
                    if hasattr(st.session_state, 'validation_results'):
                        for param_name, result in st.session_state.validation_results.items():
                            if not result.is_valid:
                                st.error(f"**{param_name}**: {result.error_message}")

                    # 检查是否还有未显示的必需参数缺失
                    param_info = self.validator.get_parameter_info(scenario_type)
                    missing_params = []
                    for param_name in param_info.keys():
                        if param_name not in st.session_state.parameters:
                            missing_params.append(param_name)

                    if missing_params:
                        st.error(f"**缺少必需参数**: {', '.join(missing_params)}")

                    return

                # 执行TOPSIS计算
                indicator_scores = self.topsis.normalize_parameters_to_indicators(
                    st.session_state.parameters,
                    scenario_type
                )

                result = self.topsis.calculate_topsis(indicator_scores, scenario_type)

                # 保存结果
                st.session_state.assessment_result = result

                # 显示成功消息
                st.success("✅ 评估完成！")

        except Exception as e:
            logger.error(f"评估失败: {e}")
            st.error(f"评估过程中发生错误: {str(e)}")

    def render_results(self, scenario_type: str):
        """渲染评估结果"""
        if not st.session_state.assessment_result:
            return

        result = st.session_state.assessment_result

        st.subheader("3. 评估结果")
        st.markdown("---")

        # 总体得分展示
        st.markdown("### 📊 总体评估")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.metric(
                label="总体得分",
                value=f"{result.overall_score:.3f}",
                delta=None
            )

        with col2:
            st.metric(
                label="性能等级",
                value=result.performance_level,
                delta=None
            )

        with col3:
            st.metric(
                label="相对排名",
                value=f"第{result.ranking}名",
                delta=None
            )

        # 生成图表
        charts, table_df = self.chart_generator.create_comprehensive_dashboard(result, scenario_type)

        # 图表展示区域
        st.markdown("### 📈 详细分析")
        st.markdown("---")

        # 第一行：总体得分和雷达图
        row1_cols = st.columns([1, 1])
        with row1_cols[0]:
            st.plotly_chart(charts[0], use_container_width=True, key="gauge_chart")
        with row1_cols[1]:
            st.plotly_chart(charts[1], use_container_width=True, key="radar_chart")

        # 第二行：柱状图和建议
        if len(charts) > 2:
            row2_cols = st.columns([2, 1])
            with row2_cols[0]:
                st.plotly_chart(charts[2], use_container_width=True, key="bar_chart")
            if len(charts) > 3:
                with row2_cols[1]:
                    st.plotly_chart(charts[3], use_container_width=True, key="suggestions_chart")

        # 详细数据表格
        st.markdown("### 📋 详细数据")
        st.markdown("---")
        st.dataframe(table_df, use_container_width=True)

        # 导出功能
        st.markdown("### 💾 导出结果")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("导出为CSV", type="secondary"):
                csv_data = table_df.to_csv(index=True, encoding='utf-8-sig')
                st.download_button(
                    label="下载CSV文件",
                    data=csv_data,
                    file_name=f"作战体系效能评估结果_{scenario_type}.csv",
                    mime='text/csv'
                )

        with col2:
            if st.button("重置评估", type="secondary"):
                st.session_state.parameters = {}
                st.session_state.assessment_result = None
                st.session_state.validation_results = {}
                st.rerun()

    def render_sidebar(self):
        """渲染侧边栏"""
        st.sidebar.title("⚙️ 系统设置")

        # 应用说明
        st.sidebar.markdown("### 📖 使用说明")
        st.sidebar.markdown("""
        1. **选择场景**: 选择要评估的作战场景
        2. **输入参数**: 根据场景输入相应的参数
        3. **执行评估**: 点击"开始评估"按钮
        4. **查看结果**: 查看详细的评估结果
        """)

        st.sidebar.markdown("---")

        # 场景说明
        st.sidebar.markdown("### 🎯 场景说明")
        scenario_info = self.get_scenario_info()
        for key, info in scenario_info.items():
            with st.sidebar.expander(info['name']):
                st.markdown(f"**描述**: {info['description']}")

        st.sidebar.markdown("---")

        # 算法说明
        st.sidebar.markdown("### 🔬 评估算法")
        st.sidebar.markdown("""
        本系统使用**TOPSIS算法**进行评估：
        - **T**echnique for **O**rder of **P**reference by **S**imilarity to **I**deal **S**olution
        - 通过计算与理想解的相对贴近度进行排序
        - 考虑5个核心评估指标
        """)

        st.sidebar.markdown("---")

        # 版本信息
        st.sidebar.markdown("### 📋 版本信息")
        st.sidebar.markdown("**版本**: v1.0.0")
        st.sidebar.markdown("**更新**: 2024年")

    def run(self):
        """运行应用"""
        # 渲染侧边栏
        self.render_sidebar()

        # 主界面
        selected_scenario = self.render_scenario_selection()

        if selected_scenario:
            # 渲染参数输入
            self.render_parameter_input(selected_scenario)

            # 评估按钮
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 开始评估", type="primary", use_container_width=True):
                    self.perform_assessment(selected_scenario)

            # 显示结果
            if st.session_state.assessment_result:
                self.render_results(selected_scenario)


def main():
    """主函数"""
    app = CombatAssessmentApp()
    app.run()


if __name__ == "__main__":
    main()