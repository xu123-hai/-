# AI 工具提示词追溯（/prompt）

本目录用于追溯课程设计过程中与 AI 工具（本课程使用**豆包**）的交流记录，
满足课程设计「AI 工具提示词追溯」要求。

## 约定

1. **每个阶段一个 JSON 文件**，命名格式：`YYYY-MM-DD_stageN_<阶段名>.json`
   - 例：`2026-08-29_stage1_data_prep.json`
2. JSON 文件记录该阶段与 AI 的关键交流：用户侧 Prompt、AI 侧关键回复/产出说明。
3. **上下文压缩前及时备份**：每次对话上下文可能被压缩，压缩前将当前阶段
   交流记录备份到 `backup/` 目录（文件名追加 `_backup`），防止记录丢失。
4. 后续每个阶段（数据预处理、功能开发、算法实现、文档整理、最终交付等）
   均需同步新增对应 JSON 记录并更新 `index.md`。
5. 记录内容如实反映交流过程，不修改、不美化。

## 目录结构

```
prompt/
├── README.md                                  # 本说明文件
├── index.md                                   # 各阶段记录索引
├── 2026-08-29_stage1_data_prep.json           # 阶段1：数据来源 + 数据预处理
└── backup/                                    # 上下文压缩前的备份
    └── 2026-08-29_stage1_data_prep_backup.json
```

## 交流记录字段说明

| 字段 | 说明 |
| --- | --- |
| timestamp | 交流时间 |
| stage | 所属阶段 |
| role | user（用户/AI 使用者）或 assistant（AI 助手） |
| content | Prompt 或 AI 回复的正文 |
| note | 补充说明（可选） |
