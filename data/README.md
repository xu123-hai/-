# 数据说明（/data）

本目录存放课程设计「面向人机运动性能评估的网页端参数匹配生成器」所使用的数据及其预处理产物。

## 1. 数据来源

| 项目 | 说明 |
| --- | --- |
| 数据类型 | **自建数据（self-built）**，由本项目网页端在运行时实时采集生成 |
| 采集方式 | 使用者在浏览器内完成定点定位、动态追踪、快速切换（Flick）、物理标定等虚拟运动测试，系统实时采集运动行为原始数据，支持导出为本地 CSV |
| 数据规模 | 数据量小（单次测试会话 KB 级），按课程设计要求**直接提交到仓库 `/data` 目录** |
| 是否公开数据集 | 否。本项目不使用公开离线数据集，数据均为现场测试实时生成（见 `方案设计.md` 3.3 节） |
| 敏感信息 | 无。数据仅包含运动测试指标，不含任何个人隐私敏感信息 |

> **样例数据说明**：仓库中的 `data/raw/sample_test_data.csv` 为**自建样例数据**，由
> `scripts/generate_sample_data.py` 按网页端导出格式模拟生成（固定随机种子，可复现），
> 用于数据管理与预处理流程演示。实际运行网页端测试后导出的真实数据格式与其一致。

## 2. 目录结构

```
data/
├── README.md                    # 本说明文件
├── raw/                         # 原始数据
│   └── sample_test_data.csv     # 自建样例原始数据（模拟网页端导出格式）
└── processed/                   # 预处理产物
    ├── cleaned_test_data.csv    # 清洗 + 去离群后的明细数据
    ├── test_statistics.csv      # 各测试类型统计汇总（均值/标准差/中位数/命中率）
    └── index.json               # 预处理结果索引
```

## 3. 数据字段说明

`raw/sample_test_data.csv` 字段（与网页端导出格式一致）：

| 字段 | 说明 |
| --- | --- |
| session_id | 测试会话编号 |
| user_id | 测试者编号 |
| test_type | 测试类型：aim=定点定位 / track=动态追踪 / flick=快速切换 / calib=物理标定 |
| trial_no | 该会话内该项目尝试序号 |
| response_time_ms | 响应时间（毫秒），aim/flick 采集 |
| positioning_error_px | 定位误差（像素），aim/flick 采集 |
| tracking_error_px | 追踪误差（像素），track 采集 |
| hit_count / target_total | 命中样本数 / 目标总数 |
| physical_move_cm | 物理移动距离（厘米），calib 采集 |
| virtual_rotate_deg | 虚拟视角转动量（度），calib 采集 |
| device_dpi | 鼠标硬件 DPI（用户录入） |
| habit_grip | 握鼠习惯（claw/palm/fingertip，用户录入） |
| timestamp | 采集时间戳 |

## 4. 数据预处理

预处理程序：`scripts/preprocess.py`（Python 标准库实现，无需额外依赖）

处理流程：
1. **加载**：读取 `data/raw/sample_test_data.csv`
2. **清洗**：剔除缺失值、负值等非法记录
3. **去离群**：按「测试类型 × 指标」分组，剔除超过 均值±3σ 的离群样本，
   降低单次偶然操作带来的误差
4. **派生指标**：计算命中率 `hit_rate = hit_count / target_total`
5. **统计聚合**：按测试类型输出均值、标准差、中位数、命中率等
6. **输出**：`data/processed/` 下清洗明细、统计汇总与 `index.json` 索引

运行方式（在 `scripts/` 目录下）：

```bash
python generate_sample_data.py   # （可选）重新生成样例原始数据
python preprocess.py             # 执行数据预处理
```

> 该预处理算法与 `方案设计.md` 3.5 节「数据预处理算法」一致，
> 后续将内嵌至网页端 JavaScript 中，本脚本为仓库数据管理用的独立实现。

## 5. 备注

- 如后续采集真实测试数据并形成较大规模数据集，将按课程设计要求在
  Hugging Face / ModelScope 平台开源并注明为自建数据集。
- 使用 `utf-8-sig` 编码，兼容 Excel 直接打开。
