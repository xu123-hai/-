# -*- coding: utf-8 -*-
"""
generate_sample_data.py
=======================
为「面向人机运动性能评估的网页端参数匹配生成器」课程设计生成自建样例原始数据。

背景说明
--------
本项目为纯前端单 HTML 网页，运行时由使用者在浏览器内完成多项虚拟运动测试，
实时采集并导出运动行为原始数据（CSV）。本脚本按照与网页端一致的导出字段格式，
模拟一名测试者（U001）在多个测试会话中的原始数据，用于仓库内数据管理与预处理
流程演示。数据为**自建样例数据**，并非真实采集数据。

字段说明
--------
- session_id           : 测试会话编号（一次完整测试流程）
- user_id              : 测试者编号
- test_type            : 测试项目类型
                         aim     = 定点定位测试
                         track   = 动态目标追踪测试
                         flick   = 快速切换(Flick)响应测试
                         calib   = 物理位移标定测试
- trial_no             : 该会话内该项目第几次尝试
- response_time_ms     : 响应时间(毫秒)，aim/flick 采集
- positioning_error_px : 定位误差(像素)，aim/flick 采集
- tracking_error_px    : 追踪误差(像素)，track 采集
- hit_count            : 命中样本数
- target_total         : 目标总数
- physical_move_cm     : 物理移动距离(厘米)，calib 采集
- virtual_rotate_deg   : 虚拟视角转动量(度)，calib 采集
- device_dpi           : 鼠标硬件 DPI
- habit_grip           : 握鼠习惯(claw=抓握 / palm=趴握 / fingertip=指握)
- timestamp            : 采集时间戳

运行方式
--------
    python generate_sample_data.py
输出：../data/raw/sample_test_data.csv
"""

import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)  # 固定随机种子，保证样例数据可复现

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "data", "raw", "sample_test_data.csv")

FIELD_NAMES = [
    "session_id", "user_id", "test_type", "trial_no",
    "response_time_ms", "positioning_error_px", "tracking_error_px",
    "hit_count", "target_total", "physical_move_cm", "virtual_rotate_deg",
    "device_dpi", "habit_grip", "timestamp",
]


def gauss(mean, sigma):
    """生成一个服从高斯分布 N(mean, sigma^2) 的数值，保留 2 位小数。"""
    return round(random.gauss(mean, sigma), 2)


def clamp_positive(value, lower=0.0):
    """确保数值不小于下限（运动指标应为非负值）。"""
    return max(value, lower)


def build_rows():
    rows = []
    user_id = "U001"
    device_dpi = 800
    habit_grip = "claw"
    base_time = datetime(2026, 8, 29, 10, 0, 0)

    # 3 个测试会话
    for session_idx in range(1, 4):
        session_id = f"S{session_idx:03d}"
        # 每个会话中 4 类测试各做 5 次尝试
        for test_type, trials in [
            ("aim", 5), ("track", 5), ("flick", 5), ("calib", 5),
        ]:
            for trial in range(1, trials + 1):
                row = {
                    "session_id": session_id,
                    "user_id": user_id,
                    "test_type": test_type,
                    "trial_no": trial,
                    "response_time_ms": "",
                    "positioning_error_px": "",
                    "tracking_error_px": "",
                    "hit_count": "",
                    "target_total": "",
                    "physical_move_cm": "",
                    "virtual_rotate_deg": "",
                    "device_dpi": device_dpi,
                    "habit_grip": habit_grip,
                    "timestamp": (base_time + timedelta(minutes=session_idx * 10 + trial)).strftime("%Y-%m-%d %H:%M:%S"),
                }

                if test_type == "aim":
                    row["response_time_ms"] = gauss(320, 40)
                    row["positioning_error_px"] = gauss(6.0, 1.5)
                    row["hit_count"] = random.randint(17, 20)
                    row["target_total"] = 20
                elif test_type == "track":
                    row["tracking_error_px"] = gauss(12.0, 2.5)
                    row["hit_count"] = random.randint(16, 19)
                    row["target_total"] = 20
                elif test_type == "flick":
                    row["response_time_ms"] = gauss(280, 35)
                    row["positioning_error_px"] = gauss(8.0, 2.0)
                    row["hit_count"] = random.randint(17, 20)
                    row["target_total"] = 20
                elif test_type == "calib":
                    # 标定测试：物理移动距离与虚拟视角转动量呈近似线性关系
                    row["physical_move_cm"] = round(random.uniform(5.0, 20.0), 2)
                    row["virtual_rotate_deg"] = round(row["physical_move_cm"] * 8.0, 2)

                rows.append(row)

    # ---- 人为注入少量离群样本，用于演示预处理中的异常剔除 ----
    # 会话1：aim 第4次尝试 响应时间明显延迟（离群）
    rows[3]["response_time_ms"] = 812.0
    # 会话1：aim 第5次尝试 定位误差异常（离群）
    rows[4]["positioning_error_px"] = 24.6
    # 会话1：track 第4次尝试 追踪误差异常（离群）
    rows[8]["tracking_error_px"] = 41.2
    # 会话1：flick 第4次尝试 响应延迟异常（离群）
    rows[13]["response_time_ms"] = 903.5

    return rows


def main():
    rows = build_rows()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"样例原始数据已生成：{OUT_PATH}")
    print(f"共 {len(rows)} 条记录（3 会话 × 4 类测试 × 5 次尝试）")


if __name__ == "__main__":
    main()
