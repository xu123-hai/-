"""
生成刀具磨损示例数据
基于 PHM 2010 数据集格式生成简化示例数据
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)

# 配置
n_samples_train = 200  # 训练样本数（窗口数）
n_samples_test = 50    # 测试样本数
window_size = 128      # 每个窗口的采样点数
sampling_freq = 50     # kHz

# 传感器列
sensor_cols = ['force_x', 'force_y', 'force_z', 'vib_x', 'vib_y', 'vib_z', 'ae_rms']

def generate_sample(tool_age_ratio):
    """
    根据刀具磨损程度生成一个窗口的传感器数据
    tool_age_ratio: 0~1, 0为新刀，1为完全磨损
    """
    t = np.linspace(0, 1, window_size)
    
    # 基础信号随磨损程度增强
    wear_factor = 1 + tool_age_ratio * 2
    
    data = {}
    # 切削力：随磨损线性增大
    data['force_x'] = (100 + 50 * tool_age_ratio) * np.sin(2 * np.pi * 10 * t) + np.random.normal(0, 5, window_size)
    data['force_y'] = (80 + 40 * tool_age_ratio) * np.sin(2 * np.pi * 10 * t + np.pi/4) + np.random.normal(0, 5, window_size)
    data['force_z'] = (150 + 80 * tool_age_ratio) * np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 8, window_size)
    
    # 振动：磨损越大，高频成分越多
    data['vib_x'] = (0.5 + 1.5 * tool_age_ratio) * np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.1, window_size)
    data['vib_y'] = (0.4 + 1.2 * tool_age_ratio) * np.sin(2 * np.pi * 50 * t + np.pi/3) + np.random.normal(0, 0.1, window_size)
    data['vib_z'] = (0.6 + 1.8 * tool_age_ratio) * np.sin(2 * np.pi * 80 * t) + np.random.normal(0, 0.15, window_size)
    
    # 声发射：磨损越大能量越高
    data['ae_rms'] = (0.2 + 0.6 * tool_age_ratio) + np.random.normal(0, 0.05, window_size)
    
    return data

def generate_dataset(n_samples, split_name):
    """生成完整数据集"""
    rows = []
    
    for i in range(n_samples):
        # 刀具从新到磨损，age_ratio 从 0 到 1
        age_ratio = i / n_samples
        
        # 生成窗口数据
        window_data = generate_sample(age_ratio)
        
        # 计算该窗口的统计特征作为一行样本
        row = {'sample_id': f'{split_name}_{i:04d}'}
        
        for col in sensor_cols:
            signal = window_data[col]
            row[f'{col}_mean'] = np.mean(signal)
            row[f'{col}_std'] = np.std(signal)
            row[f'{col}_rms'] = np.sqrt(np.mean(signal**2))
            row[f'{col}_max'] = np.max(signal)
        
        # 磨损量标签：从 0 线性增长到 300μm
        wear = age_ratio * 300 + np.random.normal(0, 5)
        row['wear'] = max(0, wear)
        
        # 磨损等级：0=轻微, 1=中度, 2=严重
        if wear < 100:
            row['wear_level'] = 0
        elif wear < 200:
            row['wear_level'] = 1
        else:
            row['wear_level'] = 2
        
        # RUL 剩余寿命：假设总寿命 300μm
        row['rul'] = max(0, 300 - wear)
        
        rows.append(row)
    
    return pd.DataFrame(rows)

# 生成训练集和测试集
train_df = generate_dataset(n_samples_train, 'train')
test_df = generate_dataset(n_samples_test, 'test')

# 保存
output_dir = 'data/raw'
os.makedirs(output_dir, exist_ok=True)

train_df.to_csv(os.path.join(output_dir, 'train_sample.csv'), index=False, encoding='utf-8-sig')
test_df.to_csv(os.path.join(output_dir, 'test_sample.csv'), index=False, encoding='utf-8-sig')

print(f"训练集: {len(train_df)} 样本, 列数: {len(train_df.columns)}")
print(f"测试集: {len(test_df)} 样本, 列数: {len(test_df.columns)}")
print(f"磨损等级分布: {train_df['wear_level'].value_counts().to_dict()}")
print(f"磨损量范围: {train_df['wear'].min():.1f} ~ {train_df['wear'].max():.1f} μm")
