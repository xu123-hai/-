# 面向数控生产线刀具磨损状态识别与剩余寿命预测系统

## 项目简介
本项目为制造智能技术基础课程设计，针对数控加工生产线中刀具磨损导致的产品不合格问题，实现刀具磨损状态识别与剩余使用寿命(RUL)预测，支持预测性维护。

## 技术方向
本项目涉及以下制造智能技术方向（均来自课程专题）：

1. **特征工程基础** - 时域/频域特征提取、数据标准化、异常值检测
2. **深度学习CNN+LSTM** - 一维CNN提取局部信号特征，LSTM学习时序退化规律
3. **故障预测与健康管理(PHM)** - 预测性维护理念、RUL剩余寿命预测
4. **机器学习模型评估** - 混淆矩阵、精确率/召回率/F1、RMSE等评估指标

## 目录结构
```
├── README.md                 # 项目说明（本文件）
├── 选题说明.md                # 选题背景、目标、技术方向
├── 方案设计.md                # 功能需求、方案论证、技术路线、计划安排
├── 学习笔记.md                # 课程学习笔记
├── generate_sample_data.py    # 示例数据生成脚本
├── preprocess.py             # 数据预处理脚本
├── data/                      # 数据目录
│   ├── README.md              # 数据集详细说明
│   ├── raw/                   # 原始数据
│   │   ├── train_sample.csv   # 训练集示例
│   │   └── test_sample.csv    # 测试集示例
│   └── processed/             # 预处理后数据
│       ├── features_train.csv # 训练集特征
│       ├── features_test.csv  # 测试集特征
│       └── preprocess_stats.json # 预处理统计信息
└── prompt/                    # AI工具提示词追溯
    └── ai_conversation_records.json  # AI交流记录
```

## 数据集说明
- **数据来源**: PHM Society 2010 刀具磨损预测公开数据集（示例子集）
- **官方链接**: https://phmsociety.org/conferences/2010/phm-2010-data-challenge/
- **数据描述**: 数控铣刀全生命周期传感器数据，包含切削力、振动、声发射信号及磨损量标签
- **示例规模**: 训练集200样本，测试集50样本
- **完整数据**: 可从上述官网下载，放置到 `data/raw/` 后重新运行预处理脚本即可

## 数据预处理流程
已完成的数据预处理工作：

1. **缺失值检查** - 示例数据无缺失值
2. **异常值检测** - 使用IQR方法检测各特征列异常值
3. **异常值处理** - 采用边界截断法处理异常值
4. **特征标准化** - Z-score标准化（零均值，单位方差）
5. **特征提取** - 28维统计特征（均值、标准差、RMS、最大值）

运行预处理：
```bash
python preprocess.py
```

## 快速开始
```bash
# 1. 安装依赖
pip install numpy pandas scikit-learn matplotlib

# 2. 生成示例数据（可选）
python generate_sample_data.py

# 3. 运行数据预处理
python preprocess.py
```

## 项目进度
- [x] 选题说明
- [x] 方案设计
- [x] 数据来源准备
- [x] 数据预处理
- [ ] 模型构建与训练
- [ ] 前端可视化
- [ ] 系统集成与测试

## 参考文献
1. PHM Society. 2010 Prognostics and Health Management Conference Data Challenge Dataset
2. Hochreiter S, Schmidhuber J. Long Short-Term Memory. Neural Computation, 1997
3. 张洁等. 智能制造生产线设备预测性维护技术研究. 计算机集成制造系统, 2023
