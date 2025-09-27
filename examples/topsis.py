# topsis.py - 完整的TOPSIS实现
import numpy as np

class Topsis:
    def __init__(self, evaluation_matrix, weights, criteria_types):
        """
        初始化TOPSIS计算器
        
        Args:
            evaluation_matrix: 决策矩阵 (m×n)，m个方案，n个指标
            weights: 权重向量 (n,)
            criteria_types: 指标类型数组，True为效益型，False为成本型
        """
        self.evaluation_matrix = np.array(evaluation_matrix, dtype=float)
        self.weights = np.array(weights, dtype=float)
        self.criteria_types = np.array(criteria_types)
        
        # 结果存储
        self.normalized_matrix = None
        self.weighted_normalized = None
        self.best_alternative = None
        self.worst_alternative = None
        self.best_distance = None
        self.worst_distance = None
        self.best_similarity = None
        self.worst_similarity = None
        
    def calc(self):
        """执行完整的TOPSIS计算流程"""
        print("Step 1: 原始决策矩阵")
        print(self.evaluation_matrix)
        
        # 步骤1：数据标准化
        self._normalize_matrix()
        print("\nStep 2: 标准化矩阵")
        print(self.normalized_matrix)
        
        # 步骤2：计算加权标准化矩阵
        self._calculate_weighted_normalized()
        print("\nStep 3: 加权标准化矩阵")
        print(self.weighted_normalized)
        
        # 步骤3：确定正负理想解
        self._find_ideal_solutions()
        print(f"\nStep 4: 正理想解: {self.best_alternative}")
        print(f"负理想解: {self.worst_alternative}")
        
        # 步骤4：计算距离
        self._calculate_distances()
        print(f"\nStep 5: 到正理想解距离: {self.best_distance}")
        print(f"到负理想解距离: {self.worst_distance}")
        
        # 步骤5：计算相对贴近度
        self._calculate_similarities()
        print(f"\nStep 6: 相对贴近度: {self.best_similarity}")
        
    def _normalize_matrix(self):
        """向量标准化"""
        # 计算每列的平方和的平方根
        column_sums = np.sqrt(np.sum(self.evaluation_matrix**2, axis=0))
        self.normalized_matrix = self.evaluation_matrix / column_sums
        
    def _calculate_weighted_normalized(self):
        """计算加权标准化矩阵"""
        # 权重归一化
        normalized_weights = self.weights / np.sum(self.weights)
        self.weighted_normalized = self.normalized_matrix * normalized_weights
        
    def _find_ideal_solutions(self):
        """确定正负理想解"""
        self.best_alternative = np.zeros(self.weighted_normalized.shape[1])
        self.worst_alternative = np.zeros(self.weighted_normalized.shape[1])
        
        for j in range(self.weighted_normalized.shape[1]):
            if self.criteria_types[j]:  # 效益型
                self.best_alternative[j] = np.max(self.weighted_normalized[:, j])
                self.worst_alternative[j] = np.min(self.weighted_normalized[:, j])
            else:  # 成本型
                self.best_alternative[j] = np.min(self.weighted_normalized[:, j])
                self.worst_alternative[j] = np.max(self.weighted_normalized[:, j])
                
    def _calculate_distances(self):
        """计算欧几里得距离"""
        m = self.weighted_normalized.shape[0]
        self.best_distance = np.zeros(m)
        self.worst_distance = np.zeros(m)
        
        for i in range(m):
            # 到正理想解的距离
            self.best_distance[i] = np.sqrt(
                np.sum((self.weighted_normalized[i] - self.best_alternative)**2)
            )
            # 到负理想解的距离
            self.worst_distance[i] = np.sqrt(
                np.sum((self.weighted_normalized[i] - self.worst_alternative)**2)
            )
            
    def _calculate_similarities(self):
        """计算相对贴近度"""
        self.best_similarity = self.worst_distance / (
            self.best_distance + self.worst_distance
        )
        # 避免除零错误
        self.best_similarity = np.nan_to_num(self.best_similarity)
        
    def rank_to_best_similarity(self):
        """返回按相对贴近度排序的方案索引"""
        return np.argsort(-self.best_similarity)  # 降序排列

# 使用示例
if __name__ == "__main__":
    # 示例数据：3个作战方案，4个评价指标
    evaluation_matrix = np.array([
        [85, 0.8, 12, 150000],  # 方案1: 效率、安全性、时间、成本
        [78, 0.9, 18, 120000],  # 方案2
        [90, 0.7, 15, 180000],  # 方案3
    ])
    
    weights = [0.4, 0.3, 0.2, 0.1]  # 权重分配
    criteria_types = [True, True, False, False]  # 效益型、效益型、成本型、成本型
    
    t = Topsis(evaluation_matrix, weights, criteria_types)
    t.calc()
    
    print(f"\n最终排序: {t.rank_to_best_similarity()}")
    print(f"相对贴近度: {t.best_similarity}")