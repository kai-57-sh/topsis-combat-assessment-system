// TopsisAnalysisDashboard.jsx - TOPSIS分析仪表板主组件
import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardHeader,
  Box,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { styled } from '@mui/material/styles';

// 样式化组件
const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[8],
  },
}));

const TabPanel = ({ children, value, index, ...other }) => (
  <div
    role="tabpanel"
    hidden={value !== index}
    id={`analysis-tabpanel-${index}`}
    aria-labelledby={`analysis-tab-${index}`}
    {...other}
  >
    {value === index && (
      <Box sx={{ p: 3 }}>
        {children}
      </Box>
    )}
  </div>
);

const TopsisAnalysisDashboard = () => {
  // 状态管理
  const [currentScenario, setCurrentScenario] = useState('chokepoint');
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [dialogOpen, setDialogOpen] = useState(false);

  // 场景配置
  const scenarios = {
    chokepoint: {
      name: '要峡封控',
      description: '在关键水道实施海上封锁作战',
      color: '#1976d2'
    },
    landing: {
      name: '登陆场通道清扫', 
      description: '为两栖登陆开辟安全航道',
      color: '#388e3c'
    },
    mcm: {
      name: '水雷清排',
      description: '系统性清除指定海域水雷威胁',
      color: '#f57c00'
    },
    surveillance: {
      name: '近岸水下监视',
      description: '重要水域持续监控防护',
      color: '#7b1fa2'
    }
  };

  // 模拟API调用
  const fetchAnalysisData = async (scenarioId) => {
    setLoading(true);
    setError(null);
    
    try {
      // 模拟API延迟
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // 模拟返回数据
      const mockData = {
        scenario: scenarioId,
        alternatives: ['方案A', '方案B', '方案C'],
        criteria: ['任务完成度', '体系生存力', '指挥控制力', '作战持续性', '效费比'],
        topsisScores: [0.65, 0.82, 0.73],
        rankings: [3, 1, 2],
        radarData: [
          {
            criteria: '任务完成度',
            '方案A': 0.7,
            '方案B': 0.9,
            '方案C': 0.8
          },
          {
            criteria: '体系生存力', 
            '方案A': 0.8,
            '方案B': 0.7,
            '方案C': 0.9
          },
          {
            criteria: '指挥控制力',
            '方案A': 0.6,
            '方案B': 0.8,
            '方案C': 0.7
          },
          {
            criteria: '作战持续性',
            '方案A': 0.9,
            '方案B': 0.8,
            '方案C': 0.6
          },
          {
            criteria: '效费比',
            '方案A': 0.5,
            '方案B': 0.9,
            '方案C': 0.8
          }
        ],
        barData: [
          {
            name: '方案A',
            score: 0.65,
            rank: 3
          },
          {
            name: '方案B', 
            score: 0.82,
            rank: 1
          },
          {
            name: '方案C',
            score: 0.73,
            rank: 2
          }
        ]
      };
      
      setAnalysisData(mockData);
    } catch (err) {
      setError('数据加载失败，请重试');
      console.error('Analysis data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  // 处理场景切换
  const handleScenarioChange = (event) => {
    const newScenario = event.target.value;
    setCurrentScenario(newScenario);
    fetchAnalysisData(newScenario);
  };

  // 组件挂载时加载默认数据
  useEffect(() => {
    fetchAnalysisData(currentScenario);
  }, []);

  // 渲染统计卡片
  const renderStatsCards = () => (
    <Grid container spacing={3} sx={{ mb: 3 }}>
      <Grid item xs={12} sm={6} md={3}>
        <StyledCard>
          <CardContent>
            <Typography color="textSecondary" gutterBottom variant="overline">
              最优方案
            </Typography>
            <Typography variant="h4" component="h2">
              {analysisData?.alternatives[analysisData.rankings.indexOf(1)] || '-'}
            </Typography>
            <Typography color="primary" variant="caption">
              TOPSIS评分最高
            </Typography>
          </CardContent>
        </StyledCard>
      </Grid>
      
      <Grid item xs={12} sm={6} md={3}>
        <StyledCard>
          <CardContent>
            <Typography color="textSecondary" gutterBottom variant="overline">
              最高得分
            </Typography>
            <Typography variant="h4" component="h2">
              {analysisData ? Math.max(...analysisData.topsisScores).toFixed(3) : '-'}
            </Typography>
            <Typography color="success.main" variant="caption">
              相对贴近度
            </Typography>
          </CardContent>
        </StyledCard>
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StyledCard>
          <CardContent>
            <Typography color="textSecondary" gutterBottom variant="overline">
              评价指标数
            </Typography>
            <Typography variant="h4" component="h2">
              {analysisData?.criteria.length || 0}
            </Typography>
            <Typography color="info.main" variant="caption">
              综合评估维度
            </Typography>
          </CardContent>
        </StyledCard>
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StyledCard>
          <CardContent>
            <Typography color="textSecondary" gutterBottom variant="overline">
              备选方案数
            </Typography>
            <Typography variant="h4" component="h2">
              {analysisData?.alternatives.length || 0}
            </Typography>
            <Typography color="warning.main" variant="caption">
              对比分析
            </Typography>
          </CardContent>
        </StyledCard>
      </Grid>
    </Grid>
  );

  // 渲染雷达图
  const renderRadarChart = () => (
    <StyledCard>
      <CardHeader 
        title="多维度能力对比雷达图"
        subheader="各方案在不同评价指标上的表现"
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={analysisData?.radarData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="criteria" />
            <PolarRadiusAxis angle={90} domain={[0, 1]} />
            <Radar 
              name="方案A" 
              dataKey="方案A" 
              stroke="#8884d8" 
              fill="#8884d8" 
              fillOpacity={0.1} 
            />
            <Radar 
              name="方案B" 
              dataKey="方案B" 
              stroke="#82ca9d" 
              fill="#82ca9d" 
              fillOpacity={0.1} 
            />
            <Radar 
              name="方案C" 
              dataKey="方案C" 
              stroke="#ffc658" 
              fill="#ffc658" 
              fillOpacity={0.1} 
            />
            <Legend />
          </RadarChart>
        </ResponsiveContainer>
      </CardContent>
    </StyledCard>
  );

  // 渲染柱状图
  const renderBarChart = () => (
    <StyledCard>
      <CardHeader 
        title="TOPSIS综合评分排名"
        subheader="基于相对贴近度的综合排序结果"
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={analysisData?.barData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="score" fill={scenarios[currentScenario].color} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </StyledCard>
  );

  // 主渲染函数
  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      {/* 页头 */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            作战体系效能评估分析
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            基于TOPSIS方法的多属性决策分析系统
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>作战场景</InputLabel>
            <Select
              value={currentScenario}
              label="作战场景"
              onChange={handleScenarioChange}
            >
              {Object.entries(scenarios).map(([key, scenario]) => (
                <MenuItem key={key} value={key}>
                  {scenario.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <Button 
            variant="contained" 
            onClick={() => setDialogOpen(true)}
            disabled={loading}
          >
            新建分析
          </Button>
        </Box>
      </Box>

      {/* 场景信息提示 */}
      <Alert severity="info" sx={{ mb: 3 }}>
        <strong>{scenarios[currentScenario].name}</strong> - {scenarios[currentScenario].description}
      </Alert>

      {/* 错误提示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* 加载指示器 */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {/* 主要内容 */}
      {!loading && analysisData && (
        <>
          {/* 统计卡片 */}
          {renderStatsCards()}

          {/* 标签页内容 */}
          <Paper sx={{ mt: 3 }}>
            <Tabs 
              value={tabValue} 
              onChange={(_, newValue) => setTabValue(newValue)}
              sx={{ borderBottom: 1, borderColor: 'divider' }}
            >
              <Tab label="综合分析" />
              <Tab label="雷达图对比" />
              <Tab label="排名结果" />
              <Tab label="敏感性分析" />
            </Tabs>

            <TabPanel value={tabValue} index={0}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  {renderBarChart()}
                </Grid>
                <Grid item xs={12} md={6}>
                  {renderRadarChart()}
                </Grid>
              </Grid>
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  {renderRadarChart()}
                </Grid>
              </Grid>
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  {renderBarChart()}
                </Grid>
              </Grid>
            </TabPanel>

            <TabPanel value={tabValue} index={3}>
              <Typography variant="h6">敏感性分析</Typography>
              <Typography color="textSecondary">
                此功能将显示权重变化对排序结果的影响分析
              </Typography>
            </TabPanel>
          </Paper>
        </>
      )}

      {/* 新建分析对话框 */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>新建分析项目</DialogTitle>
        <DialogContent>
          <Typography>此功能将允许用户创建新的TOPSIS分析项目</Typography>
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default TopsisAnalysisDashboard;