# 数据集说明

## 数据集名称
PHM 2010 刀具磨损预测公开数据集（示例子集）

## 数据集来源
- **官方来源**: PHM Society 2010 Conference Data Challenge
- **原始链接**: https://phmsociety.org/conferences/2010/phm-2010-data-challenge/
- **说明**: 本仓库 data 目录下存放的是基于该公开数据集生成的**示例子集**，用于课程设计演示和代码验证。

## 数据描述
该数据集为数控铣刀全生命周期实验数据，包含：
- **采样信号**: 三向切削力 (force_x, force_y, force_z)、三向振动 (vib_x, vib_y, vib_z)、声发射 (ae_rms)
- **采样频率**: 50 kHz
- **标签**: 刀具后刀面磨损量 (wear)，单位 μm
- **样本量**: 演示用简化子集（完整数据集约 200MB+）

## 目录结构
```
data/
├── README.md               # 本说明文件
├── raw/                    # 原始数据（示例）
│   ├── train_sample.csv    # 训练集示例（前100个样本窗口）
│   └── test_sample.csv     # 测试集示例
└── processed/              # 预处理后数据
    ├── features_train.csv  # 提取特征后的训练数据
    └── features_test.csv   # 提取特征后的测试数据
```

## 数据获取方式
如需完整数据集：
1. 访问 PHM Society 官网注册下载
2. 或使用 ModelScope / HuggingFace 镜像（搜索 "phm 2010 tool wear"）

## 数据说明
- 本示例数据为课程设计演示用途，数据量较小
- 完整数据集下载后请放置到 `data/raw/` 目录下，重新运行预处理脚本即可
- 数据预处理代码位于项目根目录 `preprocess.py`
