"""
刀具磨损数据预处理程序
功能：数据清洗、异常值检测、特征标准化、数据集划分
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os
import json

# 配置
RAW_DATA_DIR = '../data/raw'
PROCESSED_DATA_DIR = '../data/processed'

def load_raw_data():
    """加载原始数据"""
    train_path = os.path.join(RAW_DATA_DIR, 'train_sample.csv')
    test_path = os.path.join(RAW_DATA_DIR, 'test_sample.csv')
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    print(f"加载训练集: {train_df.shape}")
    print(f"加载测试集: {test_df.shape}")
    
    return train_df, test_df

def check_missing_values(df, name):
    """检查缺失值"""
    missing = df.isnull().sum()
    missing_ratio = missing / len(df) * 100
    
    result = {
        'total_missing': int(missing.sum()),
        'columns_with_missing': missing[missing > 0].to_dict()
    }
    
    print(f"\n[{name}] 缺失值检查:")
    print(f"  总缺失值数量: {result['total_missing']}")
    if result['columns_with_missing']:
        print(f"  有缺失的列: {result['columns_with_missing']}")
    else:
        print("  无缺失值")
    
    return result

def detect_outliers_iqr(df, feature_cols, name):
    """IQR方法检测异常值"""
    outlier_info = {}
    
    print(f"\n[{name}] 异常值检测 (IQR方法):")
    
    for col in feature_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_count = len(outliers)
        
        outlier_info[col] = {
            'count': outlier_count,
            'ratio': outlier_count / len(df) * 100
        }
        
        if outlier_count > 0:
            print(f"  {col}: {outlier_count} 个异常值 ({outlier_count/len(df)*100:.1f}%)")
    
    total_outliers = sum(v['count'] for v in outlier_info.values())
    print(f"  总异常值点: {total_outliers}")
    
    return outlier_info

def remove_outliers(df, feature_cols):
    """移除异常值（用边界值截断）"""
    df_clean = df.copy()
    
    for col in feature_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df_clean[col] = df_clean[col].clip(lower_bound, upper_bound)
    
    return df_clean

def standardize_features(train_df, test_df, feature_cols):
    """Z-score 标准化"""
    scaler = StandardScaler()
    
    train_scaled = train_df.copy()
    test_scaled = test_df.copy()
    
    train_scaled[feature_cols] = scaler.fit_transform(train_df[feature_cols])
    test_scaled[feature_cols] = scaler.transform(test_df[feature_cols])
    
    print(f"\n特征标准化完成 (Z-score):")
    print(f"  特征数量: {len(feature_cols)}")
    print(f"  训练集均值: {scaler.mean_[:3].round(3)}...")
    print(f"  训练集标准差: {scaler.scale_[:3].round(3)}...")
    
    return train_scaled, test_scaled, scaler

def split_features_labels(df):
    """分离特征和标签"""
    # 标签列
    label_cols = ['sample_id', 'wear', 'wear_level', 'rul']
    feature_cols = [col for col in df.columns if col not in label_cols]
    
    X = df[feature_cols]
    y_class = df['wear_level']  # 分类标签
    y_reg = df['rul']           # 回归标签
    
    return X, y_class, y_reg, feature_cols

def main():
    print("=" * 60)
    print("刀具磨损数据预处理")
    print("=" * 60)
    
    # 1. 加载数据
    train_df, test_df = load_raw_data()
    
    # 2. 检查缺失值
    train_missing = check_missing_values(train_df, '训练集')
    test_missing = check_missing_values(test_df, '测试集')
    
    # 3. 分离特征和标签
    X_train_raw, y_train_class, y_train_reg, feature_cols = split_features_labels(train_df)
    X_test_raw, y_test_class, y_test_reg, _ = split_features_labels(test_df)
    
    print(f"\n特征列数量: {len(feature_cols)}")
    print(f"标签列: wear(磨损量), wear_level(磨损等级), rul(剩余寿命)")
    
    # 4. 异常值检测
    train_outliers = detect_outliers_iqr(X_train_raw, feature_cols, '训练集')
    test_outliers = detect_outliers_iqr(X_test_raw, feature_cols, '测试集')
    
    # 5. 异常值处理（截断）
    X_train_clean = X_train_raw.copy()
    X_test_clean = X_test_raw.copy()
    
    for col in feature_cols:
        Q1 = X_train_clean[col].quantile(0.25)
        Q3 = X_train_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        X_train_clean[col] = X_train_clean[col].clip(lower, upper)
        X_test_clean[col] = X_test_clean[col].clip(lower, upper)
    
    print(f"\n异常值处理完成 (边界截断法)")
    
    # 6. 特征标准化
    X_train_scaled, X_test_scaled, scaler = standardize_features(
        X_train_clean, X_test_clean, feature_cols
    )
    
    # 7. 保存预处理后的数据
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    # 组合特征和标签
    train_processed = pd.concat([
        X_train_scaled.reset_index(drop=True),
        y_train_class.reset_index(drop=True).rename('wear_level'),
        y_train_reg.reset_index(drop=True).rename('rul')
    ], axis=1)
    
    test_processed = pd.concat([
        X_test_scaled.reset_index(drop=True),
        y_test_class.reset_index(drop=True).rename('wear_level'),
        y_test_reg.reset_index(drop=True).rename('rul')
    ], axis=1)
    
    train_path = os.path.join(PROCESSED_DATA_DIR, 'features_train.csv')
    test_path = os.path.join(PROCESSED_DATA_DIR, 'features_test.csv')
    
    train_processed.to_csv(train_path, index=False, encoding='utf-8-sig')
    test_processed.to_csv(test_path, index=False, encoding='utf-8-sig')
    
    print(f"\n预处理后数据已保存:")
    print(f"  训练集: {train_path} ({len(train_processed)} 样本)")
    print(f"  测试集: {test_path} ({len(test_processed)} 样本)")
    
    # 8. 保存预处理统计信息
    stats = {
        'train_samples': len(train_processed),
        'test_samples': len(test_processed),
        'feature_count': len(feature_cols),
        'features': feature_cols,
        'wear_level_distribution': y_train_class.value_counts().to_dict(),
        'preprocessing_steps': [
            '缺失值检查 (无缺失)',
            'IQR异常值检测与截断处理',
            'Z-score标准化'
        ]
    }
    
    stats_path = os.path.join(PROCESSED_DATA_DIR, 'preprocess_stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"  预处理统计: {stats_path}")
    
    print("\n" + "=" * 60)
    print("预处理完成!")
    print("=" * 60)

if __name__ == '__main__':
    main()
