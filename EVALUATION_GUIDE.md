# τ-bench 评测指南（DashScope 适配版）



## 快速开始

### 1. 环境要求

- Python >= 3.12, < 3.14
- Windows / macOS / Linux
- DashScope API Key（通义千问）

### 2. 安装依赖

```bash
# 使用 pip 安装（Windows 安全策略受限时推荐）
pip install -e .

# banking_knowledge 领域额外需要
pip install rank_bm25
```

### 3. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 API Key 和兼容接口地址：

```env
OPENAI_API_KEY=<your_api_key>
OPENAI_API_BASE=<your_openai_compatible_base_url>
OPENAI_BASE_URL=<your_openai_compatible_base_url>
```

> **说明**：项目通过 `OPENAI_API_BASE`（LiteLLM 用）和 `OPENAI_BASE_URL`（OpenAI SDK 用）两个变量指向同一个 OpenAI 兼容接口地址。请向你的 API 服务商获取正确的 endpoint。

### 4. 运行评测

每个领域有一个独立的 Python 启动脚本（避免 PowerShell 引号转义问题）：

```bash
# Retail 领域（114 任务）
python run_retail_think.py

# Airline 领域（120 任务）
python run_airline_think.py

# Telecom 领域（146 任务）
python run_telecom_think.py

# Banking Knowledge 领域（97 任务，含 embedding 检索）
python run_banking_think.py
```

> **Windows 用户**：用 `py -3.12 run_retail_think.py` 替代 `python`。

---

## 评测配置说明

### 默认配置（与排行榜对齐）

| 参数 | 值 | 说明 |
|------|-----|------|
| Agent 模型 | `openai/qwen3.5-397b-a17b` | 被评测的模型 |
| User Simulator | `openai/qwen3.7-max-2026-06-08` | 模拟用户的模型 |
| Thinking Mode | `enable_thinking: true` | 开启推理模式 |
| Temperature | `1.0` | Agent 采样温度 |
| top_p | `0.95` | Agent 采样参数 |
| Trials | `1` | 每任务评测次数 |
| Concurrency | `3` | 并行任务数 |

### 排行榜指标

排行榜使用 **Pass^1**（单次通过率）作为主要指标：
- 每个任务跑 1 次 trial
- reward = 1.0 算通过，否则不通过
- `Pass^1 = 通过任务数 / 总评估任务数`

> 更可靠的评测建议跑 4 trials（修改脚本中 `--num-trials` 为 4）。

### 更换被测模型

编辑对应的 `run_<domain>_think.py` 文件，修改 `--agent-llm` 参数即可：

```python
"--agent-llm", "openai/你的模型名",
```

> **注意**：非 LiteLLM 内置模型必须加 `openai/` 前缀（走 OpenAI 兼容模式）。

---

## 领域说明

| 领域 | 任务数 | 描述 | 特殊配置 |
|------|--------|------|---------|
| **retail** | 114 | 零售电商客服（查订单、换货、退款等） | 无 |
| **airline** | 120 | 航空客服（查航班、改签、行李等） | 无 |
| **telecom** | 146 | 电信客服（套餐、流量、故障排查等） | 无 |
| **banking_knowledge** | 97 | 银行客服 + 知识检索（RAG） | 需要 `rank_bm25`；使用 `openai_embeddings` 配置 + `text-embedding-v3` 模型 |

---

## 查看评测结果

```bash
# Windows
.\tau2.bat view

# macOS/Linux
tau2 view
```

结果保存在 `data/simulations/` 目录下。

---

## 项目改动说明（相比上游）

| 文件 | 改动 | 原因 |
|------|------|------|
| `src/tau2/config.py` | Judge 模型改为 `openai/qwen3.7-max-2026-06-08` | 适配 OpenAI 兼容接口可用模型 |
| `src/tau2/domains/banking_knowledge/data_model.py` | 加 `encoding="utf-8"` | Windows GBK 编码兼容 |
| `src/tau2/domains/banking_knowledge/environment.py` | 加 `encoding="utf-8"` | 同上 |
| `src/tau2/domains/banking_knowledge/retrieval.py` | embedding 模型改为 `text-embedding-v3` | 适配 OpenAI 兼容接口支持的 embedding 模型 |
| `src/tau2/knowledge/embedders/openai_embedder.py` | 加分批逻辑（batch_size=10） | 部分 OpenAI 兼容接口限制单次 embedding 条数 |
| `src/tau2/knowledge/embeddings_cache.py` | 加 `encoding="utf-8"` + 模型映射更新为 `text-embedding-v3` | Windows 兼容 + embedding 模型适配 |
| `tau2.bat` | 新增 | Windows 下绕过安全策略的运行入口 |

---

## 常见问题

### Q: 报错 `LLM Provider NOT provided`
模型名需要加 `openai/` 前缀。例如 `openai/qwen3.5-397b-a17b`。

### Q: 报错 `UnicodeDecodeError: 'gbk' codec can't decode`
Windows 编码问题，确保使用本仓库已修复的代码版本。

### Q: 报错 `model does not exist or you do not have access`
你的 API 服务商不支持该模型名。请确认服务商支持的模型列表。

### Q: `This model isn't mapped yet` 错误日志
这是 LiteLLM 无法计算费用的警告，**不影响评测功能**。

### Q: banking_knowledge 报 `No module named 'rank_bm25'`
执行 `pip install rank_bm25`。

### Q: 如何开启/关闭 thinking mode？
修改脚本中的 `--agent-llm-args`，设置 `"enable_thinking": true` 或 `false`。
