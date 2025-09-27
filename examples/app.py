# app.py - Flask API服务器
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from typing import Dict, List
import logging
import traceback

# 导入我们的TOPSIS实现
from combat_assessment.core.topsis import Topsis
from combat_assessment.scenarios import ScenarioManager
from combat_assessment.data.validator import DataValidator

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化组件
scenario_manager = ScenarioManager()
validator = DataValidator()

@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    """获取所有可用场景"""
    try:
        scenarios = scenario_manager.get_all_scenarios()
        return jsonify({
            'success': True,
            'data': scenarios
        })
    except Exception as e:
        logger.error(f"获取场景失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/scenarios/<scenario_id>/template', methods=['GET'])
def get_scenario_template(scenario_id):
    """获取场景数据模板"""
    try:
        template = scenario_manager.get_scenario_template(scenario_id)
        return jsonify({
            'success': True,
            'data': template
        })
    except KeyError:
        return jsonify({
            'success': False,
            'error': f'场景 {scenario_id} 不存在'
        }), 404
    except Exception as e:
        logger.error(f"获取场景模板失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analysis/topsis', methods=['POST'])
def run_topsis_analysis():
    """执行TOPSIS分析"""
    try:
        data = request.get_json()
        
        # 数据验证
        validation_result = validator.validate_topsis_input(data)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': validation_result['errors']
            }), 400
        
        # 提取参数
        matrix = np.array(data['matrix'])
        weights = np.array(data['weights'])
        criteria_types = data['criteria_types']
        alternatives = data.get('alternatives', [f'方案{i+1}' for i in range(len(matrix))])
        criteria = data.get('criteria', [f'指标{i+1}' for i in range(len(weights))])
        
        # 执行TOPSIS分析
        topsis = Topsis(matrix, weights, criteria_types)
        topsis.calc()
        
        # 构建返回结果
        rankings = topsis.rank_to_best_similarity()
        
        result = {
            'success': True,
            'data': {
                'alternatives': alternatives,
                'criteria': criteria,
                'topsis_scores': topsis.best_similarity.tolist(),
                'rankings': (rankings + 1).tolist(),  # 排名从1开始
                'best_alternative': alternatives[rankings[0]],
                'normalized_matrix': topsis.normalized_matrix.tolist(),
                'weighted_matrix': topsis.weighted_normalized.tolist(),
                'ideal_solutions': {
                    'positive': topsis.best_alternative.tolist(),
                    'negative': topsis.worst_alternative.tolist()
                },
                'distances': {
                    'to_positive': topsis.best_distance.tolist(),
                    'to_negative': topsis.worst_distance.tolist()
                }
            }
        }
        
        logger.info(f"TOPSIS分析完成，最优方案: {result['data']['best_alternative']}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"TOPSIS分析失败: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'分析过程出错: {str(e)}'
        }), 500

@app.route('/api/analysis/sensitivity', methods=['POST'])
def run_sensitivity_analysis():
    """执行敏感性分析"""
    try:
        data = request.get_json()
        
        base_matrix = np.array(data['matrix'])
        base_weights = np.array(data['weights'])
        criteria_types = data['criteria_types']
        weight_variations = data.get('weight_variations', [0.8, 0.9, 1.0, 1.1, 1.2])
        criteria_to_analyze = data.get('criteria_indices', list(range(len(base_weights))))
        
        sensitivity_results = {}
        
        for criterion_idx in criteria_to_analyze:
            variations = []
            
            for factor in weight_variations:
                # 修改权重
                modified_weights = base_weights.copy()
                modified_weights[criterion_idx] *= factor
                # 归一化
                modified_weights = modified_weights / np.sum(modified_weights)
                
                # 重新计算TOPSIS
                topsis = Topsis(base_matrix, modified_weights, criteria_types)
                topsis.calc()
                
                rankings = topsis.rank_to_best_similarity() + 1
                variations.append({
                    'weight_factor': factor,
                    'rankings': rankings.tolist(),
                    'scores': topsis.best_similarity.tolist()
                })
            
            sensitivity_results[f'criterion_{criterion_idx}'] = variations
        
        return jsonify({
            'success': True,
            'data': sensitivity_results
        })
        
    except Exception as e:
        logger.error(f"敏感性分析失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export/results', methods=['POST'])
def export_results():
    """导出分析结果"""
    try:
        data = request.get_json()
        
        # 这里实现结果导出逻辑
        # 可以生成Excel、PDF等格式的报告
        
        return jsonify({
            'success': True,
            'message': '结果导出成功',
            'download_url': '/api/download/report.xlsx'
        })
        
    except Exception as e:
        logger.error(f"结果导出失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'API端点不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)