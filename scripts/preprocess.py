# -*- coding: utf-8 -*-
"""
preprocess.py
=============
「面向人机运动性能评估的网页端参数匹配生成器」课程设计 —— 数据预处理程序

功能概述
--------
针对网页端人机运动性能测试导出的原始 CSV 数据，完成以下预处理步骤：
  1. 加载原始数据（data/raw/）
  2. 清洗：剔除缺失值、非法（负值/空值）记录
  3. 去离群：按“测试类型 × 指标”分组，剔除超过 均值±3σ 的离群样本，
     降低单次偶然操作带来的误差
  4. 统计聚合：按测试类型计算均值、标准差、中位数、命中率等统计量
  5. 派生指标：计算命中率 hit_rate = hit_count / target_total
  6. 输出：清洗后明细数据、统计汇总数据、处理索引（index.json）

对应方案设计 3.5 节「后端算法方案 - 数据预处理算法」，
该算法后续将内嵌至网页端 JavaScript 中，本脚本为仓库数据管理用的独立实现。

运行方式（在 scripts 目录下执行）
---------------------------------
    python preprocess.py

输出目录
--------
    ../data/processed/
        cleaned_test_data.csv   清洗后的明细数据
        test_statistics.csv     各测试类型统计汇总
        index.json              预处理结果索引
"""

import csv
import json
import os
import statistics

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "data"))
RAW_PATH = os.path.join(DATA_DIR, "raw", "sample_test_data.csv")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# 各测试类型需要参与统计的指标
METRICS_BY_TEST = {
    "aim":   ["response_time_ms", "positioning_error_px", "hit_rate"],
    "track": ["tracking_error_px", "hit_rate"],
    "flick": ["response_time_ms", "positioning_error_px", "hit_rate"],
    "calib": ["physical_move_cm", "virtual_rotate_deg"],
}

OUTLIER_SIGMA = 3.0  # 离群阈值：均值 ± 3σ


def load_csv(path):
    """读取原始 CSV，返回字典列表。"""
    with open(path, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def clean(rows):
    """
    清洗：剔除缺失或非法记录。
    非法判定：
      - 响应时间 / 定位误差 / 追踪误差 / 命中数 / 目标总数 等数值字段为空或为负
      - 标定测试中 物理移动距离 / 虚拟转动量 为空或为负
    """
    cleaned = []
    for row in rows:
        ok = True
        for key in ["response_time_ms", "positioning_error_px",
                    "tracking_error_px", "hit_count", "target_total",
                    "physical_move_cm", "virtual_rotate_deg"]:
            val = row.get(key, "").strip()
            if val == "":
                continue  # 非本项目指标，允许为空
            try:
                num = float(val)
            except ValueError:
                ok = False
                break
            if num < 0:
                ok = False
                break
        if ok:
            # 补充派生指标：命中率
            try:
                row["hit_rate"] = round(float(row["hit_count"]) / float(row["target_total"]), 4)
            except (ValueError, ZeroDivisionError):
                row["hit_rate"] = ""
            cleaned.append(row)
    return cleaned


def remove_outliers(cleaned):
    """按 测试类型×指标 分组去除 均值±3σ 之外的离群样本。"""
    kept = []
    for test_type in {r["test_type"] for r in cleaned}:
        group = [r for r in cleaned if r["test_type"] == test_type]
        metrics = METRICS_BY_TEST.get(test_type, [])
        # 逐指标计算剔除集合
        drop = set()
        for m in metrics:
            values = []
            for i, r in enumerate(group):
                try:
                    values.append((i, float(r[m])))
                except (ValueError, TypeError):
                    continue
            if not values:
                continue
            nums = [v for _, v in values]
            mu = statistics.mean(nums)
            sd = statistics.stdev(nums) if len(nums) > 1 else 0.0
            for i, v in values:
                if abs(v - mu) > OUTLIER_SIGMA * sd:
                    drop.add(i)
        for i, r in enumerate(group):
            if i not in drop:
                kept.append(r)
    return kept


def aggregate(cleaned):
    """按测试类型统计各指标：均值/标准差/中位数/样本数。"""
    stats_rows = []
    for test_type in sorted({r["test_type"] for r in cleaned}):
        group = [r for r in cleaned if r["test_type"] == test_type]
        metrics = METRICS_BY_TEST.get(test_type, [])
        row = {"test_type": test_type, "sample_count": len(group)}
        for m in metrics:
            nums = []
            for r in group:
                try:
                    nums.append(float(r[m]))
                except (ValueError, TypeError):
                    continue
            if nums:
                row[f"{m}_mean"] = round(statistics.mean(nums), 4)
                row[f"{m}_std"] = round(statistics.stdev(nums), 4) if len(nums) > 1 else 0.0
                row[f"{m}_median"] = round(statistics.median(nums), 4)
            else:
                row[f"{m}_mean"] = ""
                row[f"{m}_std"] = ""
                row[f"{m}_median"] = ""
        stats_rows.append(row)
    return stats_rows


def write_csv(path, rows, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"未找到原始数据：{RAW_PATH}，请先运行 generate_sample_data.py")

    raw = load_csv(RAW_PATH)
    cleaned = clean(raw)
    kept = remove_outliers(cleaned)
    stats = aggregate(kept)

    # 明细字段顺序
    detail_fields = list(raw[0].keys()) + ["hit_rate"]
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    write_csv(os.path.join(PROCESSED_DIR, "cleaned_test_data.csv"), kept, detail_fields)
    # 统计表字段取所有行字段的并集（不同测试类型指标不同）
    stat_fields = list(dict.fromkeys(k for s in stats for k in s.keys())) if stats else ["test_type"]
    write_csv(os.path.join(PROCESSED_DIR, "test_statistics.csv"), stats, stat_fields)

    # 索引文件
    index = {
        "dataset_name": "人机运动性能测试自建样例数据集",
        "data_type": "自建数据(self-built)",
        "source": "网页端人机运动性能测试实时采集（样例为模拟生成，见 scripts/generate_sample_data.py）",
        "version": "1.0",
        "preprocessing_version": "1.0",
        "raw_file": "data/raw/sample_test_data.csv",
        "processed_files": {
            "cleaned_detail": "data/processed/cleaned_test_data.csv",
            "test_statistics": "data/processed/test_statistics.csv",
        },
        "preprocess_script": "scripts/preprocess.py",
        "outlier_method": "均值±3σ（按测试类型×指标分组）",
        "derived_metric": "hit_rate = hit_count / target_total",
        "summary": {
            "raw_records": len(raw),
            "after_clean": len(cleaned),
            "after_outlier_removal": len(kept),
            "removed_records": len(raw) - len(kept),
            "test_types": sorted({r["test_type"] for r in kept}),
        },
        "updated_at": "2026-08-29",
    }
    with open(os.path.join(PROCESSED_DIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"原始记录数   : {len(raw)}")
    print(f"清洗后记录数 : {len(cleaned)}")
    print(f"去离群后记录数: {len(kept)}")
    print(f"剔除记录数   : {len(raw) - len(kept)}")
    print(f"输出目录     : {PROCESSED_DIR}")
    for s in stats:
        print("  ", s)


if __name__ == "__main__":
    main()
