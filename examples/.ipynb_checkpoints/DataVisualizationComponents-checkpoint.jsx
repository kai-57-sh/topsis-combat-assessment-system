// DataVisualizationComponents.jsx - 可视化组件库
import React from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  ScatterChart,
  Scatter,
  Cell,
  PieChart,
  Pie,
  ResponsiveContainer
} from 'recharts';
import { Box, Paper, Typography, useTheme } from '@mui/material';

// 敏感性分析图表
export const SensitivityAnalysisChart = ({ data }) => {
  const theme = useTheme();
  
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        权重敏感性分析
      </Typography>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <XAxis dataKey="weightFactor" />
          <YAxis />
          <Tooltip />
          <Legend />
          {data[0] && Object.keys(data[0]).filter(key => key !== 'weightFactor').map((key, index) => (
            <Line 
              key={key}
              type="monotone" 
              dataKey={key} 
              stroke={theme.palette.primary.main} 
              strokeDasharray={index % 2 === 0 ? "0" : "5 5"}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </Paper>
  );
};

// 方案性能分布图
export const AlternativePerformanceScatter = ({ data }) => {
  const theme = useTheme();
  
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        方案性能分布图
      </Typography>
      <ResponsiveContainer width="100%" height={400}>
        <ScatterChart data={data}>
          <XAxis dataKey="cost" name="成本" />
          <YAxis dataKey="effectiveness" name="效能" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter dataKey="y" fill={theme.palette.secondary.main} />
        </ScatterChart>
      </ResponsiveContainer>
    </Paper>
  );
};

// 指标权重饼图
export const CriteriaWeightsPieChart = ({ data }) => {
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];
  
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        指标权重分布
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </Paper>
  );
};

// 时间序列分析图
export const TimeSeriesAnalysisChart = ({ data }) => {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        历史分析趋势
      </Typography>
      <ResponsiveContainer width="100%" height={350}>
        <AreaChart data={data}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Area 
            type="monotone" 
            dataKey="score" 
            stackId="1" 
            stroke="#8884d8" 
            fill="#8884d8" 
            fillOpacity={0.6}
          />
        </AreaChart>
      </ResponsiveContainer>
    </Paper>
  );
};