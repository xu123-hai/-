# 面向数控生产线刀具磨损状态识别与剩余寿命预测系统

## 项目简介
本项目为制造智能技术基础课程设计，针对数控加工生产线中刀具磨损导致的产品不合格问题，实现刀具磨损状态识别与剩余使用寿命(RUL)预测，支持预测性维护。系统采用完整 B/S 架构，包含前端可视化界面、后端 API 服务、SQLite 数据库和智能算法模块。

## 技术方向
本项目涉及以下制造智能技术方向（均来自课程专题）：

1. **特征工程基础** - 时域/频域特征提取、Z-score标准化、IQR异常值检测
2. **机器学习模型** - RandomForest分类与回归，特征重要性分析
3. **故障预测与健康管理(PHM)** - 预测性维护理念、RUL剩余寿命预测、风险分级
4. **模型评估** - 分类准确率、召回率、F1分数、RMSE等评估指标

## 系统架构
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   前端UI层      │────▶│   后端API层     │────▶│   算法模块层    │
│  (HTML+JS+Chart)│◀────│  (Flask)        │◀────│  (sklearn模型)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   SQLite数据库   │
                        │  (预测记录存储)  │
                        └─────────────────┘
```

## 目录结构
```
├── README.md                 # 项目说明（本文件）
├── 选题说明.md                # 选题背景、目标、技术方向
├── 方案设计.md                # 功能需求、方案论证、技术路线、计划安排
├── 学习笔记.md                # 课程学习笔记
├── requirements.txt          # Python 依赖清单
├── src/                       # 源代码目录
│   ├── app.py                 # Flask 后端主应用
│   ├── preprocess.py          # 数据预处理脚本
│   └── generate_sample_data.py # 示例数据生成脚本
├── data/                      # 数据目录
│   ├── README.md              # 数据集详细说明
│   ├── raw/                   # 原始数据
│   │   ├── train_sample.csv   # 训练集示例
│   │   └── test_sample.csv    # 测试集示例
│   ├── processed/             # 预处理后数据
│   │   ├── features_train.csv  # 训练集特征
│   │   ├── features_test.csv   # 测试集特征
│   │   └── preprocess_stats.json # 预处理统计信息
│   └── predictions.db         # SQLite 预测记录数据库
├── templates/                 # 前端页面模板
│   └── index.html             # 主界面
└── prompt/                    # AI工具提示词追溯
    ├── ai_conversation_records.json  # AI交流记录
    └── vibe_coding_notes.md   # Vibe Coding 学习记录
```

## 数据集说明
- **数据来源**: PHM Society 2010 刀具磨损预测公开数据集（示例子集）
- **官方链接**: https://phmsociety.org/conferences/2010/phm-2010-data-challenge/
- **数据描述**: 数控铣刀全生命周期传感器数据，包含切削力、振动、声发射信号及磨损量标签
- **示例规模**: 训练集200样本，测试集50样本
- **完整数据**: 可从上述官网下载，放置到 `data/raw/` 后重新运行预处理脚本即可

## 功能模块

### 1. 数据预处理模块
- 缺失值检查与处理
- IQR 异常值检测与截断
- Z-score 特征标准化
- 28维统计特征提取（均值、标准差、RMS、最大值）

### 2. 算法预测模块
- **磨损分类**: RandomForest 三分类（轻微/中度/严重磨损）
- **RUL 预测**: RandomForest 回归预测剩余使用寿命
- **风险分级**: 根据磨损等级自动判定风险等级（正常/预警/报警）

### 3. 后端服务模块
- 预测 API: `/api/predict` - 输入特征，输出磨损等级和RUL
- 记录查询 API: `/api/records` - 查询历史预测记录
- 统计 API: `/api/stats` - 获取系统统计信息

### 4. 前端可视化模块
- 实时预测面板：输入传感器参数，一键预测
- 结果展示：磨损等级、RUL数值、风险等级
- 历史记录：最近20条预测记录表格
- 统计图表：磨损等级分布柱状图

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 生成示例数据（首次运行）
```bash
python generate_sample_data.py
python preprocess.py
```

### 3. 启动系统
```bash
cd src
python app.py
```

### 4. 访问系统
打开浏览器访问: http://127.0.0.1:5000

## 数据预处理流程
已完成的数据预处理工作：
1. **缺失值检查** - 示例数据无缺失值
2. **异常值检测** - 使用IQR方法检测各特征列异常值
3. **异常值处理** - 采用边界截断法处理异常值
4. **特征标准化** - Z-score标准化（零均值，单位方差）
5. **特征提取** - 28维统计特征（均值、标准差、RMS、最大值）

## API 接口说明

| 接口 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 前端主页面 |
| `/api/predict` | POST | 磨损状态预测 |
| `/api/records` | GET | 获取历史预测记录 |
| `/api/stats` | GET | 获取统计信息 |
| `/api/sample-data` | GET | 获取示例测试数据 |

## 项目进度
- [x] 1. Vibe Coding 方法学习
- [x] 2. Git 版本控制
- [x] 3. 选题（含技术方向映射、数据来源）
- [x] 4. 数据资源整理（收集、清洗、处理）
- [x] 5. 系统开发与集成调试（B/S架构demo）
- [ ] 6. 成果提交（设计报告、演示视频、答辩PPT）

## Vibe Coding 实践
本项目全程采用 Vibe Coding 方法开发，详见 `vibe_coding_notes.md`。
AI 交流记录详见 `prompt/ai_conversation_records.json`。

## 参考文献
1. PHM Society. 2010 Prognostics and Health Management Conference Data Challenge Dataset
2. Breiman L. Random Forests. Machine Learning, 2001
3. 张洁等. 智能制造生产线设备预测性维护技术研究. 计算机集成制造系统, 2023
4. 张智海等. 制造智能技术基础. 清华大学出版社, 2022
