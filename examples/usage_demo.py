"""
作战体系效能评估系统使用示例
演示如何使用TOPSIS算法进行作战效能评估
"""

import sys
import os
import json
from typing import Dict, Any

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.topsis import CombatTopsis
from utils.validation import ParameterValidator
from utils.visualization import ChartGenerator


class CombatAssessmentDemo:
    """作战评估演示类"""

    def __init__(self):
        """初始化演示"""
        self.topsis = CombatTopsis()
        self.validator = ParameterValidator()
        self.chart_generator = ChartGenerator()

        # 加载演示数据
        with open('examples/demo_data.json', 'r', encoding='utf-8') as f:
            self.demo_data = json.load(f)

    def demonstrate_scenario_assessment(self, scenario_key: str):
        """
        演示单个场景的评估过程

        Args:
            scenario_key: 场景键名
        """
        print(f"\n{'='*60}")
        print(f"演示场景: {self.demo_data['demo_scenarios'][scenario_key]['name']}")
        print(f"{'='*60}")

        scenario_data = self.demo_data['demo_scenarios'][scenario_key]

        # 1. 显示输入参数
        print("\n📋 输入参数:")
        print("-" * 40)
        for param_name, value in scenario_data['parameters'].items():
            param_info = self.validator.get_parameter_info(scenario_key)[param_name]
            print(f"  {param_info['description']}: {value}")

        # 2. 参数验证
        print("\n🔍 参数验证:")
        print("-" * 40)
        all_valid, results = self.validator.validate_all_parameters(
            scenario_data['parameters'], scenario_key
        )

        if all_valid:
            print("✅ 所有参数验证通过")
        else:
            print("❌ 参数验证失败:")
            for result in results:
                if not result.is_valid:
                    print(f"  - {result.error_message}")

        # 3. 执行TOPSIS评估
        print("\n🎯 执行TOPSIS评估:")
        print("-" * 40)

        # 映射参数到指标
        indicator_scores = self.topsis.normalize_parameters_to_indicators(
            scenario_data['parameters'], scenario_key
        )

        print("指标得分:")
        for indicator, score in indicator_scores.items():
            print(f"  {self.chart_generator.chinese_indicator_names.get(indicator, indicator)}: {score:.3f}")

        # 计算TOPSIS结果
        result = self.topsis.calculate_topsis(indicator_scores, scenario_key)

        print(f"\n评估结果:")
        print(f"  总体得分: {result.overall_score:.3f}")
        print(f"  性能等级: {result.performance_level}")
        print(f"  相对排名: 第{result.ranking}名")

        # 4. 显示改进建议
        print("\n💡 改进建议:")
        print("-" * 40)
        for i, suggestion in enumerate(result.suggestions, 1):
            print(f"  {i}. {suggestion}")

        # 5. 生成图表（保存为HTML文件）
        print("\n📊 生成可视化图表:")
        print("-" * 40)

        charts, table_df = self.chart_generator.create_comprehensive_dashboard(
            result, scenario_key
        )

        # 保存图表
        chart_files = []
        for i, chart in enumerate(charts):
            filename = f"examples/{scenario_key}_chart_{i+1}.html"
            chart.write_html(filename)
            chart_files.append(filename)
            print(f"  图表{i+1}已保存: {filename}")

        # 保存表格
        table_filename = f"examples/{scenario_key}_results.csv"
        table_df.to_csv(table_filename, encoding='utf-8-sig')
        print(f"  结果表格已保存: {table_filename}")

        # 6. 与预期结果对比
        expected = scenario_data['expected_results']
        print("\n📈 结果对比:")
        print("-" * 40)
        print(f"预期总体得分: {expected['overall_score']:.3f}")
        print(f"实际总体得分: {result.overall_score:.3f}")
        print(f"得分差异: {abs(result.overall_score - expected['overall_score']):.3f}")
        print(f"预期性能等级: {expected['performance_level']}")
        print(f"实际性能等级: {result.performance_level}")

        score_diff = abs(result.overall_score - expected['overall_score'])
        if score_diff < 0.05:
            print("✅ 评估结果与预期高度一致")
        elif score_diff < 0.1:
            print("⚠️ 评估结果与预期基本一致")
        else:
            print("❌ 评估结果与预期差异较大")

        return result

    def demonstrate_all_scenarios(self):
        """演示所有场景的评估"""
        print("🎯 作战体系效能评估系统 - 完整演示")
        print("=" * 80)

        results = {}

        for scenario_key in self.demo_data['demo_scenarios'].keys():
            try:
                result = self.demonstrate_scenario_assessment(scenario_key)
                results[scenario_key] = result
            except Exception as e:
                print(f"❌ 场景 {scenario_key} 评估失败: {e}")
                results[scenario_key] = None

        # 场景对比
        print("\n\n🏆 场景对比分析")
        print("=" * 80)

        valid_results = {k: v for k, v in results.items() if v is not None}

        if valid_results:
            print("各场景评估结果对比:")
            print("-" * 60)
            print(f"{'场景':<20} {'总体得分':<10} {'性能等级':<10} {'排名':<10}")
            print("-" * 60)

            for scenario_key, result in valid_results.items():
                scenario_name = self.demo_data['demo_scenarios'][scenario_key]['name']
                print(f"{scenario_name:<20} {result.overall_score:<10.3f} {result.performance_level:<10} {result.ranking:<10}")

            # 找出最佳场景
            best_scenario = max(valid_results.items(), key=lambda x: x[1].overall_score)
            best_name = self.demo_data['demo_scenarios'][best_scenario[0]]['name']
            print(f"\n🏆 最佳效能场景: {best_name} (得分: {best_scenario[1].overall_score:.3f})")

        return results

    def demonstrate_parameter_sensitivity(self):
        """演示参数敏感性分析"""
        print("\n🔍 参数敏感性分析")
        print("=" * 80)

        # 选择要峡封控场景进行敏感性分析
        scenario_key = "chokepoint_blockade"
        base_params = self.demo_data['demo_scenarios'][scenario_key]['parameters'].copy()

        print(f"基于场景: {self.demo_data['demo_scenarios'][scenario_key]['name']}")
        print("-" * 60)

        # 选择关键参数进行分析
        key_params = ['force_size', 'weapon_effectiveness', 'sensor_capability']

        for param_name in key_params:
            print(f"\n📊 参数: {param_name}")

            # 获取参数范围
            param_info = self.validator.get_parameter_info(scenario_key)[param_name]
            min_val, max_val = param_info['min_value'], param_info['max_value']
            base_val = base_params[param_name]

            # 创建变化范围
            variations = [-0.2, -0.1, 0, 0.1, 0.2]  # ±20%变化

            print(f"基础值: {base_val}, 变化范围: {min_val} - {max_val}")
            print("变化率 -> 总体得分")
            print("-" * 40)

            for variation in variations:
                # 修改参数值
                test_params = base_params.copy()
                new_value = base_val * (1 + variation)

                # 确保在有效范围内
                new_value = max(min_val, min(max_val, new_value))
                test_params[param_name] = new_value

                # 计算得分
                indicator_scores = self.topsis.normalize_parameters_to_indicators(
                    test_params, scenario_key
                )
                result = self.topsis.calculate_topsis(indicator_scores, scenario_key)

                print(f"{variation:+6.1%} -> {result.overall_score:.3f}")

        print("\n💡 敏感性分析结论:")
        print("- 参数变化对总体得分的影响程度不同")
        print("- 关键参数的微小变化可能导致得分显著变化")
        print("- 在实际应用中应重点关注高敏感性参数")

    def run_complete_demo(self):
        """运行完整演示"""
        print("🚀 启动作战体系效能评估系统演示")
        print("=" * 80)

        try:
            # 1. 演示所有场景
            results = self.demonstrate_all_scenarios()

            # 2. 演示参数敏感性
            self.demonstrate_parameter_sensitivity()

            # 3. 生成总结报告
            print("\n📋 演示总结报告")
            print("=" * 80)
            print("✅ 成功完成的演示:")
            print("  - 四种典型作战场景的效能评估")
            print("  - 参数验证和错误处理")
            print("  - TOPSIS算法计算过程")
            print("  - 可视化图表生成")
            print("  - 参数敏感性分析")
            print("  - 结果对比分析")

            print("\n📁 生成的文件:")
            print("  - 场景评估图表 (HTML格式)")
            print("  - 评估结果表格 (CSV格式)")
            print("  - 演示数据文件 (JSON格式)")

            print("\n🎯 系统特点:")
            print("  - 支持多场景作战效能评估")
            print("  - 基于TOPSIS多准则决策方法")
            print("  - 全面的参数验证机制")
            print("  - 丰富的可视化展示")
            print("  - 灵活的配置管理")

            print(f"\n🏁 演示完成！感谢使用作战体系效能评估系统。")

        except Exception as e:
            print(f"❌ 演示过程中发生错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    demo = CombatAssessmentDemo()
    demo.run_complete_demo()


if __name__ == "__main__":
    main()