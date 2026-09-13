"""
刀具磨损状态识别与RUL预测系统 - 后端服务
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 数据库初始化
DB_PATH = 'data/predictions.db'

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS prediction_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sample_id TEXT,
            wear_level INTEGER,
            wear_level_name TEXT,
            rul REAL,
            risk_level TEXT,
            features_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 加载预处理后的训练数据训练模型
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler

model_classifier = None
model_regressor = None
scaler = None
feature_cols = None

def train_model():
    """训练预测模型"""
    global model_classifier, model_regressor, scaler, feature_cols
    
    # 加载预处理后的数据
    train_df = pd.read_csv('data/processed/features_train.csv')
    
    label_cols = ['wear_level', 'rul']
    feature_cols = [col for col in train_df.columns if col not in label_cols]
    
    X = train_df[feature_cols]
    y_class = train_df['wear_level']
    y_reg = train_df['rul']
    
    # 训练分类模型（磨损等级）
    model_classifier = RandomForestClassifier(n_estimators=50, random_state=42)
    model_classifier.fit(X, y_class)
    
    # 训练回归模型（RUL预测）
    model_regressor = RandomForestRegressor(n_estimators=50, random_state=42)
    model_regressor.fit(X, y_reg)
    
    print(f"模型训练完成，特征数: {len(feature_cols)}")

@app.route('/')
def index():
    """前端页面"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """预测接口"""
    data = request.json
    
    # 获取输入特征
    input_features = data.get('features', {})
    sample_id = data.get('sample_id', f'sample_{datetime.now().strftime("%Y%m%d%H%M%S")}')
    
    # 构造特征向量
    feature_vector = []
    for col in feature_cols:
        feature_vector.append(input_features.get(col, 0))
    
    feature_vector = np.array(feature_vector).reshape(1, -1)
    
    # 预测磨损等级
    wear_level = int(model_classifier.predict(feature_vector)[0])
    level_names = {0: '轻微磨损', 1: '中度磨损', 2: '严重磨损'}
    wear_level_name = level_names.get(wear_level, '未知')
    
    # 预测RUL
    rul = float(model_regressor.predict(feature_vector)[0])
    rul = max(0, rul)
    
    # 风险等级判断
    if wear_level == 0:
        risk_level = '正常'
    elif wear_level == 1:
        risk_level = '预警'
    else:
        risk_level = '报警'
    
    # 保存到数据库
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO prediction_records 
        (timestamp, sample_id, wear_level, wear_level_name, rul, risk_level, features_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        sample_id,
        wear_level,
        wear_level_name,
        round(rul, 2),
        risk_level,
        json.dumps(input_features, ensure_ascii=False)
    ))
    conn.commit()
    record_id = c.lastrowid
    conn.close()
    
    return jsonify({
        'success': True,
        'record_id': record_id,
        'sample_id': sample_id,
        'wear_level': wear_level,
        'wear_level_name': wear_level_name,
        'rul': round(rul, 2),
        'risk_level': risk_level,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/records', methods=['GET'])
def get_records():
    """获取历史预测记录"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM prediction_records ORDER BY id DESC LIMIT 20')
    rows = c.fetchall()
    records = [dict(row) for row in rows]
    conn.close()
    
    return jsonify({
        'success': True,
        'count': len(records),
        'records': records
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 总记录数
    c.execute('SELECT COUNT(*) FROM prediction_records')
    total = c.fetchone()[0]
    
    # 各等级数量
    c.execute('SELECT wear_level_name, COUNT(*) FROM prediction_records GROUP BY wear_level_name')
    level_dist = dict(c.fetchall())
    
    # 平均RUL
    c.execute('SELECT AVG(rul) FROM prediction_records')
    avg_rul = c.fetchone()[0] or 0
    
    conn.close()
    
    return jsonify({
        'success': True,
        'total_predictions': total,
        'level_distribution': level_dist,
        'avg_rul': round(avg_rul, 2)
    })

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """获取示例测试数据"""
    test_df = pd.read_csv('data/raw/test_sample.csv')
    sample = test_df.iloc[0].to_dict()
    return jsonify({
        'success': True,
        'sample': sample
    })

if __name__ == '__main__':
    # 初始化
    os.makedirs('data', exist_ok=True)
    init_db()
    train_model()
    
    print("=" * 50)
    print("刀具磨损状态识别与RUL预测系统")
    print("=" * 50)
    print("访问地址: http://127.0.0.1:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
