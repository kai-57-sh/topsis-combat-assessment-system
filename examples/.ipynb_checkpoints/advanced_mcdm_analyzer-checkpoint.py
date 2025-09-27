# advanced_mcdm_analyzer.py - 集成pyDecision的高级分析器
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional
import logging

class CombatSystemMCDMAnalyzer:
    """作战体系多属性决策分析器"""
    
    def __init__(self, scenario_name: str):
        self.scenario_name = scenario_name
        self.logger = logging.getLogger(__name__)
        self.results = {}
        
    def load_scenario_data(self, 
                          alternatives: List[str],
                          criteria: List[str],
                          matrix: np.ndarray,
                          weights: np.ndarray,
                          criteria_types: List[str]) -> None:
        """加载场景数据
        
        Args:
            alternatives: 备选方案名称列表
            criteria: 评价指标名称列表  
            matrix: 决策矩阵
            weights: 权重向量
            criteria_types: 指标类型，'benefit'或'cost'
        """
        self.alternatives = alternatives
        self.criteria = criteria
        self.matrix = np.array(matrix, dtype=float)
        self.weights = np.array(weights, dtype=float)
        self.criteria_types = criteria_types
        
        self.logger.info(f"已加载{self.scenario_name}场景数据")
        self.logger.info(f"方案数: {len(alternatives)}, 指标数: {len(criteria)}")
        
    def run_topsis_analysis(self) -> Dict:
        """执行TOPSIS分析"""
        try:
            from pyDecision.algorithm import topsis
            
            # 转换指标类型格式
            criterion_type = ['max' if ct == 'benefit' else 'min' 
                            for ct in self.criteria_types]
            
            # 执行TOPSIS
            result = topsis.topsis(
                dataset=self.matrix,
                weights=self.weights,
                criterion_type=criterion_type,
                graph=False
            )
            
            # 处理结果
            topsis_scores = result[:, 1]  # 相对贴近度
            rankings = np.argsort(-topsis_scores) + 1  # 排序（1为最优）
            
            self.results['topsis'] = {
                'scores': topsis_scores,
                'rankings': rankings,
                'best_alternative': self.alternatives[np.argmax(topsis_scores)]
            }
            
            self.logger.info("TOPSIS分析完成")
            return self.results['topsis']
            
        except ImportError:
            self.logger.error("pyDecision库未安装，使用内置TOPSIS实现")
            return self._builtin_topsis()
            
    def _builtin_topsis(self) -> Dict:
        """内置TOPSIS实现（备用方案）"""
        # 这里可以调用上面的Topsis类
        criteria_bool = [ct == 'benefit' for ct in self.criteria_types]
        topsis = Topsis(self.matrix, self.weights, criteria_bool)
        topsis.calc()
        
        return {
            'scores': topsis.best_similarity,
            'rankings': topsis.rank_to_best_similarity() + 1,
            'best_alternative': self.alternatives[topsis.rank_to_best_similarity()[0]]
        }
        
    def sensitivity_analysis(self, weight_variations: List[float] = None) -> Dict:
        """敏感性分析"""
        if weight_variations is None:
            weight_variations = [0.8, 0.9, 1.0, 1.1, 1.2]
            
        sensitivity_results = {}
        base_weights = self.weights.copy()
        
        for i, criterion in enumerate(self.criteria):
            variations = []
            for factor in weight_variations:
                # 修改权重
                modified_weights = base_weights.copy()
                modified_weights[i] *= factor
                # 重新归一化
                modified_weights = modified_weights / np.sum(modified_weights)
                
                # 临时保存原权重
                temp_weights = self.weights
                self.weights = modified_weights
                
                # 重新计算TOPSIS
                result = self.run_topsis_analysis()
                variations.append(result['rankings'].copy())
                
                # 恢复原权重
                self.weights = temp_weights
                
            sensitivity_results[criterion] = {
                'weight_factors': weight_variations,
                'ranking_variations': variations
            }
            
        return sensitivity_results
        
    def generate_radar_chart(self, normalized: bool = True) -> None:
        """生成雷达图"""
        if normalized:
            # 标准化数据到0-1范围
            data = (self.matrix - self.matrix.min(axis=0)) / (
                self.matrix.max(axis=0) - self.matrix.min(axis=0)
            )
        else:
            data = self.matrix
            
        angles = np.linspace(0, 2*np.pi, len(self.criteria), endpoint=False).tolist()
        angles += angles[:1]  # 闭合图形
        
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(self.alternatives)))
        
        for i, (alt, color) in enumerate(zip(self.alternatives, colors)):
            values = data[i].tolist()
            values += values[:1]  # 闭合图形
            
            ax.plot(angles, values, 'o-', linewidth=2, label=alt, color=color)
            ax.fill(angles, values, alpha=0.1, color=color)
            
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.criteria)
        ax.set_ylim(0, 1 if normalized else data.max())
        ax.set_title(f'{self.scenario_name} - 作战方案对比雷达图', size=14, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
        
        plt.tight_layout()
        plt.show()
        
    def export_results(self, filename: str) -> None:
        """导出结果到Excel"""
        with pd.ExcelWriter(f'{filename}.xlsx', engine='openpyxl') as writer:
            # 决策矩阵
            df_matrix = pd.DataFrame(
                self.matrix, 
                index=self.alternatives,
                columns=self.criteria
            )
            df_matrix.to_excel(writer, sheet_name='决策矩阵')
            
            # TOPSIS结果
            if 'topsis' in self.results:
                df_topsis = pd.DataFrame({
                    '方案': self.alternatives,
                    '相对贴近度': self.results['topsis']['scores'],
                    '排名': self.results['topsis']['rankings']
                })
                df_topsis = df_topsis.sort_values('排名')
                df_topsis.to_excel(writer, sheet_name='TOPSIS结果', index=False)
                
            self.logger.info(f"结果已导出到 {filename}.xlsx")

# 使用示例
def demo_chokepoint_blockade():
    """要峡封控场景示例"""
    analyzer = CombatSystemMCDMAnalyzer("要峡封控")
    
    # 示例数据
    alternatives = ['传统布雷体系', '无人化智能体系', '混合协同体系']
    criteria = ['封锁成功率', '体系隐蔽性', '部署时间', '装备成本']
    
    # 决策矩阵 (虚拟数据)
    matrix = [
        [85, 6, 24, 800],   # 传统体系
        [92, 9, 12, 1200],  # 无人化体系  
        [90, 8, 18, 1000]   # 混合体系
    ]
    
    weights = [0.4, 0.3, 0.2, 0.1]
    criteria_types = ['benefit', 'benefit', 'cost', 'cost']
    
    # 加载数据并分析
    analyzer.load_scenario_data(alternatives, criteria, matrix, weights, criteria_types)
    
    # 执行TOPSIS分析
    results = analyzer.run_topsis_analysis()
    print(f"最优方案: {results['best_alternative']}")
    print(f"相对贴近度: {results['scores']}")
    
    # 生成可视化
    analyzer.generate_radar_chart()
    
    # 敏感性分析
    sensitivity = analyzer.sensitivity_analysis()
    
    # 导出结果
    analyzer.export_results('要峡封控分析结果')

if __name__ == "__main__":
    demo_chokepoint_blockade()